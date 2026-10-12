# 原始代码基线验证

命令（cwd 为本用例仓库）：`python3 -B -m unittest discover -s tests -v`。

实际输出：
```text
test_create_and_list (test_orders.OrdersTest.test_create_and_list) ... ok
test_empty (test_orders.OrdersTest.test_empty) ... ok
Ran 2 tests
OK
```
退出码 0。覆盖订单新建、列表返回、空列表；未覆盖备注、迁移、HTTP、浏览器和生产部署。运行的是当前原始代码，没有产品修改，不作为备注功能通过或 CP5 的证据。当前源文件摘要见 analysis/AN-001.md 的 Source Points。
