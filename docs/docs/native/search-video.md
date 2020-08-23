# 视频搜索

> 百度视频搜索，爬取站点：<http://v.baidu.com/>

```python
BaiduSpider.search_video(self: BaiduSpider, query: str, pn: int = 1) -> dict
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

# 搜索视频
pprint(spider.search_video(query=input('视频搜索关键词：')))
```

#### 指定页码

```python
from baiduspider.core import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索视频，并传入页码参数
pprint(spider.search_video(query=input('视频搜索关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，因为寻找不到合适的element，BaiduSpider会报错`AttributeError`

### 返回值

`BaiduSpider.search_video`的返回值类型是`dict`，返回模版如下：

```python
{
    # 搜索结果列表
    'results': [{
        'img': str,  # 视频封面图片链接
        'time': str,  # 视频时长
        'title': str,  # 视频标题
        'url': str  # 视频链接
    }]
    'total': int  # 搜索结果最大页数，可能因搜索页数改变而改变
}
```

!!! warning
    不要将总计页码存到一个变量后不再变动，因为它是动态的，可能随时变化

## 返回值解释

在返回值中，有两个键，分别是`results`和`total`。其中，`total`表示总计搜索结果的页数，并且可能会因为当前页数的变化而随之变化，值类型为`int`。`results`代表搜索结果列表，类型为`list`。

视频结果字典，类型为`dict`，模型如下：

```python
{
    'img': str,
    'time': str,
    'title': str,
    'url': str
}
```

### 模型解释

- `img`：视频封面图片链接，类型是`str`
- `time`：视频时长，类型是`str`
- `title`：视频标题，类型是`str`
- `url`：视频链接，类型是`str`
