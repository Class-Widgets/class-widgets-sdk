from typing import Optional, Union, Any
from pathlib import Path
from enum import IntEnum
from pydantic import BaseModel

from .api import QObject


class NotificationLevel(IntEnum):
    """
    通知级别枚举
    """
    INFO = 0          # 普通提示
    ANNOUNCEMENT = 1  # 上下课 / 状态
    WARNING = 2       # 更新 / 风险
    SYSTEM = 3        # 内部


class NotificationData(BaseModel):
    """
    通知数据模型
    """
    provider_id: str
    level: int
    title: str
    message: Optional[str] = None
    icon: Optional[Union[str, Path]] = None
    duration: int = 4000
    closable: bool = True
    silent: bool = False
    use_system: bool = False


class NotificationProvider(QObject):
    """
    通知提供者类
    一个 Provider = 一个通知来源（模块 / 插件）
    """
    
    # 属性
    id: str
    name: str
    icon: Optional[str]
    use_system_notify: bool
    manager: Any

    def __init__(
        self,
        id: str,
        name: str,
        icon: Optional[Union[str, Path]] = ...,
        use_system_notify: bool = ...,
        manager: Any = ...
    ) -> None: ...
    
    def get_config(self) -> Any: ...
    
    def push(
        self,
        level: int,
        title: str,
        message: Optional[str],
        duration: int,
        closable: bool
    ) -> None: ...


__all__ = [
    'NotificationLevel',
    'NotificationData', 
    'NotificationProvider'
]