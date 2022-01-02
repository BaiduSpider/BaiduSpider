# 经验搜索

> 百度经验搜索，获取前人经验

```python
BaiduSpider.search_jingyan(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    scope: str = "all",
    proxies: Union[dict, None] = None,
) -> JingyanResult:
```

## 参数

- query `#!py str`: 要查询知道搜索的字符串
- pn `#!py int`: 要爬取的页码，默认为`#!py 1`，可选
- scope `#!py str`: 搜索结果筛选范围，默认为`#!py "all"`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python hl_lines="6"
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

pprint(spider.search_jingyan(query="要搜索的关键词").plain)
```

### 指定页码

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_jingyan("要搜索的关键词", pn=2).plain)
```

### 筛选范围

经验搜索提供筛选范围参数：`scope`参数。你可以筛选全部经验（`#!py "all"`，默认）、优秀经验（`#!py "outstanding"`）、好评经验（`#!py "praise"`）和原创经验（`#!py "original"`）。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_jingyan("要搜索的关键词", scope="original").plain)  # 仅显示原创经验
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_jingyan)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/jingyan.html)。
