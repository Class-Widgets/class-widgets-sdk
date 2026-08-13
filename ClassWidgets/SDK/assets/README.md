   <div align="center">
<img src="icon.png" width="15%" alt="Class Widgets 2">
<h1>[PluginName]</h1>

<p>[PluginDescription]</p>


[![星标](https://img.shields.io/github/stars/[GithubOwner_Repo]?style=for-the-badge&color=orange&label=%E6%98%9F%E6%A0%87)](https://github.com/[GithubOwner_Repo]/)
[![开源许可](https://img.shields.io/badge/license-MIT-blue.svg?label=%E5%BC%80%E6%BA%90%E8%AE%B8%E5%8F%AF%E8%AF%81&style=for-the-badge)](https://github.com/[GithubOwner_Repo])
[![下载量](https://img.shields.io/github/downloads/[GithubOwner_Repo]/total.svg?label=%E4%B8%8B%E8%BD%BD%E9%87%8F&color=green&style=for-the-badge)](https://github.com/[GithubOwner_Repo])

</div>

> [!NOTE]
> 
> 该模板为自动生成 / This README is automatically generated.

## 介绍 / Introduction
[PluginDescription]

本插件基于 [Class Widgets 2 SDK](https://github.com/Class-Widgets/class-widgets-sdk)。


## 使用 / Usage
1. 在插件广场（网页版/客户端）中 [下载](https://plaza.cw.rinlit.cn/plugins/[PluginID])  /  
In Plugin Plaza (Web / Class Widgets Client), [download](https://plaza.cw.rinlit.cn/plugins/[PluginID]) this plugin

2. 在 Class Widgets 2 -> "设置" -> "插件"中导入且启用本插件  /  
Import and enable this plugin in "Settings" -> "Plugins" in Class Widgets 2

## 自动发布 / Auto Release
通过 GitHub Actions 实现自动发布功能，推送 tag 时自动生成 release。
#
当前项目已自动配置了 `release.yml` 工作流，您只需要知道如何使用：

1. 推送版本号 tag 到 GitHub（格式：`v*.*.*` ）：
```bash
git tag v1.0.0  # 版本号格式：`v*.*.*` (您也可以手动修改工作流中的格式)
git push origin v1.0.0  # 推送
```

2. 在 [GitHub 仓库](https://github.com/[GithubOwner_Repo]) 设置中添加 `CWPT_TOKEN` 密钥（从 [插件广场控制台](https://plaza.cw.rinlit.cn/console) 获取的发布令牌）

3. GitHub Actions 会自动：
   - 使用 `cw-plugin-pack` 打包插件
   - 生成 `.cwplugin` 和 `.zip` 两种格式
   - 通过 `cw-plugin-publish` 自动发布到插件广场
   - 创建 GitHub Release 并上传发布包

4. 即可在 GitHub Release 页面下载发布包，或直接在 Class Widgets 插件广场中安装


## 致谢 / Acknowledgements
### 引用资源 / Credits
- [Class Widgets 2](https://github.com/rinlit-233-shiroko/class-widgets-2)
- [Class Widgets 2 SDK](https://github.com/Class-Widgets/class-widgets-sdk)

### 贡献者们 / Contributors
[![Contributors](http://contrib.nn.ci/api?repo=[GithubOwner_Repo])](https://github.com/[GithubOwner_Repo]/graphs/contributors)

## 版权 / License
本项目基于 MIT 协议开源，详情请参阅 [LICENSE](https://github.com/[GithubOwner_Repo]/blob/main/LICENSE) 文件。

The project is licensed under the MIT license. Please refer to the [LICENSE](https://github.com/[GithubOwner_Repo]/blob/main/LICENSE) file for details.
