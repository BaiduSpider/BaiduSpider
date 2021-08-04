"""BaiduSpider移动端爬虫"""
import datetime
import time as time_lib
from time import mktime, strptime, time
from typing import Tuple, Union
from urllib.parse import SplitResult, quote

import requests
from bs4 import BeautifulSoup

from baiduspider._spider import BaseSpider
from baiduspider.mobile.parser import MobileParser
from baiduspider.mobile.models.web import WebResult


__all__ = ["BaiduMobileSpider"]


class BaiduMobileSpider(BaseSpider):
    def __init__(self) -> None:
        """爬取百度移动端的搜索结果.

        本类的所有成员方法都遵循下列格式：

            {
                'results': <一个列表，表示搜索结果，内部的字典会因为不同的成员方法而改变>,
                'total': <一个正整数，表示搜索结果的最大页数，可能会因为搜索结果页码的变化而变化，因为百度不提供总共的搜索结果页数>
            }

        目前仅支持百度网页搜索的部分内容爬取，返回的搜索结果无广告。继承自``BaseSpider``。

        BaiduMobileSpider.`search_web(self: BaiduMobileSpider, query: str, pn: int = 1) -> WebResult`: 移动端百度网页搜索
        """
        super().__init__()
        # 爬虫名称（不是请求的，只是用来表识）
        self.spider_name = "BaiduSpider"
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
            "Referer": "https://m.baidu.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        self.parser = MobileParser()
        self.EMPTY = {"results": []}

    def search_web(self, query: str, pn: int = 1, proxies: dict = None) -> WebResult:
        """搜索百度移动端网页搜索结果。

        - 基本使用：
            ```python
            BaiduMobileSpider().search_web('搜索词')
            ```

        - 带页码：
            ```python
            BaiduMobileSpider().search_web('搜索词', pn=2)
            ```

        - 设置代理：
            ```python
            BaiduMobileSpider().search_web('搜索词', proxies={
                "http": "http://xxx.xxx.xxx:xxxx",  # HTTP代理
                "https": "https://xxx.xxx.xxx:xxxx"  # HTTPS代理
            })
            ```
            详细配置请参考[requests文档](https://docs.python-requests.org/zh_CN/latest/user/advanced.html?highlight=proxies#proxies)。

        Args:
            query (str): 要爬取的搜索词.
            pn (int, optional): 爬取的页码. Defaults to 1.
            proxies (Union[dict, None]): 代理配置. Defaults to None.

        Returns:
            WebResult: 爬取的返回值和搜索结果
        """
        error = None
        try:
            text = quote(query, "utf-8")
            url = "https://m.baidu.com/s?word=%s&pn=%d" % (text, ((pn - 1) * 10))
            content = self._get_response(url, proxies)
            results = self.parser.parse_web(content)
        except Exception as err:
            error = err
        finally:
            self._handle_error(error, "BaiduSpider", "parse-web")
        return WebResult._build_instance(results["results"], query)
