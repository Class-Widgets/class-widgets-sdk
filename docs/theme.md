# ThemeAPI

`ThemeAPI` 用来读取当前主题，并监听主题变化。

## 常用方法和信号

- `current()`: 返回当前主题名称。
- `changed`: 主题变化时触发，参数为主题名称。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        print(self.api.theme.current())
        self.api.theme.changed.connect(self.on_theme_changed)

    def on_theme_changed(self, theme: str) -> None:
        print("theme changed:", theme)
```