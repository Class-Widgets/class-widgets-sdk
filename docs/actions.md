# ActionsAPI

`ActionsAPI` 用来注册和获取全局 Action。Action 通过 Qt `Signal` 传递参数。

## 常用方法

- `register(action_name, *parameter_types)`: 注册 Action，并返回对应信号。
- `get(action_name)`: 获取已经注册的 Action 信号。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        action = self.api.actions.register("com.example.open", str)
        action.connect(self.open_page)

        self.api.actions.get("com.example.open").emit("dashboard")

    def open_page(self, page: str) -> None:
        print("open", page)
```

`parameter_types` 应和信号 emit 时传入的参数类型保持一致。
