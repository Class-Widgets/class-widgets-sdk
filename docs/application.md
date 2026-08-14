# ApplicationAPI

`ApplicationAPI` 用来读取 Class Widgets 2 主程序信息，并触发重启。

## 常用方法

- `get_info()`: 返回应用信息。
- `restart()`: 重启主程序。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        info = self.api.application.get_info()
        print(info["name"], info["version"], info["pluginApiVersion"])
```

`restart()` 会影响整个主程序，建议只在用户明确确认后调用。
