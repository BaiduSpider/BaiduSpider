"""搜索词预测模型类型注释文件

此文件定义了所有现有的搜索词预测模块内返回值模型并编写了自动构建函数。
"""
from typing import Union
from baiduspider.predictor.models.typings import TiebaPredictorResult


def get_attr(d: dict, t: str):
    """获取字典`d`下的`t`"""
    try:
        return d[t]
    except:
        return None


class TiebaPredictorResult(TiebaPredictorResult):
    """贴吧搜索搜索结果预测结果模型类型注释类。

    这是一个遵照BaiduSpider百科搜索结果结果预测模型创建的返回模型类。

    Attributes:
        classifiers (List[str]): 预测结果类别分类
        cover (str): 预测结果封面图片URL
        desc (str): 预测结果介绍
        members (int): 预测结果成员数
        name (str): 预测结果名称
        threads (int): 预测结果帖子数
        plain (list): 源预测结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.classifiers = []
        self.cover = ""
        self.desc = ""
        self.members = 0
        self.name = ""
        self.threads = 0
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> TiebaPredictorResult:
        __returns = TiebaPredictorResult()
        __returns.plain = plain
        __returns.classifiers = get_attr(plain, "classifiers")
        __returns.cover = get_attr(plain, "cover")
        __returns.desc = get_attr(plain, "desc")
        __returns.members = get_attr(plain, "members")
        __returns.name = get_attr(plain, "name")
        __returns.threads = get_attr(plain, "threads")
        return __returns

    def __repr__(self) -> str:
        return "<object TiebaPredictorResult>"
