# ScheduleManagementAPI

`ScheduleManagementAPI` 用来管理多个课程表文件或配置。

## 常用方法

- `list()`: 列出可用课程表。
- `switch(name)`: 切换到指定课程表。
- `add(name)`: 新增课程表。
- `save(name)`: 保存当前课程表为指定名称。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        schedules = self.api.schedulemanagement.list()
        for item in schedules:
            print(item["name"])

        self.api.schedulemanagement.switch("default")
```

返回的列表项是 `dict[str, str]`，具体字段以主程序版本为准。
