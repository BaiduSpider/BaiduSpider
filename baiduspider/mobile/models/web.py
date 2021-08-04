"""移动端网页搜索返回值模型模块

此文件定义的所有现有的移动端网页搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime, time
from baiduspider.mobile.models.typings.typings_web import *
from baiduspider.mobile.models import get_attr, convert_time


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
        plain (dict): 源搜索结果字典
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
    def _build_instance(plain: dict) -> WebVideoDetail:
        __returns = WebVideoDetail()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        try:
            __returns.duration = time(
                minute=int(get_attr(plain, "duration").split(":")[0]),
                second=int(get_attr(plain, "duration").split(":")[1]),
            )
        except:
            __returns.duration = None
        for i in get_attr(plain, "labels"):
            __returns.labels.append(i)
        __returns.poster = get_attr(plain, "poster")
        __returns.pub_time = convert_time(get_attr(plain, "pub_time"))
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.video_num = get_attr(plain, "video_num")
        return __returns

    def __repr__(self) -> str:
        return "<WebVideoDetail %s>" % self.title


class WebVideoTag(WebVideoTag):
    """视频标签搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频标签搜索结果结果模型创建的返回模型类。

    Attributes:
        text (str): 标签文字
        url (str): 标签链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebVideoTag:
        __returns = WebVideoTag()
        __returns.plain = plain
        __returns.text = get_attr(plain, "text")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebVideoTag %s>" % self.text


class WebVideo(WebVideo):
    """视频搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebVideoDetail]): 搜索结果详情列表
        tags (List[WebVideoTag]): 搜索结果标签列表
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.tags = []
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebVideo:
        __returns = WebVideo()
        __returns.plain = plain
        for i in get_attr(plain, "results"):
            __returns.results.append(WebVideoDetail._build_instance(i))
        for i in get_attr(plain, "tags"):
            __returns.tags.append(WebVideoTag._build_instance(i))
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebVideo %s>" % self.url[:20] + "..."


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
        plain (dict): 源搜索结果字典
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
    def _build_instance(plain: dict) -> WebShortVideoDetail:
        __returns = WebShortVideoDetail()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        __returns.play_times = get_attr(plain, "play_times")
        __returns.poster = get_attr(plain, "poster")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebShortVideoDetail %s>" % self.title


class WebShortVideo(WebShortVideo):
    """短视频搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索短视频搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebShortVideoDetail]): 搜索结果详情列表
        total (int): 搜索结果总数
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.total = 0
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebShortVideo:
        __returns = WebShortVideo()
        __returns.plain = plain
        if get_attr(plain, "results") is not None:
            for i in get_attr(plain, "results"):
                __returns.results.append(WebShortVideoDetail._build_instance(i))
        __returns.total = get_attr(plain, "total")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebShortVideo %s>" % self.url[:20] + "..."


class WebSection(WebSection):
    """章节搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索章节搜索结果结果模型创建的返回模型类。

    Attributes:
        text (str): 搜索结果文字
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebSection:
        __returns = WebSection()
        __returns.plain = plain
        __returns.text = get_attr(plain, "text")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebSection %s>" % self.text


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
        plain (dict): 源搜索结果字典
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
    def _build_instance(plain: dict) -> WebBaike:
        __returns = WebBaike()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        for i in get_attr(plain, "labels"):
            __returns.labels.append(i)
        __returns.origin = get_attr(plain, "origin")
        __returns.poster = get_attr(plain, "poster")
        if get_attr(plain, "sections") is not None:
            for i in get_attr(plain, "sections"):
                __returns.sections.append(WebSection._build_instance(i))
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebBaike %s>" % self.title


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
        plain (dict): 源搜索结果字典
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
    def _build_instance(plain: dict) -> WebReyiDetail:
        __returns = WebReyiDetail()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        __returns.comments = get_attr(plain, "comments")
        __returns.des = get_attr(plain, "des")
        if get_attr(plain, "images") is not None:
            for i in get_attr(plain, "images"):
                __returns.images.append(i)
        __returns.likes = get_attr(plain, "likes")
        __returns.origin = get_attr(plain, "origin")
        __returns.pub_time = convert_time(get_attr(plain, "pub_time"))
        __returns.site = get_attr(plain, "site")
        return __returns

    def __repr__(self) -> str:
        return "<WebReyiDetail %s>" % (
            self.des if len(self.des) <= 10 else self.des[:10] + "..."
        )


class WebReyi(WebReyi):
    """热议搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索视频详情搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebReyiDetail]): 搜索结果详情列表
        total (int): 搜索结果总数
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.total = 0
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebReyi:
        __returns = WebReyi()
        __returns.plain = plain
        if get_attr(plain, "results") is not None:
            for i in get_attr(plain, "results"):
                __returns.results.append(WebReyiDetail._build_instance(i))
        __returns.total = get_attr(plain, "total")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebReyi %s>" % self.url[:20] + "..."


class WebKnowledgeDetail(WebKnowledgeDetail):
    """相关知识详情搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索相关知识详情搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        image (str): 搜索结果图片链接
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebKnowledgeDetail:
        __returns = WebKnowledgeDetail()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.image = get_attr(plain, "image")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns

    def __repr__(self) -> str:
        return "<WebKnowledgeDetail %s>" % self.title


class WebKnowledge(WebKnowledge):
    """相关知识搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索相关知识搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WebKnowledgeDetail]): 搜索结果详情列表
        title (str): 搜索结果标题
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.results = []
        self.title = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebKnowledge:
        __returns = WebKnowledge()
        __returns.plain = plain
        for i in get_attr(plain, "results"):
            __returns.results.append(WebKnowledgeDetail._build_instance(i))
        __returns.title = get_attr(plain, "title")
        return __returns

    def __repr__(self) -> str:
        return "<WebKnowledge %s>" % self.title


class WebNormal(WebNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索普通搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 搜索结果简介
        image (str): 搜索结果图片链接
        title (str): 搜索结果标题
        url (str): 搜索结果链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.sections = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebNormal:
        __returns = WebNormal()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.image = get_attr(plain, "image")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        if get_attr(plain, "sections") is not None:
            for i in get_attr(plain, "sections"):
                __returns.sections.append(WebSection._build_instance(i))
        return __returns

    def __repr__(self) -> str:
        return "<WebNormal %s>" % self.title


class WebVideoNormalInfo(WebVideoNormalInfo):
    """普通视频信息搜索结果模型

    这是一个遵照BaiduSpider移动端网页搜索普通视频信息搜索结果结果模型创建的返回模型类。

    Attributes:
        data (str): 搜索结果数据
        type (str): 搜索结果类型
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        self.data = ""
        self.type = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebVideoNormalInfo:
        __returns = WebVideoNormalInfo()
        __returns.plain = plain
        __returns.data = get_attr(plain, "data")
        __returns.type = get_attr(plain, "type")
        return __returns

    def __repr__(self) -> str:
        return "<WebVideoNormalInfo %s>" % self.type


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
        plain (dict): 源搜索结果字典
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
    def _build_instance(plain: dict) -> WebVideoNormal:
        __returns = WebVideoNormal()
        __returns.plain = plain
        __returns.poster = get_attr(plain, "poster")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.duration = time(
            minute=int(get_attr(plain, "duration").split(":")[0]),
            second=int(get_attr(plain, "duration").split(":")[1]),
        )
        __returns.origin = get_attr(plain, "origin")
        for i in get_attr(plain, "labels"):
            __returns.info.append(i)
        if get_attr(plain, "info") is not None:
            for i in get_attr(plain, "info"):
                __returns.info.append(WebVideoNormalInfo._build_instance(i))
        __returns.video_num = get_attr(plain, "video_num")
        return __returns

    def __repr__(self) -> str:
        return "<WebVideoNormal %s>" % self.title


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
        plain (dict): 源搜索结果字典
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
            if get_attr(p, "type") == "result":
                __returns.normal.append(WebNormal._build_instance(p))
            elif get_attr(p, "type") == "video":
                __returns.video = WebVideo._build_instance(p)
            elif get_attr(p, "type") == "short_video":
                __returns.short_video = WebShortVideo._build_instance(p)
            elif get_attr(p, "type") == "reyi":
                __returns.reyi = WebReyi._build_instance(p)
            elif get_attr(p, "type") == "knowledge":
                __returns.knowledge = WebKnowledge._build_instance(p)
            elif get_attr(p, "type") == "baike":
                __returns.baike = WebBaike._build_instance(get_attr(p, "result"))
            elif get_attr(p, "type") == "video_normal":
                __returns.video_normal.append(WebVideoNormal._build_instance(p))
        return __returns

    def __repr__(self) -> str:
        return "<WebResult %s>" % self.query
