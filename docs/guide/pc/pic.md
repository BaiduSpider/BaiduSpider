# 图片搜索

> 百度图片搜索，检索互联网上繁多的图片。

```python
BaiduSpider.search_pic(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    proxies: Union[dict, None] = None,
) -> PicResult
```

## 参数

- query `#!python str`: 要查询图片搜索的字符串
- pn `#!python int`: 要爬取的页码，默认为`#!py 1`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

与网页搜索一样，这也是最基础的。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_pic("要搜索的关键词").plain)
```

### 指定页码

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_pic("要搜索的关键词", pn=2).plain)
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_pic)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/pic.html)。
