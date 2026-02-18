from typing import Dict, List, Optional, Any, Union, TypedDict
from datetime import datetime
from pathlib import Path
from enum import Enum

from .notification import NotificationPayload, NotificationProvider
from .base_model import QObject, Signal


class ConfigBaseModel: ...


class RuntimeMetaPayload(TypedDict):
    id: str
    version: int
    maxWeekCycle: int
    startDate: str


class RuntimeEntryPayload(TypedDict):
    id: str
    type: str
    startTime: str
    endTime: str
    subjectId: Optional[str]
    title: Optional[str]


class RuntimeEntryChangedPayload(TypedDict, total=False):
    id: str
    type: str
    startTime: str
    endTime: str
    subjectId: Optional[str]
    title: Optional[str]


class RuntimeSubjectPayload(TypedDict):
    id: str
    name: str
    simplifiedName: Optional[str]
    teacher: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    location: Optional[str]
    isLocalClassroom: bool


class RuntimeRemainingTimePayload(TypedDict):
    minute: int
    second: int


class SettingsPagePayload(TypedDict):
    id: str
    page: str
    title: str
    icon: str


class EntryType(str, Enum):
    CLASS = "class"
    BREAK = "break"
    FREE = "free"
    ACTIVITY = "activity"
    UNKNOWN = "unknown"


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


# NotificationAPI
class NotificationAPI(QObject):
    pushed: Signal[NotificationPayload]

    def __init__(self, app: Any) -> None: ...

    def get_provider(
        self,
        provider_id: str,
        name: Optional[str] = ...,
        icon: Optional[Union[str, Path]] = ...,
        use_system_notify: bool = ...
    ) -> NotificationProvider: ...

    def register_provider(
        self,
        provider_id: str,
        name: Optional[str] = ...,
        icon: Optional[Union[str, Path]] = ...,
        use_system_notify: bool = ...
    ) -> NotificationProvider: ...


# ScheduleAPI
class ScheduleAPI:
    def __init__(self, app: Any) -> None: ...

    def get(self) -> Any: ...  # 返回 Schedule 对象

    def reload(self) -> None: ...


# ThemeAPI
class ThemeAPI(QObject):
    changed: Signal[str]

    def __init__(self, app: Any) -> None: ...

    def current(self) -> Optional[str]: ...


# RuntimeAPI
class RuntimeAPI(QObject):
    updated: Signal
    statusChanged: Signal[str]
    entryChanged: Signal[RuntimeEntryChangedPayload]

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
    def schedule_meta(self) -> Optional[RuntimeMetaPayload]: ...

    @property
    def current_day_entries(self) -> List[RuntimeEntryPayload]: ...

    @property
    def current_entry(self) -> Optional[RuntimeEntryPayload]: ...

    @property
    def next_entries(self) -> List[RuntimeEntryPayload]: ...

    @property
    def remaining_time(self) -> RuntimeRemainingTimePayload: ...

    @property
    def progress(self) -> float: ...

    @property
    def current_status(self) -> str: ...

    @property
    def current_subject(self) -> Optional[RuntimeSubjectPayload]: ...

    @property
    def current_title(self) -> Optional[str]: ...


# ConfigAPI
class ConfigAPI:
    def __init__(self, app: Any) -> None: ...

    def register_plugin_model(self, plugin_id: str, model: ConfigBaseModel) -> None: ...

    def get_plugin_model(self, plugin_id: str) -> Optional[ConfigBaseModel]: ...

    def save(self) -> Any: ...


# AutomationAPI
class AutomationAPI:
    def __init__(self, app: Any) -> None: ...

    def register(self, task: Any) -> None: ...


# UiAPI
class UiAPI(QObject):
    settingsPageRegistered: Signal

    def __init__(self, app: Any) -> None: ...

    @property
    def pages(self) -> List[SettingsPagePayload]: ...

    def unregister_settings_page(self, qml_path: Union[str, Path]) -> None: ...

    def register_settings_page(
            self,
            qml_path: Union[str, Path],
            title: Optional[str] = ...,
            icon: Optional[str] = ...
    ) -> None: ...


# PluginAPI
class PluginAPI:
    def __init__(self, app: Any) -> None: ...

    def set_current_plugin(self, plugin: Any) -> None: ...

    @property
    def current_plugin(self) -> Any: ...

    widgets: WidgetsAPI
    notification: NotificationAPI
    schedule: ScheduleAPI
    theme: ThemeAPI
    runtime: RuntimeAPI
    config: ConfigAPI
    automation: AutomationAPI
    ui: UiAPI


__all__ = [
    'RuntimeMetaPayload',
    'RuntimeEntryPayload',
    'RuntimeEntryChangedPayload',
    'RuntimeSubjectPayload',
    'RuntimeRemainingTimePayload',
    'SettingsPagePayload',
    'EntryType',
    'WidgetsAPI',
    'NotificationAPI',
    'ScheduleAPI',
    'ThemeAPI',
    'RuntimeAPI',
    'ConfigAPI',
    'AutomationAPI',
    'UiAPI',
    'PluginAPI',
]