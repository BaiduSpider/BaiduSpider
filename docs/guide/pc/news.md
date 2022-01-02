# 资讯搜索

> 百度资讯搜索，从海量新闻当中提取重要信息。

```python
BaiduSpider.search_news(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    sort_by: str = "focus",
    show: str = "all",
    proxies: Union[dict, None] = None,
) -> NewsResult:
```

## 参数

- query `#!py str`: 要查询资讯搜索的字符串
- pn `#!py int`: 要爬取的页码，默认为`#!py 1`，可选
- sort_by `#!py str`: 搜索结果排序方式，默认为`#!py "focus"`，可选
- show `#!py str`: 搜索结果筛选方式，默认为`#!py "all"`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python hl_lines="6"
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

pprint(spider.search_news(query="要搜索的关键词").plain)
```

### 指定页码

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_news("要搜索的关键词", pn=2).plain)
```

### 搜索结果排序方式

BaiduSpider 提供两种不同的资讯搜索搜索结果排序方式：焦点与时间。默认情况下，BaiduSpider 会按照焦点进行排序，当然你也可以指定使用时间进行排序：通过更改`sort_by`参数的值。

`sort_by`参数接受两种字符串的值：`focus`（焦点，默认）与`time`（时间）。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_news("要搜索的关键词", sort_by="time").plain)  # 按时间排序
```

### 筛选资讯来源

这个参数可以让你搜到所需要的来源。你可以通过更改`show`参数的值来达到这一目的。默认无筛选。

目前支持的选项有：`all`（全部，即无筛选，默认）、`media`（来自媒体的新闻）、`baijiahao`（来自百家号的新闻）。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_news("要搜索的关键词", show="media").plain)  # 仅显示来自媒体的资讯
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_news)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/news.html)。
