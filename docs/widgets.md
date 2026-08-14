# WidgetsAPI

`WidgetsAPI` 用来向 Class Widgets 2 注册插件提供的 Widget。

## 常用方法

- `register(widget_id, name, qml_path, backend_obj=None, settings_qml=None, default_settings=None)`: 注册一个 Widget。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        self.api.widgets.register(
            widget_id="com.example.weather.card",
            name="Weather Card",
            qml_path="assets/weather_card.qml",
            settings_qml="assets/weather_settings.qml",
            default_settings={"city": "Shanghai"},
        )
```

`widget_id` 建议使用插件域名式前缀，避免和其他插件冲突。
