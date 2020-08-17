import sys
import os
# 导入包
sys.path.append(os.path.abspath('./baiduspider/core'))
from baiduspider.core.main import BaiduSpider
from unittest import TestCase
from unittest.util import safe_repr


class WebTestCase(TestCase):
    def __init__(self, methodName):
        """测试网页搜索

        本测试用于测试BaiduSpider.`search_web`
        """
        super().__init__(methodName)

    def setUp(self):
        self.spider = BaiduSpider()
        self.normal_query = 'Python'
        self.normal_res = {
            'title': 'python官方网站 - Welcome toPython.org',
            'des': 'The official home of thePythonProgramming Language... #Python3: Simple output (with Unicode) >>> print("Hello, I\'mPython!") Hello, I\'mPython!',
            'url': None,
            'time': None,
            'type': 'result',
            'origin': 'www.python.org/',
        }
        self.video_query = '1+1'
        self.video_res = {
            'title': '这么简单的数学题1+1等于多少1+2等于多少都答错,真的是好搞笑啊',
            'url': 'https://baijiahao.baidu.com/s?id=1636752055718346803&wfr=content',
            'cover': 'https://vdposter.bdstatic.com/30f7291aaa82ca09f05a273ba0f199a9.jpeg?x-bce-process=image/resize,m_fill,w_256,h_170/format,f_jpg/quality,Q_100',
            'length': '01:12',
            'origin': '好看视频'
        }
        self.baike_query = 'Python'
        self.baike_res = {
            'title': 'Python(计算机程序设计语言) - 百度百科',
            'des': 'Python是一种跨平台的计算机程序设计语言。 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言新功能的添加，越多被用于独立的、大型项目的开发。',
            'cover': 'https://dss0.bdstatic.com/6Ox1bjeh1BF3odCf/it/u=783017482,219941889&fm=74&app=80&f=JPEG&size=f121,121?sec=1880279984&t=a1d51ad46dbc4f05dde70b250aff0afd',
            'cover-type': 'image',
            'url': None
        }
        self.calc_query = '20*4+5'
        self.calc_res = {
            'process': '20*4+5',
            'result': '85',
            'type': 'calc'
        }
        self.related_query = 'Python'
        self.related_res = ['python有什么用', 'python为什么叫爬虫', 'python教程',
                            'python爬虫教程', 'Python官网', 'Python代码', 'Python怎么读', 'Python软件', 'Python3']
        self.pages_query = 'Python'
        self.pages_res = 10
        self.total_query = 'Python'
        self.total_res = 75700000

    def assertIn(self, member, container, msg=None, test_url=False):
        """确认某个元素是否在数组中

        Args:
            member (any): 要检测的元素
            container (any): 要检测的列表
            msg (str, optional): 测试失败的信息. Defaults to None.
            test_url (bool, optional): 是否测试字典中的链接（字典的['url']）. Defaults to False.
        """
        if not test_url:
            for _ in container:
                try:
                    _['url'] = None
                except:
                    pass
        if member not in container:
            standardMsg = '%s not found in %s' % (safe_repr(member),
                                                  safe_repr(container))
            self.fail(self._formatMessage(msg, standardMsg))

    def test_normal_result(self):
        """测试普通搜索结果"""
        result = self.spider.search_web(self.normal_query)
        self.assertIn(self.normal_res, result['results'])

    def test_video_result(self):
        """测试视频搜索结果"""
        result = self.spider.search_web(self.video_query)
        res = []
        for r in result['results']:
            if r['type'] == 'video':
                res = r
                break
        self.assertIn(self.video_res, res['results'], test_url=True)

    def test_news_result(self):
        """测试资讯搜索结果"""
        # 资讯随时变化，无法测试
        pass

    def test_baike_result(self):
        """测试百科搜索结果"""
        result = self.spider.search_web(self.baike_query)
        res = {}
        for r in result['results']:
            if r['type'] == 'baike':
                res = r
                break
        res['result']['url'] = None
        self.assertEqual(self.baike_res, res['result'])

    def test_calc_result(self):
        """测试运算搜索结果"""
        result = self.spider.search_web(self.calc_query)
        res = {}
        for r in result['results']:
            if r['type'] == 'calc':
                res = r
                break
        self.assertEqual(self.calc_res, res)

    def test_related_result(self):
        """测试相关搜索结果"""
        result = self.spider.search_web(self.related_query)
        res = []
        for r in result['results']:
            if r['type'] == 'related':
                res = r
                break
        self.assertEqual(self.related_res, res['results'])

    def test_result_pages(self):
        """测试搜索结果页数"""
        result = self.spider.search_web(self.pages_query)
        self.assertEqual(self.pages_res, result['total'])

    def test_result_total(self):
        """测试总计搜索结果数"""
        result = self.spider.search_web(self.total_query)
        res = 0
        for r in result['results']:
            if r['type'] == 'total':
                res = r
                break
        self.assertEqual(self.total_res, res['result'])
