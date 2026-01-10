"""
Class Widgets 2 Plugin SDK (Runtime Tools)
"""
import sys
from typing import TYPE_CHECKING

__version__ = '0.3.1'
__author__ = 'Class Widgets Official'

if TYPE_CHECKING:
    from .api import (
        WidgetsAPI,
        NotificationAPI,
        ScheduleAPI,
        ThemeAPI,
        RuntimeAPI,
        ConfigAPI,
        AutomationAPI,
        UiAPI,
        PluginAPI,
    )

    from .plugin_base import CW2Plugin
    from .config import ConfigBaseModel
else:
    CW2Plugin = type('CW2Plugin', (), {})
    ConfigBaseModel = type('ConfigBaseModel', (), {})
    PluginAPI = type('PluginAPI', (), {})
    WidgetsAPI = type('WidgetsAPI', (), {})
    NotificationAPI = type('NotificationAPI', (), {})
    ScheduleAPI = type('ScheduleAPI', (), {})
    ThemeAPI = type('ThemeAPI', (), {})
    RuntimeAPI = type('RuntimeAPI', (), {})
    ConfigAPI = type('ConfigAPI', (), {})
    AutomationAPI = type('AutomationAPI', (), {})
    UiAPI = type('UiAPI', (), {})

__all__ = [
    'CW2Plugin', 
    'ConfigBaseModel', 
    'PluginAPI',
    'WidgetsAPI',
    'NotificationAPI',
    'ScheduleAPI',
    'ThemeAPI',
    'RuntimeAPI',
    'ConfigAPI',
    'AutomationAPI',
    'UiAPI',
    '__version__', 
    '__author__'
]


if 'PySide6' not in sys.modules and not TYPE_CHECKING:
    import warnings
    warnings.warn(
        "Class Widgets 2 SDK is type-hints only for core APIs. "
        "Plugins must run inside Class Widgets 2 main program.",
        ImportWarning,
        stacklevel=2
    )