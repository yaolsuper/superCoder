# Behavior Test Results

本目录记录 superCoder 行为压力场景的 RED/GREEN 证据。场景规格只说明“应该测什么”；本目录说明“实际测过什么、失败和通过证据是什么”。

每个结果文件建议命名为：

```text
YYYY-MM-DD-<scenario-id>.md
```

## Result Template

```markdown
# <scenario-id> Result

- Date:
- Model / agent:
- Harness / entry:
- superCoder version or commit:
- Scenario file:

## RED Evidence

- Baseline condition:
- Observed failure:
- Verbatim rationalization or output excerpt:

## GREEN Evidence

- Skill files loaded:
- Observed compliant behavior:
- Required verdicts present:
- Forbidden outcomes absent:

## Score

- PASS / FAIL / PARTIAL:
- Notes:
- Follow-up scenarios:
```
