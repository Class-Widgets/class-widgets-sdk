# Class Widgets SDK Docs

这里是 `ClassWidgets.SDK` 的项目级文档入口。

## 导航

- [快速开始](quick-start.md)
- [API 参考](api-reference.md)
  - [WidgetsAPI](widgets.md)
  - [NotificationAPI](notification.md)
  - [ScheduleAPI](schedule.md)
  - [ScheduleManagementAPI](schedule-management.md)
  - [GlobalConfigAPI](global-config.md)
  - [ApplicationAPI](application.md)
  - [DiagnosticsAPI](diagnostics.md)
  - [ThemeAPI](theme.md)
  - [RuntimeAPI](runtime.md)
  - [ConfigAPI](config.md)
  - [AutomationAPI](automation.md)
  - [ActionsAPI](actions.md)
  - [UiAPI](ui.md)

## 先看这个

SDK 主要提供类型声明、插件基类占位、配置模型类型和开发工具。插件运行时的真实能力仍由 Class Widgets 2 主程序注入。

最常见的流程是：

1. `pip install class-widgets-sdk`
2. 用 `CW2Plugin` 写插件入口
3. 在 `on_load()` 里注册配置、Widget、设置页或快捷方式

## 最小示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        self.api.ui.register_settings_page(
            qml_path="assets/settings.qml",
            title="My Plugin",
        )
```
