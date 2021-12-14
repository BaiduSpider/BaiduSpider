"""搜索词预测模型类型注释文件

此模块中定义了所有现有搜索词预测模块内所有结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime
from typing import List, Union


class TiebaPredictorResult(object):
    """贴吧搜索搜索结果预测结果模型类型注释类。

    详见`baiduspider.predictor.models.TiebaPredictorResult`类。
    """

    def __init__(self) -> None:
        self.classifiers: List[str]
        self.cover: str
        self.desc: str
        self.members: int
        self.name: str
        self.threads: int
