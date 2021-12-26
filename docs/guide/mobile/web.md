# 网页搜索

> 移动端百度网页搜索，更轻巧，更便捷。

```python
BaiduMobileSpider.search_web(
    self: BaiduMobileSpider,
    query: str,
    pn: int = 1,
    proxies: Union[dict, None] = None,
) -> WebResult
```

## 参数

- query `#!python str`: 需要查询的字符串
- pn `#!python int`: 要爬取的页码，默认为`#!py 1`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python
from baiduspider import BaiduMobileSpider
from pprint import pprint

pprint(BaiduMobileSpider().search_web("要搜索的关键词"))
```

### 指定页码

你可以通过设置`pn`参数来更改 BaiduSpider 所获取的页码。

```python
from baiduspider import BaiduMobileSpider
from pprint import pprint

pprint(BaiduMobileSpider().search_web("要搜索的关键词", pn=2))
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/mobile/__init__.html#baiduspider.mobile.__init__.BaiduMobileSpider.search_web)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/mobile/models/web.html)。
