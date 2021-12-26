# FAQ

FAQ，即`Frequently Asked Questions`，常见问题。这篇文档将会逐一解答这些问题。

## 技术方面

### 为什么有时候 BaiduSpider 会出现警告？

如果你遇到了类似于下面的警告[^1]：

<p style="color: #F3B319">WARNING: An error occurred while executing function BaiduSpider.parse-web, which is currently ignored. However, the rest of the parsing process is still being executed normally. This is most likely an inner parse failure of BaiduSpider. For more details, please set the environment variable `DEBUG` to `1` to see the error trace and open up a new issue at https://github.com/BaiduSpider/BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D.</p>

不要紧张，你的设备并没有出现任何问题，只是在数据的获取过程中出现了一点小差错。

（最难调试的 Bug 是不报错的 Bug，而不是抛出异常的 Bug）

注：如果你使用的是百度文库搜索，请先使用[特例](#特例文库搜索)进行验证，若仍然不能解决问题，再按照下述方法进行检查。

#### Why?

这是由于 BaiduSpider 内部解析出现错误导致的。抛出此异常的目的是为了在解析过程中不因为偶然出现的错误而导致整个程序终止。

但是，除了 BaiduSpider 内部解析出现错误以外，还有可能是用户请求过于频繁造成无法正常获取到百度网页造成的解析错误。

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

然后，重新运行你出错的那段程序。这次，由于是在`DEBUG`模式下进行，BaiduSpider 会直接抛出错误并终止程序运行。请仔细检查错误信息并确认是否为你的程序错误。

一般来讲，BaiduSpider 解析错误会是类似这样的：

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

如果你的报错是由`Requests`或其他请求包发出的，那么很有可能是你的程序请求次数过多导致 IP 被封禁，请自行解决或[设置Cookie](/guide/index.html#设置Cookie)以延缓封禁。

##### 特例：文库搜索

由于文库搜索的特殊侦测机制，每隔一段时间需要进行人工验证。如果文库搜索出现上述警告，请自行访问[文库搜索](https://wenku.baidu.com/search?word=placeholder&lm=0&od=0&fr=top_home&ie=utf-8)进行手动验证。

BaiduSpider 暂不考虑实现模拟人工验证。

#### Fix?

既然发现了问题，接下来就是解决问题。如果你是由于自身原因程序运行出错，请自行解决；如果是由于 IP 被封禁导致出错，可以参考[设置Cookie](/guide/index.html#设置Cookie)来延缓封禁；如果真的是 BaiduSpider 的内部问题，请[提出issue](https://github.com/BaiduSpider/BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D)，并附上错误详细信息和您的代码。

### 为什么我的 BaiduSpider 返回值都是字典？

这是由于你没有安装最新版本的 BaiduSpider。在较旧版本[^2]的 BaiduSpider 中，搜索函数的返回值都会以字典形式呈现，而非现在新版的返回结果类。

想要解决这个问题，请下载并安装[最新版的 BaiduSpider](https://pypi.org/project/BaiduSpider/)。

### 我爬取的数量太多，百度把我的IP封禁了怎么办？

请参考[设置 Cookie](/guide/index.html#设置Cookie) 来延缓封禁[^3]。

强烈不建议大量爬取百度内容，违者后果自负。BaiduSpider不为此承担任何法律责任。

## 文档方面

### 我发现有一篇文档写的不太详细怎么办？

首先，特别感谢你发现这个问题！你可以去 GitHub [报告这个问题](https://github.com/BaiduSpider/BaiduSpider/issues/new/choose)，或者直接提交一个 PR 来自己修复它！

在提交 Issue 或 PR 的时候，建议包含以下几点：

- 你发现的错误
- 你提出的意见
- 错误的位置
- 为什么你认为是错的
- ……

不管你选的是哪项，BaiduSpider 团队都会热烈欢迎！我们也将在第一时间回复你。

### 为什么每篇文档下面都有“评论”二字，但是却没有评论区？

由于我们使用的是国外的[Disqus](https://disqus.com/)评论系统，在国内可能会由于网络原因无法访问该站点，请自行解决。

## 贡献方面

### 我发现了一个 Bug / 有一个功能请求，我该如何让开发团队知道？

你可以[开启一个 Issue](https://github.com/BaiduSpider/BaiduSpider/issues/new/choose)来告诉我们，我们也会在第一时间回复你。

请提供关于你 Issue 的详细信息。

垃圾 Issue 将被直接关闭。

### 我自己做出了一个新功能 / 修复了一个bug，我怎么告知BaiduSpider成员？

最好的方式是在 GitHub 上提交一个 Pull Request，我们会第一时间审核并回复你的 PR。

此外，请详细描述你的 PR 做了哪些更改，实现了什么功能。

## 条例方面

### BaiduSpider 可以商用吗？

不可以。不仅如此，根据许可证规定，任何使用 BaiduSpider 的项目必须开源，不得闭源。

### 我可以使用 BaiduSpider 爬取大量数据吗？

不可以。虽然 BaiduSpider 提供这种爬虫，但是不代表你就能够爬取百度大量数据。BaiduSpider 的用途仅限学习与研究，违者后果自负。BaiduSpider 团队任何成员不承担因此而造成的任何法律责任。

### 我可以二次开发 BaiduSpider 吗？

当然可以。我们非常鼓励这种行为！但是，在您二次开发 BaiduSpider 的同时，请遵守许可证规定，保持项目开源且不可进行商用。


[^1]: BaiduSpider v0.1.5 之前的版本尚未添加错误处理。对于 v0.0.2 - v0.1.4 版本，所有错误将会直接弹出而非发出警告。如果需要使用错误处理或其他新功能，请升级BaiduSpider到[最新稳定版本](https://pypi.org/project/BaiduSpider/)。

[^2]: 确切的说，在 BaiduSpider v0.5 Preview 版本之前的 v0.x 版本都没有这一功能。但是，如果你想要使用字典类型的返回值也不必退回这些早期版本。每个返回类的`plain`成员变量都是这个类的字典或数组形式。详见[API文档](/api/baiduspider/models/web.html#baiduspider.models.web.WebNormal)。

[^3]: 虽然BaiduSpider提供这个功能，但仅供学习与研究使用。此外，这一功能并不保证能 100% 有效。
