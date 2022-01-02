# 文库搜索

> 百度文库搜索，获取文档更加便捷

```python
BaiduSpider.search_wenku(
    self: BaiduSpider,
    query: str,
    pn: int = 1,
    scope: str = "all",
    format: str = "all",
    time: str = "all",
    page_range: Union[Tuple[int], str] = "all",
    sort_by: str = "relation",
    proxies: Union[dict, None] = None,
) -> WenkuResult:
```

## 参数

- query `#!py str`: 要查询文库搜索的字符串
- pn `#!py int`: 要爬取的页码，默认为`#!py 1`，可选
- scope `#!py str`: 搜索结果筛选范围，默认为`#!py "all"`，可选
- format `#!py str`: 搜索结果格式筛选方式，默认为`#!py "all"`，可选
- time `#!py str`: 搜索结果时间筛选方式，默认为`#!py "all"`，可选
- page_range `#!py Union[Tuple[int], str]`，搜索结果页码范围，默认为`#!py "all`，可选
- sort_by `#!py str`: 搜索结果排序方式，默认为`#!py "relation"`，可选
- proxies `#!py Union[dict, None]`: 代理配置，默认为`#!py None`，可选

## 实例

### 基本的调用

```python
from baiduspider import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

pprint(spider.search_wenku(query="要搜索的关键词").plain)
```

### 指定页码

```python
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", pn=2).plain)
```

### 筛选文档来源

这四个参数可以让你搜到所需要的来源。下面我们来一一介绍它们的用法与含义。

当然，除了单一地使用，你也可以组合这些筛选一起使用。

#### 按范围筛选

正如百度文库搜索本身所提供的一样，BaiduSpider也提供这项筛选。它的选项分别为`#!py "all"`（显示全部，即不筛选，默认）、`#!py "vip-only"`（VIP专享）、`#!py "vip-free"`（VIP免费）、`#!py "free"`（免费）和`#!py "high-quality"`（精品）。参数`scope`负责这项功能。

值得一提的是，当使用`#!py "free"`作为筛选的时候，需要额外[提供 Cookie](/guide/index.html#设置Cookie)。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", scope="vip-only").plain)  # 仅显示VIP专享的文档
```

#### 按格式筛选

目前 BaiduSpider 支持六种格式可供筛选，分别为`#!py ["all", "doc", "ppt", "txt", "pdf", "xls"]`。其中，`#!py "all"`的含义为不筛选格式（默认），其余含义如字面。

你可以通过设置`format`参数来改变筛选。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", format="ppt").plain)  # 仅显示PPT格式的文档
```

#### 按时间筛选

使用`time`筛选参数，你可以进行以年为单位的时间筛选。选项分别为`#!py "all"`（不筛选，默认）、`#!py "this-year"`（今年）、`#!py "last-year"`（去年）和`#!py "previous-years"`（前年及以前）。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", time="last-year").plain)  # 仅显示去年发布的文档
```

#### 按页数筛选

你可以使用`page_range`参数来通过页数筛选文档。`page_range`的可选值为`#!py ["all", Tuple[start: int, end: int]]`。其中，`#!py "all"`的含义为不通过页数进行筛选（默认）。另一个元组选项则是筛选区间。

例如，我们可以使用元组`#!py (1, 10)`表示仅筛选页数为1 ~ 10页的文档。元组的第一个参数是区间开始页码，第二个参数则是区间结束的页码。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", page_range=(5, 19)).plain)  # 仅显示页数为5页到19页的文档
```

### 搜索结果排序方式

对于文库搜索，BaiduSpider 提供四种不同的排序方式，分别为：按相关性、按时间、按下载量和按评分。你可以通过更改`sort_by`参数的值来修改排序方式。

`sort_by`参数接受四种字符串的值：`#!py ["relation", "time", "downloads", "score"]`。其含义分别如上述。

```python hl_lines="4"
from baiduspider import BaiduSpider
from pprint import pprint

pprint(BaiduSpider().search_wenku("要搜索的关键词", sort_by="downloads").plain)  # 按下载量排序
```

## 返回值

### 字典返回值

详见 [API 文档](/api/baiduspider/__init__.html#baiduspider.__init__.BaiduSpider.search_wenku)。

### 模型结果返回值

详见 [API 文档](/api/baiduspider/models/wenku.html)。
