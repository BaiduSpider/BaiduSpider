# 知道搜索

> 百度知道搜索，秒取问题答案

```python
BaiduSpider.search_zhidao(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    time: Union[str, None] = None,
    proxies: Union[dict, None] = None,
) -> ZhidaoResult:
```

## 参数

- query `#!py str`: 要查询知道搜索的字符串
- pn `#!py int`: 要爬取的页码，默认为`#!py 1`，可选
- time `#!py Union[str, None]`: 搜索结果时间筛选方式，默认为`#!py None`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

pprint(spider.search_zhidao(query="要搜索的关键词").plain)
```

### 指定页码

```python
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_zhidao("要搜索的关键词", pn=2).plain)
```

### 按时间筛选

通过更改`time`参数的值，你可以按时间筛选搜索结果。`time`默认为`None`，即不筛选，你也可以把它更改为下列任一一种：`#!py ["week", "month", "year"]`。它们分别表示：一周内、一月内和一年内。

```python
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_zhidao("要搜索的关键词", time="month").plain)  # 仅显示发布时间在一个月内的问答
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_zhidao)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/zhidao.html)。
