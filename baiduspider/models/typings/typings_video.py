"""视频搜索结果模型类型注释文件

此模块中定义了所有现有视频搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime, time
from typing import List, Union


class VideoNormal(object):
    """视频搜索普通搜索结果模型类型注释类。

    详见`baiduspider.models.video.VideoNormal`类。
    """

    def __init__(self) -> None:
        self.img: str
        self.length: time
        self.pub_time: datetime
        self.title: str
        self.url: str
        self.des: Union[str, None]
        self.origin: Union[str, None]
        self.plain: dict


class VideoResult(object):
    """视频搜索结果模型类型注释类。

    详见`baiduspider.models.video.VideoResult`类。
    """

    def __init__(self) -> None:
        self.results: List[VideoNormal]
        self.is_last: bool
