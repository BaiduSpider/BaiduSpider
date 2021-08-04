"""图片搜索结果模型类型注释文件

此模块中定义了所有现有图片搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from typing import List


class PicNormal(object):
    """图片搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.pic.PicNormal`类。
    """

    def __init__(self) -> None:
        self.host: str
        self.title: str
        self.url: str
        self.plain: dict


class PicResult(object):
    """图片搜索结果模型类型注释类。

    详见`baiduspider.models.pic.PicResult`类。
    """

    def __init__(self) -> None:
        self.results: List[PicNormal]
        self.pages: int
        self.total: int
