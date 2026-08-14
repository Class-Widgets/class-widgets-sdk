# NotificationAPI

`NotificationAPI` 用来注册通知提供者，并通过提供者推送通知。

## 常用方法

- `get_provider(provider_id, name=None, icon=None, use_system_notify=False)`: 获取已有提供者，不存在时通常会创建或返回可用对象。
- `register_provider(provider_id, name=None, icon=None, use_system_notify=False)`: 注册通知提供者。

## 信号

- `pushed`: 有通知被推送时触发。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        provider = self.api.notification.register_provider(
            provider_id="com.example.notice",
            name="Example Notice",
            icon="assets/icon.png",
            use_system_notify=True,
        )
        provider.push(title="Hello", content="Plugin loaded")
```

通知内容结构由 `NotificationProvider` 和 `NotificationPayload` 定义。
