# RuntimeAPI

`RuntimeAPI` 用来读取当前时间、课程运行状态、当前课程和进度。

## 常用属性

- `current_time`: 当前时间。
- `current_day_of_week`: 当前星期。
- `current_week`: 当前周数。
- `current_week_of_cycle`: 当前循环周。
- `time_offset`: 时间偏移。
- `schedule_meta`: 当前课程表元数据。
- `current_day_entries`: 当天条目。
- `current_entry`: 当前条目。
- `next_entries`: 后续条目。
- `remaining_time`: 当前条目剩余时间。
- `progress`: 当前进度，通常是 `0.0` 到 `1.0`。
- `current_status`: 当前状态。
- `current_subject`: 当前科目。
- `current_title`: 当前标题。

## 信号

- `updated`: 运行态更新时触发。
- `statusChanged`: 状态变化时触发。
- `entryChanged`: 当前条目变化时触发。

## 示例

```python
from ClassWidgets.SDK import CW2Plugin, PluginAPI


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI) -> None:
        super().__init__(api)

    def on_load(self) -> None:
        super().on_load()
        self.api.runtime.updated.connect(self.refresh)
        self.refresh()

    def refresh(self) -> None:
        entry = self.api.runtime.current_entry
        remaining = self.api.runtime.remaining_time
        print(entry, remaining["minute"], remaining["second"])
```

运行态数据大多是只读快照，插件应通过信号更新自己的显示。
