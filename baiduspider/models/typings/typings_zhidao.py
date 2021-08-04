"""知道搜索结果模型类型注释文件

此模块中定义了所有现有知道搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Union


class ZhidaoNormal(object):
    """知道搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.zhidao.ZhidaoNormal`类。
    """

    def __init__(self) -> None:
        self.count: Union[int, None]
        self.date: Union[datetime, None]
        self.answer: Union[str, None]
        self.question: Union[str, None]
        self.agree: int
        self.answerer: str
        self.title: str
        self.url: str
        self.plain: dict


class ZhidaoResult(object):
    """知道搜索结果模型类型注释类。

    详见`baiduspider.models.zhidao.ZhidaoResult`类。
    """

    def __init__(self) -> None:
        self.results: List[ZhidaoNormal]
        self.pages: int
        self.total: int
