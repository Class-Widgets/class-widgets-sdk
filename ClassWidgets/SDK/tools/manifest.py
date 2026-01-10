from typing import Optional
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ConfigDict
import json

from ClassWidgets.SDK import __version__ as sdk_version


class PluginManifestModel(BaseModel):
    """
    Data model for the plugin manifest file (cwplugin.json).
    插件清单文件的数据模型。
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "com.example.myplugin",
                "name": "My Plugin",
                "version": "1.0.0",
                "api_version": "~=2.0.0",
                "entry": "main.py",
                "author": "Developer Name",
                "description": "A useful plugin.",
                "url": "https://github.com/owner/repo",
                "readme": "README.md",
                "icon": "icon.png"
            }
        }
    )

    # Required fields 必填字段
    id: str = Field(...,
                    description="Unique plugin identifier (e.g., 'com.example.myplugin'). 唯一插件标识符")
    name: str = Field(...,
                      description="Display name of the plugin. 插件的显示名称")
    version: str = Field("1.0.0",
                         description="Plugin version, following SemVer. 插件版本，遵循语义化版本控制")
    api_version: str = Field(f"~={sdk_version}",
                             description="Required main application API version (PEP 440). 所需主程序API版本")
    entry: str = Field("main.py",
                       description="Entry point Python file. 入口Python文件")
    author: str = Field(...,
                        description="Author name. 作者名称")

    # Optional fields 可选字段
    description: Optional[str] = Field(None,
                                       description="Short description of the plugin. 插件简短描述")
    url: Optional[str] = Field(None,
                               description="Project homepage or repository URL. 项目主页或仓库URL")
    readme: Optional[str] = Field("README.md",
                                  description="Path to the README file. 自述文件路径")
    icon: Optional[str] = Field(None,
                                description="Path to the icon file. 图标文件路径")

    # --- Validators 验证器 ---
    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        if not v or '.' not in v:
            raise ValueError(
                'Plugin ID must contain a dot (e.g., "com.example.plugin"). '
                '插件ID必须包含点号（例如："com.example.plugin"）。'
            )
        return v

    @field_validator('entry')
    @classmethod
    def validate_entry_exists(cls, v: str):
        # This validator is mainly for loading existing manifests.
        # 此验证器主要用于加载已存在的清单。
        # The scaffold tool will create the file later.
        # 脚手架工具会在之后创建该文件。
        return v

    def save(self, path: Path) -> None:
        """Save the manifest to a JSON file. 将清单保存为JSON文件。"""
        with open(path, 'w', encoding='utf-8') as f:
            # Use the Pydantic model's model_dump and dump with json for prettier formatting
            # 使用Pydantic模型的model_dump方法，并用json库进行美化输出
            data = self.model_dump(exclude_none=True)
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add newline at EOF

    @classmethod
    def load(cls, path: Path) -> 'PluginManifestModel':
        """Load a manifest from a JSON file. 从JSON文件加载清单。"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.model_validate(data)