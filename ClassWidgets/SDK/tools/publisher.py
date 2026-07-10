"""
Plugin Publisher Tool
Class Widgets SDK 插件发布工具
"""
import sys
import json
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional, List

import click

from ClassWidgets.SDK.tools.manifest import PluginManifestModel


# url常量
DEFAULT_API_URL = "https://plaza.cw.rinlit.cn/"


def tr(en: str, cn: str) -> str:
    """Return bilingual text string."""
    return f"{en} ({cn})"


def print_step(msg: str):
    """Prints a step with a styled bullet point."""
    click.echo(click.style("  ➜ ", fg="green", bold=True) + msg)


def print_info(key: str, value: str):
    """Prints a key-value pair nicely."""
    click.echo(f"    {click.style(key, fg='cyan', dim=True):<25} {value}")


def detect_git_branch(plugin_dir: Path) -> Optional[str]:
    """Try to detect the default branch of the git repo in plugin_dir."""
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD", "--short"],
            capture_output=True, text=True, cwd=str(plugin_dir),
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            # e.g. "origin/main" -> "main"
            branch = result.stdout.strip().split("/", 1)[-1]
            return branch
    except Exception:
        pass

    # Fallback: try reading HEAD directly
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, cwd=str(plugin_dir),
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass

    return None


# --- Core ---
class PluginPublisher:
    """Handles publishing a plugin to the Class Widgets plugin registry."""

    def __init__(
        self,
        plugin_dir: Path,
        token: str,
        api_url: str = DEFAULT_API_URL,
        branch: Optional[str] = None,
    ):
        self.plugin_dir = plugin_dir.resolve()
        self.token = token
        self.api_url = api_url.rstrip("/")
        # Auto-detect branch from git, fallback to "main"
        self.branch = branch or detect_git_branch(self.plugin_dir) or "main"

    def load_manifest(self) -> PluginManifestModel:
        """Load and validate the plugin manifest from cwplugin.json."""
        manifest_path = self.plugin_dir / "cwplugin.json"
        if not manifest_path.exists():
            raise FileNotFoundError(
                tr("cwplugin.json not found", "未找到 cwplugin.json")
            )
        return PluginManifestModel.load(manifest_path)

    def build_payload(self, manifest: PluginManifestModel) -> dict:
        """Map manifest fields to the API request body."""
        payload = {
            "id": manifest.id,
            "name": manifest.name,
            "version": manifest.version,
            "api_version": manifest.api_version,
            "repo_url": manifest.url or "",
            "description": manifest.description,
            "branch": self.branch,
            "readme": manifest.readme,
            "icon": manifest.icon,
            "tag_ids": manifest.tag_ids,
        }
        # Remove None values for optional fields
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    def dry_run(self) -> None:
        """Validate manifest and preview what would be published."""
        manifest = self.load_manifest()
        payload = self.build_payload(manifest)

        print_step(tr("Dry run — validating manifest", "试运行 — 正在验证清单"))
        click.echo("")

        print_info(tr("Plugin ID", "插件 ID"), manifest.id)
        print_info(tr("Name", "名称"), manifest.name)
        print_info(tr("Version", "版本"), manifest.version)
        print_info(tr("API Version", "API 版本"), manifest.api_version)
        print_info(tr("Repo URL", "仓库地址"), manifest.url or "(empty)")
        print_info(tr("Description", "描述"), manifest.description or "(empty)")
        print_info(tr("Branch", "分支"), self.branch)
        print_info(tr("Readme", "自述文件"), manifest.readme or "README.md")
        print_info(tr("Icon", "图标"), manifest.icon or "icon.png")
        print_info(
            tr("Tags", "标签"),
            ", ".join(manifest.tag_ids) if manifest.tag_ids else "(none)",
        )

        click.echo("")
        print_info(tr("API URL", "API 地址"), self.api_url)
        print_info(tr("Endpoint", "端点"), f"/api/plugins/{manifest.id}/publish")

        # Warn about missing url
        if not manifest.url:
            click.secho(
                f"\n  ⚠️  {tr('Warning: url is required in cwplugin.json for publishing', '警告：cwplugin.json 中未设置 url，发布需要此配置')}",
                fg="yellow",
            )

        click.echo("")
        click.secho(
            tr("Dry run complete. No request was sent.", "试运行完成，未发送请求。"),
            fg="green",
        )

    def publish(self) -> None:
        """Publish the plugin to the registry."""
        manifest = self.load_manifest()
        payload = self.build_payload(manifest)

        # Pre-flight check: url is required for publishing
        if not manifest.url:
            raise ValueError(
                tr(
                    "'url' is required in cwplugin.json for publishing",
                    "cwplugin.json 中未设置 'url' 字段，发布需要此配置",
                )
            )

        # Build request
        endpoint = f"{self.api_url}/api/plugins/{manifest.id}/publish"
        body = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            endpoint,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "X-CWPT-Token": self.token,
            },
        )

        print_step(tr("Publishing plugin...", "正在发布插件..."))
        print_info(tr("Plugin ID", "插件 ID"), manifest.id)
        print_info(tr("Version", "版本"), manifest.version)
        print_info(tr("Endpoint", "端点"), endpoint)

        try:
            with urllib.request.urlopen(req) as resp:
                resp_data = json.loads(resp.read().decode("utf-8"))
                self._handle_success(resp_data)
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            try:
                error_data = json.loads(error_body)
            except json.JSONDecodeError:
                error_data = {"error": error_body}
            self._handle_error(e.code, error_data)
        except urllib.error.URLError as e:
            raise ConnectionError(
                tr(
                    f"Failed to connect to {self.api_url}: {e.reason}",
                    f"无法连接到 {self.api_url}: {e.reason}",
                )
            )

    def _handle_success(self, data: dict) -> None:
        """Display a successful publish result."""
        click.echo("")
        click.secho(tr("Publish successful!", "发布成功！"), fg="green", bold=True)

        plugin = data.get("plugin", {})
        updated = plugin.get("updated", {})
        if updated:
            print_info(tr("Name", "名称"), updated.get("name", ""))
            print_info(tr("Version", "版本"), updated.get("version", ""))
            print_info(tr("Repo URL", "仓库地址"), updated.get("repo_url", ""))
            print_info(tr("Branch", "分支"), updated.get("branch", ""))

        updated_at = plugin.get("updated_at")
        if updated_at:
            print_info(tr("Updated at", "更新时间"), updated_at)

        tags = data.get("tags", {})
        if tags:
            print_info(
                tr("Tags applied", "已应用标签"),
                str(tags.get("appliedTagCount", 0)),
            )

    def _handle_error(self, status_code: int, data: dict) -> None:
        """Display a publish error with user-friendly hints."""
        error_msg = data.get("error", "Unknown error")
        click.echo("")
        click.secho(
            f"❌ {tr('Publish failed', '发布失败')} (HTTP {status_code})",
            fg="red", bold=True,
        )
        click.secho(f"   {error_msg}", fg="red")

        # Map backend field names to cwplugin.json field names
        field_mapping = {
            "repo_url": "url",
            "name": "name",
            "version": "version",
            "api_version": "api_version",
            "id": "id",
        }

        # Handle specific field errors from backend
        if "Missing or invalid field:" in error_msg:
            # Extract the field name from error message
            import re
            match = re.search(r"Missing or invalid field:\s*(\w+)", error_msg)
            if match:
                backend_field = match.group(1)
                cw_field = field_mapping.get(backend_field, backend_field)
                click.echo("")
                click.secho(
                    tr(
                        f"Please check the '{cw_field}' field in cwplugin.json",
                        f"请检查 cwplugin.json 中的 '{cw_field}' 字段",
                    ),
                    fg="yellow",
                )

        if status_code == 401:
            click.secho(
                f"   {tr('Please check your CWPT_TOKEN.', '请检查你的 CWPT_TOKEN。')}",
                fg="yellow",
            )
            click.secho(
                tr(
                    "The token may be invalid, expired, or not authorized for this plugin.",
                    "令牌可能无效、已过期，或未授权访问此插件。",
                ),
                fg="yellow",
            )
        elif status_code == 400:
            if "Missing or invalid field" not in error_msg:
                click.secho(
                    f"   {tr('Please check your cwplugin.json fields.', '请检查 cwplugin.json 中的字段。')}",
                    fg="yellow",
                )

        if "Plugin manifest id does not exist" in error_msg:
            click.echo("")
            click.secho(
                tr(
                    "The plugin with this ID does not exist in the registry.",
                    "该插件 ID 在插件市场中不存在。",
                ),
                fg="yellow",
            )
            click.secho(
                tr(
                    "Please first register the plugin in the Class Widgets console,",
                    "请先在 Class Widgets 控制台中注册该插件，",
                ),
                fg="yellow",
            )
            click.secho(
                tr(
                    "then use this command to update its information.",
                    "然后再使用此命令更新插件信息。",
                ),
                fg="yellow",
            )

        if "Token owner does not match plugin owner" in error_msg:
            click.echo("")
            click.secho(
                tr(
                    "The publish token is not authorized for this plugin.",
                    "发布令牌未授权访问此插件。",
                ),
                fg="yellow",
            )
            click.secho(
                tr(
                    "Please use a token that was created for this specific plugin ID.",
                    "请使用为此插件 ID 创建的发布令牌。",
                ),
                fg="yellow",
            )

        sys.exit(1)


# --- CLI ---

@click.command()
@click.argument('plugin_dir', required=False)
@click.option(
    '--token', '-t',
    envvar='CWPT_TOKEN',
    help=tr('Publish token (or set CWPT_TOKEN env var)', '发布令牌（或设置 CWPT_TOKEN 环境变量）'),
)
@click.option(
    '--api-url',
    default=DEFAULT_API_URL,
    show_default=True,
    help=tr('API base URL (use localhost for debugging)', 'API 基础 URL（调试时可使用 localhost）'),
)
@click.option(
    '--branch', '-b',
    default=None,
    help=tr('Repository branch (auto-detected from git, fallback: main)', '仓库分支（自动从 git 检测，回退: main）'),
)
@click.option(
    '--dry-run',
    is_flag=True,
    help=tr('Validate and preview without publishing', '仅验证并预览，不实际发布'),
)
def publish_plugin(
    plugin_dir: Optional[str],
    token: Optional[str],
    api_url: str,
    branch: Optional[str],
    dry_run: bool,
):
    """
    Publish a plugin to the Class Widgets plugin registry.
    发布插件到 Class Widgets 插件市场。
    """
    click.clear()
    click.secho("Class Widgets Plugin Publisher", fg="green", bold=True)
    click.secho("-" * 30, dim=True)

    # 1. Determine plugin directory
    if not plugin_dir:
        plugin_dir = "."
    source_path = Path(plugin_dir).resolve()
    click.echo(tr("Source Directory", "源目录") + f": {click.style(str(source_path), fg='cyan')}")

    # 2. Check cwplugin.json exists
    if not (source_path / "cwplugin.json").exists():
        click.secho(
            f"\n❌ {tr('Error: cwplugin.json not found!', '错误：未找到 cwplugin.json！')}",
            fg="red",
        )
        click.echo(
            tr("Please run this command inside a plugin directory.", "请在插件目录下运行此命令。")
        )
        sys.exit(1)

    # 3. Token check (dry-run can skip token)
    if not dry_run and not token:
        click.secho(
            f"\n❌ {tr('Error: Publish token is required.', '错误：发布令牌必填。')}",
            fg="red",
        )
        click.echo(
            tr("Use --token or set CWPT_TOKEN environment variable.", "使用 --token 参数或设置 CWPT_TOKEN 环境变量。")
        )
        sys.exit(1)

    # 4. Execute
    try:
        publisher = PluginPublisher(
            plugin_dir=source_path,
            token=token or "",
            api_url=api_url,
            branch=branch,
        )

        if dry_run:
            publisher.dry_run()
        else:
            publisher.publish()

    except FileNotFoundError as e:
        click.secho(f"\n❌ {e}", fg="red")
        sys.exit(1)
    except ValueError as e:
        click.secho(f"\n❌ {e}", fg="red")
        sys.exit(1)
    except ConnectionError as e:
        click.secho(f"\n❌ {e}", fg="red")
        sys.exit(1)
    except Exception as e:
        click.secho(f"\n❌ {tr('Unexpected error', '意外错误')}: {e}", fg="red")
        sys.exit(1)


if __name__ == "__main__":
    publish_plugin()
