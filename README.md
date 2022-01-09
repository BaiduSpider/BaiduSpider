<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/BaiduSpider/BaiduSpider">
    <img src="https://baiduspider.github.io/assets/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BaiduSpider</h3>

  <p align="center">
    一个爬取百度的利器
    <br />
    <span>简体中文</span>
    |
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README-zh-tw.md"><strong>繁體中文</strong></a>
    |
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README-en.md"><strong>English</strong></a>
    <br />
    <a href="https://baiduspider.github.io/"><strong>快速上手 »</strong></a>
    <br />
    <br />
    <a href="https://baiduspider.github.io/usage/get-started/">查看示例</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">报告问题</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">请求需求</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#关于本项目">关于本项目</a>
      <ul>
        <li><a href="#依赖库">依赖库</a></li>
      </ul>
    </li>
    <li>
      <a href="#起步">起步</a>
      <ul>
        <li><a href="#预先条件">预先条件</a></li>
        <li><a href="#安装">安装</a></li>
      </ul>
    </li>
    <li><a href="#简单使用">简单使用</a></li>
    <li><a href="#项目路线图">项目路线图</a></li>
    <li><a href="#项目共建">项目共建</a></li>
    <li><a href="#开源协议">开源协议</a></li>
    <li><a href="#联系方式">联系方式</a></li>
    <li><a href="#免责声明">免责声明</a></li>
    <li><a href="#贡献者">贡献者</a></li>
    <li><a href="#致谢">致谢</a></li>
  </ol>
</details>


<!-- ## 警告

此分支为`dev`分支（开发分支）。该分支的所有代码或功能都可能不稳定，仅供参考。不建议在开源项目中使用此分支的 BaiduSpider。 -->


<!-- ABOUT THE PROJECT -->
## 关于本项目

[![项目截图][product-screenshot]](https://baiduspider.github.io)

搜索引擎是一个十分强大的工具，如果能让其他工具集成搜索引擎的众多强大功能，那么这些工具必将变得更加强大。但目前我没有找到一个可以精准提取搜索引擎搜索结果的开源爬虫。于是，我便编写了这个爬取百度搜索引擎的项目：BaiduSpider。

BaiduSpider 的独特功能:
* 节省提取数据的时间，对于类似深度学习项目的数据模型建立与训练起到了良好的帮助。

* 精准提取数据，并删除广告。

* 搜索结果大而全，支持多种搜索类型，支持多种返回类型。

当然，没有一个项目是完美的。任何一个项目的发展都需要社区的帮助。你可以通过发布 Issue 或提交 PR 来帮助 BaiduSpider 进步！:smile:

一些比较有帮助的文档或工具将在最后的致谢部分中列出。

### 依赖库

一些 BaiduSpider 使用的主要开源依赖库。

* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/zh_CN/latest/)



<!-- GETTING STARTED -->
## 起步

为了安装 BaiduSpider，请按照以下几个步骤操作。

### 预先条件

在安装 BaiduSpider 之前，请确保你安装了`Python3.6+`：

```sh
$ python --version
```

若版本小于`3.6.0`，请到[Python官网](https://www.python.org/downloads/)下载并安装 Python。

### 安装

#### 使用`pip`安装

请在命令行中键入：

```sh
$ pip install baiduspider
```

#### 从 GitHub 手动安装

```sh
$ git clone git@github.com:BaiduSpider/BaiduSpider.git

# ...

$ python setup.py install
```


<!-- USAGE EXAMPLES -->
## 简单使用

你可以使用以下代码，通过 BaiduSpider 获取百度的网页搜索结果：

```python
# 导入BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()

# 搜索网页
pprint(spider.search_web(query='Python'))
```

_更多样例和配置，请参照[文档](https://baiduspider.github.io)_



<!-- ROADMAP -->
## 项目路线图

请参考 [Opening Issues](https://github.com/BaiduSpider/BaiduSpider/issues) 以获取最新的项目规划以及已知问题。



<!-- CONTRIBUTING -->
## 项目共建

社区的贡献是开源项目的灵魂所在，也是整个开源社区学习、交流、获得灵感的方式。我们**极力欢迎**任何人参与本项目的开发与维护。

具体参与步骤如下：

1. Fork 此项目
2. 创建 Feature 分支 (`git checkout -b NewFeatures`)
3. 在每次修改代码后，提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 将更改推送到自己的远程仓库 (`git push origin username/BaiduSpider`)
5. 在 GitHub 上打开你的仓库，根据指引提交 PR



<!-- LICENSE -->
## 开源协议

本项目基于`GPL-V3`开源，详情请参见`LICENSE`。



<!-- CONTACT -->
## 联系方式

samzhangjy - [@samzhangjy](https://twitter.com/samzhangjy) - samzhang951@outlook.com

项目链接：[https://github.com/BaiduSpider/BaiduSpider](https://github.com/BaiduSpider/BaiduSpider)


## 免责声明

此项目仅作为学习用途，不可商用或用于爬取百度大量数据。此外，本项目使用`GPL-V3`版权协议，意味着涉及（使用）此项目的任何其它项目必须开源且注明出处，并且本项目作者不承担滥用导致的任何法律风险。特此说明，违者后果自负。


## 贡献者

<a href="https://github.com/baiduspider/baiduspider/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=baiduspider/baiduspider" />
</a>


<!-- ACKNOWLEDGEMENTS -->
## 致谢
* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
* [Requests](https://docs.python-requests.org/zh_CN/latest/)
* [Img Shields](https://shields.io)
* [Gitmoji](https://gitmoji.dev/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BaiduSpider/BaiduSpider?style=for-the-badge
[contributors-url]: https://github.com/BaiduSpider/BaiduSpider/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BaiduSpider/BaiduSpider?style=for-the-badge
[forks-url]: https://github.com/BaiduSpider/BaiduSpider/network/members
[stars-shield]: https://img.shields.io/github/stars/BaiduSpider/BaiduSpider?style=for-the-badge
[stars-url]: https://github.com/BaiduSpider/BaiduSpider/stargazers
[issues-shield]: https://img.shields.io/github/issues/BaiduSpider/BaiduSpider?style=for-the-badge
[issues-url]: https://github.com/BaiduSpider/BaiduSpider/issues
[license-shield]: https://img.shields.io/github/license/BaiduSpider/BaiduSpider?style=for-the-badge
[license-url]: https://github.com/BaiduSpider/BaiduSpider/blob/master/LICENSE
[product-screenshot]: https://i.loli.net/2021/04/22/V7gGrmTDlfR5U24.png