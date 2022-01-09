"""知道搜索返回值模型模块

此文件定义的所有现有的知道搜索返回值模型并编写了自动构建函数。
"""
from typing import Union

from baiduspider.models import convert_time
from baiduspider.models.typings.typings_zhidao import *


class ZhidaoNormal(ZhidaoNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider知道搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        agree (int): 回答赞同数
        answer (str | None): 回答简介
        answerer (str): 回答者
        count (int | None): 回答总数
        date (datetime.datetime): 回答发布日期
        title (str): 问题标题
        question (str | None): 问题简介
        url (str): 问题链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.date = None
        self.answer = None
        self.question = None
        self.answerer = ""
        self.count = None
        self.title = ""
        self.agree = 0
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> ZhidaoNormal:
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
        plain (list): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.pages = 0
        self.total = 0
        self.plain = []

    @staticmethod
    def _build_instance(plain: list, pages: int, total: int) -> ZhidaoResult:
        __returns = ZhidaoResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(ZhidaoNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Union[ZhidaoNormal, None]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object ZhidaoResult>"
