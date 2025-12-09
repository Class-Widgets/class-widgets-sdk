"""
Plugin Project Scaffolding Tool
Class Widgets SDK 插件项目脚手架工具
"""
import sys
import os
import time
import textwrap
import shutil
import subprocess
from pathlib import Path
from typing import Optional
import click

from ClassWidgets.SDK.tools.manifest import PluginManifestModel
from ClassWidgets.SDK import __version__ as sdk_version


# --- Visual & Text Assets ---
def tr(en: str, cn: str) -> str:
    """Return bilingual text string."""
    return f"{en} ({cn})"


# --- Templates ---
GITIGNORE_TEMPLATE = textwrap.dedent("""\
    __pycache__/
    *.pyc
    .env
    venv/
    .idea/
    .vscode/
    libs/
    dist/
    build/
    *.egg-info/
    *.cwplugin
""")

PYPROJECT_TEMPLATE = textwrap.dedent("""\
    [project]
    name = "{safe_name}"
    version = "{version}"
    description = "{description}"
    authors = [
        {{name = "{author}"}},
    ]
    readme = "README.md"
    requires-python = ">=3.8"
    dependencies = []

    [build-system]
    requires = ["setuptools"]
    build-backend = "setuptools.build_meta"
""")

ENTRY_PY_TEMPLATE = textwrap.dedent("""\
    \"\"\"
    {name}
    {description}
    \"\"\"
    
    from ClassWidgets.SDK import CW2Plugin, PluginAPI


    class Plugin(CW2Plugin):
        def __init__(self, api: PluginAPI):
            super().__init__(api)
            # 请在此导入第三方库 / Import third-party libraries here
    
        def on_load(self):
            super().on_load()
            print(f"{name} loaded")
            
        def on_unload(self):
            print(f"{name} unloaded")
""")

README_TEMPLATE = textwrap.dedent("""\
    # {name}
    
    {description}
    
    ## Getting Started / 开始使用
    
    1. Install dependencies / 安装依赖: 
       `pip install -e .`
       
    2. Run Class Widgets to test / 运行主程序测试.
""")

# --- Helper Functions ---

def get_git_remote_url() -> str:
    """Attempts to get the git remote origin url of the current repo."""
    try:
        url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        # 将 SSH URL 转换为 HTTPS (可选，视偏好而定)
        if url.startswith("git@"):
            url = url.replace(":", "/").replace("git@", "https://")
        url = url.removesuffix(".git") # Remove trailing ".git"
        return url
    except Exception:
        return ""

def print_info(key: str, value: str):
    """Prints a formatted key-value pair."""
    click.echo(f"    {click.style(key, fg='cyan', dim=True):<25} {value}")

def get_sdk_asset_path(filename: str) -> Optional[Path]:
    """Locates an asset file relative to this script."""
    # 假设结构: SDK/tools/scaffold.py -> SDK/assets/filename
    base_path = Path(__file__).parent.parent / "assets"
    asset_path = base_path / filename
    return asset_path if asset_path.exists() else None

# --- Core Logic ---

class PluginScaffold:
    def __init__(self, target_dir: Path, manifest: PluginManifestModel):
        self.target_dir = target_dir
        self.manifest = manifest

    def create(self, force: bool = False):
        """Executes the scaffolding process."""

        # 1. Prepare Directories
        if not self.target_dir.exists():
            self.target_dir.mkdir(parents=True)

        subdirs = ['qml', 'assets']
        for d in subdirs:
            (self.target_dir / d).mkdir(exist_ok=True)

        # 2. Define File Generation Tasks
        files = {
            "cwplugin.json": self._generate_manifest,
            self.manifest.entry: self._generate_entry,
            "README.md": self._generate_readme,
            ".gitignore": lambda: GITIGNORE_TEMPLATE,
            "pyproject.toml": self._generate_pyproject,
            "icon.png": self._copy_icon  # New: Icon handling
        }

        # 3. Execute
        with click.progressbar(
            files.items(),
            label=click.style('Creating files / 正在生成文件', fg='cyan'),
            length=len(files)
        ) as bar:
            for filename, generator in bar:
                content = generator()
                # If content is None, it means the generator handled the file IO (like copying)
                if content is not None:
                    self._write(filename, content, force)
                time.sleep(0.05) # Visual smoothing

    def _write(self, filename: str, content: str, force: bool):
        path = self.target_dir / filename
        if path.exists() and not force:
            return

        if filename == "cwplugin.json":
            # Version constraint logic
            if self.manifest.api_version == ">=2.0.0":
                major = sdk_version.split('.')[0]
                self.manifest.api_version = f">={major}.0.0"
            self.manifest.save(path)
        else:
            path.write_text(content, encoding='utf-8')

    def _copy_icon(self) -> None:
        """Copies the default icon from SDK assets."""
        target_path = self.target_dir / "icon.png"
        if target_path.exists():
            return None

        source_path = get_sdk_asset_path("default_icon.png")
        if source_path:
            shutil.copy(source_path, target_path)
        else:
            # Fallback if SDK asset missing: create a dummy empty file or warn
            # click.secho("Warning: Default icon not found in SDK assets.", err=True, fg='yellow')
            pass
        return None

    def _generate_manifest(self): return "" # Handled specially inside _write

    def _generate_entry(self):
        return ENTRY_PY_TEMPLATE.format(**self.manifest.__dict__)

    def _generate_readme(self):
        return README_TEMPLATE.format(**self.manifest.__dict__)

    def _generate_pyproject(self):
        return PYPROJECT_TEMPLATE.format(
            safe_name=self.manifest.id.replace('.', '-').lower(),
            **self.manifest.__dict__
        )


@click.command()
@click.argument('plugin_dir', required=False)
@click.option('--force', is_flag=True, help='Overwrite existing files.')
def create_plugin(plugin_dir: Optional[str], force: bool):
    """
    Initialize a new Class Widgets plugin.
    初始化一个新的 Class Widgets 插件项目。
    """

    # --- 1. Clean Header (No ASCII Logo) ---
    click.clear()
    click.secho("Class Widgets Plugin Creator", fg='green', bold=True)
    click.secho("-" * 30, dim=True)

    # --- 2. Location Selection ---

    current_cwd = Path.cwd()

    if not plugin_dir:
        # Prompt: Create in current directory?
        click.echo(tr("Current directory", "当前目录") + f": {click.style(str(current_cwd), fg='cyan')}")

        if click.confirm(tr("Create project here?", "在此处创建项目?"), default=False):
            plugin_dir = "."
        else:
            plugin_dir = click.prompt(
                click.style(tr("Folder Name", "文件夹名称"), fg='green'),
                default="my-plugin"
            )

    target_path = (current_cwd / plugin_dir).resolve()

    # --- 3. Interactive Inputs (Flow: Name -> Author -> ID -> URL) ---

    # A. Name
    default_name = target_path.name if target_path.name != '.' else "My Plugin"
    name = click.prompt(
        click.style(tr("Plugin Name", "插件名称"), fg='green'),
        default=default_name.replace('-', ' ').title()
    )

    # B. Author
    default_author = os.getenv('USER', os.getenv('USERNAME', 'Developer'))
    author = click.prompt(
        click.style(tr("Author", "作者"), fg='green'),
        default=default_author
    )

    # C. ID (Auto-generated default based on Author + Name)
    clean_author = "".join(c for c in author if c.isalnum()).lower()
    clean_name = "".join(c for c in name if c.isalnum()).lower()
    suggested_id = f"com.{clean_author}.{clean_name}"

    plugin_id = click.prompt(
        click.style(tr("Plugin ID", "插件 ID"), fg='green'),
        default=suggested_id
    )

    # D. URL (Auto-detect Git)
    git_url = get_git_remote_url()
    url = click.prompt(
        click.style(tr("Repository URL", "仓库地址"), fg='green'),
        default=git_url,
        show_default=True if git_url else False
    )

    description = click.prompt(
        click.style(tr("Description", "描述"), fg='green'),
        default="A Class Widgets plugin."
    )

    # --- 4. Confirmation ---

    click.echo("\n" + click.style(tr("Configuration Summary", "配置概览"), bold=True) + ":")
    print_info(tr("Path", "路径"), str(target_path))
    print_info(tr("Name", "名称"), name)
    print_info(tr("Author", "作者"), author)
    print_info(tr("ID", "标识符"), plugin_id)
    print_info("URL", url or "(None)")
    print_info("Icon", "icon.png (Default)")

    # Directory Check
    is_empty = not target_path.exists() or not any(target_path.iterdir())
    if not is_empty and not force:
        click.secho(f"\n⚠️  {tr('Target directory is not empty!', '目标目录不为空！')}", fg='yellow')
        if not click.confirm(tr("Merge with existing files?", "是否合并文件?"), default=False):
            click.echo(tr("Aborted.", "已取消"))
            sys.exit(0)

    click.echo("")
    if not click.confirm(click.style(tr("Ready to create?", "确认创建?"), bold=True), default=True):
        click.echo(tr("Cancelled.", "已取消"))
        sys.exit(0)

    # --- 5. Execution ---

    click.echo("")

    manifest = PluginManifestModel(
        id=plugin_id,
        name=name,
        author=author,
        description=description,
        version="1.0.0",
        api_version=f">={sdk_version}",
        entry="main.py",
        url=url,
        icon="icon.png",
        readme="README.md"
    )

    scaffolder = PluginScaffold(target_path, manifest)

    try:
        scaffolder.create(force=force or not is_empty)

        # --- 6. Success ---
        click.echo("\n" + click.style(tr("Success!", "创建成功！"), fg='green', bold=True))
        click.echo(tr("Run the following to start:", "运行以下命令开始开发：") + "\n")

        if target_path != Path.cwd():
            click.echo(f"  cd {plugin_dir}")

        click.echo("  pip install -e .\n")
        click.echo(tr("To run and debug your plugin, launch the main Class Widgets application.", "要运行和调试插件，请启动 Class Widgets 主程序。"))

    except Exception as e:
        click.secho(f"\n❌ Error: {e}", fg='red')
        # import traceback
        # traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    create_plugin()