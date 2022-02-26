"""百科搜索返回值模型模块

此文件定义的所有现有的百科搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime
from typing import Dict, List, Optional

from baiduspider.models import convert_time


class BaikeNormal():
    """普通搜索结果模型

    这是一个遵照BaiduSpider百科搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        upd_date (Optional[datetime]): 百科更新时间
        des (str): 百科简介
        title (str): 百科标题
        url (str): 百科链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.upd_date: Optional[datetime] = None
        self.des: str = ""
        self.title: str = ""
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: dict) -> "BaikeNormal":
        __returns = BaikeNormal()
        __returns.plain = plain
        __returns.upd_date = convert_time(plain.get("upd_date"))
        __returns.des = plain.get("des")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class BaikeResult():
    """百科搜索结果模型

    这是一个遵照BaiduSpider百科搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[BaikeNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (List[Dict]): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results: List[BaikeNormal] = []
        self.pages: int = 0
        self.total: int = 0
        self.plain: List[Dict] = []

    @staticmethod
    def _build_instance(plain: list, total: int) -> "BaikeResult":
        __returns = BaikeResult()
        __returns.plain = plain
        __returns.total = total
        for p in plain:
            __returns.results.append(BaikeNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Optional[BaikeNormal]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object BaikeResult>"
