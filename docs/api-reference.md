# API 参考

所有核心能力都从 `PluginAPI` 进入。

```python
class PluginAPI:
    widgets: WidgetsAPI
    notification: NotificationAPI
    schedule: ScheduleAPI
    schedulemanagement: ScheduleManagementAPI
    globalconfig: GlobalConfigAPI
    application: ApplicationAPI
    diagnostics: DiagnosticsAPI
    theme: ThemeAPI
    runtime: RuntimeAPI
    config: ConfigAPI
    automation: AutomationAPI
    actions: ActionsAPI
    ui: UiAPI
```

## 组件

- [`WidgetsAPI`](widgets.md): 注册 Widget
- [`NotificationAPI`](notification.md): 注册通知提供者
- [`ScheduleAPI`](schedule.md): 读取和更新课程表
- [`ScheduleManagementAPI`](schedule-management.md): 切换和保存课程表
- [`GlobalConfigAPI`](global-config.md): 访问全局配置
- [`ApplicationAPI`](application.md): 读取应用信息和重启
- [`DiagnosticsAPI`](diagnostics.md): 读取日志
- [`ThemeAPI`](theme.md): 读取主题
- [`RuntimeAPI`](runtime.md): 读取当前运行态
- [`ConfigAPI`](config.md): 注册插件配置模型
- [`AutomationAPI`](automation.md): 注册自动化任务
- [`ActionsAPI`](actions.md): 注册全局 Action
- [`UiAPI`](ui.md): 注册设置页和托盘快捷方式
