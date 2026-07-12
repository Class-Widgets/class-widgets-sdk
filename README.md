<div align="center">

<img src="/docs/logo.png" width="15%" alt="Class Widgets 2">
<h1>Class Widgets SDK</h1>
<p>适用于 Class Widgets 2 插件开发的完整 SDK、工具和类型提示。</p>

**中文** | [English](README_EN.md)

[![PyPI version](https://img.shields.io/pypi/v/class-widgets-sdk.svg?style=for-the-badge&color=blue)](https://pypi.org/project/class-widgets-sdk/)
[![星标](https://img.shields.io/github/stars/Class-Widgets/class-widgets-sdk?style=for-the-badge&color=orange&label=%E6%98%9F%E6%A0%87)](https://github.com/Class-Widgets/class-widgets-sdk/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg?style=for-the-badge)](https://github.com/Class-Widgets/class-widgets-sdk/)

</div>

> [!NOTE]
> 
> 本项目还处**在开发**阶段，API 接口可能随时发生变化，敬请谅解。
> 
> This project is still **in development**. The API may change at any time, so please bear with us.
>
> 可从 [Class-Widgets/Plugin-Template-V2](https://github.com/Class-Widgets/plugin-template-v2) 获取最新的插件模板、工作流以快速开始。

## 概述
`class-widgets-sdk` 为创建 Class Widgets 2 插件提供了**核心基类**、**开发工具**（如脚手架和打包）以及**完整的类型提示**。

该包提供了开发所需的核心 SDK，必须安装在你的插件环境中。插件将在 Class Widgets 2 主应用程序中运行。

## 安装

```bash
pip install class-widgets-sdk
```

## 快速开始
### 1. 创建新插件
使用附带的 CLI 工具生成新的插件项目结构：
```bash
cw-plugin-init com.example.myplugin
```

### 2. 安装依赖
进入插件目录并以可编辑模式安装 SDK：

```bash
cd com.example.myplugin
pip install -e .
```

### 3. 使用（基类和类型）
SDK 提供了基类 `CW2Plugin` 和配置模型，支持完整的 IDE 自动补全和静态分析。

```python
from ClassWidgets.SDK import CW2Plugin, ConfigBaseModel, PluginAPI

class MyConfig(ConfigBaseModel):
    enabled: bool = True
    text: str = "你好，世界"

class MyPlugin(CW2Plugin):
    
    def __init__(self, api: PluginAPI):
        super().__init__(api)
        self.config = MyConfig()
    
    def on_load(self):
        self.api.config.register_plugin_model(self.pid, self.config)
        # 你的 IDE 将提供完整的自动补全
        self.api.widgets.register(
            widget_id="com.example.mywidget",
            name="My Widget",
            qml_path="path/to/mywidget.qml"
        )
```

### 4. 打包
使用附带的 CLI 工具构建并打包插件为可分发的 `.cwplugin` 或 `.zip` 文件：

```bash
cw-plugin-pack
```

## 工具
SDK 包含了强大的命令行工具，用于插件开发和分发：

| 命令 | 描述 |
| :--- | :--- |
| `cw-plugin-init` | 生成新的插件项目脚手架。 |
| `cw-plugin-pack` | 构建并打包插件为可分发的 `.cwplugin` 或 `.zip` 文件。 |
| `cw-plugin-publish` | 将插件发布到 Class Widgets 插件注册中心。 |


<details>
<summary align="center">
了解更多 >
</summary>

### `cw-plugin-init`

使用交互式设置向导初始化一个新的 Class Widgets 插件项目。

**用法：**
```bash
# 在当前目录创建插件（交互式）
cw-plugin-init

# 在指定目录创建插件
cw-plugin-init my-plugin

# 强制覆盖已有文件
cw-plugin-init my-plugin --force
```

#### 流程：
1. 选择位置（当前目录或新文件夹）
2. 输入插件元数据（名称、作者、ID 等）
3. 确认并生成文件

### `cw-plugin-pack`

构建并打包插件为可分发的 `.cwplugin` 或 `.zip` 文件。

```bash
# 打包当前目录（默认格式：.cwplugin）
cw-plugin-pack

# 指定格式（.cwplugin 或 .zip）
cw-plugin-pack --format zip

# 指定输出路径
cw-plugin-pack -o ./dist/my-plugin.cwplugin

# 打包指定目录
cw-plugin-pack ./my-plugin
```

#### 格式
- `.cwplugin` - 推荐的插件格式
- `.zip` - 标准归档格式

### `cw-plugin-publish`

将插件发布到 Class Widgets 插件注册中心。该命令会读取 `cwplugin.json` 并将插件元数据发送到注册中心 API。

```bash
# 发布当前目录插件（从 CWPT_TOKEN 环境变量读取令牌）
cw-plugin-publish

# 使用显式令牌发布
cw-plugin-publish --token cwpt_xxxxxxxxxxxxxxxxxxxx

# 试运行 — 验证和预览（不发布到插件广场）
cw-plugin-publish --dry-run

# 使用自定义 API URL 进行调试
cw-plugin-publish --api-url http://localhost:1145 

# 指定分支（默认从 git 自动检测）
cw-plugin-publish --branch dev
```

#### 选项：
- `--token, -t` — 发布令牌（或设置 `CWPT_TOKEN` 环境变量）
- `--api-url` — API 基础 URL（默认：`https://plaza.cw.rinlit.cn/`）
- `--branch, -b` — 仓库分支（从 git 自动检测，回退：`main`）
- `--dry-run` — 验证和预览而不实际发布

#### `cwplugin.json` 发布字段：

| 字段 | 必需 | 描述 |
| :--- | :--- | :--- |
| `id` | 是 | 插件 ID |
| `name` | 是 | 插件显示名称 |
| `version` | 是 | 插件版本 |
| `api_version` | 是 | 所需 API 版本 |
| `url` | 是 | 仓库 URL |
| `description` | 否 | 插件描述 |
| `readme` | 否 | README 文件路径（默认：`README.md`） |
| `icon` | 否 | 图标文件路径（默认：`icon.png`） |

[//]: # (| `tag_ids` | 否 | 注册中心的标签 ID 列表 &#40;例如：`["ai", "tools"]`&#41; |)

</details>


## 工作原理
1.  **开发**：安装此 SDK 包后，你可以在 IDE 中获得基类、类型提示、自动补全和静态类型检查（使用 mypy/pyright）。
2.  **运行时**：当你的插件被 Class Widgets 2 主应用程序加载时，你的 `CW2Plugin` 子类将被实例化并执行。

> [!IMPORTANT]
> 
> - 该包是插件的**开发工具包**。插件必须在 [Class Widgets 2](https://github.com/RinLit-233-shiroko/Class-Widgets-2) 主应用程序中测试。
> - SDK 的导入路径为 `ClassWidgets.SDK`。

## 链接
- [Class Widgets 2](https://github.com/rinlit-233-shiroko/class-widgets-2)
- [报告 Issue](https://github.com/rinlit-233-shiroko/class-widgets-2/issues)

## 许可证
本项目基于 **MIT 许可证** 授权 - 详见 [LICENSE.md](LICENSE.md) 文件。
