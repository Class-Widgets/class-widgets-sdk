<div align="center">
<h1>Class Widgets 2 Plugin SDK (Type Stubs)</h1>
<p>Pure type stubs for Class Widgets 2 plugin development.</p>

[![PyPI version](https://img.shields.io/pypi/v/class-widgets-stubs.svg?style=for-the-badge&color=blue)](https://pypi.org/project/class-widgets-stubs/)
[![星标](https://img.shields.io/github/stars/Class-Widgets/class-widgets-stubs?style=for-the-badge&color=orange&label=%E6%98%9F%E6%A0%87)](https://github.com/Class-Widgets/class-widgets-stubs/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg?style=for-the-badge)](https://github.com/Class-Widgets/class-widgets-stubs/)

</div>

> [!CAUTION]
> 
> 本项目还处**在开发**阶段，API 接口可能随时发生变化，敬请谅解。
> 
> This project is still **in development**. The API may change at any time, so please bear with us.

## Overview
`class-widgets-sdk` provides complete type hints and IDE autocompletion for developing plugins for Class Widgets 2.

This is a **type stubs only** package—it contains no executable code. Plugins must be loaded and run within the Class Widgets 2 main application.

## Installation
pip install class-widgets-stubs

## Usage
In your plugin code, import the stubs to get full IDE support:

```python
from ClassWidgets.SDK import CW2Plugin, ConfigBaseModel, PluginAPI

class MyConfig(ConfigBaseModel):
    enabled: bool = True
    text: str = "hEIlo, WoRId"

class MyPlugin(CW2Plugin):
    
    def __init__(self, api: PluginAPI):
        super().__init__(api)
        self.config = MyConfig()
    
    def on_load(self):
        self.api.config.register_plugin_model(self.pid, self.config)
        # Your IDE will provide full autocompletion here
        self.api.widgets.register(
            widget_id="com.example.mywidget",
            name="My Widget",
            qml_path="path/to/mywidget.qml"
        )
```

## How It Works
1.  **Development**: You install this package to get type hints, autocompletion, and static type checking (with mypy/pyright) in your IDE.
2.  **Runtime**: When your plugin is loaded by the Class Widgets 2 main application, the real implementations are injected, replacing these type stubs.

> [!IMPORTANT]
> 
> - This package **cannot run your plugin**. Plugins must be tested within the [Class Widgets 2](https://github.com/RinLit-233-shiroko/Class-Widgets-2).
> - The import path is `ClassWidgets.SDK`, while the PyPI project name is `class-widgets-stubs`.

## Links
- [Class Widgets 2](https://github.com/rinlit-233-shiroko/class-widgets-2)
- [Report an Issue](https://github.com/rinlit-233-shiroko/class-widgets-2/issues)

## License
This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for details.