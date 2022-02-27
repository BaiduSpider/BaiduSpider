"""网页搜索返回值模型模块

此文件定义的所有现有的网页搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime, time
from typing import Any, Dict, List, Optional

from baiduspider.models import convert_time


class WebNormal():
    """普通搜索结果模型

    这是一个遵照BaiduSpider网页搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        origin (str): 搜索结果来源
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        time (datetime): 搜索结果发布时间
        snapshot (str): 搜索结果快照链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.des: str = ""
        self.origin: str = ""
        self.title: str = ""
        self.url: str = ""
        self.time: datetime = None
        self.snapshot: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebNormal":
        __returns = WebNormal()
        __returns.plain = plain
        __returns.des = plain.get("des")
        __returns.origin = plain.get("origin")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.time = convert_time(plain.get("time"))
        __returns.snapshot = plain.get("snapshot")
        return __returns


class WebCalc():
    """计算搜索结果模型

    这是一个遵照BaiduSpider网页搜索计算搜索结果结果模型创建的返回模型类。

    Attributes:
        process (str): 计算过程，如：12 + 21
        result (str): 计算结果，由于可能是`1e6`这样的形式，所以类型为`str`
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.process: str = ""
        self.result: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebCalc":
        __returns = WebCalc()
        __returns.plain = plain
        __returns.process = plain.get("process")
        __returns.result = int(plain.get("result"))
        return __returns


class WebNews():
    """资讯搜索结果模型

    这是一个遵照BaiduSpider网页搜索资讯搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 资讯作者（来源）
        time (datetime): 资讯发布时间
        url (str): 资讯链接
        des (str): 资讯简介
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.author: str = ""
        self.time: datetime = None
        self.url: str = ""
        self.des: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebNews":
        __returns = WebNews()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.time = convert_time(plain.get("time"))
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.des = plain.get("des")
        return __returns


class WebVideo():
    """视频搜索结果模型

    这是一个遵照BaiduSpider网页搜索视频搜索结果结果模型创建的返回模型类。

    Attributes:
        cover (str): 视频封面图片链接
        origin (str): 视频来源
        length (str): 视频时长
        title (str): 视频标题
        url (str): 视频链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover: str = ""
        self.origin: str = ""
        self.length: str = ""
        self.title: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebVideo":
        __returns = WebVideo()
        __returns.plain = plain
        __returns.cover = plain.get("cover")
        __returns.origin = plain.get("origin")
        __returns.length = plain.get("length")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class WebBaike():
    """百科搜索结果模型

    这是一个遵照BaiduSpider网页搜索百科搜索结果结果模型创建的返回模型类。

    Attributes:
        cover (str): 百科封面图片（视频）链接
        cover_type (str): 百科封面类型，图片时为"image"，视频时为"video"
        des (str): 百科简介
        title (str): 百科标题
        url (str): 百科链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover: str = ""
        self.cover_type: str = ""
        self.des: str = ""
        self.title: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebBaike":
        __returns = WebBaike()
        __returns.plain = plain
        __returns.cover = plain.get("cover")
        __returns.cover_type = plain.get("cover-type")
        __returns.des = plain.get("des")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class WebTiebaHot():
    """贴吧热门搜索结果模型

    这是一个遵照BaiduSpider网页搜索贴吧热门搜索结果结果模型创建的返回模型类。

    Attributes:
        clicks (str): 帖子点击次数，可能会有形如`1万`的结果，故类型为`str`
        replies (str): 帖子回复次数，可能会有形如`1万`的结果，故类型为`str`
        title (str): 帖子标题
        url (str): 帖子链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.clicks: str = ""
        self.replies: str = ""
        self.title: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebTiebaHot":
        __returns = WebTiebaHot()
        __returns.plain = plain
        __returns.clicks = plain.get("clicks")
        __returns.replies = plain.get("replies")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class WebTieba():
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
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.cover: str = ""
        self.des: str = ""
        self.title: str = ""
        self.followers: str = ""
        self.total: str = ""
        self.url: str = ""
        self.hot: List[WebTiebaHot] = []
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebTieba":
        __returns = WebTieba()
        __returns.plain = plain
        __returns.cover = plain.get("cover")
        __returns.des = plain.get("des")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.followers = plain.get("followers")
        __returns.total = plain.get("total")
        __returns.url = plain.get("url")
        for i in plain.get("hot"):
            __returns.hot.append(WebTiebaHot._build_instance(i))
        return __returns


class WebBlogDetail():
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
        self.title: str = ""
        self.url: str = ""
        self.des: str = ""
        self.origin: str = ""
        self.tags: List[str] = []
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebBlogDetail":
        __returns = WebBlogDetail()
        __returns.plain = plain
        __returns.des = plain.get("des")
        __returns.origin = plain.get("origin")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        for i in plain.get("tags"):
            __returns.tags.append(i)
        return __returns


class WebBlog():
    """博客搜索结果模型

    这是一个遵照BaiduSpider网页搜索博客搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 博客搜索结果标题
        url (str): 博客搜索结果链接
        blogs (List[WebBlogDetail]): 博客详情列表
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.title: str = ""
        self.url: str = ""
        self.blogs: List[str] = []
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebBlog":
        __returns = WebBlog()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        for i in plain.get("blogs"):
            __returns.blogs.append(WebBlogDetail._build_instance(i))
        return __returns


class WebGitee():
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
        self.title: str = ""
        self.des: str = ""
        self.url: str = ""
        self.star: int = 0
        self.fork: int = 0
        self.watch: int = 0
        self.license: str = ""
        self.lang: str = ""
        self.status: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebGitee":
        __returns = WebGitee()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.des = plain.get("des")
        __returns.star = plain.get("star")
        __returns.fork = plain.get("fork")
        __returns.watch = plain.get("watch")
        __returns.license = plain.get("license")
        __returns.lang = plain.get("lang")
        __returns.status = plain.get("status")
        return __returns


class WebMusicSong():
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
        pub_company (Optional[str]): 歌曲发布公司
        pub_date (datetime.Optional[datetime]): 歌曲发布日期
        site (str): 歌曲发布站点（拼音）
        url (str): 歌曲链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.copyright: bool = False
        self.duration: time = None
        self.is_original: bool = False
        self.labels: List[str] = []
        self.name: str = ""
        self.other_sites: List[str] = []
        self.poster: str = ""
        self.pub_company: Optional[str] = None
        self.pub_date: Optional[str] = None
        self.site: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "WebMusicSong":
        __returns = WebMusicSong()
        __returns.plain = plain
        __returns.copyright = plain.get("copyright")
        __returns.duration = plain.get("duration")
        __returns.is_original = plain.get("is_original")
        __returns.labels = plain.get("labels")
        __returns.name = plain.get("name")
        __returns.other_sites = plain.get("other_sites")
        __returns.poster = plain.get("poster")
        __returns.pub_company = plain.get("pub_company")
        __returns.pub_date = plain.get("pub_date")
        __returns.site = plain.get("site")
        __returns.url = plain.get("url")
        return __returns


class WebMusicAlbum():
    """网页搜索音乐歌曲专辑搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲专辑搜索结果结果模型创建的返回模型类。

    Attributes:
        name (str): 专辑名称
        url (str): 专辑链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.name: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebMusicAlbum":
        __returns = WebMusicAlbum()
        __returns.plain = plain
        __returns.name = plain.get("name")
        __returns.url = plain.get("url")
        return __returns


class WebMusicSinger():
    """网页搜索音乐歌曲歌手搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲歌手搜索结果结果模型创建的返回模型类。

    Attributes:
        name (str): 歌手名称
        url (str): 歌手链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.name: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebMusicSinger":
        __returns = WebMusicSinger()
        __returns.plain = plain
        __returns.name = plain.get("name")
        __returns.url = plain.get("url")
        return __returns


class WebMusicSongs():
    """网页搜索音乐歌曲搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐歌曲搜索结果结果模型创建的返回模型类。

    Attributes:
        album (WebMusicAlbum): 歌曲专辑
        singers (List[WebMusicSinger]): 歌曲歌手
        song (WebMusicSong): 歌曲信息
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.album: WebMusicAlbum = None
        self.singers: List[WebMusicSinger] = []
        self.song: WebMusicSong = None
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebMusicSongs":
        __returns = WebMusicSongs()
        __returns.plain = plain
        __returns.album = WebMusicAlbum._build_instance(plain.get("album"))
        for i in plain.get("singer"):
            __returns.singers.append(WebMusicSinger._build_instance(i))
        __returns.song = WebMusicSong._build_instance(plain.get("song"))
        return __returns


class WebMusic():
    """网页搜索音乐搜索结果结果模型。

    这是一个遵照BaiduSpider网页搜索音乐搜索结果结果模型创建的返回模型类。

    Attributes:
        songs (List[WebMusicSongs]): 歌曲信息
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.songs = []
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "WebMusic":
        __returns = WebMusic()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        for i in plain.get("songs"):
            __returns.songs.append(WebMusicSongs._build_instance(i))
        return __returns


class WebResult():
    """网页搜索结果模型

    这是一个遵照BaiduSpider网页搜索结果结果模型创建的返回模型类。

    Attributes:
        normal (List[WebNormal]): 普通搜索结果列表
        total (int): 搜索结果总数
        related (List[str]): 相关搜索结果列表
        calc (Optional[WebCalc]): 计算搜索结果
        news (List[WebNews]): 资讯搜索结果列表
        video (List[WebVideo]): 视频搜索结果列表
        baike (Optional[WebBaike]): 百科搜索结果
        tieba (Optional[WebTieba]): 贴吧搜索结果
        blog (Optional[WebBlog]): 博客搜索结果
        gitee (Optional[WebGitee]): 码云仓库搜索结果
        music (Optional[WebMusic]): 音乐搜索结果
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (list): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.normal: List[WebNormal] = []
        self.total: int = 0
        self.related: List[Dict] = []
        self.calc: WebCalc = None
        self.news: List[WebNews] = []
        self.video: List[WebVideo] = []
        self.baike: Optional[WebBaike] = None
        self.tieba: Optional[WebTieba] = None
        self.blog: Optional[WebBlog] = None
        self.gitee: Optional[WebGitee] = None
        self.music: Optional[WebMusic] = None
        self.pages: int = 0
        self.plain: List[str] = []
        self.total: int = 0

    @staticmethod
    def _build_instance(plain: list, pages: int, total: int) -> "WebResult":
        __returns = WebResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            if p.get("type") == "result":
                __returns.normal.append(WebNormal._build_instance(p))
            elif p.get("type") == "total":
                __returns.total = p.get("result")
            elif p.get("type") == "related":
                __returns.related = p.get("results")
            elif p.get("type") == "calc":
                __returns.calc = WebCalc._build_instance(p)
            elif p.get("type") == "news":
                __returns.news = [WebNews._build_instance(i) for i in p.get("results")]
            elif p.get("type") == "video":
                __returns.video = [
                    WebVideo._build_instance(i) for i in p.get("results")
                ]
            elif p.get("type") == "baike":
                __returns.baike = WebBaike._build_instance(p.get("result"))
            elif p.get("type") == "tieba":
                __returns.baike = WebTieba._build_instance(p.get("result"))
            elif p.get("type") == "blog":
                __returns.blog = WebBlog._build_instance(p.get("result"))
            elif p.get("type") == "gitee":
                __returns.gitee = WebGitee._build_instance(p.get("result"))
            elif p.get("type") == "music":
                __returns.music = WebMusic._build_instance(p.get("result"))
        return __returns

    def __getitem__(self, key) -> Any:
        return self.plain[key]

    def __repr__(self) -> str:
        return "<object WebResult>"
