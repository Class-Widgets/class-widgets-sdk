"""
Class Widgets 2 Stubs-Only SDK

插件需要在 Class Widgets 2 本体中调试及运行.
You should debug and run plugins in Class Widgets 2.
"""

from .plugin_base import CW2Plugin
from .config import ConfigBaseModel
from .api import PluginAPI
from .notification import NotificationProvider, NotificationLevel, NotificationData

__version__: str
__author__: str

__all__ = [
    'CW2Plugin',
    'ConfigBaseModel',
    'PluginAPI',
    'NotificationProvider',
    'NotificationLevel',
    'NotificationData',
    "__version__",
    "__author__",
]