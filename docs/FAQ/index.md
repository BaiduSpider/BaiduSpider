# FAQ

FAQ，即`Frequently Asked Questions`，经常被问到的问题。这篇文档将会逐一解答这些普遍的问题。

## 技术方面

### 为什么有时候BaiduSpider会出现警告？

如果你遇到了类似于下面这个警告[^1]：

<p style="color: #F3B319">WARNING: An error occurred while executing function BaiduSpider.parse-web, which is currently ignored. However, the rest of the parsing process is still being executed normally. This is most likely an inner parse failure of BaiduSpider. For more details, please set the environment variable `DEBUG` to `1` to see the error trace and open up a new issue at https://github.com/BaiduSpider/BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D.</p>

先不要慌张，你的程序没有把什么病毒激活了。让我们先来看看为什么会发出这个警告。

注：如果你使用的是百度文库搜索，请先按照[特例](#特例文库搜索)验证，若仍然不能解决问题，再按照下述方法进行检查。

#### Why?

这个警告是由于BaiduSpider内部解析出现错误才会触发的。目的在于循环搜集数据时，若有某个特定解析错误出现仅是跳过并发出警告，而非报错而终止整个程序。这也是BaiduSpider的内部保护机制。

但是，除了BaiduSpider内部解析出现错误以外，还有可能是用户请求次数过多造成无法正常请求到百度网页造成的请求错误。

#### How?

首先，我们需要确定是否为BaiduSpider内部解析错误。请在你的终端下输入以下命令：

=== "Linux / macOS"

    ```bash
    $ export DEBUG=1
    ```

=== "Windows"

    ```bash
    $ set DEBUG=1
    ```

然后，重新运行你出错的那段程序。这次，由于是在`DEBUG`模式下进行，BaiduSpider会直接弹出错误并终止程序运行。请仔细检查错误信息并确认是否为你的程序错误。

一般来讲，BaiduSpider解析错误会是类似这样的：

```py3tb
Traceback (most recent call last):
  File "d:\Develop\Python\BaiduSpider\exp.py", line 8, in <module>
    result = spider.search_web("南京疫情")
  File "d:\Develop\Python\BaiduSpider\baiduspider\__init__.py", line 408, in search_web
    self._handle_error(error, "BaiduSpider", "parse-web")
  File "d:\Develop\Python\BaiduSpider\baiduspider\_spider.py", line 87, in _handle_error
    raise err
  File "d:\Develop\Python\BaiduSpider\baiduspider\__init__.py", line 404, in search_web
    results = self.parser.parse_web(content, exclude=exclude)
  File "d:\Develop\Python\BaiduSpider\baiduspider\parser\__init__.py", line 47, in parse_web
    news_detail = self.webSubParser.parse_news_block(news)
  File "d:\Develop\Python\BaiduSpider\baiduspider\util.py", line 15, in wrapper
    raise err
  File "d:\Develop\Python\BaiduSpider\baiduspider\util.py", line 12, in wrapper
    return func(*args, **kwargs)
  File "d:\Develop\Python\BaiduSpider\baiduspider\parser\subparser.py", line 45, in parse_news_block
    row_time = self._format(row.find("div", class_="c-color-gray2").text)
AttributeError: 'NoneType' object has no attribute 'text'
```

如果你的报错是由`requests`或其他请求包发出的，那么很有可能是你的程序请求次数过多导致IP封禁，请自行解决或[设置Cookie](/guide/index.html#设置Cookie)以延缓封禁。

##### 特例：文库搜索

由于文库搜索的特殊侦测机制，每隔一段时间需要进行人工验证。如果文库搜索出现上述警告，请自行访问[文库搜索](https://wenku.baidu.com/search?word=placeholder&lm=0&od=0&fr=top_home&ie=utf-8)进行手动验证。

BaiduSpider暂不考虑实现模拟人工验证。

#### Fix?

既然发现了问题，接下来就是解决问题。如果你是由于自身原因程序运行出错，请自行解决；如果是由于IP被封禁问题出错，可以参考[设置Cookie](/guide/index.html#设置Cookie)来延缓封禁；如果真的是BaiduSpider的内部问题，我们也十分欢迎你[提出issue](https://github.com/BaiduSpider/BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D)，并提供关于错误的详细信息。

### 为什么我的BaiduSpider返回值都是个字典？

这是由于你没有安装最新版本的BaiduSpider。在较旧版本[^2]的BaiduSpider中，搜索函数的返回值都会以字典形式呈现，而非现在新版的返回结果类。

想要解决这个问题，请下载并安装[最新版的BaiduSpider](https://pypi.org/project/BaiduSpider/)。

### 我爬取的数量太多，百度把我的IP封禁了怎么办？

请参考[设置Cookie](/guide/index.html#设置Cookie)来延缓封禁[^3]。

强烈不建议大量爬取百度内容，违者后果自负。BaiduSpider不为此承担任何法律责任。

## 文档方面

### 我发现有一篇文档写的不太详细怎么办？

首先，特别感谢你发现这个问题！你可以去GitHub[报告这个问题](https://github.com/BaiduSpider/BaiduSpider/issues/new/choose)，或者直接干脆提交一个PR来自己修复它！

在提交issue或PR的时候，建议包含以下几点：

- 你发现的错误
- 你提出的意见
- 错误的位置
- 为什么你认为是错的
- ……

不管你选的是哪项，BaiduSpider团队都会激励欢迎！我们也会在第一时间回复你。

### 为什么每篇文档下面都有“评论”二字，但是却没有评论区？

由于我们使用的是国外的[Disqus](https://disqus.com/)评论系统，在国内可能会由于网络原因无法访问该站点。请自行解决。

## 贡献方面

### 我发现了一个bug / 有一个功能请求，我该如何上报？

你可以[开启一个issue](https://github.com/BaiduSpider/BaiduSpider/issues/new/choose)来告诉我们，我们也会在第一时间回复你。

请提供详细的关于你的issue的信息。

请勿发送垃圾issue。

### 我自己做出了一个新功能 / 修复了一个bug，我怎么告知BaiduSpider成员？

最好的方式是在GitHub上提交一个Pull Request，我们会第一时间审核并回复你的PR。

此外，请详细描述你的PR做了哪些更改，实现了什么目的。

## 条例方面

### BaiduSpider可以商用吗？

不可以。不仅如此，任何使用BaiduSpider的项目必须开源，不得闭源。

### 我可以使用BaiduSpider爬取大量数据吗？

不可以。虽然BaiduSpider提供这种爬虫，但是不代表你就能够爬取百度大量数据。BaiduSpider的用途仅限于学习与研究方面，违者后果自负。BaiduSpider团队任何成员都不承担任何法律责任。

### 我可以二次开发BaiduSpider吗？

当然可以。我们还极力欢迎这种社区行为！但是，在你二次开发BaiduSpider的同时，也必须开源你的项目并且不得商用。


[^1]: 在BaiduSpider v0.1.5之前的版本尚未添加错误处理。对于v0.0.2 ~ v0.1.4版本，所有错误将会直接弹出而非发出警告。如果需要使用错误处理或其他新功能，请升级BaiduSpider到[最新稳定版本](https://pypi.org/project/BaiduSpider/)。

[^2]: 确切的说，在BaiduSpider v0.5 Preview版本之前的v0.x版本都没有这一功能。但是，如果你想要使用字典类型的返回值也不必退回这些早期版本。每个返回类的`plain`成员变量都是这个类的字典或数组形式。详见[API文档](/api/baiduspider/models/web.html#baiduspider.models.web.WebNormal)。

[^3]: 虽然BaiduSpider提供这个功能，但仅供学习与研究使用。此外，这一功能并不保证能100%有效。
