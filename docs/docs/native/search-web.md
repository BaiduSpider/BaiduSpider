# 网页搜索

> 百度网页搜索，也可以作为综合搜索使用。

```python
BaiduSpider.search_web(self: BaiduSpider, query: str, pn: int = 1) -> dict
```

## 参数

- self: BaiduSpider，即必须实例化`BaiduSpider`对象后才可调用。

- query: str，要查询网页搜索的字符串

- pn: int，要爬取的页码，默认为1，为可选参数

### 实例

#### 基本的调用

```python
# 导入BaiduSpider
from baiduspider.core import BaiduSpider
from pprint import pprint

# 实例化BaiduSpider
spider = BaiduSpider()

# 搜索网页
pprint(spider.search_web(query=input('要搜索的关键词：')))
```

#### 指定页码

```python
from baiduspider.core import BaiduSpider
from pprint import pprint

spider = BaiduSpider()

# 搜索网页，并传入页码参数
pprint(spider.search_web(query=input('要搜索的关键词：'), pn=int(input('页码：'))))
```

!!! warning
    传入页码参数的时候一定要小心，务必不要传入过大的页码，因为百度搜索会自动跳转回第一页

## 返回值

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
            'results': [str],  # 相关搜索建议
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
            'results': [{
                'author': str,  # 新闻来源
                'time': str,  # 新闻发布时间
                'title': str,  # 新闻标题
                'url': str,  # 新闻链接
                'des': str  # 新闻简介，大部分时间是None
            }],
            'type': 'news'
        },
        # 相关视频，仅会在搜索词有相关视频时出现
        {
            'results': [{
                'cover': str,  # 视频封面图片链接
                'origin': str,  # 视频来源
                'length': str,  # 视频时长
                'title': str,  # 视频标题
                'url': str  # 视频链接
            }],
            'type': 'video'
        },
        # 相关百科，仅会在搜索词有相关百科时出现
        {
            'result': {
                'cover': str,  # 百科封面图片/视频链接
                'cover-type': str,  # 百科封面类别，图片是image，视频是video
                'des': str,  # 百科简介
                'title': str,  # 百科标题
                'url': str  # 百科链接
            },
            'type': 'baike'
        },
        # 普通的搜索结果
        {
            'des': str,  # 搜索结果简介
            'origin': str,  # 搜索结果的来源，可能是域名，也可能是名称
            'title': str, # 搜索结果标题
            'type': 'result',
            'url': str # 搜索结果链接
        }
    ],
    # 总计的搜索结果页数，可能会因为当前页数的变化而随之变化
    'total': int
}
```

!!! note
    因为百度网页搜索有多种搜索结果，所以`search_web`函数使用`type`标签为不同类别的搜索结果分类，如视频是`video`，资讯是`news`，运算是`calc`等不同标签，其中`result`为普通的搜索结果。

## 返回值解释

在返回值中，有两个键，分别是`results`和`total`。其中，`total`表示总计搜索结果的页数，并且可能会因为当前页数的变化而随之变化，值类型为`int`。`results`代表搜索结果列表，类型为`list`。下面是列表中各个值的详细解释。

### 结果数量

该项的分类为`total`，模型如下：

```python
{
    'result': int,
    'type': 'total'
}
```

#### 解释

- `result`：该项表示总计的搜索结果数量（大约），值类型为`int`
- `type`：该项表示该结果的类别，值为`total`，类型是`str`

### 相关搜索建议

该项的分类为`related`，模型如下：

```python
{
    'results': [str],
    'type': 'related'
}
```

#### 解释

- `results`：该项中每个成员类型为`str`，表示一个相关搜索，值类型为`list`
- `type`：该项表示该结果的类别，值为`related`，类型是`str`

### 运算

该项的分类为`calc`，模型如下：

```python
{
    'process': str,
    'result': str,
    'type': 'calc'
}
```

#### 解释

- `process`：该项为运算过程，如`10*9-8`，值类型为`str`
- `result`：该项为运算结果，如`82`，值类型为`str`
- `type`：该项表示该结果的类别，值为`calc`，类型是`str`

!!!warning
    本项搜索结果仅在搜索词参与运算时出现，请谨慎调用

### 相关新闻

该项的分类为`news`，模型如下：

```python
{
    'results': [{
        'author': str,
        'time': str,
        'title': str,
        'url': str,
        'des': str
    }],
    'type': 'news'
}
```

#### 解释

- `results`：表示相关新闻，其中有许多子字典，每个子字典表示一条新闻。值类型为`list`
    - `author`：新闻来源，类型为`str`
    - `time`：新闻发布时间，类型为`str`
    - `title`：新闻标题，类型为`str`
    - `url`：新闻链接，类型为`str`
    - `des`：新闻简介，类型为`str`，大部分时间为None
- `type`：该项表示该结果的类别，值为`news`，类型是`str`

!!!warning
    本项搜索结果仅在搜索词有相关新闻时出现，请谨慎调用

### 相关视频

该项的分类为`video`，模型如下：

```python
{
    'results': [{
        'cover': str,
        'origin': str,
        'length': str,
        'title': str,
        'url': str
    }],
    'type': 'video'
}
```

#### 解释

- `results`：表示相关视频，其中有若干个子字典，每个子字典表示一个相关视频。值类型为`list`
    - `cover`：视频封面图片链接，值类型为`str`
    - `origin`：视频来源，值类型为`str`
    - `length`：视频时长，值类型为`str`
    - `title`：视频标题，值类型为`str`
    - `url`：视频链接，值类型为`str`
- `type`：该项表示该结果的类别，值为`video`，类型是`str`

!!!warning
    本项搜索结果仅在搜索词有相关视频时出现，请谨慎调用

### 相关百科

该项的分类为`baike`，模型如下：

```python
{
    'result': {
        'cover': str,
        'cover-type': str,
        'des': str,
        'title': str,
        'url': str
    },
    'type': 'baike'
},
```

#### 解释

- `result`：表示一个百科，值类型为`dict`
    - `cover`：百科的封面链接，可能时图片，也可能是视频，值类型为`str`
    - `cover-type`：百科的封面类型，图片为`image`，视频为`video`，值类型为`str`
    - `des`：百科简介，值类型为`str`
    - `title`：百科标题，值类型为`str`
    - `url`：百科链接，值类型为`str`
- `type`：该项表示该结果的类别，值为`baike`，类型是`str`

!!!warning
    本项搜索结果仅在搜索词有相关百科时出现，请谨慎调用

### 普通的搜索结果

该项的分类为`result`，模型如下：

```python
{
    'des': str,
    'origin': str,
    'title': str,
    'type': 'result',
    'url': str
}
```

#### 解释

- `des`：搜索结果简介，类型为`str`
- `origin`：搜索结果来源，类型为`str`
- `title`：搜索结果标题，类型为`str`
- `type`：该项表示该结果的类别，值为`result`，类型是`str`
- `url`：搜索结果链接，类型为`str`

!!!note
    普通搜索结果没有一个父字典包围着，它的父字典就是返回值中的`results`字典

## 提醒

!!!warning
    不要使用爬虫搜索大量信息（如每天一万条），这样可能导致被百度封锁IP地址。使用IP池即可解决该问题
