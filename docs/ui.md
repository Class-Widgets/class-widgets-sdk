# UiAPI

`UiAPI` 管理设置页和托盘快捷方式。

## 信号

- `settingsPageRegistered`
- `shortcutsChanged`

## 属性

- `pages`
- `shortcuts`

## 设置页

```python
self.api.ui.register_settings_page(
    qml_path="assets/settings.qml",
    title="Weather Settings",
    icon="ic_fluent_weather_sunny_20_regular",
)

self.api.ui.unregister_settings_page("assets/settings.qml")
```

## 托盘快捷方式

```python
shortcut_id = self.api.ui.register_shortcut(
    shortcut_id="open-dashboard",
    name="Open dashboard",
    icon="assets/dashboard.png",
    action=self.open_dashboard,
)

self.api.ui.set_shortcut_name(shortcut_id, "Open dashboard now")
self.api.ui.invoke_shortcut(shortcut_id)
self.api.ui.unregister_plugin_shortcuts(self.pid)
```

`register_shortcut()` 在插件上下文里会自动把 ID 变成 `<plugin id>.<shortcut_id>`。
