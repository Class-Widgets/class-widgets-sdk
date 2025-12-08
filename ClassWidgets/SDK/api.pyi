from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from pathlib import Path


class QObject: ...


class Signal: ...


class ConfigBaseModel: ...


# WidgetsAPI
class WidgetsAPI:
    def __init__(self, app: Any) -> None: ...

    def register(
            self,
            widget_id: str,
            name: str,
            qml_path: Union[str, Path],
            backend_obj: Optional[QObject] = ...,
            settings_qml: Optional[Union[str, Path]] = ...,
            default_settings: Optional[Dict[str, Any]] = ...
    ) -> None: ...


# NotifyAPI
class NotifyAPI(QObject):
    pushed: Signal  # Signal(str)

    def __init__(self, app: Any) -> None: ...

    def send(self, message: str) -> None: ...


# ScheduleAPI
class ScheduleAPI:
    def __init__(self, app: Any) -> None: ...

    def get(self) -> Any: ...  # 返回 Schedule 对象

    def reload(self) -> None: ...


# ThemeAPI
class ThemeAPI(QObject):
    changed: Signal  # Signal(str)

    def __init__(self, app: Any) -> None: ...

    def current(self) -> Optional[str]: ...


# RuntimeAPI
class RuntimeAPI(QObject):
    updated: Signal  # Signal()
    statusChanged: Signal  # Signal(str)
    entryChanged: Signal  # Signal(dict)

    def __init__(self, app: Any) -> None: ...

    # 时间属性
    @property
    def current_time(self) -> datetime: ...

    @property
    def current_day_of_week(self) -> int: ...

    @property
    def current_week(self) -> int: ...

    @property
    def current_week_of_cycle(self) -> int: ...

    @property
    def time_offset(self) -> int: ...

    # 日程属性
    @property
    def schedule_meta(self) -> Optional[Dict[str, Any]]: ...

    @property
    def current_day_entries(self) -> List[Dict[str, Any]]: ...

    @property
    def current_entry(self) -> Optional[Dict[str, Any]]: ...

    @property
    def next_entries(self) -> List[Dict[str, Any]]: ...

    @property
    def remaining_time(self) -> Dict[str, int]: ...

    @property
    def progress(self) -> float: ...

    @property
    def current_status(self) -> str: ...

    @property
    def current_subject(self) -> Optional[Dict[str, Any]]: ...

    @property
    def current_title(self) -> Optional[str]: ...


# ConfigAPI
class ConfigAPI:
    def __init__(self, app: Any) -> None: ...

    def register_plugin_model(self, plugin_id: str, model: ConfigBaseModel) -> None: ...

    def get_plugin_model(self, plugin_id: str) -> Optional[ConfigBaseModel]: ...

    def save(self) -> None: ...


# AutomationAPI
class AutomationAPI:
    def __init__(self, app: Any) -> None: ...

    def register(self, task: Any) -> None: ...


# UiAPI
class UiAPI(QObject):
    settingsPageRegistered: Signal  # Signal()

    def __init__(self) -> None: ...

    @property
    def pages(self) -> List[Dict[str, Any]]: ...

    def unregister_settings_page(self, plugin: Any, qml_path: Union[str, Path]) -> None: ...

    def register_settings_page(
            self,
            plugin: Any,
            qml_path: Union[str, Path],
            title: Optional[str] = ...,
            icon: Optional[str] = ...
    ) -> None: ...


# PluginAPI
class PluginAPI:
    def __init__(self, app: Any) -> None: ...

    widgets: WidgetsAPI
    notify: NotifyAPI
    schedule: ScheduleAPI
    theme: ThemeAPI
    runtime: RuntimeAPI
    config: ConfigAPI
    automation: AutomationAPI
    ui: UiAPI


__all__ = [
    'WidgetsAPI',
    'NotifyAPI',
    'ScheduleAPI',
    'ThemeAPI',
    'RuntimeAPI',
    'ConfigAPI',
    'AutomationAPI',
    'UiAPI',
    'PluginAPI',
]