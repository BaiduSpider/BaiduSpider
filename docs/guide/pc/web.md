# 网页搜索

> 百度网页搜索，也可以作为综合搜索使用。

```python
BaiduSpider.search_web(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    exclude: list = [],
    proxies: Union[dict, None] = None,
) -> WebResult
```

## 参数

- query `#!python str`: 要查询网页搜索的字符串
- pn `#!python int`: 要爬取的页码，默认为`#!py 1`，可选
- exclude `#!python dict`: 要屏蔽的子部件列表，可选
- time `#!python str | List[datetime.datetime]`: 搜索时间范围
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

这是一个最基本的参数——`query`。它用于传递搜索词（字符串类型）。

```python hl_lines="9"
# 导入BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()

# 搜索网页
pprint(spider.search_web(query="要搜索的关键词").plain)
```

### 指定页码

你可以通过设置`pn`参数来更改 BaiduSpider 所获取的页码。

```python hl_lines="7"
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，并传入页码参数（此处为第二页）
pprint(spider.search_web(query="要搜索的关键词", pn=2).plain)
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，否则百度搜索会自动跳转回第一页

### 屏蔽特定的搜索结果

这个参数可以为你提供很大的便捷。通过设置`exclude`列表，你可以屏蔽某些特定的网页搜索子搜索结果来提高解析速度。

```python
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，并传入要屏蔽的结果
# 在本样例中，屏蔽了贴吧和博客
pprint(spider.search_web(query="要搜索的关键词", exclude=["tieba", "blog"]).plain)
```

`exclude`的值可以包含：`#!python ["news", "video", "baike", "tieba", "blog", "gitee", "related", "calc"]`，分别表示：资讯，视频，百科，贴吧，博客，Gitee代码仓库，相关搜索，计算。`exclude`的值也可以是`#!python ["all"]`，表示屏蔽除了普通搜索结果外的所有搜索结果。实例：

```python
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，并传入要屏蔽的结果
# 在本样例中，屏蔽了所有非普通的搜索结果
pprint(spider.search_web(query="要搜索的关键词", exclude=["all"]).plain)
```

如果`exclude`中包含`all`且还有其他参数，那么将按照只有`all`的方式过滤搜索结果。

### 按时间筛选

`time`参数能够实现更精准的搜索。`time`的取值可以是一个字符串或者是一个由`datetime.datetime`组成的元组。比如，使用字符串形式：

```python hl_lines="8"
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，仅显示时间段内的搜索结果
# 在本样例中，筛选后仅显示一周内的搜索结果
pprint(spider.search_web(query="要搜索的关键词", time="week").plain)
```

此功能使用百度内置的搜索时间筛选器筛选结果，并非使用程序筛选。在这个样例中，`time`的值是`#!python "week"`，代表筛选一周内的搜索结果。`time`的可选值如下：`#!python ["day", "week", "month", "year"]`。分别表示：一天内、一周内、一月内、一年内。除此以外，BaiduSpider 还支持自定义时间段。例如：

```python hl_lines="8"
from baiduspider import BaiduSpider
from pprint import pprint
from datetime import datetime

spider = BaiduSpider()

# 在本样例中，筛选后仅显示2020.1.5 - 2020.4.9的搜索结果
pprint(spider.search_web(query="要搜索的关键词", time=(datetime(2020, 1, 5), datetime(2020, 4, 9))).plain)
```
在这个样例中，`time`的值是一个元组（`#!python tuple`）。元组的第一个值是起始时间，第二个值是结束时间。BaiduSpider会把他们都转化成`#!python time.time()`形式的浮点数（然后仅保留整数），所以你也可以将`#!python datetime`替换为一个整数。

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_web)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/web.html)。
