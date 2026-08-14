# AutomationAPI

`AutomationAPI` 用来注册自动化任务。

## 常用方法

- `register(task)`: 注册一个自动化任务对象。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class ExampleTask:
    id = "com.example.task"
    name = "Example Task"

    def run(self) -> None:
        print("task running")


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        self.api.automation.register(ExampleTask())
```

任务对象的完整协议由主程序自动化系统决定，SDK 这里只提供注册入口的类型提示。
