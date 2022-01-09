"""文库搜索返回值模型模块

此文件定义的所有现有的文库搜索返回值模型并编写了自动构建函数。
"""
from typing import Union

from baiduspider.models import convert_time
from baiduspider.models.typings.typings_wenku import *


class WenkuUploader(WenkuUploader):
    """文档上传者模型

    这是一个遵照BaiduSpider文库搜索文档上传者结果模型创建的返回模型类。

    Attributes:
        name (str): 文档上传者用户名
        url (str): 文档上传者链接
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.name = ""
        self.url = ""
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WenkuUploader:
        __returns = WenkuUploader()
        __returns.plain = plain
        __returns.name = plain.get("name")
        __returns.url = plain.get("url")
        return __returns


class WenkuNormal(WenkuNormal):
    """普通搜索结果模型

    这是一个遵照BaiduSpider文库搜索基本搜索结果结果模型创建的返回模型类。

    Attributes:
        pub_date (datetime.datetime): 文档发布日期
        des (str): 文档简介
        downloads (int): 文档下载量
        pages (int): 文档页数
        title (str): 文档标题
        type (str): 文档格式，全部为大写字母
        url (str): 文档链接
        quality (float): 文档质量分
        uploader (WenkuUploader): 文档上传者信息
        is_vip (bool): 该文档是否需要VIP权限下载
        plain (dict): 源搜索结果字典
    """

    def __init__(self) -> None:
        super().__init__()
        self.pub_date = None
        self.des = ""
        self.downloads = 0
        self.pages = 0
        self.title = ""
        self.type = ""
        self.url = ""
        self.quality = 0.0
        self.uploader = None
        self.is_vip = False
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WenkuNormal:
        __returns = WenkuNormal()
        __returns.plain = plain
        __returns.title = plain.get("title")
        __returns.des = plain.get("des")
        __returns.downloads = plain.get("downloads")
        __returns.pages = plain.get("pages")
        __returns.type = plain.get("type")
        __returns.quality = plain.get("quality")
        __returns.uploader = WenkuUploader._build_instance(plain.get("uploader"))
        __returns.is_vip = plain.get("is_vip")
        __returns.pub_date = convert_time(plain.get("pub_date"))
        __returns.url = plain.get("url")
        return __returns


class WenkuResult(WenkuResult):
    """文库搜索结果模型

    这是一个遵照BaiduSpider文库搜索结果结果模型创建的返回模型类。

    Attributes:
        results (List[WenkuNormal]): 普通搜索结果列表
        pages (int): 搜索结果页数
        plain (list): 源搜索结果列表
    """

    def __init__(self) -> None:
        super().__init__()
        self.results = []
        self.pages = 0
        self.plain = []

    @staticmethod
    def _build_instance(plain: list, pages: int) -> WenkuResult:
        __returns = WenkuResult()
        __returns.plain = plain
        __returns.pages = pages
        for p in plain:
            __returns.results.append(WenkuNormal._build_instance(p))
        return __returns

    def __getitem__(self, key) -> Union[WenkuNormal, None]:
        return self.results[key]

    def __repr__(self) -> str:
        return "<object WenkuResult>"
