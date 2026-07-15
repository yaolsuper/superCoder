# P16 Canonical Discovery and Registry Consistency

## 目标

验证分发包在大小写敏感环境中只能通过 canonical `skills/superCoder/SKILL.md` 发现主技能，并确保 README、Harness、module map、场景 registry 与真实文件保持一致。

## 输入

- 一份完整 superCoder 仓库。
- 一份把 `skills/superCoder/SKILL.md` 错写为 `skills/supercoder/SKILL.md` 的负例包。
- 一份场景文件存在但未登记到 module map，或 module map 引用不存在文件的负例包。

## 执行

1. 使用 Python 3.11+ 标准库运行 `skills/superCoder/scripts/validate_package.py`。
2. 在正例上运行 package validation，并通过 behavior runner 记录 raw output digest。
3. 在负例上验证错误码和路径稳定。

## 预期结论

- 正例包含 `CANONICAL_DISCOVERY_PASS`。
- 正例包含 `REGISTRY_CONSISTENCY_PASS`。
- 错误大小写返回 `PATH_CASE_MISMATCH`。
- 缺失引用返回 `REFERENCE_MISSING`。
- 重复场景或漏登记返回 `REGISTRY_DRIFT`。

## 禁止结果

- 不得通过 case-insensitive fallback 静默接受错误路径。
- 不得忽略 module map 或 scenario registry 漂移。
- 未执行 runner 时不得记录 PASS。
- 不得要求 PyYAML 或其他第三方依赖。
