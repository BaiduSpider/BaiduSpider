# 百科搜索

> 百度百科搜索，移动的百科全书。

```python
BaiduSpider.search_baike(
    self: BaiduSpider,
    query: str,
    proxies: Union[dict, None] = None,
) -> BaikeResult
```

## 参数

- query `#!python str`: 要查询视频搜索的字符串
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_baike("要搜索的关键词").plain)
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_baike)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/baike.html)。
