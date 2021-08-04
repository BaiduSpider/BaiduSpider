"""经验搜索结果模型类型注释文件

此模块中定义了所有现有经验搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Union


class JingyanPublisher(object):
    """经验搜索文档发布者模型类型注释类。

    详见`baiduspider.models.jingyan.JingyanPublisher`类。
    """

    def __init__(self) -> None:
        self.name: str
        self.url: str


class JingyanNormal(object):
    """经验搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.jingyan.JingyanNormal`类。
    """

    def __init__(self) -> None:
        self.title: str
        self.url: str
        self.des: str
        self.pub_date: datetime
        self.category: List[str]
        self.votes: int
        self.publisher: JingyanPublisher
        self.is_original: bool
        self.is_outstanding: bool
        self.plain: dict


class JingyanResult(object):
    """经验搜索结果模型类型注释类。

    详见`baiduspider.models.jingyan.JingyanResult`类。
    """

    def __init__(self) -> None:
        self.results: List[JingyanNormal]
        self.pages: int
        self.total: int
