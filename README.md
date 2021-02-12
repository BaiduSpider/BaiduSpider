<p align="center">
    <img width="40%" src="https://baiduspider.github.io/assets/favicon.png" alt="BaiduSpider" />
    <br />
    <h2 align="center">
        BaiduSpider
    </h2>
    <br />
    <p align="center">
        <i>
            BaiduSpider，一个爬取百度的利器
        </i>
    </p>
</p>

<br />

<p align="center">
    <b>
        简体中文 | <a href="https://github.com/BaiduSpider/BaiduSpider/blob/master/README-en.md">English</a>
    </b>
</p>

<p align="center">
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg" alt="made-with-python"/>
    </a>
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/master/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/BaiduSpider/BaiduSpider">
    </a>
    <a href="https://github.com/BaiduSpider/BaiduSpider/stargazers">
        <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/BaiduSpider/BaiduSpider">
    </a>
    <a href="https://github.com/BaiduSpider/BaiduSpider/network/members">
        <img alt="GitHub forks" src="https://img.shields.io/github/forks/BaiduSpider/BaiduSpider">
    </a>
    <a href="https://travis-ci.org/github/BaiduSpider/BaiduSpider">
        <img alt="build status" src="https://travis-ci.org/BaiduSpider/BaiduSpider.svg?branch=master">
    </a>
    <a href="https://pepy.tech/project/baiduspider">
        <img alt="downloads" src="https://pepy.tech/badge/baiduspider/month">
    </a>
</p>

<h1></h1>

BaiduSpider是一个爬取百度搜索结果的Python爬虫，目前支持百度网页搜索，百度图片搜索，百度知道搜索，百度视频搜索，百度资讯搜索，百度文库搜索，百度经验搜索和百度百科搜索。

<br />

<h2 align="center">
    免责声明
</h2>

<br />

此项目仅作为学习用途，不可商用或爬取百度大量数据。此外，本项目已经更新为`GPL-V3`版权协议，意味着涉及（使用）此项目的任何其它项目必须开源且注明出处。特此说明，违者后果自负。

<br />

<h2 align="center">
    安装
</h2>

<br />

BaiduSpider现已发布PyPI包，可以使用`pip`安装：

```bash
$ pip install baiduspider
```

或者从GitHub直接clone：

```bash
$ git clone https://github.com/BaiduSpider/BaiduSpider.git

# ...

$ python setup.py install
```

<br />

<h3 align="center">
    提示
</h3>

<p align="center">
    <b>
        BaiduSpider目前仅支持Python 3.6+，暂不支持Python 2.x
    </b>
</p>

<br />

<h2 align="center">
    快速上手
</h2>

<br />

BaiduSpider提供简易的，人性化的API，可通过实例化`BaiduSpider`对象后调用。例如，我想要使用网页搜索函数查询有关`Python`的信息：

```python
# 导入BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()

# 搜索网页
pprint(spider.search_web(query='Python'))
```

获得的搜索结果将类似下面的这个Python字典结果：

```python
{'results': [{'result': 100000000, 'type': 'total'},
             {'results': ['0基础学python有多难',
                          'python自学行吗',
                          '学python要多久',
                          'python手机版',
                          'python有什么用',
                          '财务有必要学python吗',
                          'python为什么叫爬虫',
                          'python处理excel的优势',
                          'python自学免费教程'],
              'type': 'related'},
             {'result': {'cover': None,
                         'cover-type': None,
                         'des': 'Python是一种跨平台的计算机程序设计语言。 '
                                '是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言新功能的添加，越多被用于独立的、大型项目的开发。',
                         'title': 'Python(计算机程序设计语言) - 百度百科',
                         'url': 'http://www.baidu.com/link?url=2z_Q_urbKikP4py4Y9tlMImyT090fjjaKi1gi4Z6bjvk1lU8MqYHewJTumd9YEpC5Jusis_8nqlTKsJgEMcRUa'},
              'type': 'baike'},
             {'des': 'The official home of the Python Programming Language... '
                     '# Python 3: Simple output (with Unicode) >>> '
                     'print("Hello, I\'m Python!") Hello, I\'m Python!',
              'origin': 'www.python.org/',
              'time': None,
              'title': 'Welcome to Python.org',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=NC7GXkMtnZ9t8csmbawkvfp2QbDaaMHleael-qkCOtlSy_kfPsT8ARljUiIVOH2L'},
             {'des': 'The official home of the Python Programming Language',
              'origin': 'www.python.org/getit',
              'time': None,
              'title': 'Download Python | Python.org',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=AKBkNZv2L7600dOvqeylKK0fSRJJboDgjf7xGPuZfx2giBnXAiukP5ch7Tb619zC'},
             {'des': 'Python(英国发音:/ˈpaɪθən/ 美国发音:/ˈpaɪθɑːn/), '
                     '是一种面向对象的解释型计算机程序设计语言,由荷兰人Guido van Rossum于1989年发明,第...',
              'origin': '知乎',
              'time': None,
              'title': 'Python - 知乎',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=xxKNKxpUHwEvoPt7OlqXceI0jTqTgvkJr0cncYDUPVNpYB397k-mbLlMOrw4IhNa'},
             {'des': 'Python 基础教程 Python 是一种解释型、面向对象、动态数据类型的高级程序设计语言。 Python 由 '
                     'Guido van Rossum 于 1989 年底发明,第一个公开发行版发行于 1991...',
              'origin': 'www.runoob.com/python/python-t...',
              'time': '2020年1月1日',
              'title': 'Python 基础教程 | 菜鸟教程',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=ShmleIIBtIEfujCO1Wqh3PrOab_VrP87gN9GkEDGwQSj9OJ27Hst5NRomZtDRaxI7-WWSGLJ0-olY7Gt5merVK'},
             {'des': '在Python 中,* 和 ** 具有语法多义性,具体来说是有三类用法。1. 算数运算* 代表乘法** '
                     '代表乘方>>> 2 * 510>>> 2 ** 5322...',
              'origin': 'CSDN技术社区',
              'time': '2018年6月5日',
              'title': 'Python3 * 和 ** 运算符_极客点儿-CSDN博客',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=Wo6dq8qZ24BrXjb6ZO5Ft20HEUmtEvGn7zTArPFe6IGnYYID3jjhQK_iwtP2G_rawgQLa52_68YRCVWzYjfPyptYEJmoGu-kDlTsmNoJ26S'},
             {'des': '首先上一首 Python 之禅:我从 2015 年 3 月第一次接触 Python 这门语言(之前一直写 '
                     'PHP),就对其简洁…',
              'origin': '知乎',
              'time': '2019年3月28日',
              'title': '你都用 Python 来做什么? - 知乎',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=9Yve5ybsv1wP2WlxkOqO0z7wa_DaY__D1bTMLOaxT_UAqayv9RVWNHOjo68Hj1GycG5KSNutW6ofYdO4pYsjrTBz3Pe4hl-yQRxMtOfiWES'},
             {'des': 'Python是由创始人贵铎·范·罗萨姆(Guido van '
                     'Rossum)在阿姆斯特丹于1989年圣诞节期间,为了打发圣诞节的无趣,开发的一个新的解释型脚本语言。',
              'origin': 'www.yunweipai.com/python',
              'time': '2019年4月25日',
              'title': 'Python教程 - 运维派',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=px_zi74_EXc23TEOILqPGQfW49CRQv448R7MXLXGQiV-HQNiuxW8sYGRhasJSOVp'},
             {'des': '这套Python基础教程通俗易懂,深入浅出,旨在帮助大家快速入门。这套Python教程虽然学习门槛低,但是知识体系很丰富,并且包含了大量实例,让大家学以致用。',
              'origin': 'c.biancheng.net/python',
              'time': None,
              'title': 'Python基础教程,Python入门教程(非常详细)_C语言中文网',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=etpIrqd8bVpZzDq54FotETIfGChVtHeVAjLjdVHgdFSyN-jvo421D01Tdjt7FsJ9'},
             {'des': 'Python 100例 以下实例在Python2.7下测试通过: Python 练习实例1 Python '
                     '练习实例2 Python 练习实例3 Python 练习实例4 Python 练习实例5 Python '
                     '练习实例6 Python...',
              'origin': 'www.runoob.com/python/python-1...',
              'time': None,
              'title': 'Python 100例 | 菜鸟教程',
              'type': 'result',
              'url': 'http://www.baidu.com/link?url=pMlhzHAsK3rai-RLPA0nY_s1nahEjH5nrkPw23lbXbCUWeV0moA3vvMfa0wTSSpJ0FUjizbPCEq0d_lIFiGiHK'}],
 'total': 10}
```

更详细的新手教程可在[文档](https://baiduspider.github.io/usage/get-started/)中找到。

<br />

<h2 align="center">
    维护BaiduSpider
</h2>

<br />

如果你想要参与BaiduSpider的维护工作，我将十分感激！维护的方式多种多样，可以通过[提交新的issue](https://github.com/BaiduSpider/BaiduSpider/issues/new/choose)，可以为新手解答issue，甚至[提交一个PR](https://github.com/BaiduSpider/BaiduSpider/compare)！

<br />

<h2 align="center">
    特别致谢
</h2>

<br />

- 感谢[requests](https://requests.readthedocs.io/en/master/)提供爬虫的HTTP获取网页的支持

- 感谢[MkDocs](https://github.com/mkdocs/mkdocs)和[Material for MkDocs](squidfunk.github.io/mkdocs-material/)提供的精致的文档框架

- 感谢[FastAPI](https://fastapi.tiangolo.com/)提供的小巧但强大的Web API框架，为BaiduSpider即将发布的API提供了支持

- 感谢[Vue](http://vuejs.org/)这个强大的前端框架，为BaiduSpider的[前端](https://baiduspider.now.sh)提供了强有力的支持

- 感谢所有对BaiduSpider提交错误报告，解答issue，和提交PR的你们！
