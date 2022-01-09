"""资讯搜索返回值模型模块

此文件定义的所有现有的资讯搜索返回值模型并编写了自动构建函数。
"""
from typing import Union

from baiduspider.models import convert_time
from baiduspider.models.typings.typings_news import *


class NewsNormal(NewsNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider资讯搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 资讯来源（作者）
        date (datetime.datetime | None): 资讯发布时间
        des (str): 资讯简介
        title (str): 资讯标题
        url (str): 资讯链接
        cover (str): 资讯封面图片链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.author = ""
        self.date = None
        self.des = ""
        self.title = ""
        self.url = ""
        self.cover = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> NewsNormal:
        __returns = NewsNormal()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.date = convert_time(plain.get("date"))
        __returns.des = plain.get("des")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.cover = plain.get("cover")
        return __returns


class NewsResult(NewsResult):
    """资讯搜索结果模型

    这是一个遵照BaiduSpider资讯搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[NewsNormal]): 普通搜索结果列表
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
    def _build_instance(plain: list, pages: int, total: int) -> NewsResult:
        __returns = NewsResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(NewsNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Union[NewsNormal, None]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object NewsResult>"
