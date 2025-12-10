"""
Class Widgets 2 Plugin SDK
包含用于创建、打包插件的命令行工具。
"""

from .manifest import PluginManifestModel
from .scaffold import PluginScaffold, create_plugin
from .packager import PluginPackager, pack_plugin

__all__ = [
    'PluginManifestModel',
    'PluginScaffold',
    'create_plugin',
    'pack_plugin',
    'PluginPackager',
]