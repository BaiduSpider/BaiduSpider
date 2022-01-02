"""网页搜索结果模型类型注释文件

此模块中定义了所有现有网页搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime, time
from typing import List, Union


class WebNormal(object):
    """网页搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebNormal`类。
    """

    def __init__(self) -> None:
        self.des: str
        self.origin: str
        self.title: str
        self.url: str
        self.time: datetime
        self.snapshot: str
        self.plain: dict


class WebCalc(object):
    """网页搜索计算搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebCalc`类。
    """

    def __init__(self) -> None:
        self.process: str
        self.result: str
        self.plain: dict


class WebNews(object):
    """网页搜索资讯搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebNews`类。
    """

    def __init__(self) -> None:
        self.author: str
        self.time: str
        self.url: datetime
        self.des: str
        self.plain: dict


class WebVideo(object):
    """网页搜索视频搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebVideo`类。
    """

    def __init__(self) -> None:
        self.cover: str
        self.origin: str
        self.length: str
        self.title: str
        self.url: str
        self.plain: dict


class WebBaike(object):
    """网页搜索百科搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebBaike`类。
    """

    def __init__(self) -> None:
        self.cover: str
        self.cover_type: str
        self.des: str
        self.title: str
        self.url: str
        self.plain: dict


class WebTiebaHot(object):
    """网页搜索贴吧热门搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebTiebaHot`类。
    """

    def __init__(self) -> None:
        self.clicks: str
        self.replies: str
        self.title: str
        self.url: str
        self.plain: dict


class WebTieba(object):
    """网页搜索贴吧搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebTieba`类。
    """

    def __init__(self) -> None:
        self.cover: str
        self.des: str
        self.title: str
        self.followers: str
        self.total: str
        self.hot: List[WebTiebaHot]
        self.url: str
        self.plain: dict


class WebBlogDetail(object):
    """网页搜索博客详情搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebBlogDetail`类。
    """

    def __init__(self) -> None:
        self.title: str
        self.url: str
        self.des: str
        self.origin: str
        self.tags: List[str]
        self.plain: dict


class WebBlog(object):
    """网页搜索博客搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebBlog`类。
    """

    def __init__(self) -> None:
        self.title: str
        self.url: str
        self.blogs: List[WebBlogDetail]
        self.plain: dict


class WebGitee(object):
    """网页搜索码云仓库搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebGitee`类。
    """

    def __init__(self) -> None:
        self.title: str
        self.des: str
        self.url: str
        self.star: int
        self.fork: int
        self.watch: int
        self.license: str
        self.lang: str
        self.status: str
        self.plain: dict


class WebMusicSong(object):
    """网页搜索音乐歌曲信息搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebMusicSong`类。
    """

    def __init__(self) -> None:
        self.copyright: bool
        self.duration: time
        self.is_original: bool
        self.labels: List[str]
        self.name: str
        self.other_sites: List[str]
        self.poster: str
        self.pub_company: Union[str, None]
        self.pub_date: Union[str, None]
        self.site: str
        self.url: str


class WebMusicAlbum(object):
    """网页搜索音乐歌曲专辑搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebMusicAlbum`类。
    """

    def __init__(self) -> None:
        self.name: str
        self.url: str


class WebMusicSinger(object):
    """网页搜索音乐歌曲歌手搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebMusicSinger`类。
    """

    def __init__(self) -> None:
        self.name: str
        self.url: str


class WebMusicSongs(object):
    """网页搜索音乐歌曲搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebMusicSongs`类。
    """

    def __init__(self) -> None:
        self.album: WebMusicAlbum
        self.singers: List[WebMusicSinger]
        self.song: WebMusicSong


class WebMusic(object):
    """网页搜索音乐搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebMusic`类。
    """

    def __init__(self) -> None:
        self.songs: List[WebMusicSongs]
        self.title: str
        self.url: str


class WebResult(object):
    """网页搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebResult`类。
    """

    def __init__(self) -> None:
        self.normal: List[WebNormal]
        self.pages: int
        self.related: list
        self.calc: WebCalc
        self.news: List[WebNews]
        self.video: List[WebVideo]
        self.baike: WebBaike
        self.tieba: WebTieba
        self.blog: WebBlog
        self.gitee: WebGitee
        self.music: WebMusic
        self.pages: int
        self.plain: list
        self.total: int
