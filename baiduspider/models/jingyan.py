"""经验搜索返回值模型模块

此文件定义的所有现有的经验搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime
from typing import Dict, List, Optional

from baiduspider.models import convert_time


class JingyanPublisher():
    """经验发布者模型

    这是一个遵照BaiduSpider经验搜索经验发布者结果模型创建的返回模型类。

    Attributes:
        name (str): 经验上传者用户名
        url (str): 经验上传者链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.name: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "JingyanPublisher":
        __returns = JingyanPublisher()
        __returns.plain = plain
        __returns.name = plain.get("name")
        __returns.url = plain.get("url")
        return __returns


class JingyanNormal():
    """普通搜索结果模型

    这是一个遵照BaiduSpider经验搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        title (str): 经验标题
        url (str): 经验链接
        des (str): 经验简介
        pub_date (datetime.datetime): 经验发布日期
        category (List[str]): 经验分类
        votes (int): 经验的支持票数
        publisher (JingyanPublisher): 经验发布者信息
        is_original (bool): 经验是否为原创
        is_outstanding (bool): 经验是否为优秀经验
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.title: str = ""
        self.url: str = ""
        self.des: str = ""
        self.pub_date: datetime = None
        self.category: List[str] = []
        self.votes: int = 0
        self.publisher: JingyanPublisher = None
        self.is_original: bool = False
        self.is_outstanding: bool = False
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "JingyanNormal":
        __returns = JingyanNormal()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.des = plain.get("des")
        __returns.pub_date = convert_time(plain.get("pub_date"))
        __returns.category = plain.get("category")
        __returns.votes = plain.get("votes")
        __returns.publisher = JingyanPublisher._build_instance(plain.get("publisher"))
        __returns.is_original = plain.get("is_original")
        __returns.is_outstanding = plain.get("is_outstanding")
        return __returns


class JingyanResult():
    """经验搜索结果模型

    这是一个遵照BaiduSpider经验搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[JingyanNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (List): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results: List[JingyanNormal] = []
        self.pages: int = 0
        self.total: int = 0
        self.plain: Dict = []

    @staticmethod
    def _build_instance(plain: List, pages: int, total: int) -> "JingyanResult":
        __returns = JingyanResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(JingyanNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Optional[JingyanNormal]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object JingyanResult>"
