# Product Tree Contract

产品树由 Module 与 Capability 资源组成，canonical 文件位于 `.coder/_knowledge/product-modules/<module-id>.md`。Module 是长期产品边界，Capability 是可被需求、改动、验证、风险和建议关联的能力节点。

新增模块先为 `CANDIDATE`，只有 `product_module_maintainers` 明确治理并校验父子关系、唯一 ID 与证据后才能 `ACTIVE`。Requirement 通过 `REQUIREMENT_ALLOCATED_TO_MODULE` 进入产品树；Change、Validation、Risk、Recommendation 分别通过注册关系连接。树不复制任务实现细节，实际开发事实保留在 Card/Activity/Artifact 中。

CLI 查询必须支持按 module id 精确定位、metadata/section 局部读取和向上/向下关系导航；禁止以目录名、宽泛关键词或本地绝对路径作为稳定标识。
