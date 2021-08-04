![BaiduSpider](/assets/banner.png)

# BaiduSpider

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

BaiduSpider是一个使用Python编写的轻量级百度爬虫。它使用轻量的[requests](https://docs.python-requests.org/zh_CN/latest/)和[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)搭建，并提供了易用的API接口以及完善的类型注释`typing`，提高开发速度。

<div style="width:100%;height:0px;position:relative;padding-bottom:56.327%;"><iframe src="https://streamja.com/embed/rd9kO" frameborder="0" width="100%" height="100%" allowfullscreen style="width:100%;height:100%;position:absolute;"></iframe></div>

有了BaiduSpider，你可以：

- 精准，快速提取百度搜索结果
- 获取全方位的结果类型
- 获得易用的，人性化的API
<!-- - 获取多平台支持，如`CLI`，`Web UI`, `Web API`等。 -->

## 必要条件

- Python 3.6+

## 安装

```bash
$ pip install baiduspider
```

## 链接

- 文档：<https://baiduspider.github.io>
- PyPI：<https://pypi.org/project/BaiduSpider/>
- GitHub：<https://github.com/BaiduSpider/BaiduSpider>
- 讨论：<https://github.com/BaiduSpider/BaiduSpider/discussions>
- 报告Issue：<https://github.com/BaiduSpider/BaiduSpider/issues>

## 示例

=== "普通"

    ```python
    from baiduspider import BaiduSpider
    from pprint import pprint

    pprint(BaiduSpider().search_web(input('搜索词：')).plain)
    ```

=== "指定页码"

    ```python
    from baiduspider import BaiduSpider
    from pprint import pprint

    pprint(BaiduSpider().search_web(input('搜索词：'), pn=int(input('页码：'))).plain)
    ```

???+ tip "什么是`pprint`？"
    `pprint`是一个Python内置的美化输出包，可以通过`#!python import pprint`导入。下面是它的一个实例，使用BaiduSpider的返回值作为对比。

    ```python
    from pprint import pprint
    from baiduspider import BaiduSpider

    result = BaiduSpider().search_web('Python')
    print(result)  # print
    print('\n\n')
    pprint(result)  # pprint
    ```

    在接下来的文档中，我们将会大量使用此函数，因为BaiduSpider的字典返回值十分复杂。

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
