import os
import sys
from unittest import TestCase

sys.path.append(os.path.abspath('.'))


class BaiduSpiderOtherTestCase(TestCase):
    def setUp(self) -> None:
        from baiduspider import BaiduSpider
        self.spider = BaiduSpider()

    def test_calc(self):
        result = self.spider.search_web('12345679*9')
        flag = False
        for i in result['results']:
            if i['type'] == 'calc':
                print(i['process'])
                print(i['result'])
                flag = True
        self.assertTrue(flag)

    def test_tieba(self):
        result = self.spider.search_web('python吧')
        for i in result['results']:
            if i['type'] == 'tieba':
                self.are_in(['title', 'des', 'cover', 'url', 'followers', 'hot', 'total'], i['result'])
            elif i['type'] == 'result':
                self.are_in(['des', 'origin', 'title', 'url'], i)

    def test_video(self):
        result = self.spider.search_web('视频')
        print(result)
        for i in result['results']:
            if i['type'] == 'result':
                self.are_in(['des', 'origin', 'title', 'url'], i)
            elif i['type'] == 'tieba':
                self.are_in(['title', 'des', 'cover', 'url', 'followers', 'hot', 'total'], i['result'])
            elif i['type'] == 'video':
                self.are_in(['length', 'origin', 'title', 'url'], i['results'][0])

    def test_news(self):
        result = self.spider.search_web('今日新闻')
        for i in result['results']:
            if i['type'] == 'news':
                self.are_in(['author', 'time', 'title', 'url', 'des'], i['results'][0])

    def test_exclude_all(self):
        result = self.spider.search_web('python', exclude=['all'])
        for i in result['results']:
            self.assertIn(i['type'], ['result', 'total'])

    def test_page(self):
        result = self.spider.search_web('ocaiueno')
        print(result)
        result = self.spider.search_web('774f43c6744b47de98b1661d2344490b3761829a', pn=100)
        print(result)

    def are_in(self, members: list, container: list):
        for i in members:
            self.assertIn(i, container)

