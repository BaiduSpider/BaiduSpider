"""移动端网页搜索返回值模型模块

此文件定义的所有现有的移动端网页搜索返回值模型并编写了自动构建函数。
"""
from datetime import time
from typing import Dict

from baiduspider.util import convert_time
from baiduspider.mobile.models.typings.typings_web import *


class WebVideoDetail(WebVideoDetail):
    """视频详情搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频详情搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 搜索结果作者（来源）
        author_avatar (str): 搜索结果作者（来源）头像
        duration (datetime.time): 搜索结果时长
        labels (List[str]): 搜索结果标签列表
        poster (str): 搜索结果海报图片链接
        pub_time (datetime.datetime): 搜索结果发表时间
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        video_num (int): 搜索结果“合集”中视频数量
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.duration = None
        self.labels = []
        self.poster = ""
        self.pub_time = None
        self.title = ""
        self.url = ""
        self.video_num = 0
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebVideoDetail:
        __returns = WebVideoDetail()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.author_avatar = plain.get("author_avatar")
        try:
            __returns.duration = time(
                minute=int(plain.get("duration").split(":")[0]),
                second=int(plain.get("duration").split(":")[1]),
            )
        except:
            __returns.duration = None
        for i in plain.get("labels"):
            __returns.labels.append(i)
        __returns.poster = plain.get("poster")
        __returns.pub_time = convert_time(plain.get("pub_time"))
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.video_num = plain.get("video_num")
        return __returns

    def __repr__(self) -> str:
        return f"<WebVideoDetail {self.title}>"


class WebVideoTag(WebVideoTag):
    """视频标签搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频标签搜索结果结果模型创建的返回模型类。

    Attributes:
        text (str): 标签文字
        url (str): 标签链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebVideoTag:
        __returns = WebVideoTag()
        __returns.plain = plain
        __returns.text = plain.get("text")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebVideoTag {self.text}>"


class WebVideo(WebVideo):
    """视频搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebVideoDetail]): 搜索结果详情列表
        tags (List[WebVideoTag]): 搜索结果标签列表
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.tags = []
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebVideo:
        __returns = WebVideo()
        __returns.plain = plain
        for i in plain.get("results"):
            __returns.results.append(WebVideoDetail._build_instance(i))
        for i in plain.get("tags"):
            __returns.tags.append(WebVideoTag._build_instance(i))
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebVideo {self.url[:20]}...>"


class WebShortVideoDetail(WebShortVideoDetail):
    """短视频详情搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索短视频详情搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 搜索结果作者（来源）
        author_avatar (str): 搜索结果作者（来源）头像
        play_times (int): 搜索结果播放次数
        poster (str): 搜索结果海报图片链接
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.play_times = 0
        self.poster = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebShortVideoDetail:
        __returns = WebShortVideoDetail()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.author_avatar = plain.get("author_avatar")
        __returns.play_times = plain.get("play_times")
        __returns.poster = plain.get("poster")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebShortVideoDetail {self.title}>"


class WebShortVideo(WebShortVideo):
    """短视频搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索短视频搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebShortVideoDetail]): 搜索结果详情列表
        total (int): 搜索结果总数
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.total = 0
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebShortVideo:
        __returns = WebShortVideo()
        __returns.plain = plain
        if plain.get("results") is not None:
            for i in plain.get("results"):
                __returns.results.append(WebShortVideoDetail._build_instance(i))
        __returns.total = plain.get("total")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebShortVideo {self.url[:20]}>..."


class WebSection(WebSection):
    """章节搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索章节搜索结果结果模型创建的返回模型类。

    Attributes:
        text (str): 搜索结果文字
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebSection:
        __returns = WebSection()
        __returns.plain = plain
        __returns.text = plain.get("text")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebSection {self.text}>"


class WebBaike(WebBaike):
    """百科搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索百科搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        labels (List[str]): 搜索结果标签列表
        origin (str): 搜索结果来源
        poster (str): 搜索结果海报图片链接
        sections (List[WebSection]): 搜索结果章节列表
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.des = ""
        self.labels = []
        self.origin = ""
        self.poster = ""
        self.sections = []
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebBaike:
        __returns = WebBaike()
        __returns.plain = plain
        __returns.des = plain.get("des")
        for i in plain.get("labels"):
            __returns.labels.append(i)
        __returns.origin = plain.get("origin")
        __returns.poster = plain.get("poster")
        if plain.get("sections") is not None:
            for i in plain.get("sections"):
                __returns.sections.append(WebSection._build_instance(i))
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebBaike {self.title}>"


class WebReyiDetail(WebReyiDetail):
    """热议详情搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索热议详情搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 搜索结果作者（来源）
        author_avatar (str): 搜索结果作者（来源）头像
        comments (int): 搜索结果评论数
        des (str): 搜索结果简介
        images (List[str]): 搜索结果图片列表
        likes (int): 搜索结果喜欢数
        origin (str): 搜索结果来源（作者）
        pub_time (datetime.datetime): 搜索结果发布时间
        site (str): 搜索结果发布站点
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.comments = 0
        self.des = ""
        self.images = []
        self.likes = 0
        self.origin = ""
        self.pub_time = None
        self.site = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebReyiDetail:
        __returns = WebReyiDetail()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.author_avatar = plain.get("author_avatar")
        __returns.comments = plain.get("comments")
        __returns.des = plain.get("des")
        if plain.get("images") is not None:
            for i in plain.get("images"):
                __returns.images.append(i)
        __returns.likes = plain.get("likes")
        __returns.origin = plain.get("origin")
        __returns.pub_time = convert_time(plain.get("pub_time"))
        __returns.site = plain.get("site")
        return __returns

    def __repr__(self) -> str:
        if len(self.des) <= 10:
            return f"<WebReyiDetail {self.des}>"
        else:
            return f"<WebReyiDetail {self.des[:10]}...>"


class WebReyi(WebReyi):
    """热议搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频详情搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebReyiDetail]): 搜索结果详情列表
        total (int): 搜索结果总数
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.total = 0
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebReyi:
        __returns = WebReyi()
        __returns.plain = plain
        if plain.get("results") is not None:
            for i in plain.get("results"):
                __returns.results.append(WebReyiDetail._build_instance(i))
        __returns.total = plain.get("total")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebReyi {self.url[:20]}>..."


class WebKnowledgeDetail(WebKnowledgeDetail):
    """相关知识详情搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索相关知识详情搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        image (str): 搜索结果图片链接
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebKnowledgeDetail:
        __returns = WebKnowledgeDetail()
        __returns.plain = plain
        __returns.des = plain.get("des")
        __returns.image = plain.get("image")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns

    def __repr__(self) -> str:
        return f"<WebKnowledgeDetail {self.title}>"


class WebKnowledge(WebKnowledge):
    """相关知识搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索相关知识搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebKnowledgeDetail]): 搜索结果详情列表
        title (str): 搜索结果标题
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.title = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebKnowledge:
        __returns = WebKnowledge()
        __returns.plain = plain
        for i in plain.get("results"):
            __returns.results.append(WebKnowledgeDetail._build_instance(i))
        __returns.title = plain.get("title")
        return __returns

    def __repr__(self) -> str:
        return f"<WebKnowledge {self.title}>"


class WebNormal(WebNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索普通搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        image (str): 搜索结果图片链接
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.sections = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebNormal:
        __returns = WebNormal()
        __returns.plain = plain
        __returns.des = plain.get("des")
        __returns.image = plain.get("image")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        if plain.get("sections") is not None:
            for i in plain.get("sections"):
                __returns.sections.append(WebSection._build_instance(i))
        return __returns

    def __repr__(self) -> str:
        return f"<WebNormal {self.title}>"


class WebVideoNormalInfo(WebVideoNormalInfo):
    """普通视频信息搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索普通视频信息搜索结果结果模型创建的返回模型类。

    Attributes:
        data (str): 搜索结果数据
        type (str): 搜索结果类型
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.data = ""
        self.type = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebVideoNormalInfo:
        __returns = WebVideoNormalInfo()
        __returns.plain = plain
        __returns.data = plain.get("data")
        __returns.type = plain.get("type")
        return __returns

    def __repr__(self) -> str:
        return f"<WebVideoNormalInfo {self.type}>"


class WebVideoNormal(WebVideoNormal):
    """普通视频搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索普通视频搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        poster (str): 搜索结果海报链接
        duration (time): 搜索结果时长
        info (List[WebVideoNormalInfo]): 搜索结果信息列表
        origin (str): 搜索结果来源（作者）
        labels (List[str]): 搜索结果标签列表
        video_num (int): 搜索结果视频数量
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.title = ""
        self.url = ""
        self.poster = ""
        self.duration = None
        self.info = []
        self.origin = ""
        self.labels = []
        self.video_num = 0
        self.plain = {}

    @staticmethod
    def _build_instance(plain: Dict) -> WebVideoNormal:
        __returns = WebVideoNormal()
        __returns.plain = plain
        __returns.poster = plain.get("poster")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.duration = time(
            minute=int(plain.get("duration").split(":")[0]),
            second=int(plain.get("duration").split(":")[1]),
        )
        __returns.origin = plain.get("origin")
        for i in plain.get("labels"):
            __returns.info.append(i)
        if plain.get("info") is not None:
            for i in plain.get("info"):
                __returns.info.append(WebVideoNormalInfo._build_instance(i))
        __returns.video_num = plain.get("video_num")
        return __returns

    def __repr__(self) -> str:
        return f"<WebVideoNormal {self.title}>"


class WebResult(WebResult):
    """网页搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索结果结果模型创建的返回模型类。

    Attributes:
        video (Union[WebVideo, None]): 视频搜索结果
        short_video (Union[WebShortVideo, None]): 短视频搜索结果
        baike (Union[WebBaike, None]): 百科搜索结果
        reyi (Union[WebReyi, None]): 热议搜索结果
        knowledge (Union[WebKnowledge, None]): 相关知识搜索结果
        normal (List[WebNormal]): 普通搜索结果列表
        video_normal (List[WebVideoNormal]): 普通视频搜索结果列表
        query (str): 搜索词
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.video = None
        self.short_video = None
        self.baike = None
        self.reyi = None
        self.knowledge = None
        self.normal = []
        self.video_normal = []
        self.query = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: list, query: str = "") -> WebResult:
        __returns = WebResult()
        __returns.plain = plain
        __returns.query = query
        for p in plain:
            if plain.get("type") == "result":
                __returns.normal.append(WebNormal._build_instance(p))
            elif plain.get("type") == "video":
                __returns.video = WebVideo._build_instance(p)
            elif plain.get("type") == "short_video":
                __returns.short_video = WebShortVideo._build_instance(p)
            elif plain.get("type") == "reyi":
                __returns.reyi = WebReyi._build_instance(p)
            elif plain.get("type") == "knowledge":
                __returns.knowledge = WebKnowledge._build_instance(p)
            elif plain.get("type") == "baike":
                __returns.baike = WebBaike._build_instance(plain.get("result"))
            elif plain.get("type") == "video_normal":
                __returns.video_normal.append(WebVideoNormal._build_instance(p))
        return __returns

    def __repr__(self) -> str:
        return f"<WebResult {self.query}>"
