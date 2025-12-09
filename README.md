<div align="center">
<h1>Class Widgets 2 Plugin SDK</h1>
<p>Complete SDK, tools, and type hints for Class Widgets 2 plugin development.</p>

[![PyPI version](https://img.shields.io/pypi/v/class-widgets-sdk.svg?style=for-the-badge&color=blue)](https://pypi.org/project/class-widgets-sdk/)
[![星标](https://img.shields.io/github/stars/Class-Widgets/class-widgets-sdk?style=for-the-badge&color=orange&label=%E6%98%9F%E6%A0%87)](https://github.com/Class-Widgets/class-widgets-sdk/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg?style=for-the-badge)](https://github.com/Class-Widgets/class-widgets-sdk/)

</div>

> [!CAUTION]
> 
> 本项目还处**在开发**阶段，API 接口可能随时发生变化，敬请谅解。
> 
> This project is still **in development**. The API may change at any time, so please bear with us.

## Overview
`class-widgets-sdk` provides the **essential base classes**, **development tools** (like scaffolding and packaging), and **complete type hints** for creating plugins for Class Widgets 2.

This package provides the core SDK for development and must be installed in your plugin's environment. Plugins are executed within the Class Widgets 2 main application.

## Installation

```bash
pip install class-widgets-sdk
```

## Getting Started
### 1. Create a new plugin
Use the included CLI tool to generate a new plugin project structure:
```bash
cw-plugin-init com.example.myplugin
```

### 2. Install dependencies
Navigate to your new plugin directory and install the SDK in editable mode:

```bash
cd com.example.myplugin
pip install -e .
```

### 3. Usage (Base Class & Types)
The SDK provides the base class `CW2Plugin` and models for configuration, giving you full IDE autocompletion and static analysis support.

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

### 4. Package
Use the included CLI tool to build and package your plugin into a distributable `.cwplugin` or `.zip` file:

```bash
cw-plugin-pack
```

## Tools
The SDK includes powerful command-line tools for plugin development and distribution:

| Command | Description |
| :--- | :--- |
| `cw-plugin-init` | Generate a new plugin project scaffold. |
| `cw-plugin-pack` | Build and package the plugin into a distributable `.cwplugin` or `.zip` file. |

<details>
<summary align="center">
Learn more >
</summary>

### `cw-plugin-init`

Initialize a new Class Widgets plugin project with an interactive setup wizard.

**Usage:**
```bash
# Create plugin in current directory (interactive)
cw-plugin-init

# Create plugin in specific directory
cw-plugin-init my-plugin

# Force overwrite existing files
cw-plugin-init my-plugin --force
```

#### Flow:
1. Select location (current dir or new folder)
2. Enter plugin metadata (name, author, ID, etc.)
3. Confirm and generate files

### `cw-plugin-pack`

Build and package the plugin into a distributable `.cwplugin` or `.zip` file.

```bash
# Package current directory (default: .cwplugin)
cw-plugin-pack

# Specify format (.cwplugin or .zip)
cw-plugin-pack --format zip

# Specify output path
cw-plugin-pack -o ./dist/my-plugin.cwplugin

# Package specific directory
cw-plugin-pack ./my-plugin
```

#### Format
- `.cwplugin` - Recommended plugin format
- `.zip` - Standard archive format

</details>

## How It Works
1.  **Development**: You install this SDK package to get base classes, type hints, autocompletion, and static type checking (with mypy/pyright) in your IDE.
2.  **Runtime**: When your plugin is loaded by the Class Widgets 2 main application, your `CW2Plugin` subclass is instantiated and executed.

> [!IMPORTANT]
> 
> - This package is the **Development Kit** for your plugin. Plugins must be tested within the [Class Widgets 2](https://github.com/RinLit-233-shiroko/Class-Widgets-2) main application.
> - The import path for the SDK is `ClassWidgets.SDK`.

## Links
- [Class Widgets 2](https://github.com/rinlit-233-shiroko/class-widgets-2)
- [Report an Issue](https://github.com/rinlit-233-shiroko/class-widgets-2/issues)

## License
This project is licensed under the **MIT License** - see the [LICENSE.md](LICENSE.md) file for details.