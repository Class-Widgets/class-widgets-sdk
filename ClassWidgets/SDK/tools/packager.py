"""
Plugin Packager Tool
Class Widgets SDK 插件打包工具
"""
import sys
import shutil
import zipfile
import subprocess
import tempfile
import json
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
import click


def tr(en: str, cn: str) -> str:
    """Return bilingual text string."""
    return f"{en} ({cn})"

def print_step(msg: str):
    """Prints a step with a styled bullet point."""
    click.echo(click.style("  ➜ ", fg="green", bold=True) + msg)

def print_info(key: str, value: str):
    """Prints a key-value pair nicely."""
    click.echo(f"    {click.style(key, fg='cyan', dim=True):<20} {value}")


class PluginPackager:
    """
    Handles the build and packaging process of a plugin.
    """

    # 默认忽略的文件模式
    DEFAULT_IGNORE_PATTERNS = {
        '__pycache__', '*.pyc', '*.pyo', '*.pyd',
        '.DS_Store', 'Thumbs.db', 'desktop.ini',
        '.git', '.gitignore', '.gitattributes',
        '.venv', 'venv', 'env', '.idea', '.vscode',
        '*.cwplugin', '*.zip',  # 防止递归打包
        'dist', 'build', '*.egg-info',
        'cwplugin.local.json'   # 本地开发配置
    }

    def __init__(self, source_dir: Path):
        self.source_dir = source_dir.resolve()
        self.build_dir: Optional[Path] = None # 临时构建目录
        self.manifest_data: Dict[str, Any] = {}

    def pack(self, output_path: Optional[Path] = None, file_format: str = 'cwplugin') -> Path:
        """Execute the packaging pipeline."""

        # 1. Validation / 验证
        print_step(tr("Validating plugin structure...", "正在验证插件结构..."))
        self._validate_source()

        plugin_id = self.manifest_data.get('id', 'unknown_plugin')
        # version = self.manifest_data.get('version', '1.0.0')

        # 确定输出路径和后缀
        if not output_path:
            # 根据格式设置后缀
            suffix = f".{file_format.lower().lstrip('.')}"
            # output_name = f"{plugin_id}_{version}{suffix}"
            output_name = f"{plugin_id}{suffix}"
            output_path = self.source_dir.parent / output_name

        output_path = Path(output_path).resolve()

        # 2. Build Environment Setup / 构建环境设置
        with tempfile.TemporaryDirectory(prefix=f"cw_build_{plugin_id}_") as temp_dir_str:
            self.build_dir = Path(temp_dir_str)

            # 3. Copy Source / 复制源码
            self._copy_source_to_build()

            # 4. Install Dependencies / 安装依赖
            self._install_dependencies()

            # 5. Create Archive / 创建压缩包
            print_step(tr(f"Archiving to {output_path.name}...", "正在打包..."))
            self._create_zip(output_path)

        return output_path

    def _validate_source(self):
        """Check if the source directory is a valid plugin."""
        manifest_path = self.source_dir / "cwplugin.json"
        if not manifest_path.exists():
            raise FileNotFoundError(tr("cwplugin.json not found", "未找到 cwplugin.json"))

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                self.manifest_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(tr("Invalid JSON in cwplugin.json", "cwplugin.json 格式错误"))

        # 检查关键字段
        required_fields = ['id', 'name', 'version', 'entry']
        for field in required_fields:
            if field not in self.manifest_data:
                raise ValueError(tr(f"Missing '{field}' in manifest", f"清单缺失 '{field}' 字段"))

        # 检查入口文件
        entry_file = self.source_dir / self.manifest_data['entry']
        if not entry_file.exists():
            raise FileNotFoundError(tr(f"Entry file '{entry_file.name}' missing", f"入口文件 '{entry_file.name}' 不存在"))

        # 检查 Icon (可选但推荐)
        icon_file = self.manifest_data.get('icon')
        if icon_file and not (self.source_dir / icon_file).exists():
             click.secho(f"    ⚠️  {tr('Warning: Icon file not found', '警告: 未找到图标文件')}: {icon_file}", fg='yellow')

    def _copy_source_to_build(self):
        """Copy files to temp build dir, respecting ignore patterns."""
        print_step(tr("Copying source files...", "复制源文件..."))

        def _ignore_filter(src, names):
            # 简单的 glob 匹配
            ignored = set()
            for name in names:
                for pattern in self.DEFAULT_IGNORE_PATTERNS:
                    # 使用 fnmatch 风格匹配
                    import fnmatch
                    if fnmatch.fnmatch(name, pattern):
                        ignored.add(name)
                        break
            return ignored

        shutil.copytree(
            self.source_dir,
            self.build_dir,
            ignore=_ignore_filter,
            dirs_exist_ok=True
        )

    def _resolve_dependencies(self) -> List[str]:
        """Extract dependencies from pyproject.toml or requirements.txt."""
        deps = []

        # 1. Try pyproject.toml (Standard)
        toml_path = self.source_dir / "pyproject.toml"
        if toml_path.exists():
            try:
                if sys.version_info >= (3, 11):
                    import tomllib
                    with open(toml_path, 'rb') as f:
                        data = tomllib.load(f)
                else:
                    try:
                        import tomli
                        with open(toml_path, 'rb') as f:
                            data = tomli.load(f)
                    except ImportError:
                        click.secho("    ⚠️  Python < 3.11 needs 'tomli' to parse pyproject.toml", fg='yellow')
                        data = {}

                deps = data.get('project', {}).get('dependencies', [])
                if deps:
                    print_info(tr("Source", "来源"), "pyproject.toml")
            except Exception as e:
                click.secho(f"    ⚠️  Failed to parse pyproject.toml: {e}", fg='yellow')

        # 2. Try requirements.txt (Legacy/Fallback)
        if not deps:
            req_path = self.source_dir / "requirements.txt"
            if req_path.exists():
                with open(req_path, 'r', encoding='utf-8') as f:
                    deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                if deps:
                    print_info(tr("Source", "来源"), "requirements.txt")

        return deps

    def _install_dependencies(self):
        """Install dependencies into build_dir/lib."""
        deps = self._resolve_dependencies()
        if not deps:
            print_step(tr("No dependencies to install.", "无须安装依赖。"))
            return

        print_step(tr(f"Installing {len(deps)} dependencies...", f"正在安装 {len(deps)} 个依赖..."))

        # 目标目录名 lib
        lib_dir = self.build_dir / "lib"
        lib_dir.mkdir(exist_ok=True)

        cmd = [
            sys.executable, "-m", "pip", "install",
            *deps,
            "--target", str(lib_dir),
            "--no-python-version-warning",
            "--disable-pip-version-check",
            "--upgrade"
        ]

        try:
            # 运行 pip install
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # 显示进度条
            with click.progressbar(length=100, label="    Pip installing", show_eta=False, show_percent=False) as bar:
                while process.poll() is None:
                    bar.update(1) # Fake update
                    time.sleep(0.1)

            stdout, stderr = process.communicate()

            if process.returncode != 0:
                click.secho(f"\n❌ Dependency installation failed:", fg='red')
                click.echo(stderr)
                raise RuntimeError("Pip install failed")

            self._clean_libs_dir(lib_dir)

            installed_pkgs = len(list(lib_dir.glob("*-info")))
            print_info(tr("Installed", "已安装"), f"{installed_pkgs} packages")

        except Exception as e:
            raise RuntimeError(f"Dependency install error: {e}")

    def _clean_libs_dir(self, lib_dir: Path):
        """Remove unnecessary files from installed libs to save space."""
        for item in lib_dir.rglob('*'):
            if item.suffix in ['.pyc', '.pyo']:
                item.unlink()

    def _create_zip(self, output_path: Path):
        """Zip the build directory."""
        all_files = list(self.build_dir.rglob('*'))
        files_to_zip = [f for f in all_files if f.is_file()]

        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            with click.progressbar(files_to_zip, label="    Compressing") as bar:
                for file_path in bar:
                    arcname = file_path.relative_to(self.build_dir)
                    zipf.write(file_path, arcname)


# --- CLI ---

@click.command()
@click.argument('plugin_dir', required=False)
@click.option('-o', '--output', help='Output file path / 输出路径')
@click.option('-f', '--format', 'file_format', type=click.Choice(['cwplugin', 'zip'], case_sensitive=False), default='cwplugin', help=tr('Output file format (cwplugin or zip)', '输出文件格式 (cwplugin 或 zip)'))
def pack_plugin(plugin_dir: Optional[str], output: Optional[str], file_format: str):
    """
    Package a plugin for distribution.
    打包插件以供分发。
    """
    click.clear()
    click.secho("Class Widgets Plugin Packager", fg='green', bold=True)
    click.secho("-" * 30, dim=True)

    # 1. Determine Source
    if not plugin_dir:
        plugin_dir = "."

    source_path = Path(plugin_dir).resolve()
    click.echo(tr("Source Directory", "源目录") + f": {click.style(str(source_path), fg='cyan')}")
    print_info(tr("Output Format", "输出格式"), file_format) # 显示选择的格式

    # 2. Confirm
    if not (source_path / "cwplugin.json").exists():
        click.secho(f"\n❌ {tr('Error: cwplugin.json not found!', '错误：未找到 cwplugin.json！')}", fg='red')
        click.echo(tr("Please run this command inside a plugin directory.", "请在插件目录下运行此命令。"))
        sys.exit(1)

    # 3. Execute
    try:
        packager = PluginPackager(source_path)
        # 传入 format 参数
        output_path = packager.pack(output_path=output, file_format=file_format)

        # 4. Success
        size_mb = output_path.stat().st_size / (1024 * 1024)
        click.echo("")
        click.secho(tr("Packaging Complete!", "打包完成！"), fg='green', bold=True)
        print_info(tr("File", "文件"), str(output_path))
        print_info(tr("Size", "大小"), f"{size_mb:.2f} MB")

    except Exception as e:
        click.secho(f"\n❌ {tr('Packaging Failed', '打包失败')}: {e}", fg='red')
        sys.exit(1)

if __name__ == "__main__":
    pack_plugin()