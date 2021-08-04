"""文库搜索结果模型类型注释文件

此模块中定义了所有现有文库搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Union


class WenkuUploader(object):
    """文库搜索文档上传者模型类型注释类。

    详见`baiduspider.models.wenku.WenkuUploader`类。
    """

    def __init__(self) -> None:
        self.name: str
        self.url: str


class WenkuNormal(object):
    """文库搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.wenku.WenkuNormal`类。
    """

    def __init__(self) -> None:
        self.pub_date: datetime
        self.des: str
        self.downloads: int
        self.pages: int
        self.title: str
        self.type: str
        self.url: str
        self.quality: float
        self.uploader: WenkuUploader
        self.is_vip: bool
        self.plain: dict


class WenkuResult(object):
    """文库搜索结果模型类型注释类。

    详见`baiduspider.models.wenku.WenkuResult`类。
    """

    def __init__(self) -> None:
        self.results: List[WenkuNormal]
        self.pages: int
