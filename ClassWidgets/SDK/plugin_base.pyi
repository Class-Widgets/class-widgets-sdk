from typing import Dict, Any
from pathlib import Path
from .api import PluginAPI, QObject


class ConfigBaseModel: ...


# CW2Plugin
class CW2Plugin(QObject):
    """
    :param api: PluginAPI instance
    """
    PATH: Path
    meta: Dict[str, str] = {
        'id': 'com.example.plugin',
        'name': 'Example Plugin',
        'author': '<NAME>',
        'description': 'This is an example plugin',
        'version': '1.0.0',
        'api_version': '1.0.0',
    }
    pid: str = 'com.example.plugin'
    api: PluginAPI

    def __init__(self, api: Any) -> None: ...

    def on_load(self) -> None: ...

    def on_unload(self) -> None: ...


__all__ = ['CW2Plugin']