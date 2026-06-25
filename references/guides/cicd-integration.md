# CI/CD 集成指南

本文档详细说明如何将 Coder 开发执行技能与 CI/CD 流水线集成，实现开发执行的自动化协同。

示例中的 `DEVELOPMENT_PROJECT_ID` 应与 `.coder-config.yaml` 的 `workspace.development_project_id` 保持一致；执行记录默认位于 `.coder/${DEVELOPMENT_PROJECT_ID}/records/execution-log.md`。

## 1. 集成架构

```
Coder 执行开发
    ↓
完成 MR 实现
    ↓
本地验证通过
    ↓
触发 CI/CD 流水线
    ├─ 代码质量检查
    ├─ 自动化测试
    ├─ 构建与打包
    └─ 部署验证
    ↓
流水线结果反馈
    ├─ 成功 → 标记 ACCEPTED
    └─ 失败 → 登记偏差
```

## 2. GitLab CI 集成

### 2.1 基础配置

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - build
  - deploy

# Coder 本地验证后的 CI 验证
coder-ci-validation:
  stage: validate
  script:
    - echo "=== Coder CI Validation ==="
    - test -f .coder-config.yaml && echo "Coder config found" || echo "No coder config found"
    - mvn clean compile -DskipTests
    - mvn checkstyle:check
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - when: manual

# 单元测试
unit-test:
  stage: test
  script:
    - mvn test
    - mvn jacoco:report
  artifacts:
    reports:
      coverage_report:
        coverage_report_format: jacoco
        coverage_report_path: target/site/jacoco/jacoco.xml
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

# 集成测试
integration-test:
  stage: test
  script:
    - mvn verify -Pintegration-test
  services:
    - postgres:15
    - redis:7
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: testuser
    POSTGRES_PASSWORD: testpass
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

# 构建 Docker 镜像
build-image:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual
```

### 2.2 使用 GitLab API

```yaml
# 查询流水线状态
check-pipeline-status:
  stage: validate
  script:
    - |
      PIPELINE_ID=$CI_PIPELINE_ID
      STATUS=$(curl --silent --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        "$CI_SERVER_URL/api/v4/projects/$CI_PROJECT_ID/pipelines/$PIPELINE_ID" | \
        jq -r '.status')
      echo "Pipeline status: $STATUS"
      if [ "$STATUS" != "success" ]; then
        echo "Pipeline failed"
        exit 1
      fi
  rules:
    - when: manual
```

### 2.3 MR 自动化

```yaml
# 自动创建 MR 描述
update-mr-description:
  stage: validate
  script:
    - |
      # 读取执行记录
      EXECUTION_LOG=$(cat ".coder/${DEVELOPMENT_PROJECT_ID}/records/execution-log.md" | tail -n 50)
      
      # 更新 MR 描述
      curl --request PUT --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" \
        "$CI_SERVER_URL/api/v4/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID" \
        --data-urlencode "description=## Coder 执行记录\n\n\`\`\`\n$EXECUTION_LOG\n\`\`\`"
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual
```

## 3. GitHub Actions 集成

### 3.1 基础工作流

```yaml
# .github/workflows/coder-validation.yml
name: Coder Validation

on:
  pull_request:
    branches: [main, develop]
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '17'
          cache: 'maven'
      
      - name: Load Coder Config
        run: |
          if [ -f .coder-config.yaml ]; then
            echo "=== Coder Config ==="
            echo "Coder config found"
          fi
      
      - name: Compile
        run: mvn clean compile -DskipTests
      
      - name: Checkstyle
        run: mvn checkstyle:check
      
      - name: Unit Tests
        run: mvn test
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./target/site/jacoco/jacoco.xml

  integration-test:
    needs: validate
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Integration Tests
        run: mvn verify -Pintegration-test
        env:
          DB_HOST: localhost
          DB_PORT: 5432
          DB_NAME: testdb
          DB_USER: testuser
          DB_PASSWORD: testpass

  build-and-push:
    needs: integration-test
    runs-on: ubuntu-latest
    if: github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v3
      
      - name: Docker Build
        run: |
          docker build -t ${{ github.repository }}:${{ github.sha }} .
          docker push ${{ github.repository }}:${{ github.sha }}
```

### 3.2 使用 GitHub CLI

```yaml
# 查询 PR 状态
check-pr-status:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    
    - name: Check PR Status
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        PR_NUMBER=$(gh pr view --json number -q .number)
        gh pr view $PR_NUMBER --json state,mergeStateStatus
        
    - name: Update PR Description
      env:
        GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        EXECUTION_LOG=$(cat ".coder/${DEVELOPMENT_PROJECT_ID}/records/execution-log.md" | tail -n 50)
        gh pr edit $PR_NUMBER --body "## Coder 执行记录\n\n\`\`\`\n$EXECUTION_LOG\n\`\`\`"
```

## 4. Jenkins 集成

### 4.1 Jenkinsfile

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        MAVEN_HOME = tool 'maven-3.9'
    }
    
    stages {
        stage('Load Coder Config') {
            steps {
                script {
                    if (fileExists('.coder-config.yaml')) {
                        echo '=== Coder Config ==='
                        sh 'test -f .coder-config.yaml && echo "Coder config found" || echo "No coder config found"'
                    }
                }
            }
        }
        
        stage('Compile') {
            steps {
                sh 'mvn clean compile -DskipTests'
            }
        }
        
        stage('Code Quality') {
            steps {
                sh 'mvn checkstyle:check'
                sh 'mvn spotbugs:check'
            }
        }
        
        stage('Unit Tests') {
            steps {
                sh 'mvn test'
                junit 'target/surefire-reports/*.xml'
                jacoco executionData: 'target/jacoco.exec'
            }
        }
        
        stage('Integration Tests') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'db-credentials', 
                                                  usernameVariable: 'DB_USER', 
                                                  passwordVariable: 'DB_PASS')]) {
                    sh "mvn verify -Pintegration-test -Ddb.user=${DB_USER} -Ddb.password=${DB_PASS}"
                }
            }
        }
        
        stage('Build Docker') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} ."
                sh "docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline succeeded'
            // 通知 Coder 执行结果
        }
        failure {
            echo 'Pipeline failed'
            // 通知 Coder 登记偏差
        }
    }
}
```

## 5. CI/CD 状态查询

### 5.1 执行过程中查询 CI 状态

在 Coder 执行过程中，可以查询 CI/CD 状态：

#### GitLab

```bash
# 查询最新流水线状态
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipelines?per_page=1" | \
  jq '.[0] | {id, status, created_at}'

# 查询流水线详情
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipelines/$PIPELINE_ID" | \
  jq '{status, duration, started_at, finished_at}'

# 查询 MR 状态
curl --silent --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/merge_requests/$MR_IID" | \
  jq '{state, merge_status, head_pipeline_status}'
```

#### GitHub

```bash
# 查询 PR 状态
gh pr view $PR_NUMBER --json state,mergeStateStatus

# 查询工作流运行状态
gh run list --limit 5

# 查询特定运行详情
gh run view $RUN_ID --json status,conclusion,startedAt,updatedAt
```

### 5.2 CI 状态与 MR 状态映射

| CI/CD 状态 | MR 状态 | 处理动作 |
|---|---|---|
| success/passed | ACCEPTED | 可进入下一 MR |
| failed | BLOCKED | 登记偏差，分析原因 |
| running | VERIFYING | 等待完成 |
| canceled | BLOCKED | 重新触发或登记偏差 |
| skipped | - | 检查是否必需 |

## 6. 流水线触发策略

### 6.1 自动触发

```yaml
# 在 MR 验证通过后自动触发
post_acceptance_trigger:
  enabled: true
  trigger_type: "api"  # api / webhook / polling
  trigger_conditions:
    - mr_status: "ACCEPTED"
    - validation_passed: true
    - no_high_risk_deviation: true
```

### 6.2 手动触发

```bash
# GitLab
curl --request POST --header "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "https://gitlab.example.com/api/v4/projects/$PROJECT_ID/pipeline" \
  --data "ref=main"

# GitHub
gh workflow run coder-validation.yml --ref main

# Jenkins
curl -X POST "https://jenkins.example.com/job/coder-validation/build" \
  --user "$JENKINS_USER:$JENKINS_TOKEN"
```

## 7. 流水线结果处理

### 7.1 成功处理

```markdown
## CI/CD 验证通过

| 项 | 内容 |
|---|---|
| 流水线 ID |  |
| 流水线状态 | success |
| 触发时间 |  |
| 完成时间 |  |
| 持续时间 |  |
| 测试结果 |  |
| 代码质量 |  |
| 构建产物 |  |

### 结论
- 是否允许标记 ACCEPTED: 是
- 是否允许进入下一 MR: 是
```

### 7.2 失败处理

```markdown
## CI/CD 验证失败

| 项 | 内容 |
|---|---|
| 流水线 ID |  |
| 流水线状态 | failed |
| 失败阶段 |  |
| 失败原因 |  |
| 失败日志 | （有界摘要，不超过 200 行） |

### 偏差登记
- 偏差类型: TEST_FAILURE / BUILD_FAILURE
- 是否当前 MR 内可修: 是 / 否
- 处理建议:  |

### 结论
- 是否允许标记 ACCEPTED: 否
- 是否允许进入下一 MR: 否
```

## 8. 认证管理

### 8.1 安全原则

1. **不要在代码中暴露认证信息**
2. **使用环境变量或密钥管理服务**
3. **定期轮换密钥**
4. **最小权限原则**

### 8.2 配置示例

```yaml
# 项目配置中的 CI/CD 配置
cicd:
  api_integration:
    enabled: true
    platform: "gitlab"
    base_url: "https://gitlab.example.com/api/v4"
    
    # 认证方式（实际值存储在环境变量或密钥管理中）
    auth_type: "private_token"
    auth_variable: "GITLAB_API_TOKEN"
    
    # 不要这样做：
    # auth_value: "glpat-xxxxxxxxxxxxx"  # 危险！
```

### 8.3 环境变量使用

```bash
# 设置环境变量
export GITLAB_API_TOKEN="your-token-here"
export GITHUB_TOKEN="your-token-here"
export JENKINS_TOKEN="your-token-here"

# 在脚本中使用
curl --header "PRIVATE-TOKEN: $GITLAB_API_TOKEN" ...
```

## 9. 最佳实践

### 9.1 流水线设计

1. **快速反馈**：将快速检查（编译、静态检查）放在前面
2. **分层验证**：编译 → 单元测试 → 集成测试 → E2E
3. **缓存依赖**：利用 CI/CD 平台的缓存机制
4. **并行执行**：独立的测试任务并行运行

### 9.2 错误处理

1. **明确的失败原因**：输出清晰的错误信息
2. **失败重试**：对不稳定的测试进行重试
3. **失败通知**：及时通知相关人员
4. **失败归档**：记录失败信息便于分析

### 9.3 安全实践

1. **密钥管理**：使用密钥管理服务
2. **权限控制**：最小权限原则
3. **审计日志**：记录所有 API 调用
4. **定期审查**：定期审查权限和密钥

### 9.4 性能优化

1. **增量构建**：只构建变更的部分
2. **测试并行**：并行执行独立测试
3. **缓存复用**：复用依赖和构建产物
4. **资源优化**：合理配置 CI/CD 资源

## 10. 故障排查

### 10.1 常见问题

| 问题 | 原因 | 解决方案 |
|---|---|---|
| 流水线未触发 | 配置错误 | 检查触发条件 |
| 认证失败 | 密钥过期 | 更新密钥 |
| 测试失败 | 环境问题 | 检查服务依赖 |
| 构建超时 | 资源不足 | 增加资源或优化 |

### 10.2 排查流程

```
流水线失败
    ↓
查看失败阶段
    ↓
查看失败日志（有界）
    ↓
判断失败类型
    ├─ 代码问题 → 修复并重试
    ├─ 环境问题 → 检查服务状态
    ├─ 配置问题 → 更新配置
    └─ 资源问题 → 调整资源
    ↓
执行修复
    ↓
重新触发流水线
```

## 11. 监控与报告

### 11.1 监控指标

- 流水线成功率
- 平均执行时间
- 失败率趋势
- 代码覆盖率变化

### 11.2 报告模板

```markdown
## CI/CD 执行报告

### 基本信息
| 项 | 内容 |
|---|---|
| MR | MR-X |
| 流水线 ID |  |
| 触发方式 | 自动 / 手动 |
| 开始时间 |  |
| 结束时间 |  |
| 总耗时 |  |

### 各阶段结果
| 阶段 | 状态 | 耗时 | 备注 |
|---|---|---|---|
| 编译 |  |  |  |
| 静态检查 |  |  |  |
| 单元测试 |  |  |  |
| 集成测试 |  |  |  |
| 构建 |  |  |  |

### 测试统计
| 项 | 数量 |
|---|---|
| 总测试数 |  |
| 通过 |  |
| 失败 |  |
| 跳过 |  |

### 代码质量
| 项 | 结果 |
|---|---|
| 代码覆盖率 |  |
| 静态检查问题 |  |
| 技术债务 |  |
```
