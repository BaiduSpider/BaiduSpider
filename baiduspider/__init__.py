"""BaiduSpider，一个爬取百度的利器.

:Author: Sam Zhang

:Licence: GPL_V3

:GitHub: https://github.com/BaiduSpider/BaiduSpider
"""
import datetime
import hashlib
import random
import time as time_lib
from typing import Dict, Tuple, Union
from urllib.parse import quote

from baiduspider._spider import BaseSpider
from baiduspider.models.baike import BaikeResult
from baiduspider.models.jingyan import JingyanResult
from baiduspider.models.news import NewsResult
from baiduspider.models.pic import PicResult
from baiduspider.models.video import VideoResult
from baiduspider.models.web import WebResult
from baiduspider.models.wenku import WenkuResult
from baiduspider.models.zhidao import ZhidaoResult
from baiduspider.parser import Parser

__all__ = ["BaiduSpider"]


class BaiduSpider(BaseSpider):
    """爬取百度的搜索结果.

    本类的所有成员方法都遵循下列格式：

        {
            'results': <一个列表，表示搜索结果，内部的字典会因为不同的成员方法而改变>,
            'total': <一个正整数，表示搜索结果的最大页数，可能会因为搜索结果页码的变化而变化，因为百度不提供总共的搜索结果页数>
        }

    目前支持百度搜索，百度图片，百度知道，百度视频，百度资讯，百度文库，百度经验和百度百科，并且返回的搜索结果无广告。继承自``BaseSpider``。

    - BaiduSpider.`#!python search_web(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        exclude: list = [],
        time: Union[tuple, str, None] = None,
        proxies: Dict = None
    ) -> WebResult`: 百度网页搜索

    - BaiduSpider.`#!python search_pic(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        proxies: Dict = None
    ) -> PicResult`: 百度图片搜索

    - BaiduSpider.`#!python search_zhidao(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        time: Union[str, None] = None,
        proxies: Dict = None
    ) -> ZhidaoResult`: 百度知道搜索

    - BaiduSpider.`#!python search_video(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        proxies: Dict = None
    ) -> VideoResult`: 百度视频搜索

    - BaiduSpider.`#!python search_news(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        sort_by: str = "focus",
        show: str = "all",
        proxies: Dict = None
    ) -> NewsResult`: 百度资讯搜索

    - BaiduSpider.`#!python search_wenku(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        scope: str = "all",
        format: str = "all",
        time: str = "all",
        page_range: Union[Tuple[int], str] = "all",
        sort_by: str = "relation",
        proxies: Dict = None
    ) -> WenkuResult`: 百度文库搜索

    - BaiduSpider.`#!python search_jingyan(
        self: BaiduSpider,
        query: str,
        pn: int = 1,
        scope: str = "all",
        proxies: Dict = None
    ) -> JingyanResult`: 百度经验搜索

    - BaiduSpider.`#!python search_baike(
        self: BaiduSpider,
        query: str,
        proxies: Dict = None
    )`: 百度百科搜索
    """

    def __init__(self, cookie: str = None) -> None:
        """初始化BaiduSpider.

        - 设置Cookie：
            ```python
            spider = BaiduSpider(cookie="你的cookie")
            ```
            Cookie可以被用于增强爬虫的真实性，尽可能使百度减少封禁IP的最大限制。

            如果你想获取你的Cookie，请打开<https://www.baidu.com/s?wd=placeholder&pn=0>，并
            按F12打开开发者工具，然后在开发者工具最上方的选项栏中选择“网络”（Network）这一选项，点击
            出现的列表中最上方的以`s?wd=placeholder`开头的选项，在出现的详情中找到`Request Headers`
            一项，然后在它的下方找到`Cookie`，并复制Cookie这一选项内（不包括`Cookie: `）后面的所有内容，
            并将它粘贴在你需要的位置。

            请勿传入非法的Cookie。

        Args:
            cookie (Union[str, None], optional): 浏览器抓包得到的cookie. Defaults to None.
        """
        super().__init__()
        # 爬虫名称（不是请求的，只是用来标识）
        self.spider_name = "BaiduSpider"
        # 解析Cookie
        if cookie:
            if "__yjs_duid" not in cookie:
                cookie += "; __yjs_duid=1_" + str(hashlib.md5().hexdigest()) + "; "
            else:
                _ = cookie.split("__yjs_duid=")
                __ = _[1].split(";", 1)[-1]
                ___ = hashlib.md5()
                cookie = _[0] + "__yjs_duid=1_" + str(___.hexdigest()) + "; " + __
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "Referer": "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&ch=&tn=baiduhome_pg&bar=&wd=123&oq=123&rsv_pq=896f886f000184f4&rsv_t=fdd2CqgBgjaepxfhicpCfrqeWVSXu9DOQY5WyyWqQYmsKOC%2Fl286S248elzxl%2BJhOKe2&rqlang=cn",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Sec-Fetch-Mode": "navigate",
            "Cookie": cookie,
            "Connection": "Keep-Alive",
        }
        self.parser = Parser()
        self.EMPTY = {"results": [], "pages": 0, "total": 0}
        self.RESULTS_PER_PAGE = {
            "web": 10,
            "pic": 20,
            "zhidao": 10,
            "news": 10,
            "jingyan": 10,
        }

    def search_web(
        self,
        query: str,
        pn: int = 1,
        exclude: list = [],
        time: Union[tuple, str, None] = None,
        proxies: Dict = None,
    ) -> WebResult:
        """百度网页搜索。

        - 简单搜索：
            ```python
            BaiduSpider().search_web('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'result': int,  # 总计搜索结果数,
                        'type': 'total'  # type用来区分不同类别的搜索结果
                    },
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
                    {
                        'process': str,  # 算数过程
                        'result': str,  # 运算结果
                        'type': 'calc'
                        # 这类搜索结果仅会在搜索词涉及运算时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'results': [
                            {
                                'author': str,  # 新闻来源
                                'time': str,  # 新闻发布时间
                                'title': str,  # 新闻标题
                                'url': str,  # 新闻链接
                                'des': str,  # 新闻简介，大部分情况为None
                            },
                            { ... },
                            { ... },
                            { ... },
                            ...
                        ],
                        'type': 'news'
                        # 这类搜索结果仅会在搜索词有相关新闻时出现，不一定每个搜索结果都会出现的
                    },
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
                        # 这类搜索结果仅会在搜索词有相关视频时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                            'cover': str,  # 百科封面图片/视频链接
                            'cover-type': str,  # 百科封面类别，图片是image，视频是video
                            'des': str,  # 百科简介
                            'title': str,  # 百科标题
                            'url': str,  # 百科链接
                        },
                        'type': 'baike'
                        # 这类搜索结果仅会在搜索词有相关百科时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                            'cover': str,  # 贴吧封面图片链接
                            'des': str,  # 贴吧简介
                            'title': str,  # 贴吧标题
                            'url': str,  # 贴吧链接
                            'followers': str,  # 贴吧关注人数（可能有汉字，如：1万）
                            'hot': [{  # list, 热门帖子
                                'clicks': str,  # 帖子点击总数
                                'replies': str,  # 帖子回复总数
                                'title': str,  # 帖子标题
                                'url': str,  # 帖子链接
                            }],
                            'total': str,  # 贴吧总帖子数（可能有汉字，如：17万）'
                        },
                        'type': 'tieba'
                        # 这类搜索结果仅会在搜索词有相关贴吧时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                            'blogs': [{  # list, 博客列表
                                'des': str,  # 博客简介，没有时为`None`
                                'origin': str,  # 博客来源
                                'tags': [  # list, 博客标签
                                    str,  # 标签文字
                                ],
                                'title': str,  # 博客标题
                                'url': str,  # 博客链接
                            }],
                            'title': str,  # 博客搜索标题
                            'url': str,  # 博客搜索链接 (https://kaifa.baidu.com)
                        },
                        'type': 'blog'
                        # 这类搜索结果仅会在搜索词有相关博客时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                            'title': str,  # 仓库标题
                            'des': str,  # 仓库简介
                            'url': str,  # 仓库链接
                            'star': int,  # 仓库star数
                            'fork': int,  # 仓库fork数
                            'watch': int,  # 仓库watch数
                            'license': str,  # 仓库版权协议
                            'lang': str,  # 仓库使用的编程语言
                            'status': str,  # 仓库状态图表链接
                        },
                        'type': 'gitee'
                        # 这类搜索结果仅会在搜索词有相关代码仓库时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                            {
                                'songs': [{  # list, 歌曲信息
                                    'album': {  # Dict, 歌曲专辑
                                        'name': str,  # 专辑名称
                                        'url': str,  # 专辑链接
                                    },
                                    'singer': [{  # list, 歌手信息
                                        'name': str,  # 歌手名称
                                        'url': str,  # 歌手链接
                                    }],
                                    'song': {  # Dict, 歌曲信息
                                        'copyright': bool,  # 歌曲是否有版权
                                        'duration': datetime.time,  # 歌曲时长
                                        'is_original': bool,  # 歌曲是否为原唱
                                        'labels': List[str],  # 歌曲标签
                                        'name': str,  # 歌曲名称
                                        'other_sites: List[str],  # 歌曲在其他网站发布的链接
                                        'poster': str,  # 歌曲海报图片链接
                                        'pub_company': str,  # 歌曲发行公司名称
                                        'pub_date': datetome.datetime,  # 歌曲发行时间
                                        'site': str,  # 歌曲发布网站名称（拼音）
                                        'url': str  # 歌曲链接
                                    }
                                }],
                                'title': str,  # 音乐标题
                                'url': str  # 音乐链接
                            }
                        },
                        'type': 'music'
                        # 这类搜索结果仅会在搜索词有相关音乐时出现，不一定每个搜索结果都会出现的
                    }
                    {
                        'des': str,  # 搜索结果简介
                        'origin': str,  # 搜索结果的来源，可能是域名，也可能是名称
                        'time': str,  # 搜索结果的发布时间
                        'title': str,  # 搜索结果标题
                        'type': 'result,  # 正经的搜索结果
                        'url': str  # 搜索结果链接
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 总计的搜索结果页数，可能会因为当前页数的变化而随之变化
            }
            ```

        - 带页码：
            ```python
            BaiduSpider().search_web('搜索词', pn=2)
            ```

        - 按需解析：
            ```python
            BaiduSpider().search_web('搜索词', exclude=['要屏蔽的子部件列表'])
            ```
            可选值：`['news', 'video', 'baike', 'tieba', 'blog', 'gitee', 'related', 'calc', 'music']`，
            分别表示：资讯，视频，百科，贴吧，博客，Gitee代码仓库，相关搜索，计算。
            当`exclude=['all']`时，将仅保留基本搜索结果和搜索结果总数。
            如果`all`在`exclude`列表里，则将忽略列表中的剩余部件，返回`exclude=['all']`时的结果。

        - 按时间筛选：
            ```python
            BaiduSpider().search_web('搜索词', time=(开始时间, 结束时间))
            ```
            其中，开始时间和结束时间均为datetime.datetime类型，或者是使用time.time()函数生成的时间戳。
            time参数也可以是以下任意一个字符串：`['day', 'week', 'month', 'year']`。它们分别表示：一天内、
            一周内、一月内、一年内。当`time`为`None`时，BaiduSpider将展示全部结果，忽略筛选。
            如果参数非法，BaiduSpider会忽略此次筛选。

        - 设置代理：
            ```python
            BaiduSpider().search_web('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要爬取的搜索词.
            pn (int, optional): 爬取的页码. Defaults to 1.
            exclude (list, optional): 要屏蔽的控件. Defaults to [].
            time (Union[tuple, str, None]): 按时间筛选参数. Defaults to None.
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            WebResult: 爬取的返回值和搜索结果
        """
        error = None
        # 按需解析
        if "all" in exclude:
            exclude = [
                "news",
                "video",
                "baike",
                "tieba",
                "blog",
                "gitee",
                "calc",
                "related",
                "music",
            ]
        # 按时间筛选
        if type(time) == str:
            to = datetime.datetime.now()
            from_ = datetime.datetime(
                to.year, to.month, to.day, to.hour, to.minute, to.second, to.microsecond
            )
            time_str_to_timedelta = {
                "day": datetime.timedelta(days=-1),
                "week": datetime.timedelta(days=-7),
                "month": datetime.timedelta(days=-31),
                "year": datetime.timedelta(days=-365),
            }
            from_ = time_str_to_timedelta[time]

        elif type(time) == tuple or type(time) == list:
            from_ = time[0]
            to = time[1]
        else:
            to = from_ = None
        if type(to) == datetime.datetime and type(from_) == datetime.datetime:
            FORMAT = r"%Y-%m-%d %H:%M:%S"
            to = int(time_lib.mktime(time_lib.strptime(to.strftime(FORMAT), FORMAT)))
            from_ = int(
                time_lib.mktime(time_lib.strptime(from_.strftime(FORMAT), FORMAT))
            )
        try:
            text = quote(query, "utf-8")
            url = f"https://www.baidu.com/s?wd={text}&pn={(pn - 1) * 10}&inputT={random.randint(500, 4000)}"
            if all((to, from_)):
                url += "&gpc=" + quote(f"stf={from_},{to}|stftype=2")
            # 解析Cookie
            cookie = self.headers["Cookie"]
            if cookie:
                if "__yjs_duid" not in cookie:
                    pass
                else:
                    _ = cookie.split("__yjs_duid=")
                    __ = _[1].split(";", 1)[-1]
                    ___ = hashlib.md5()
                    cookie = _[0] + "__yjs_duid=1_" + str(___.hexdigest()) + __
            self.headers["Cookie"] = cookie
            content = self._get_response(url, proxies)
            results = self.parser.parse_web(content, exclude=exclude)
        except Exception as err:
            error = err
        finally:
            self._handle_error(error, "BaiduSpider", "parse-web")
        pages = self._calc_pages(results["total"], self.RESULTS_PER_PAGE["web"])
        return WebResult._build_instance(
            plain=results["results"], pages=pages, total=results["total"]
        )

    def search_pic(self, query: str, pn: int = 1, proxies: Dict = None) -> PicResult:
        """百度图片搜索。

        - 实例：
            ```python
            BaiduSpider().search_pic('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'host': str,  # 图片来源域名
                        'title': str,  # 图片标题
                        'url': str,  # 图片链接
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 搜索结果总计页码，可能会变化
            }
            ```

        - 带页码的搜索：
            ```python
            BaiduSpider().search_pic('搜索词', pn=2)
            ```

        - 设置代理：
            ```python
            BaiduSpider().search_pic('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要爬取的query
            pn (int, optional): 爬取的页码. Defaults to 1.
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            PicResult: 爬取的搜索结果
        """
        error = None
        result = self.EMPTY
        try:
            url = "http://image.baidu.com/search/flip?tn=baiduimage&word=%s&pn=%d" % (
                quote(query),
                (pn - 1) * 20,
            )
            content = self._get_response(url, proxies)
            result = self.parser.parse_pic(content)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            self._handle_error(error)
        pages = self._calc_pages(result["total"], self.RESULTS_PER_PAGE["pic"])
        return PicResult._build_instance(
            plain=result["results"], pages=pages, total=result["total"]
        )

    def search_zhidao(
        self,
        query: str,
        pn: int = 1,
        time: Union[str, None] = None,
        proxies: Dict = None,
    ) -> ZhidaoResult:
        """百度知道搜索。

        - 普通搜索：
            ```python
            BaiduSpider().search_zhidao('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'count': int,  # 回答总数
                        'date': str,  # 回答发布日期
                        'question': str,  # 问题简介
                        'answer': str,  # 回答简介
                        'agree': int,  # 回答赞同数
                        'answerer': str,  # 回答者
                        'title': str,  # 问题标题
                        'url': str  # 问题链接
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 搜索结果最大页数，可能会变化
            }
            ```

        - 带页码的搜索：
            ```python
            BaiduSpider().search_zhidao('搜索词', pn=2)
            ```

        - 按时间筛选：
            ```python
            BaiduSpider().search_zhidao('搜索词', time='时间范围')
            ```
            其中，time参数可以是以下任意一个字符串：['week', 'month', 'year']。它们分别表示：一周内、一月内、
            一年内。当`time`为`None`时，BaiduSpider将展示全部结果，忽略筛选。
            如果参数非法，BaiduSpider会忽略此次筛选。

        - 设置代理：
            ```python
            BaiduSpider().search_zhidao('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索结果的页码. Defaults to 1.
            time (Union[str, None], optional): 时间筛选参数. Defaults to None.
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            Dict: 搜索结果以及总页码
        """
        error = None
        result = self.EMPTY
        _ = [None, None, "week", "month", "year"]
        if _.index(time) > 0:
            time = _.index(time)
        else:
            time = 0
        try:
            url = (
                "https://zhidao.baidu.com/search?lm=0&rn=10&fr=search&pn=%d&word=%s&date=%d"
                % ((pn - 1) * 10, quote(query), time)
            )
            code = self._get_response(url, proxies, "gb2312")
            # 转化编码
            # source.encoding = "gb2312"
            # code = source.text
            result = self.parser.parse_zhidao(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        pages = self._calc_pages(result["total"], self.RESULTS_PER_PAGE["zhidao"])
        return ZhidaoResult._build_instance(result["results"], pages, result["total"])

    def search_video(
        self, query: str, pn: int = 1, proxies: Dict = None
    ) -> VideoResult:
        """百度视频搜索。

        - 普通搜索：
            ```python
            BaiduSpider().search_video('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'img': str,  # 视频封面图片链接
                        'time': str,  # 视频时长
                        'title': str,  # 视频标题
                        'url': str  # 视频链接
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                'pages': int  # 搜索结果最大页数，可能因搜索页数改变而改变
            }
            ```

        - 带页码：
            ```python
            BaiduSpider().search_video('搜索词', pn=2)
            ```

        - 设置代理：
            ```python
            BaiduSpider().search_video('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索结果的页码. Defaults to 1.
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            VideoResult: 爬取的搜索结果
        """
        error = None
        result = self.EMPTY
        try:
            url = f"https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&wd={quote(query)}&pn={(pn - 1) * 10}&async=1"
            # 获取源码
            code = self._get_response(url, proxies)
            result = self.parser.parse_video(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        return VideoResult._build_instance(result["results"])

    def search_news(
        self,
        query: str,
        pn: int = 1,
        sort_by: str = "focus",
        show: str = "all",
        proxies: Dict = None,
    ) -> NewsResult:
        """百度资讯搜索。

        - 获取资讯搜索结果：
            ```python
            BaiduSpider().search_news('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'author': str,  # 资讯来源（作者）
                        'date': str,  # 资讯发布时间
                        'des': str,  # 资讯简介
                        'title': str,  # 资讯标题
                        'url': str  # 资讯链接
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 搜索结果最大页码，可能会因为当前页数变化而变化
            }
            ```

        - 带页码：
            ```python
            BaiduSpider().search_news('搜索词', pn=2)
            ```

        - 排序方式：
            目前支持两种排序方式：按焦点排序（默认）和按时间排序。可以通过设置`sort_by`参数来设置排序方式。`sort_by`
            参数只支持两种值：`focus`（按焦点排序，默认值）和`time`（按时间排序）。样例：
            ```python
            BaiduSpider().search_news('搜索词', sort_by='time')  # 按时间排序
            ```

        - 筛选：
            你可以通过设置`show`参数设置要筛选显示的资讯来源。目前支持三种来源：`all`（全部显示，默认）、`media`（媒体）
            和`baijiahao`（百家号）。样例：
            ```python
            BaiduSpider().search_news('搜索词', show='media')  # 仅显示来自媒体的新闻结果
            ```

        - 设置代理：
            ```python
            BaiduSpider().search_news('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 搜索query
            pn (int, optional): 搜索结果的页码. Defaults to 1.
            sort_by (str, optional): 搜索结果排序方式. Defaults to "focus".
            show (str, optional): 搜索结果筛选方式. Defaults to "all".
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            NewsResult: 爬取的搜索结果与总页码。
        """
        error = None
        result = self.EMPTY
        try:
            if sort_by == "time":
                sort_by = 4
            else:
                sort_by = 1
            if show == "media":
                show = 1
            elif show == "baijiahao":
                show = 2
            else:
                show = 0
            url = f"https://www.baidu.com/s?tn=news&wd={quote(query)}&pn={(pn - 1) * 10}&rtt={sort_by}&medium={show}&cl=2"
            # 源码
            code = self._get_response(url, proxies)
            result = self.parser.parse_news(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        pages = self._calc_pages(result["total"], self.RESULTS_PER_PAGE["news"])
        return NewsResult._build_instance(result["results"], pages, result["total"])

    def search_wenku(
        self,
        query: str,
        pn: int = 1,
        scope: str = "all",
        format: str = "all",
        time: str = "all",
        page_range: Union[Tuple[int, int], str] = "all",
        sort_by: str = "relation",
        proxies: Dict = None,
    ) -> WenkuResult:
        """百度文库搜索。

        请注意，目前百度文库搜索若报错，则可能需要先手动打开百度文库搜索
        （`https://wenku.baidu.com/search?word=placeholder&lm=0&od=0&fr=top_home&ie=utf-8`）
        通过安全验证后才能正常搜索。

        - 普通搜索：
            ```python
            BaiduSpider().search_wenku('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'pub_date': str,  # 文档发布日期
                        'des': str,  # 文档简介
                        'downloads': int,  # 文档下载量
                        'pages': int,  # 文档页数
                        'title': str,  # 文档标题
                        'type': str,  # 文档格式，为全部大写字母
                        'url': str,  # 文档链接
                        'quality': float,  # 文档质量分
                        'uploader': {  # Dict, 文档上传者信息
                            'name': str,  # 文档上传者用户名
                            'url': str  # 文档上传者链接
                        },
                        'is_vip': bool  # 该文档是否需要VIP权限下载
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 总计搜索结果的页数
            }
            ```

        - 带页码的搜索：
            ```python
            BaiduSpider().search_wenku('搜索词', pn=2)
            ```

        - 筛选范围：
            BaiduSpider支持五种筛选范围：全部、VIP专享、VIP免费、免费、精品。你可以使用`scope`参数来定义此次搜索
            范围。`scope`参数的取值可以是下列任一一项：['all', 'vip-only', 'vip-free', 'free', 'high-quality']。
            他们的含义与上文所述一致。样例：
            ```python
            BaiduSpider().search_wenku('搜索词', scope='free')  # 仅显示免费的文档
            ```
            若`scope`参数非法，BaiduSpider将忽略此次筛选。

        - 格式筛选：
            BaiduSpider支持六种格式筛选。你可以通过设置`format`参数来设置需要筛选的格式。`format`参数取值可以是：
            `all`（全部）、`doc`（DOC文档）、`ppt`（幻灯片文档）、`txt`（纯文本文档）、`pdf`（PDF文档）、`xls`
            （Excel表格文档）。例如：
            ```python
            BaiduSpider().search_wenku('搜索词', format='ppt')  # 仅显示幻灯片文档
            ```
            若`format`参数非法，BaiduSpider将忽略此次筛选。

        - 按时间筛选：
            BaiduSpider提供百度文科搜索的按时间筛选。`time`参数接受的合法传参如下：['all', 'this-year', 'last-year',
            'previous-years']。他们分别表示全部、今年、去年和前年及以前。示例：
            ```python
            BaiduSpider().search_wenku('搜索词', time='last-year')  # 仅显示去年上传的文档
            ```
            若`time`参数非法，BaiduSpider将忽略此次筛选。

        - 按页数筛选：
            BaiduSpider提供使用页数筛选文档，参数为`page_range`。`page_range`可选值为：['all', Tuple[start: int, end: int]]。
            分别表示全部和Tuple[开始页码(`int`), 结束页码(`int`)]。样例：
            ```python
            BaiduSpider().search_wenku('搜索词', page_range=(0, 10))  # 仅显示页数为0 - 10页的文档
            ```
            若`page_range`参数非法，BaiduSpider将忽略此次筛选。

        - 搜索结果排序：
            BaiduSpider提供由百度文库内置的搜索结果排序。你可以通过设置`sort_by`参数来设置排序方式，默认为按相关性排序。`sort_by`可选值为：
            ['relation', 'time', 'downloads', 'score']，分别表示按相关性、按时间、按下载量和按评分排序。样例：
            ```python
            BaiduSpider().search_wenku('搜索词', sort_by='downloads')  # 按下载量排序
            ```
            若`sort_by`参数非法，BaiduSpider将忽略此次筛选。

        - 设置代理：
            ```python
            BaiduSpider().search_wenku('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索的页码. Defaults to 1.
            scope (str, optional): 按范围筛选. Defaults to "all".
            format (str, optional): 按格式筛选. Defaults to "all".
            time (str, optional): 按时间筛选. Defaults to "all".
            page_range (Union[str, Tuple[int]]): 按页数筛选. Defaults to "all".
            sort_by (str): 排序方式. Defaults to "relation".
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            WenkuResult: 搜索结果和总计页数
        """
        error = None
        result = self.EMPTY
        # 范围筛选
        _ = ["all", "vip-only", "vip", "free", "high-quality"]
        if _.index(scope) > 0:
            scope = _.index(scope)
        else:
            scope = 0
        # 格式筛选
        _ = ["all", "doc", "pdf", "ppt", "xls", "txt"]
        if _.index(format) > 0:
            format = _.index(format)
        else:
            format = 0
        # 按时间筛选
        _ = ["all", "this-year", "last-year", "previous-years"]
        if _.index(time) > 0:
            time = _.index(time)
        else:
            time = 0
        # 按页数筛选
        if (
            type(page_range) is tuple
            and len(page_range) == 2
            and type(page_range[0]) is int
            and type(page_range[1]) is int
        ):
            pass
        else:
            page_range = -1
        # 排序方式
        _ = ["relation", "time", "downloads", "score"]
        if _.index(sort_by) > 0:
            sort_by = _.index(sort_by)
        else:
            sort_by = 0
        try:
            url = (
                "https://wenku.baidu.com/gsearch/search/pcsearch?word=%s&pn=%d&fr=top_home&fd=%d&lm=%d&pt=%d&od=%d"
                % (quote(query), (pn - 1) * 10, scope, format, time, sort_by)
            )
            if page_range != -1:
                url += f"&pb={page_range[0]}&pe={page_range[1]}"
            else:
                url += "&pg=0"
            code = self._get_response(url, proxies)
            result = self.parser.parse_wenku(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        return WenkuResult._build_instance(result["results"], result["pages"])

    def search_jingyan(
        self, query: str, pn: int = 1, scope: str = "all", proxies: Dict = None
    ) -> JingyanResult:
        """百度经验搜索。

        - 例如：
            ```python
            BaiduSpider().search_jingyan('关键词')
            ```
            `plain`返回值：
            ```python
            {
                'results': [
                    {
                        'title': str,  # 经验标题
                        'url': str,  # 经验链接
                        'des': str,  # 经验简介
                        'date': str,  # 经验发布日期
                        'category': List[str],  # 经验分类
                        'votes': int,  # 经验的支持票数
                        'publisher': {  # Dict, 经验发布者信息
                            'name': str,  # 经验发布者用户名
                            'url': str  # 经验发布者链接
                        },
                        'is_original': bool,  # 经验是否为原创
                        'is_outstanding': bool  # 经验是否为优秀经验
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'pages': int  # 总计搜索结果页数
            }
            ```

        - 带页码的：
            ```python
            BaiduSpider().search_jingyan('搜索词', pn=2)
            ```

        - 筛选经验：
            你可以通过设置`scope`参数来设定筛选范围。`scope`参数的可选值为：["all", "outstanding", "praise", "original"]。
            它们分别表示：全部经验、优秀经验、最受好评和原创经验。例子：
            ```python
            BaiduSpider().search_jingyan('搜索词', scope="outstanding")  # 仅显示优秀经验
            ```

        - 设置代理：
            ```python
            BaiduSpider().search_jingyan('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要搜索的关键词
            pn (int, optional): 搜索结果的页码. Defaults to 1.
            scope (str, optional): 筛选范围. Defaults to "all".
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            JingyanResult: 搜索结果以及总计的页码.
        """
        error = None
        result = self.EMPTY
        _ = ["all", "outstanding", "praise", "original"]
        if _.index(scope) > 0:
            scope = _.index(scope)
        else:
            scope = 0
        try:
            url = f"https://jingyan.baidu.com/search?word={quote(query)}&pn={(pn - 1) * 10}&lm={scope}"
            code = self._get_response(url, proxies)
            result = self.parser.parse_jingyan(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        pages = self._calc_pages(result["total"], self.RESULTS_PER_PAGE["jingyan"])
        return JingyanResult._build_instance(result["results"], pages, result["total"])

    def search_baike(self, query: str, proxies: Dict = None) -> BaikeResult:
        """百度百科搜索。

        - 使用方法：
            ```python
            BaiduSpider().search_baike('搜索词')
            ```
            `plain`返回值：
            ```python
            {
                'results': {
                    [
                        'title': str,  # 百科标题
                        'des': str,  # 百科简介
                        'date': str,  # 百科最后更新时间
                        'url': str  # 百科链接
                    ],
                    [ ... ],
                    [ ... ],
                    [ ... ]
                },
                'total': int  # 搜索结果总数
            }
            ```

        - 设置代理：
            ```python
            BaiduSpider().search_baike('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要搜索的关键词.
            proxies (Union[Dict, None]): 代理配置. Defaults to None.

        Returns:
            Dict: 搜索结果和总页数
        """
        error = None
        result = self.EMPTY
        try:
            url = f"https://baike.baidu.com/search?word={quote(query)}"
            code = self._get_response(url, proxies)
            result = self.parser.parse_baike(code)
            result = result if result else self.EMPTY
        except Exception as err:
            error = err
        finally:
            if error:
                self._handle_error(error)
        return BaikeResult._build_instance(result["results"], result["total"])
