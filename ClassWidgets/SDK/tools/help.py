"""
Class Widgets SDK Help Tool
提供 SDK 工具的完整帮助信息
"""
import click
import sys
from pathlib import Path

from ClassWidgets.SDK import __version__ as sdk_version


def print_header():
    """打印帮助头部信息"""
    click.clear()
    click.secho("Class Widgets 2 Plugin SDK", fg='green', bold=True)
    click.secho(f"版本: {sdk_version}", fg='cyan')
    click.secho("=" * 50, dim=True)
    click.echo("")


def print_section(title: str, description: str = ""):
    """打印章节标题"""
    click.echo("")
    click.secho(f"📋 {title}", fg='yellow', bold=True)
    if description:
        click.secho(f"    {description}", fg='white', dim=True)
    click.secho("-" * 30, dim=True)


def print_command(name: str, usage: str, description: str, examples: list = None):
    """打印命令信息"""
    click.echo("")
    click.secho(f"🔧 {name}", fg='cyan', bold=True)
    click.secho(f"   用法: {usage}", fg='white')
    click.secho(f"   说明: {description}", fg='white')
    
    if examples:
        click.echo("   示例:")
        for example in examples:
            click.secho(f"     • {example}", fg='green', dim=True)


def print_tip(title: str, content: str):
    """打印提示信息"""
    click.echo("")
    click.secho(f"💡 {title}", fg='blue', bold=True)
    click.secho(f"   {content}", fg='white')


def show_commands_help():
    """显示所有命令的帮助信息"""
    
    print_section("可用命令", "SDK 命令一览")
    
    commands = [
        {
            "name": "cw-plugin-init",
            "usage": "cw-plugin-init [选项] [目录]",
            "description": "初始化新插件项目",
            "examples": [
                "cw-plugin-init                    # 在当前目录创建",
                "cw-plugin-init my-plugin         # 指定目录名",
                "cw-plugin-init --force           # 覆盖已有文件"
            ]
        },
        {
            "name": "cw-plugin-pack", 
            "usage": "cw-plugin-pack [选项] 源目录",
            "description": "打包插件为 .cwplugin 格式",
            "examples": [
                "cw-plugin-pack my-plugin         # 打包插件",
                "cw-plugin-pack --zip my-plugin  # 打包为 zip",
                "cw-plugin-pack --output out/ my-plugin  # 指定输出目录"
            ]
        },
        {
            "name": "cw-help",
            "usage": "cw-help [命令]",
            "description": "显示帮助信息",
            "examples": [
                "cw-help                          # 全部帮助",
                "cw-help plugin-init            # 特定命令帮助"
            ]
        },
        {
            "name": "cw-plugin-publish",
            "usage": "cw-plugin-publish [选项] [目录]",
            "description": "发布插件到插件市场",
            "examples": [
                "cw-plugin-publish                          # 发布当前目录",
                "cw-plugin-publish --token cwpt_xxx         # 指定令牌",
                "cw-plugin-publish --dry-run                # 预览不发布",
                "cw-plugin-publish --api-url http://localhost:3000  # 调试"
            ]
        }
    ]
    
    for cmd in commands:
        print_command(cmd["name"], cmd["usage"], cmd["description"], cmd["examples"])


def show_detailed_help(command_name: str = None):
    """Show detailed help for a specific command."""
    
    if command_name:
        command_name = command_name.lower().replace('cw-', '')
        
        if 'init' in command_name or 'plugin' in command_name:
            print_command(
                "cw-plugin-init",
                "cw-plugin-init [选项] [目录]", 
                "初始化新插件项目",
                [
                    "cw-plugin-init                    # 交互式创建",
                    "cw-plugin-init my-plugin         # 指定目录名", 
                    "cw-plugin-init --force           # 覆盖已有文件"
                ]
            )
            
            print_section("选项说明")
            click.echo("  --force, -f    覆盖现有文件")
            click.echo("  --help         显示帮助")
            
            print_section("创建流程")
            click.echo("  1. 选择目录")
            click.echo("  2. 输入插件信息（名称、作者、描述等）")
            click.echo("  3. 生成项目文件")
            click.echo("  4. 安装并测试")
            
            print_tip("提示", "创建后执行 'pip install -e .' 安装到开发环境")
            
        elif 'pack' in command_name:
            print_command(
                "cw-plugin-pack",
                "cw-plugin-pack [选项] 源目录",
                "打包插件为可分发的格式",
                [
                    "cw-plugin-pack my-plugin         # 打包插件",
                    "cw-plugin-pack --zip my-plugin  # 打包为 zip",
                    "cw-plugin-pack --output out/ my-plugin  # 指定输出目录"
                ]
            )
            
            print_section("选项说明")
            click.echo("  --output, -o   输出文件路径")
            click.echo("  --format, -f   打包格式 (cwplugin|zip)")
            click.echo("  --help         显示帮助")
            
            print_tip("提示", ".cwplugin 文件可直接在 Class Widgets 2 中安装")

        elif 'publish' in command_name:
            print_command(
                "cw-plugin-publish",
                "cw-plugin-publish [选项] [目录]",
                "发布插件到插件市场",
                [
                    "cw-plugin-publish                          # 发布当前目录",
                    "cw-plugin-publish --token cwpt_xxx         # 指定令牌",
                    "cw-plugin-publish --dry-run                # 预览不发布",
                    "cw-plugin-publish --api-url http://localhost:3000  # 调试"
                ]
            )

            print_section("选项说明")
            click.echo("  --token, -t    发布令牌（或设置 CWPT_TOKEN 环境变量）")
            click.echo("  --api-url      API 地址（默认: https://plaza.cw.rinlit.cn/）")
            click.echo("  --branch, -b   分支（自动检测，默认 main）")
            click.echo("  --dry-run      仅预览不发布")
            click.echo("  --help         显示帮助")

            print_section("发布流程")
            click.echo("  1. 验证 cwplugin.json")
            click.echo("  2. 验证令牌")
            click.echo("  3. 发送发布请求")
            click.echo("  4. 查看结果")

            print_tip("提示", "令牌在控制台生成，仅展示一次请妥善保存")

        else:
            click.secho(f"❌ 未知命令: {command_name}", fg='red', bold=True)
            click.echo("使用 'cw-help' 查看所有命令")
            return
    
    else:
        show_commands_help()
        
        print_section("开发流程")
        click.echo("  1. 创建:  cw-plugin-init my-plugin")
        click.echo("  2. 开发:  编辑 my-plugin/main.py")
        click.echo("  3. 测试:  pip install -e .")
        click.echo("  4. 打包:  cw-plugin-pack my-plugin")
        click.echo("  5. 发布:  cw-plugin-publish --token <token>")
        click.echo("  6. 分发:  安装 .cwplugin 文件")
        
        print_section("提示")
        click.echo("  • 所有命令支持 --help 查看详情")
        click.echo("  • 需要 Python 3.9+")
        click.echo("  • 建议使用虚拟环境")
        click.echo("  • 查看 SDK 文档获取更多信息")


@click.command()
@click.argument('command', required=False)
def show_help(command: str = None):
    """
    Class Widgets 2 Plugin SDK 帮助工具
    
    使用方法:
        cw-help              显示完整帮助信息
        cw-help <命令>       显示特定命令的详细帮助
    
    可用命令:
        plugin-init          初始化新插件项目
        plugin-pack          打包插件项目
        plugin-publish       发布插件到插件市场
    """
    print_header()
    
    if command:
        show_detailed_help(command)
    else:
        show_detailed_help()
    
    click.echo("")
    click.secho("更多信息请访问: https://github.com/RinLit-233-shiroko/Class-Widgets-2", fg='blue', dim=True)


def main():
    """入口函数"""
    show_help()


if __name__ == '__main__':
    main()