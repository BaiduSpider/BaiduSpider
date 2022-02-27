"""资讯搜索返回值模型模块

此文件定义的所有现有的资讯搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime
from typing import Dict, List, Optional

from baiduspider.models import convert_time


class NewsNormal():
    """普通搜索结果模型

    这是一个遵照BaiduSpider资讯搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        author (str): 资讯来源（作者）
        date (Optional[datetime]): 资讯发布时间
        des (str): 资讯简介
        title (str): 资讯标题
        url (str): 资讯链接
        cover (str): 资讯封面图片链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.author: str = ""
        self.date: Optional[datetime] = None
        self.des: str = ""
        self.title: str = ""
        self.url: str = ""
        self.cover: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "NewsNormal":
        __returns = NewsNormal()
        __returns.plain = plain
        __returns.author = plain.get("author")
        __returns.date = convert_time(plain.get("date"))
        __returns.des = plain.get("des")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        __returns.cover = plain.get("cover")
        return __returns


class NewsResult():
    """资讯搜索结果模型

    这是一个遵照BaiduSpider资讯搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[NewsNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (List): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results: List[NewsNormal] = []
        self.pages: int = 0
        self.total: int = 0
        self.plain: List[Dict] = []

    @staticmethod
    def _build_instance(plain: List, pages: int, total: int) -> "NewsResult":
        __returns = NewsResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(NewsNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Optional[NewsNormal]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object NewsResult>"
