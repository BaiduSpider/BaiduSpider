"""视频搜索返回值模型模块

此文件定义的所有现有的视频搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime, time
from typing import Dict, List, Optional


class VideoNormal():
    """视频搜索普通搜索结果模型

    这是一个遵照BaiduSpider视频搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        des (str): 视频简介
        img (str): 视频封面图片链接
        origin (str): 视频来源（作者）
        pub_time (datetime): 视频发布时间
        length (time): 视频时长
        title (str): 视频标题
        url (str): 视频链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.img: str = ""
        self.length: time = None
        self.pub_time: datetime = None
        self.des: str = ""
        self.title: str = ""
        self.url: str = ""
        self.origin: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "VideoNormal":
        __returns = VideoNormal()
        __returns.plain = plain
        __returns.des = plain.get("des")
        __returns.img = plain.get("img")
        __returns.origin = plain.get("origin")
        __returns.pub_time = plain.get("pub_time")
        __returns.length = plain.get("length")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class VideoResult():
    """视频搜索结果模型

    这是一个遵照BaiduSpider视频搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[VideoNormal]): 普通搜索结果列表
        is_last (bool): 当前页数是否为最后一页
        plain (List): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results: List[VideoNormal] = []
        self.is_last: bool = False
        self.plain: List[Dict] = []

    @staticmethod
    def _build_instance(plain: List) -> "VideoResult":
        __returns = VideoResult()
        __returns.plain = plain
        if not plain:
            __returns.is_last = True
            return __returns
        for p in plain:
            __returns.results.append(VideoNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Optional[VideoNormal]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object VideoResult>"
