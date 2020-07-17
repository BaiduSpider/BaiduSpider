# 网页搜索

```python
BaiduSpider.search_web(self: BaiduSpider, query: str, pn: int = 1) -> dict
```

### 参数

- self: BaiduSpider，即必须实例化`BaiduSpider`对象后才可调用。

- query: str，要查询网页搜索的字符串

- pn: int，要爬取的页码，默认为1，为可选参数

#### 实例

- 基本的调用

```python
# 导入BaiduSpider
from main import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()

# 搜索网页
pprint(spider.search_web(word=input('要搜索的关键词：')))
```

- 指定页码

```python
from main import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，并传入页码参数
pprint(spider.search_web(word=input('要搜索的关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，因为百度搜索会自动跳转回第一页

### 返回值

`BaiduSpider.search_web`函数的返回类型是`dict`，大致返回模版如下：

```python
{
    # 搜索结果列表
    'results': [
        # 总计搜索结果数量
        {
            'result': int,  # 总计搜索结果数
            'type': 'total'  # type用来区分不同类别的搜索结果
        },
        # 相关搜索建议
        {
            'results': [
                str,  # 相关搜索建议
                '...',
                '...',
                '...',
                ...
            ],
            'type': 'related'
        },
        # 运算窗口，仅会在搜索词涉及运算时出现
        {
            'process': str,  # 算数过程
            'result': str,  # 运算结果
            'type': 'calc'
        },
        # 相关新闻，仅会在搜索词有相关新闻时出现
        {
            'results': [
                {
                    'author': str,  # 新闻来源
                    'time': str,  # 新闻发布时间
                    'title': str,  # 新闻标题
                },
                { ... },
                { ... },
                { ... },
                ...
            ],
            'type': 'news'
        },
        # 相关视频，仅会在搜索词有相关视频时出现
        {
            'results': [
                {
                    'cover': str,  # 视频封面图片链接
                    'origin': str,  # 视频来源
                    'length': str,  # 视频时长
                    'title': str,  # 视频标题
                    'url': str,  # 视频链接
                },
                { ... },
                { ... },
                { ... },
                ...
            ],
            'type': 'video'
        },
        # 普通的搜索结果
        {
            'des': str,  # 搜索结果简介
            'origin': str,  # 搜索结果的来源，可能是域名，也可能是名称
            'title': str, # 搜索结果标题
            'type': 'result',
            'url': str, # 搜索结果链接
        },
        { ... },
        { ... },
        { ... },
        ...
    ],
    # 总计的搜索结果页数，可能会因为当前页数的变化而随之变化
    'total': int
}
```

!!! note
    因为百度网页搜索有多种搜索结果，所以`search_web`函数使用`type`标签为不同类别的搜索结果分类，如视频是`video`，资讯是`news`，运算是`calc`等不同标签，其中`result`为普通的搜索结果。
