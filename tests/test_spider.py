"""
新的测试
"""

from unittest import TestCase

from baiduspider import BaiduSpider


class SpiderTestCase(TestCase):
    """
    BaiduSpider的测试
    """
    def setUp(self):
        self.spider = BaiduSpider()

    def test_search_web(self):
        for pn in range(1, 6):
            python = self.spider.search_web("python", exclude=['教程'], pn=pn)
            total = False
            for i in python['results']:
                # 开始判断各项数据是否合规
                if i['type'] == 'total':
                    total = 'total' in python   # 结果里有两个total
                    self.assertTrue(type(i['result']) == int)
                elif i['type'] == 'related':
                    self.assertEqual(type(i['results']), list)
                elif i['type'] == 'calc':
                    self.assertIn('process', i)
                elif i['type'] == 'news':
                    self.are_in(['author', 'time', 'title', 'url', 'des'])
                elif i['type'] == 'video':
                    self.are_in(['cover', 'origin', 'length', 'url', 'title'], i['results'])
                elif i['type'] == 'baike':
                    self.are_in(['cover', 'cover-type', 'des', 'url', 'title'], i['result'])
                elif i['type'] == 'blog':
                    self.are_in(['blogs', 'url', 'title'], i['result'])
                    # TODO: 结构检查得更精确一些
                elif i['type'] == 'gitee':
                    self.are_in(['star', 'fork', 'watch', 'url', 'title', 'license', 'lang', 'status'], i['result'])
                elif i['type'] == 'result':
                    self.are_in(['des', 'origin', 'title', 'url'], i)
            self.assertTrue(total)
            print(f'{pn}/5', end='\r')

    def are_in(self, members: list, container: list):
        for i in members:
            self.assertIn(i, container)

