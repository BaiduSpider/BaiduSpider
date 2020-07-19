# 图片搜索

```python
BaiduSpider.search_pic(self: BaiduSpider, query: str, pn: int = 1) -> dict
```

### 参数

- self: BaiduSpider，即必须实例化`BaiduSpider`对象后才可调用。

- query: str，搜索关键字

- pn: int，要爬取的页码，默认为1，为可选参数

#### 实例

- 基本的调用

```python
from main import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索图片
pprint(spider.search_pic(query=input('要搜索的关键词：')))
```

- 指定页码

```python
from main import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索图片，并传入页码参数
pprint(spider.search_pic(query=input('要搜索的关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，因为寻找不到合适的element，BaiduSpider会报错`AttributeError`

### 返回值

`BaiduSpider.search_pic`的返回值类型是`dict`，大致返回模版如下：

```python
{
    # 搜索结果列表
    'results': [
        {
            'host': str,  # 图片来源域名
            'title': str,  # 图片标题
            'url': str  # 图片链接
        },
        { ... },
        { ... },
        { ... },
        ...
    ],
    # 搜索结果总计页码，可能会变化
    'total': int
}
```

!!! note
    图片的来源不一定是准确的，因为百度有时不提供图片来源

!!! warning
    不要将总计页码存到一个变量后不再变动，因为它是动态的，可能随时变化
