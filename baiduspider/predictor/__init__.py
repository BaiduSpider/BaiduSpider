import json
from typing import List

from baiduspider._spider import BaseSpider
from baiduspider.predictor.models import TiebaPredictorResult


class BaiduPredictor(BaseSpider):
    """百度搜索词预测

    本模块爬取百度的搜索词预测部分信息，按照百度提供的默认预测顺序排序，给出百度的搜索词预测
    """

    def __init__(self) -> None:
        super().__init__()
        self.spider_name = "BaiduPredictor"

    def predict_web(self, query: str) -> List[str]:
        """百度网页搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[str]: 百度网页搜索搜索词预测
        """
        data = json.loads(
            self._get_response(
                f"https://www.baidu.com/sugrec?ie=utf-8&json=1&prod=pc&from=pc_web&wd={query}"
            )
        )
        ret = [i["q"] for i in data["g"]]
        if "g" not in data:
            return [data["q"]]
        return ret

    def predict_news(self, query: str) -> List[str]:
        """百度资讯搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[str]: 百度资讯搜索搜索词预测
        """
        data = json.loads(
            self._get_response(f"http://news.baidu.com/sn/api/sug?wd={query}&prod=news")
        )
        return data["data"]

    def predict_pic(self, query: str) -> List[str]:
        """百度图片搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[str]: 百度图片搜索搜索词预测
        """
        data = json.loads(
            self._get_response(
                f"https://www.baidu.com/sugrec?ie=utf-8&wd={query}&prod=open_image"
            )
        )
        ret = [i["q"] for i in data["g"]]
        if "g" not in data:
            return [data["q"]]
        return ret

    def predict_wenku(self, query: str) -> List[str]:
        """百度文库搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[str]: 百度文库搜索搜索词预测
        """
        data = json.loads(
            self._get_response(
                f"https://www.baidu.com/sugrec?prod=open_wenku&wd={query}"
            )
        )
        ret = [i["q"] for i in data["g"]]
        if "g" not in data:
            return [data["q"]]
        return ret

    def predict_zhidao(self, query: str) -> List[str]:
        """百度知道搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[str]: 百度知道搜索搜索词预测
        """
        data = json.loads(
            self._get_response(
                f"https://www.baidu.com/sugrec?wd={query}&prod=open_zhidao"
            )
        )
        if "g" not in data:
            return [data["q"]]
        ret = [i["q"] for i in data["g"]]
        return ret

    def predict_tieba(self, query: str) -> List[TiebaPredictorResult]:
        """百度贴吧搜索搜索词预测

        Args:
            query (str): 要预测的部分搜索词

        Returns:
            List[TiebaPredictorResult]: 百度贴吧搜索搜索词预测
        """
        data = json.loads(
            self._get_response(
                f"https://tieba.baidu.com/suggestion?query={query}&ie=utf-8"
            )
        )
        if not data["query_match"]["search_data"]:
            return []
        ret = [
            {
                "name": i["fname"],
                "cover": i["fpic"],
                "members": i["member_num"],
                "threads": i["thread_num"],
                "classifiers": [i["fclass1"], i["fclass2"]],
                "desc": i["forum_desc"],
            }
            for i in data["query_match"]["search_data"]
        ]
        return ret
