# 指南

`指南`这部分文档将介绍BaiduSpider绝大多数函数的使用方法以及常见问题。

下面我们会介绍函数间通用的一些文档。

## 搜索返回值

BaiduSpider的所有搜索函数都是一个自定义结果类。例如，PC端网页搜索返回类型为`WebResult`，而移动端网页搜索则为`mobile.WebResult`。

对于不同的搜索类型，BaiduSpider提供不同的返回结果。更详细的返回类型请参考[API文档](/api/index.html)。

## 代理设置

几乎所有的BaiduSpider搜索函数都支持`proxies`参数。该参数的作用为设定代理IP。下面是它的一些使用场景：

- 做数据分析，需要爬取大量数据时
- 人工智能无监督学习时
- 通过百度搜索进行特定的大量定时任务时
- 大量，频繁地搜集热点新闻时
- ……

由于用户的种种需求，我们特开发出了此功能。

该参数接受一个`#!python dict`对象，例如：

```python hl_lines="7 8 9 10"
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()
result = spider.search_news(
    "搜索词",
    proxies={
        "http": "http://192.168.xxx.xxx",  # HTTP代理IP地址
        "https": "https://192.168.xxx.xxx"  # HTTPS代理IP地址
    }
)
pprint(result.plain)

```

该功能的原理为设定`requests.get`函数的`proxies`参数，BaiduSpider仅提供了一个接口。由此，更详细的说明请参考[`requests`文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

???tip "请求过多怎么办？"
    如果遇到单个IP请求过多的话，可以使用IP代理池轮换使用。或者可以参考[设置Cookie](#设置Cookie)来延缓封禁。

???+warning
    此功能仅为学习和研究使用，请勿使用此功能爬取百度大量数据，违者后果自负。BaiduSpider不为此功能承担任何法律责任。

## 出现解析警告

请参考[FAQ](/FAQ/index.html#%E4%B8%BA%E4%BB%80%E4%B9%88%E6%9C%89%E6%97%B6%E5%80%99BaiduSpider%E4%BC%9A%E5%87%BA%E7%8E%B0%E8%AD%A6%E5%91%8A)。

## 设置Cookie

BaiduSpider提供设定用户的Cookie来延缓被百度IP封禁的问题。**目前仅支持[PC端网页搜索](/guide/pc/web.html)，且不保证100%有效。**

除此以外，[PC端文库搜索](/guide/pc/wenku.html)在搜索范围为“免费”（`#!py "free"`）时，也需要传入Cookie才能进行正常搜索。

***只有在登录了百度账号时获取的Cookie才能有效使用，未登录情况下无效。***

???todo
    移动端爬虫`BaiduMobileSpider`尚未开发此接口，请勿使用[^1]。后期可能会考虑加入此接口。

你需要把你的Cookie传给BaiduSpider，方式如下：

```python
from baiduspider import BaiduSpider

# 在实例化BaiduSpider对象时传入cookie
spider = BaiduSpider(cookie="你的cookie")
```

然后，BaiduSpider会在每次调用`search_web`的时候根据你的Cookie重新生成新的Cookie并稍加更改。

### 如何获取你的Cookie

首先，打开你的浏览器并访问<https://www.baidu.com/s?wd=placeholder&pn=0>：

![上述URL访问后的界面](https://i.loli.net/2021/08/03/S2xmDbvQkc7gTnj.png)

然后，点击 ++f12++ 打开开发者工具，并在开发者工具顶部选项栏中选择“网络”（Network）选项并按 ++ctrl+r++：（Windows）或 ++cmd+r++ （Mac）重新加载网页。开发者工具中将会显示一串列表，表示所有的请求。

![开发者工具](https://i.loli.net/2021/08/03/pj1LEM5KxWBHiXY.png)

最后，在列表最上方点击以`s?wd=placeholder`开头的选项，将会弹出一个信息框。在信息框内的`Headers`（第一个）选项内找到`Request Headers`（请求头），再在`Request Headers`内找到 **`Cookie: `**，复制Cookie下的全部内容（不包括`Cookie: `），这就是你的Cookie。

![要复制的内容](https://i.loli.net/2021/08/03/enPE7yIMLdx5rwh.png)

???+danger "不要传入非法Cookie！"
    请勿传入非法的Cookie给BaiduSpider。这可能会导致错误，但更重要的是可能会使你的IP长时间封禁！

???+warning
    即使BaiduSpider提供这个功能，但是仅是为了学习用途，任何非法爬取百度大量数据的人后果自负，BaiduSpider不承担任何法律责任。

[^1]: 即`BaiduMobileSpider`类暂时没有`cookie`参数，若使用会出现错误。
