from typing import Dict, Any
from pathlib import Path

from pydantic import BaseModel

from .api import PluginAPI, QObject


class ConfigBaseModel(BaseModel): ...


# CW2Plugin
class CW2Plugin(QObject):
    """
    :param api: PluginAPI instance
    """
    PATH: Path
    meta: Dict[str, Any]
    pid: str
    api: PluginAPI

    def __init__(self, api: Any) -> None:
        """
        Initialize the plugin.

        :param api: PluginAPI instance for interacting with the host application
        """
        ...

    def _load_plugin_libs(self) -> None:
        """
        Automatically adds the plugin's 'lib' subdirectory to sys.path.
        This is an internal method.
        """
        ...

    def on_load(self) -> None:
        """
        Called when the plugin is loaded.
        Registers the plugin with the backend bridge if meta.id exists.
        """
        ...

    def on_unload(self) -> None:
        """
        Called when the plugin is unloaded.
        """
        ...


__all__ = ['CW2Plugin']