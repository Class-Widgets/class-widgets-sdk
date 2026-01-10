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
    click.secho(f"   描述: {description}", fg='white')
    
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
    
    print_section("可用命令", "以下是目前可用的所有 Class Widgets SDK 命令")
    
    commands = [
        {
            "name": "cw-plugin-init",
            "usage": "cw-plugin-init [选项] [目录]",
            "description": "初始化一个新的 Class Widgets 插件项目",
            "examples": [
                "cw-plugin-init                    # 在当前目录创建插件",
                "cw-plugin-init my-plugin         # 创建指定名称的插件",
                "cw-plugin-init --force           # 强制覆盖现有文件"
            ]
        },
        {
            "name": "cw-plugin-pack", 
            "usage": "cw-plugin-pack [选项] 源目录",
            "description": "将插件项目打包成 .cwplugin 格式",
            "examples": [
                "cw-plugin-pack my-plugin         # 打包插件",
                "cw-plugin-pack --zip my-plugin  # 打包成 zip 格式",
                "cw-plugin-pack --output out/ my-plugin  # 指定输出目录"
            ]
        },
        {
            "name": "cw-help",
            "usage": "cw-help [命令]",
            "description": "显示帮助信息，或显示特定命令的详细帮助",
            "examples": [
                "cw-help                          # 显示完整帮助",
                "cw-help plugin-init            # 显示 plugin-init 命令帮助"
            ]
        }
    ]
    
    for cmd in commands:
        print_command(cmd["name"], cmd["usage"], cmd["description"], cmd["examples"])


def show_detailed_help(command_name: str = None):
    """显示详细帮助信息"""
    
    if command_name:
        command_name = command_name.lower().replace('cw-', '')
        
        if 'init' in command_name or 'plugin' in command_name:
            print_command(
                "cw-plugin-init",
                "cw-plugin-init [选项] [目录]", 
                "初始化一个新的 Class Widgets 插件项目",
                [
                    "cw-plugin-init                    # 交互式创建插件",
                    "cw-plugin-init my-plugin         # 创建指定名称的插件", 
                    "cw-plugin-init --force           # 强制覆盖现有文件"
                ]
            )
            
            print_section("选项说明")
            click.echo("  --force, -f    覆盖现有文件")
            click.echo("  --help         显示帮助信息")
            
            print_section("创建流程")
            click.echo("  1. 选择创建目录")
            click.echo("  2. 输入插件信息（名称、作者、描述等）")
            click.echo("  3. 生成插件文件结构")
            click.echo("  4. 指导安装和测试")
            
            print_tip("提示", "创建后请使用 'pip install -e .' 安装插件到开发环境")
            
        elif 'pack' in command_name:
            print_command(
                "cw-plugin-pack",
                "cw-plugin-pack [选项] 源目录",
                "将插件项目打包成可分发的格式",
                [
                    "cw-plugin-pack my-plugin         # 打包插件",
                    "cw-plugin-pack --zip my-plugin  # 打包成 zip 格式",
                    "cw-plugin-pack --output out/ my-plugin  # 指定输出目录"
                ]
            )
            
            print_section("选项说明")
            click.echo("  --output, -o   指定输出文件路径")
            click.echo("  --format, -f   指定打包格式 (cwplugin|zip)")
            click.echo("  --help         显示帮助信息")
            
            print_tip("提示", "生成的 .cwplugin 文件可以直接在 Class Widgets 2 中安装")
            
        else:
            click.secho(f"❌ 未知命令: {command_name}", fg='red', bold=True)
            click.echo("使用 'cw-help' 查看所有可用命令")
            return
    
    else:
        show_commands_help()
        
        print_section("插件开发流程")
        click.echo("  1. 创建插件:  cw-plugin-init my-plugin")
        click.echo("  2. 开发插件:  编辑 my-plugin/main.py")
        click.echo("  3. 测试插件:  pip install -e .")
        click.echo("  4. 打包插件:  cw-plugin-pack my-plugin")
        click.echo("  5. 分发插件:  安装 .cwplugin 文件")
        
        print_section("重要提示")
        click.echo("  • 所有命令都支持 --help 参数查看详细用法")
        click.echo("  • 插件开发需要 Python 3.9+ 环境")
        click.echo("  • 建议使用虚拟环境进行开发")
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