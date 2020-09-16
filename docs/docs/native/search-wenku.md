# 文库搜索

> 百度文库搜索，爬取站点：<https://wenku.baidu.com>

```python
BaiduSpider.search_wenku(self: BaiduSpider, query: str, pn: int = 1) -> dict
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
pprint(spider.search_wenku(query=input('文库搜索关键词：')))
```

#### 指定页码

```python
from baiduspider.core import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索资讯，并传入页码参数
pprint(spider.search_wenku(query=input('文库搜索关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，因为寻找不到合适的element，BaiduSpider会报错AttributeError

### 返回值

`BaiduSpider.search_news`的返回值类型是`dict`，返回模版如下：

```python
{
    # 搜索结果列表
    'results': [{
        'date': str,  # 文章发布日期
        'des': str,  # 文章简介
        'downloads': int,  # 文章下载量
        'pages': int,  # 文章页数
        'title': str,  # 文章标题
        'type': str,  # 文章格式，全部为大写字母
        'url': str  # 文章链接
    }],
    'total': int  # 搜索结果最大页码，可能会因为当前页数变化而变化
}
```

!!! warning
    不要将总计页码存到一个变量后不再变动，因为它是动态的，可能随时变化

## 返回值解释

在返回值中，有两个键，分别是`results`和`total`。其中，`total`表示总计搜索结果的页数，并且可能会因为当前页数的变化而随之变化，值类型为`int`。`results`代表搜索结果列表，类型为`list`。

文库搜索结果字典，类型为`dict`，模型如下：

```python
{
    'date': str,
    'des': str,
    'downloads': int,
    'pages': int,
    'title': str,
    'type': str,
    'url': str
}
```

### 模型解释

- `date`：文章发布日期，类型是`str`
- `des`：文章简介，类型是`str`
- `downloads`：文章下载量，类型是`int`
- `pages`：文章页数，类型是`int`
- `title`：文章标题，类型是`str`
- `type`：文章格式，全部为大写字母，word格式为`DOC`，ppt格式为`PPT`，pdf格式为`PDF`，纯文本格式为`TXT`等，类型是`str`
- `url`：文章链接，类型是`str`
