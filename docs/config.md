# ConfigAPI

`ConfigAPI` 用来注册和保存插件自己的配置模型。

## 常用方法

- `register_plugin_model(plugin_id, model)`: 注册插件配置模型。
- `get_plugin_model(plugin_id)`: 获取已注册的插件配置模型。
- `save()`: 保存配置。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, ConfigBaseModel, PluginAPI


class WeatherConfig(ConfigBaseModel):
    city: str = "Shanghai"
    enabled: bool = True


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)
        self.config = WeatherConfig()

    def on_load(self) -> None:
        super().on_load()
        if self.pid is None:
            return

        self.api.config.register_plugin_model(self.pid, self.config)
        self.config.city = "Beijing"
        self.api.config.save()
```

配置模型建议继承 `ConfigBaseModel`，这样 IDE 和类型检查器能正确提示字段。
