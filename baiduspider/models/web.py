"""网页搜索返回值模型模块

此文件定义的所有现有的网页搜索返回值模型并编写了自动构建函数。
"""
from typing import Any

from baiduspider.models import convert_time, get_attr
from baiduspider.models.typings.typings_web import *


class WebNormal(WebNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider网页搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        origin (str): 搜索结果来源
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        time (datetime): 搜索结果发布时间
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.des = ""
        self.origin = ""
        self.title = ""
        self.url = ""
        self.time = None
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebNormal:
        __returns = WebNormal()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.origin = get_attr(plain, "origin")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.time = convert_time(get_attr(plain, "time"))
        return __returns


class WebCalc(WebCalc):
    """计算搜索结果模型

    这是一个遵照BaiduSpider网页搜索计算搜索结果结果模型创建的返回模型类。

    Attributes:
        process (str): 计算过程，如：12 + 21
        result (str): 计算结果，由于可能是`1e6`这样的形式，所以类型为`str`
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.process = ""
        self.result = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebCalc:
        __returns = WebCalc()
        __returns.plain = plain
        __returns.process = get_attr(plain, "process")
        __returns.result = int(get_attr(plain, "result"))
        return __returns


class WebNews(WebNews):
    """资讯搜索结果模型

    这是一个遵照BaiduSpider网页搜索资讯搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 资讯作者（来源）
        time (datetime): 资讯发布时间
        url (str): 资讯链接
        des (str): 资讯简介
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.author = ""
        self.time = None
        self.url = ""
        self.des = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebNews:
        __returns = WebNews()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.time = convert_time(get_attr(plain, "time"))
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.des = get_attr(plain, "des")
        return __returns


class WebVideo(WebVideo):
    """视频搜索结果模型

    这是一个遵照BaiduSpider网页搜索视频搜索结果结果模型创建的返回模型类。

    Attributes:
        cover (str): 视频封面图片链接
        origin (str): 视频来源
        length (str): 视频时长
        title (str): 视频标题
        url (str): 视频链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover = ""
        self.origin = ""
        self.length = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebVideo:
        __returns = WebVideo()
        __returns.plain = plain
        __returns.cover = get_attr(plain, "cover")
        __returns.origin = get_attr(plain, "origin")
        __returns.length = get_attr(plain, "length")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebBaike(WebBaike):
    """百科搜索结果模型

    这是一个遵照BaiduSpider网页搜索百科搜索结果结果模型创建的返回模型类。

    Attributes:
        cover (str): 百科封面图片（视频）链接
        cover_type (str): 百科封面类型，图片时为"image"，视频时为"video"
        des (str): 百科简介
        title (str): 百科标题
        url (str): 百科链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover = ""
        self.cover_type = ""
        self.des = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebBaike:
        __returns = WebBaike()
        __returns.plain = plain
        __returns.cover = get_attr(plain, "cover")
        __returns.cover_type = get_attr(plain, "cover-type")
        __returns.des = get_attr(plain, "des")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebTiebaHot(WebTiebaHot):
    """贴吧热门搜索结果模型

    这是一个遵照BaiduSpider网页搜索贴吧热门搜索结果结果模型创建的返回模型类。

    Attributes:
        clicks (str): 帖子点击次数，可能会有形如`1万`的结果，故类型为`str`
        replies (str): 帖子回复次数，可能会有形如`1万`的结果，故类型为`str`
        title (str): 帖子标题
        url (str): 帖子链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.clicks = ""
        self.replies = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebTiebaHot:
        __returns = WebTiebaHot()
        __returns.plain = plain
        __returns.clicks = get_attr(plain, "clicks")
        __returns.replies = get_attr(plain, "replies")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebTieba(WebTieba):
    """贴吧搜索结果模型

    这是一个遵照BaiduSpider网页搜索贴吧搜索结果结果模型创建的返回模型类。

    Attributes:
        cover (str): 贴吧封面图片链接
        des (str): 贴吧简介
        title (str): 贴吧标题
        followers (str): 贴吧关注人数，可能会有形如`1万`的结果，故类型为`str`
        total (str): 贴吧总帖子数，可能会有形如`1万`的结果，故类型为`str`
        hot (List[WebTiebaHot]): 贴吧热门帖子
        url (str): 贴吧链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover = ""
        self.des = ""
        self.title = ""
        self.followers = ""
        self.total = ""
        self.url = ""
        self.hot = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebTieba:
        __returns = WebTieba()
        __returns.plain = plain
        __returns.cover = get_attr(plain, "cover")
        __returns.des = get_attr(plain, "des")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.followers = get_attr(plain, "followers")
        __returns.total = get_attr(plain, "total")
        __returns.url = get_attr(plain, "url")
        for i in get_attr(plain, "hot"):
            __returns.hot.append(WebTiebaHot._build_instance(i))
        return __returns


class WebBlogDetail(WebBlogDetail):
    """博客详情搜索结果模型

    这是一个遵照BaiduSpider网页搜索博客详情搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 博客标题
        url (str): 博客链接
        des (str): 博客简介
        origin (str): 博客来源（作者）
        tags (List[str]): 博客标签
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.url = ""
        self.des = ""
        self.origin = ""
        self.tags = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebBlogDetail:
        __returns = WebBlogDetail()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.origin = get_attr(plain, "origin")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        for i in get_attr(plain, "tags"):
            __returns.tags.append(i)
        return __returns


class WebBlog(WebBlog):
    """博客搜索结果模型

    这是一个遵照BaiduSpider网页搜索博客搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 博客搜索结果标题
        url (str): 博客搜索结果链接
        blogs (List[WebBlogDetail]): 博客详情列表
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.title = ""
        self.url = ""
        self.blogs = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebBlog:
        __returns = WebBlog()
        __returns.plain = plain
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        for i in get_attr(plain, "blogs"):
            __returns.blogs.append(WebBlogDetail._build_instance(i))
        return __returns


class WebGitee(WebGitee):
    """Gitee仓库搜索结果模型

    这是一个遵照BaiduSpider网页搜索Gitee仓库搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 仓库标题
        des (str): 仓库简介
        url (str): 仓库链接
        star (int): 仓库star数
        fork (int): 仓库fork数
        watch (int): 仓库watch数
        license (str): 仓库使用的开源协议
        lang (str): 仓库使用的编程语言
        status (str): 仓库状态（码云指数）图片链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.des = ""
        self.url = ""
        self.star = 0
        self.fork = 0
        self.watch = 0
        self.license = ""
        self.lang = ""
        self.status = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebGitee:
        __returns = WebGitee()
        __returns.plain = plain
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.des = get_attr(plain, "des")
        __returns.star = get_attr(plain, "star")
        __returns.fork = get_attr(plain, "fork")
        __returns.watch = get_attr(plain, "watch")
        __returns.license = get_attr(plain, "license")
        __returns.lang = get_attr(plain, "lang")
        __returns.status = get_attr(plain, "status")
        return __returns


class WebMusicSong(WebMusicSong):
    """网页搜索音乐歌曲信息搜索结果结果模型

    这是一个遵照BaiduSpider网页搜索音乐歌曲信息搜索结果结果模型创建的返回模型类。

    Attributes:
        copyright (bool): 歌曲是否有版权限制
        duration (datetime.time): 歌曲时长
        is_original (bool): 歌曲是否为原唱
        labels (List[str]): 歌曲标签
        name (str): 歌曲名称
        other_sites (List[str]): 歌曲其他网站链接
        poster (str): 歌曲海报图片链接
        pub_company (str | None): 歌曲发布公司
        pub_date (datetime.datetime | None): 歌曲发布日期
        site (str): 歌曲发布站点（拼音）
        url (str): 歌曲链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.copyright = False
        self.duration = None
        self.is_original = False
        self.labels = []
        self.name = ""
        self.other_sites = []
        self.poster = ""
        self.pub_company = None
        self.pub_date = None
        self.site = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebMusicSong:
        __returns = WebMusicSong()
        __returns.plain = plain
        __returns.copyright = get_attr(plain, "copyright")
        __returns.duration = get_attr(plain, "duration")
        __returns.is_original = get_attr(plain, "is_original")
        __returns.labels = get_attr(plain, "labels")
        __returns.name = get_attr(plain, "name")
        __returns.other_sites = get_attr(plain, "other_sites")
        __returns.poster = get_attr(plain, "poster")
        __returns.pub_company = get_attr(plain, "pub_company")
        __returns.pub_date = get_attr(plain, "pub_date")
        __returns.site = get_attr(plain, "site")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebMusicAlbum(WebMusicAlbum):
    """网页搜索音乐歌曲专辑搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲专辑搜索结果结果模型创建的返回模型类。

    Attributes:
        name (str): 专辑名称
        url (str): 专辑链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.name = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebMusicAlbum:
        __returns = WebMusicAlbum()
        __returns.plain = plain
        __returns.name = get_attr(plain, "name")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebMusicSinger(WebMusicSinger):
    """网页搜索音乐歌曲歌手搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲歌手搜索结果结果模型创建的返回模型类。

    Attributes:
        name (str): 歌手名称
        url (str): 歌手链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.name = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebMusicSinger:
        __returns = WebMusicSinger()
        __returns.plain = plain
        __returns.name = get_attr(plain, "name")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebMusicSongs(WebMusicSongs):
    """网页搜索音乐歌曲搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲搜索结果结果模型创建的返回模型类。

    Attributes:
        album (WebMusicAlbum): 歌曲专辑
        singers (List[WebMusicSinger]): 歌曲歌手
        song (WebMusicSong): 歌曲信息
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.album = None
        self.singers = []
        self.song = None
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebMusicSongs:
        __returns = WebMusicSongs()
        __returns.plain = plain
        __returns.album = WebMusicAlbum._build_instance(get_attr(plain, "album"))
        for i in get_attr(plain, "singer"):
            __returns.singers.append(WebMusicSinger._build_instance(i))
        __returns.song = WebMusicSong._build_instance(get_attr(plain, "song"))
        return __returns


class WebMusic(WebMusic):
    """网页搜索音乐搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐搜索结果结果模型创建的返回模型类。

    Attributes:
        songs (List[WebMusicSongs]): 歌曲信息
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.songs = []
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebMusic:
        __returns = WebMusic()
        __returns.plain = plain
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        for i in get_attr(plain, "songs"):
            __returns.songs.append(WebMusicSongs._build_instance(i))
        return __returns


class WebResult(WebResult):
    """网页搜索结果模型

    这是一个遵照BaiduSpider网页搜索结果结果模型创建的返回模型类。

    Attributes:
        normal (List[WebNormal]): 普通搜索结果列表
        total (int): 搜索结果总数
        related (List[str]): 相关搜索结果列表
        calc (WebCalc | None): 计算搜索结果
        news (List[WebNews]): 资讯搜索结果列表
        video (List[WebVideo]): 视频搜索结果列表
        baike (WebBaike | None): 百科搜索结果
        tieba (WebTieba | None): 贴吧搜索结果
        blog (WebBlog | None): 博客搜索结果
        gitee (WebGitee | None): 码云仓库搜索结果
        music (WebMusic | None): 音乐搜索结果
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (list): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.normal = []
        self.total = 0
        self.related = []
        self.calc = None
        self.news = []
        self.video = []
        self.baike = None
        self.tieba = None
        self.blog = None
        self.gitee = None
        self.music = None
        self.pages = 0
        self.plain = []
        self.total = 0

    @staticmethod
    def _build_instance(plain: list, pages: int, total: int) -> WebResult:
        __returns = WebResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            if get_attr(p, "type") == "result":
                __returns.normal.append(WebNormal._build_instance(p))
            elif get_attr(p, "type") == "total":
                __returns.total = get_attr(p, "result")
            elif get_attr(p, "type") == "related":
                __returns.related = get_attr(p, "results")
            elif get_attr(p, "type") == "calc":
                __returns.calc = WebCalc._build_instance(p)
            elif get_attr(p, "type") == "news":
                __returns.news = [
                    WebNews._build_instance(i) for i in get_attr(p, "results")
                ]
            elif get_attr(p, "type") == "video":
                __returns.video = [
                    WebVideo._build_instance(i) for i in get_attr(p, "results")
                ]
            elif get_attr(p, "type") == "baike":
                __returns.baike = WebBaike._build_instance(get_attr(p, "result"))
            elif get_attr(p, "type") == "tieba":
                __returns.baike = WebTieba._build_instance(get_attr(p, "result"))
            elif get_attr(p, "type") == "blog":
                __returns.blog = WebBlog._build_instance(get_attr(p, "result"))
            elif get_attr(p, "type") == "gitee":
                __returns.gitee = WebGitee._build_instance(get_attr(p, "result"))
            elif get_attr(p, "type") == "music":
                __returns.music = WebMusic._build_instance(get_attr(p, "result"))
        return __returns

    def __getitem__(self, key) -> Any:
        return self.plain[key]

    def __repr__(self) -> str:
        return "<object WebResult>"
