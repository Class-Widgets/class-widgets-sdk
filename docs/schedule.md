# ScheduleAPI

`ScheduleAPI` 用来读取、重新加载和更新当前课程表。

## 常用方法

- `get()`: 获取当前 Schedule 对象。
- `reload()`: 重新加载课程表。
- `update(schedule_dict)`: 用字典更新课程表，返回是否成功。
- `set_readonly(readonly)`: 设置课程表是否只读。
- `readonly`: 当前只读状态。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        schedule = self.api.schedule.get()
        print(schedule)

        self.api.schedule.set_readonly(True)
        self.api.schedule.reload()
```

`update()` 需要传入主程序能识别的课程表字典结构。
