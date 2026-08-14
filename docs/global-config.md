# GlobalConfigAPI

`GlobalConfigAPI` 用来访问和锁定主程序的全局配置。

## 常用属性和方法

- `configs`: 全局配置管理器。
- `lock(keys)`: 锁定一个或多个配置项。
- `unlock(keys)`: 解锁一个或多个配置项。
- `is_locked(key)`: 检查配置项是否被锁定。
- `locked_keys`: 当前被锁定的配置项集合。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        self.api.globalconfig.lock(["theme", "schedule"])

        if self.api.globalconfig.is_locked("theme"):
            print("theme config is locked")
```

只在确实需要接管某项全局配置时使用锁定能力。
