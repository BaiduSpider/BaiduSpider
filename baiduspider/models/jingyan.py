"""经验搜索返回值模型模块

此文件定义的所有现有的经验搜索返回值模型并编写了自动构建函数。
"""
from typing import Union

from baiduspider.models import convert_time
from baiduspider.models.typings.typings_jingyan import *


class JingyanPublisher(JingyanPublisher):
    """经验发布者模型

    这是一个遵照BaiduSpider经验搜索经验发布者结果模型创建的返回模型类。

    Attributes:
        name (str): 经验上传者用户名
        url (str): 经验上传者链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.name = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> JingyanPublisher:
        __returns = JingyanPublisher()
        __returns.plain = plain
        __returns.name = plain.get("name")
        __returns.url = plain.get("url")
        return __returns


class JingyanNormal(JingyanNormal):
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
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.url = ""
        self.des = ""
        self.pub_date = None
        self.category = []
        self.votes = 0
        self.publisher = None
        self.is_original = False
        self.is_outstanding = False
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> JingyanNormal:
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


class JingyanResult(JingyanResult):
    """经验搜索结果模型

    这是一个遵照BaiduSpider经验搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[JingyanNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (list): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.pages = 0
        self.total = 0
        self.plain = []

    @staticmethod
    def _build_instance(plain: list, pages: int, total: int) -> JingyanResult:
        __returns = JingyanResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(JingyanNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Union[JingyanNormal, None]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object JingyanResult>"
