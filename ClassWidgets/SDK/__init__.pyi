"""
Class Widgets 2 Stubs-Only SDK

插件需要在 Class Widgets 2 本体中调试及运行.
You should debug and run plugins in Class Widgets 2.
"""

import sys
from typing import TYPE_CHECKING

from .plugin_base import CW2Plugin
from .config import ConfigBaseModel
from .api import PluginAPI

# 版本信息
__version__ = '0.1.0'
__author__ = 'Class Widgets Official'


__all__ = [
    'CW2Plugin',
    'ConfigBaseModel',
    'PluginAPI'
]


if not TYPE_CHECKING and 'PySide6' not in sys.modules:
    import warnings
    warnings.warn(
        "Class Widgets 2 SDK is type-hints only. "
        "Plugins must run inside Class Widgets 2 main program.",
        ImportWarning,
        stacklevel=2
    )