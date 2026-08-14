# DiagnosticsAPI

`DiagnosticsAPI` 用来读取主程序诊断日志。

## 常用方法

- `get_logs(limit=...)`: 读取最近的日志。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        logs = self.api.diagnostics.get_logs(limit=20)
        for log in logs:
            print(log["time"], log["level"], log["message"])
```

日志项结构见 `DiagnosticLogPayload`。
