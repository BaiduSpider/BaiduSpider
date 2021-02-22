"""
新的测试
"""

import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath("."))


class SpiderTestCase(TestCase):
    """
    BaiduSpider的测试
    """

    def setUp(self):
        from baiduspider import BaiduSpider

        self.spider = BaiduSpider()

    def test_search_web(self):
        for pn in range(1, 10):
            python = self.spider.search_web("python", exclude=["tieba"], pn=pn)
            total = False
            # print(python)
            for i in python["results"]:
                # 开始判断各项数据是否合规
                if i["type"] == "total":
                    total = "total" in python  # 结果里有两个total
                    self.assertTrue(type(i["result"]) == int)
                elif i["type"] == "related":
                    self.assertEqual(type(i["results"]), list)
                elif i["type"] == "calc":
                    self.assertIn("process", i)
                elif i["type"] == "news":
                    self.are_in(["author", "time", "title", "url", "des"], i["results"])
                elif i["type"] == "video":
                    self.are_in(
                        ["cover", "origin", "length", "url", "title"], i["results"]
                    )
                elif i["type"] == "baike":
                    self.are_in(
                        ["cover", "cover-type", "des", "url", "title"], i["result"]
                    )
                elif i["type"] == "blog":
                    self.are_in(["blogs", "url", "title"], i["result"])
                elif i["type"] == "gitee":
                    self.are_in(
                        [
                            "star",
                            "fork",
                            "watch",
                            "url",
                            "title",
                            "license",
                            "lang",
                            "status",
                        ],
                        i["result"],
                    )
                elif i["type"] == "result":
                    self.are_in(["des", "origin", "title", "url"], i)
                else:
                    self.assertTrue(False)
                # print(i['type'])
                self.assertNotEqual(i["type"], "tieba")
            self.assertTrue(total)

    def test_search_pic(self):
        python = self.spider.search_pic("python")
        self.assertIn("total", python)
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.assertTrue(i["title"])
            self.assertTrue(i["url"])
            self.assertIn("host", i)

    def test_search_video(self):
        python = self.spider.search_video("python")
        self.assertIn("total", python)
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.assertTrue(i["title"])
            self.assertTrue(i["url"])
            self.assertIn("img", i)
            self.assertIn("time", i)

    def test_search_news(self):
        python = self.spider.search_news("python")
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.are_in(["author", "des", "date", "title", "url"], i)

    def test_search_wenku(self):
        try:
            python = self.spider.search_wenku("python")
            self.assertEqual(type(python["total"]), int)
            for i in python["results"]:
                self.are_in(
                    ["downloads", "pages", "date", "des", "title", "url", "type"], i
                )
        except UnboundLocalError:
            pass

    def test_search_jingyan(self):
        python = self.spider.search_jingyan("python")
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.are_in(["title", "url", "des", "date", "category", "votes"], i)

    def test_search_baike(self):
        python = self.spider.search_baike("python")
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.are_in(["title", "des", "date", "url"], i)

    def test_zhidao(self):
        python = self.spider.search_zhidao("python")
        self.assertEqual(type(python["total"]), int)
        for i in python["results"]:
            self.are_in(["title", "des", "date", "url", "count"], i)

    def are_in(self, members: list, container: list):
        for i in members:
            self.assertIn(i, container)


'''
def structure(to_be_compare, sample):
    """
    结构比较
    好吧做了半小时发现没用
    """
    if sample in (int, str, dict, tuple, list, bool):  # 如果指定类型
        return type(to_be_compare) == sample  # 那么比较类型
    elif type(sample) in (str, bool, int):  # 否则如果样本是一些简单的类型
        return to_be_compare == sample  # 直接比较
    # 如果是其它的容器，那么就得细细比较每个元素
    if type(sample) == dict:  # 比如字典，就得比较键是一致的
        to_be_compare: dict
        sample: dict
        flag = to_be_compare.keys() == sample.keys()
        if not flag:
            return False
        for i in sample.keys():
            flag = flag and structure(to_be_compare[i], sample[i])  # 并且每个元素的结构也相同
        return flag
    if type(sample) in (list, tuple):
        # if len(sample) != len(to_be_compare):
        #    return False
        flag = True
        for i in range(len(sample)):
            flag = flag and structure(to_be_compare[i], sample[i])
'''
