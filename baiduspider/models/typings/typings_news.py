"""资讯搜索结果模型类型注释文件

此模块中定义了所有现有资讯搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Optional


class NewsNormal(object):
    """资讯搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.news.NewsNormal`类。
    """

    def __init__(self) -> None:
        self.author: str
        self.date: Optional[datetime]
        self.des: str
        self.title: str
        self.url: str
        self.cover: Optional[str]
        self.plain: dict


class NewsResult(object):
    """资讯搜索结果模型类型注释类。

    详见`baiduspider.models.news.NewsResult`类。
    """

    def __init__(self) -> None:
        self.results: List[NewsNormal]
        self.pages: int
        self.total: int
