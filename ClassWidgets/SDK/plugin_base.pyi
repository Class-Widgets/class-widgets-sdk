from typing import Dict, Any, Optional
from pathlib import Path
from enum import IntEnum
from pydantic import BaseModel

from .api import PluginAPI

from .base_model import QObject, Signal

class ConfigBaseModel(BaseModel):
    """
    插件配置模型的基类
    继承自Pydantic的BaseModel，提供配置数据验证和管理功能
    """
    ...


# CW2Plugin
class CW2Plugin(QObject):
    """
    所有Class Widgets 2插件的基类
    
    提供插件生命周期管理、API访问和插件注册功能
    """
    initialized: Signal
    
    # 插件属性
    PATH: Path  # 插件根目录路径
    meta: Dict[str, Any]  # 插件元数据
    pid: Optional[str]  # 插件ID
    api: PluginAPI  # 插件API实例

    def __init__(self, api: PluginAPI) -> None:
        """
        初始化插件实例
        
        :param api: PluginAPI实例，用于与主应用程序交互
        """
        ...

    def _load_plugin_libs(self) -> None:
        """
        自动将插件的'lib'子目录添加到sys.path
        这是一个内部方法
        """
        ...

    def on_load(self) -> None:
        """
        当插件被加载时调用
        如果存在meta.id，则向后端桥注册插件
        """
        ...

    def on_unload(self) -> None:
        """
        当插件被卸载时调用
        插件应该在此方法中清理资源
        """
        ...


__all__ = ['CW2Plugin', 'ConfigBaseModel']