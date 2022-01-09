"""图片搜索返回值模型模块

此文件定义的所有现有的图片搜索返回值模型并编写了自动构建函数。
"""
from typing import Union

from baiduspider.models.typings.typings_pic import *


class PicNormal(PicNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider图片搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        host (str): 图片来源域名
        title (str): 图片标题
        url (str): 图片链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.host = ""
        self.title = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> PicNormal:
        __returns = PicNormal()
        __returns.plain = plain
        __returns.host = plain.get("host")
        __returns.title = plain.get("title")
        __returns.url = plain.get("url")
        return __returns


class PicResult(PicResult):
    """图片搜索结果模型

    这是一个遵照BaiduSpider图片搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[PicNormal]): 普通搜索结果列表
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
    def _build_instance(plain: list, pages: int, total: int) -> PicResult:
        __returns = PicResult()
        __returns.plain = plain
        __returns.pages = pages
        __returns.total = total
        for p in plain:
            __returns.results.append(PicNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Union[PicNormal, None]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object PicResult>"
