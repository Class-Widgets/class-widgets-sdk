"""
Class Widgets 2 Plugin SDK (Runtime Tools)
"""
import sys
from typing import TYPE_CHECKING

__version__ = '0.1.1'
__author__ = 'Class Widgets Official'


class CW2Plugin:
    pass

class ConfigBaseModel:
    pass

class PluginAPI:
    pass


__all__ = ['CW2Plugin', 'ConfigBaseModel', 'PluginAPI', '__version__', '__author__']


if 'PySide6' not in sys.modules and not TYPE_CHECKING:
    import warnings
    warnings.warn(
        "Class Widgets 2 SDK is type-hints only for core APIs. "
        "Plugins must run inside Class Widgets 2 main program.",
        ImportWarning,
        stacklevel=2
    )