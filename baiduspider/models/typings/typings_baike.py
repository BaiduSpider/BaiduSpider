"""百科搜索结果模型类型注释文件

此模块中定义了所有现有百科搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Union


class BaikeNormal(object):
    """百科搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.baike.BaikeNormal`类。
    """

    def __init__(self) -> None:
        self.upd_date: Union[datetime, None]
        self.des: str
        self.title: str
        self.url: str
        self.plain: dict


class BaikeResult(object):
    """百科搜索结果模型类型注释类。

    详见`baiduspider.models.baike.BaikeResult`类。
    """

    def __init__(self) -> None:
        self.results: List[BaikeNormal]
        self.total: int
