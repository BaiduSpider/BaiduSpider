"""知道搜索返回值模型模块

此文件定义的所有现有的知道搜索返回值模型并编写了自动构建函数。
"""
from datetime import datetime
from typing import Dict, List, Optional

from baiduspider.models import convert_time


class ZhidaoNormal(ZhidaoNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider知道搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        agree (int): 回答赞同数
        answer (Optional[str]): 回答简介
        answerer (str): 回答者
        count (Optional[int]): 回答总数
        date (datetime.datetime): 回答发布日期
        title (str): 问题标题
        question (Optional[str]): 问题简介
        url (str): 问题链接
        plain (Dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.date: Optional[datetime] = None
        self.answer: Optional[str] = None
        self.question: Optional[str] = None
        self.answerer: str = ""
        self.count: Optional[int] = None
        self.title: str = ""
        self.agree: int = 0
        self.url: str = ""
        self.plain: Dict = {}

    @staticmethod
    def _build_instance(plain: Dict) -> "ZhidaoNormal":
        __returns = ZhidaoNormal()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.question = plain.get("question")
        __returns.answer = plain.get("answer")
        __returns.count = plain.get("count")
        __returns.agree = plain.get("agree")
        __returns.answerer = plain.get("answerer")
        __returns.date = convert_time(plain.get("date"))
        __returns.url = plain.get("url")
        return __returns


class ZhidaoResult(ZhidaoResult):
    """知道搜索结果模型

    这是一个遵照BaiduSpider知道搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[ZhidaoNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        total (int): 搜索结果总数
        plain (List): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results: List[ZhidaoNormal] = []
        self.pages: int = 0
        self.total: int = 0
        self.plain: List[Dict] = []

    @staticmethod
    def _build_instance(plain: List, pages: int, total: int) -> "ZhidaoResult":
        __returns = ZhidaoResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(ZhidaoNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Optional[ZhidaoNormal]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object ZhidaoResult>"
