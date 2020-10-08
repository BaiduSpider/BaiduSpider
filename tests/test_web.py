"""测试BaiduSpider的网页搜索函数

本测试案例用于测试`BaiduSpider.search_web`及其实现函数。
"""
import os
import sys
from unittest import TestCase
import requests


class WebTestCase(TestCase):
    def __init__(self, methodName):
        """测试网页搜索

        本测试用于测试BaiduSpider.`search_web`
        """
        super().__init__(methodName)

    def setUp(self):
        # 导入包
        sys.path.append(os.path.abspath('.'))
        from baiduspider import BaiduSpider
        from baiduspider.errors import ParseError, UnknownError
        self.spider = BaiduSpider()
        self.assets_base_url = 'https://cdn.jsdelivr.net/gh/BaiduSpider/BaiduSpiderTestAssets@master/web'
        self.normal_res = {
            'title': 'Welcome to Python.org',
            'des': 'The official home of the Python Programming Language... # Python 3: Simple output (with Unicode) >>> print("Hello, I\'m Python!") Hello, I\'m Python!',
            'url': 'http://www.baidu.com/link?url=yC-vpJc3cGCINc7SrFvV0A5-mBa3lrOseRMxZzZxXmlh1TqtxC8jgrOPHgSJi7_O',
            'time': None,
            'type': 'result',
            'origin': 'www.python.org/'
        }
        self.video_res = {
            'title': 'python在excel中神运用,亮瞎眼的操作哦',
            'url': 'https://baijiahao.baidu.com/s?id=1659418735845772463&wfr=content',
            'cover': 'https://vdposter.bdstatic.com/5ecdac23471e6248259e256427ea66c3.jpeg?x-bce-process=image/resize,m_fill,w_242,h_182/format,f_jpg/quality,Q_100',
            'length': '05:41',
            'origin': '好看视频'
        }
        self.news_res = {
            'author': '国际在线',
            'time': '9分钟前',
            'title': '特朗普确诊新冠!',
            'url': 'http://www.baidu.com/link?url=_APr4uGsSQzeq7MRkeoxLZlS6TfL8np6zzDnQqVuM9_Kwby5rypESvXHhX5ByEBChsusU4ZO_0p4smy0iz4iP0Kh2QsACY9s1_Fa1YACavW',
            'des': None
        }
        self.baike_img_res = {
            'title': 'Python(计算机程序设计语言)_百度百科',
            'des': 'Python是一种跨平台的计算机程序设计语言。 是一个高层次的结合了解释性、编译性、互动性和面向对象的脚本语言。最初被设计用于编写自动化脚本(shell)，随着版本的不断更新和语言...',
            'cover': 'https://dss0.bdstatic.com/6Ox1bjeh1BF3odCf/it/u=783017482,219941889&fm=74&app=80&f=JPEG&size=f121,90?sec=1880279984&t=b639fbc82a72772a726d11888a54d8f6',
            'cover-type': 'image',
            'url': 'http://www.baidu.com/link?url=Clp7kAWYKDauuI0IomD4-yj3EPlzvzhtUsU8eODlD2b6rCmZ0R1mH3RgeuVxJ0QerYWOj1f2cI3gvqJPnDiaNa'
        }
        self.baike_video_res = {
            'title': '我(汉语汉字)_百度百科',
            'des': '我，汉语常用字，读作wǒ，最早见于甲骨文，其甲骨文本义指奴隶社会里一种用来行刑杀人和肢解牲口的凶器，后由本义衍生出“手持大戉，呐喊示威”等意；但到了战国时代，“我”字本义所代表的凶器被后起的更优良的凶器淘汰，于是“我”字在汉...',
            'cover': 'http://www.baidu.com/link?url=6VGNfYIuPl2uh-HOGwQnK04K4WL2MICdv6ZpoEIhhgxAUanK2l1aTp_6oC51mpYh8LKEem911tdb4pgp3fNK3UN6GPDqFg-iXcmj9aHzQ4xEodjoO0fsgst1Mf3XAW_DW4idF_QXDhBW_R-vskbcZK',
            'cover-type': 'video',
            'url': 'http://www.baidu.com/link?url=2_SPS_eUtRUiJS3eT5pvwHmstP1QBW8YXGzDxc3QRRb0xqWBNkIRbL-S8isFYHztETZv59iF_iDPV5ognLjNna'
        }
        self.baike_none_res = {
            'title': 'ASTM A106无缝钢管_百度百科',
            'des': 'ASTM A106无缝钢管是属于美标的无缝钢管，材质是普通碳钢系列。',
            'cover': None,
            'cover-type': None,
            'url': 'http://www.baidu.com/link?url=uLJ0kfXAXVu14FztaB4KMU7N4yN5lJikkRBI3b8LeUGGCn-8UoyHbYjo1jyXpVEB95B3htArzho5yreAGJS0SElyhz1euRHtbIb8hzpLESe_Q3Zqrt-U8RJARsapbJ4WLSxyjusGQK-ft_Xflkboz_'
        }
        self.calc_res = {
            'process': '20^5+107*13',
            'result': '3 201 391',
            'type': 'calc'
        }
        self.related_res = ['python有什么用', 'python为什么叫爬虫', 'python教程',
                            'Python官网', 'python爬虫教程', 'python和java', 'Python代码',
                            'Python软件', 'Python3']
        self.pages_res = 10
        self.pages_single_res = 1
        self.total_res = 74700000
        self.invalid_res = ParseError
        self.spider_invalid_param_res = ParseError
        self.spider_unknown_error_res = UnknownError
        self.no_related_res = []
        self.no_pager_res = 1

    def __get_asset(self, name):
        return requests.get('{base_url}/test_web_{name}.html'.format(base_url=self.assets_base_url, name=name)).text

    def test_normal_result(self):
        """测试普通搜索结果"""
        asset = self.__get_asset('normal')
        result = self.spider.parser.parse_web(asset)
        self.assertIn(self.normal_res, result['results'])

    def test_video_result(self):
        """测试视频搜索结果"""
        asset = self.__get_asset('video')
        result = self.spider.parser.parse_web(asset)
        res = []
        for r in result['results']:
            if r['type'] == 'video':
                res = r
                break
        self.assertIn(self.video_res, res['results'])

    def test_news_result(self):
        """测试资讯搜索结果"""
        asset = self.__get_asset('news')
        result = self.spider.parser.parse_web(asset)
        res = []
        for r in result['results']:
            if r['type'] == 'news':
                res = r
                break
        self.assertIn(self.news_res, res['results'])

    def test_baike_img_result(self):
        """测试百科封面类型为图片的搜索结果"""
        asset = self.__get_asset('baike-img')
        result = self.spider.parser.parse_web(asset)
        res = {}
        for r in result['results']:
            if r['type'] == 'baike':
                res = r
                break
        self.assertEqual(self.baike_img_res, res['result'])

    def test_baike_video_result(self):
        """测试百科封面类型为视频的搜索结果"""
        asset = self.__get_asset('baike-video')
        result = self.spider.parser.parse_web(asset)
        res = {}
        for r in result['results']:
            if r['type'] == 'baike':
                res = r
                break
        self.assertEqual(self.baike_video_res, res['result'])

    def test_baike_none_result(self):
        """测试百科封面类型为空的搜索结果"""
        asset = self.__get_asset('baike-none')
        result = self.spider.parser.parse_web(asset)
        res = {}
        for r in result['results']:
            if r['type'] == 'baike':
                res = r
                break
        self.assertEqual(self.baike_none_res, res['result'])

    def test_calc_result(self):
        """测试运算搜索结果"""
        asset = self.__get_asset('calc')
        result = self.spider.parser.parse_web(asset)
        res = {}
        for r in result['results']:
            if r['type'] == 'calc':
                res = r
                break
        self.assertEqual(self.calc_res, res)

    def test_related_result(self):
        """测试相关搜索结果"""
        asset = self.__get_asset('related')
        result = self.spider.parser.parse_web(asset)
        res = []
        for r in result['results']:
            if r['type'] == 'related':
                res = r
                break
        self.assertEqual(self.related_res, res['results'])

    def test_result_pages(self):
        """测试搜索结果页数"""
        asset = self.__get_asset('pages')
        result = self.spider.parser.parse_web(asset)
        self.assertEqual(self.pages_res, result['pages'])

    def test_result_pages_single(self):
        """测试搜索结果仅有一页的页数"""
        asset = self.__get_asset('pages-single')
        result = self.spider.parser.parse_web(asset)
        self.assertEqual(self.pages_single_res, result['pages'])

    def test_result_total(self):
        """测试总计搜索结果数"""
        asset = self.__get_asset('total')
        result = self.spider.parser.parse_web(asset)
        res = 0
        for r in result['results']:
            if r['type'] == 'total':
                res = r
                break
        self.assertEqual(self.total_res, res['result'])

    def test_invalid_template(self):
        """测试无效的HTML对网页搜索的影响"""
        asset = self.__get_asset('invalid')
        self.assertRaises(self.invalid_res,
                          self.spider.parser.parse_web, asset)

    def test_spider_request(self):
        """测试爬虫获取网页"""
        result = self.spider.search_web('Python')
        self.assertIsNotNone(result['results'])

    def test_spider_invalid_param(self):
        """测试无效参数对网页搜索的影响"""
        self.assertRaises(self.spider_invalid_param_res,
                          self.spider.search_web, '')

    def test_spider_unknown_error(self):
        """测试未知错误对网页搜索的影响"""
        self.assertRaises(self.spider_unknown_error_res,
                          self.spider.search_web, 123)
    
    def test_no_related(self):
        """测试没有相关搜索结果对网页搜索的影响"""
        asset = self.__get_asset('no_related')
        result = self.spider.parser.parse_web(asset)
        res = []
        for r in result['results']:
            # 此判断不应该通过
            if r['type'] == 'related':  # pragma: no cover
                res = r
                break
        self.assertEqual(self.no_related_res, res)
    
    def test_no_pager(self):
        """测试没有分页的搜索结果对爬虫对影响"""
        asset = self.__get_asset('no_pager')
        result = self.spider.parser.parse_web(asset)
        res = result['pages']
        self.assertEqual(self.no_pager_res, res)
