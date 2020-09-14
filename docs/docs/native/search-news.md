# 资讯搜索

> 百度资讯搜索，爬取站点：<https://news.baidu.com>

```python
BaiduSpider.search_news(self: BaiduSpider, query: str, pn: int = 1) -> dict
```

## 参数

- self: BaiduSpider，即必须实例化`BaiduSpider`对象后才可调用。

- query: str，搜索关键字

- pn: int，要爬取的页码，默认为1，为可选参数

### 实例

#### 基本的调用

```python
from baiduspider.core import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索资讯
pprint(spider.search_news(query=input('资讯搜索关键词：')))
```

#### 指定页码

```python
from baiduspider.core import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索资讯，并传入页码参数
pprint(spider.search_news(query=input('资讯搜索关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，否则由于百度自动跳转的原因，BaiduSpider会提供第一页的搜索结果

### 返回值

`BaiduSpider.search_news`的返回值类型是`dict`，返回模版如下：

```python
{
    # 搜索结果列表
    'results': [{
        'author': str,  # 资讯来源（作者）
        'date': str,  # 资讯发布时间
        'des': str,  # 资讯简介
        'title': str,  # 资讯标题
        'url': str  # 资讯链接
    }],
    'total': int  # 搜索结果最大页码，可能会因为当前页数变化而变化
}
```

!!! warning
    不要将总计页码存到一个变量后不再变动，因为它是动态的，可能随时变化

## 返回值解释

在返回值中，有两个键，分别是`results`和`total`。其中，`total`表示总计搜索结果的页数，并且可能会因为当前页数的变化而随之变化，值类型为`int`。`results`代表搜索结果列表，类型为`list`。

资讯搜索结果字典，类型为`dict`，模型如下：

```python
{
    'author': str,
    'date': str,
    'des': str,
    'title': str,
    'url': str
}
```

### 模型解释

- `author`：资讯来源（作者），类型是`str`
- `date`：资讯发布时间，类型是`str`
- `des`：资讯简介，类型是`str`
- `title`：资讯标题，类型是`str`
- `url`：资讯链接，类型是`str`
