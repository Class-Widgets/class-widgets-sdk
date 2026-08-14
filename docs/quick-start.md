# 快速开始

## 安装

```bash
pip install class-widgets-sdk
```

## 建议结构

```text
my-plugin/
  cwplugin.json
  main.py
  assets/
    widget.qml
    settings.qml
```

## 插件入口

```python
from ClassWidgets.SDK import CW2Plugin, ConfigBaseModel, PluginAPI


class MyConfig(ConfigBaseModel):
    enabled: bool = True
    title: str = "Hello"


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)
        self.config = MyConfig()

    def on_load(self) -> None:
        super().on_load()
        if self.pid is None:
            return

        self.api.config.register_plugin_model(self.pid, self.config)
        self.api.widgets.register(
            widget_id="com.example.hello.widget",
            name="Hello Widget",
            qml_path="assets/widget.qml",
        )
```

## 生命周期

- `__init__(api)`: 初始化对象和本地状态。
- `on_load()`: 注册资源。
- `on_unload()`: 清理资源。
