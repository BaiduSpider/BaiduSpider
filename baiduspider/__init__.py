"""BaiduSpider，爬取百度的利器

:Author: Sam Zhang
:Licence: MIT
:GitHub: https://github.com/samzhangjy
:GitLab: https://gitlab.com/samzhangjy

TODO: 完成文档
TODO: 添加更多爬虫
"""
import json
import os
import re
from html import unescape
from pprint import pprint
from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup

from baiduspider._spider import BaseSpider
from baiduspider.parser import Parser
from baiduspider.errors import ParseError, UnknownError

__all__ = ['BaiduSpider']


class BaiduSpider(BaseSpider):
    def __init__(self) -> None:
        """爬取百度的搜索结果

        本类的所有成员方法都遵循下列格式：

            {
                'results': <一个列表，表示搜索结果，内部的字典会因为不同的成员方法而改变>,
                'total': <一个正整数，表示搜索结果的最大页数，可能会因为搜索结果页码的变化而变化，因为百度不提供总共的搜索结果页数>
            }

        目前支持百度搜索，百度图片，百度知道，百度视频，百度资讯，百度文库，百度经验和百度百科，并且返回的搜索结果无广告。继承自``BaseSpider``。

        BaiduSpider.`search_web(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度网页搜索

        BaiduSpider.`search_pic(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度图片搜索

        BaiduSpider.`search_zhidao(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度知道搜索

        BaiduSpider.`search_video(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度视频搜索

        BaiduSpider.`search_news(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度资讯搜索

        BaiduSpider.`search_wenku(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度文库搜索

        BaiduSpider.`search_jingyan(self: BaiduSpider, query: str, pn: int = 1) -> dict`: 百度经验搜索

        BaiduSpider.`search_baike(self: BaiduSpider, query: str) -> dict`: 百度百科搜索
        """
        super().__init__()
        # 爬虫名称（不是请求的，只是用来表识）
        self.spider_name = 'BaiduSpider'
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Referer': 'https://www.baidu.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }
        self.parser = Parser()

    def search_web(self, query: str, pn: int = 1) -> dict:
        """百度网页搜索

        - 简单搜索：
            >>> BaiduSpider().search_web('搜索词')
            {
                'results': [
                    {
                        'result': int, 总计搜索结果数,
                        'type': 'total'  # type用来区分不同类别的搜索结果
                    },
                    {
                        'results': [
                            'str, 相关搜索建议',
                            '...',
                            '...',
                            '...',
                            ...
                        ],
                        'type': 'related'
                    },
                    {
                        'process': 'str, 算数过程',
                        'result': 'str, 运算结果',
                        'type': 'calc'
                        # 这类搜索结果仅会在搜索词涉及运算时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'results': [
                            {
                                'author': 'str, 新闻来源',
                                'time': 'str, 新闻发布时间',
                                'title': 'str, 新闻标题',
                                'url': 'str, 新闻链接',
                                'des': 'str, 新闻简介，大部分情况为None'
                            },
                            { ... },
                            { ... },
                            { ... },
                            ...
                        ],
                        'type': 'news'
                        # 这类搜索结果仅会在搜索词有相关新闻时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'results': [
                            {
                                'cover': 'str, 视频封面图片链接',
                                'origin': 'str, 视频来源',
                                'length': 'str, 视频时长',
                                'title': 'str, 视频标题',
                                'url': 'str, 视频链接'
                            },
                            { ... },
                            { ... },
                            { ... },
                            ...
                        ],
                        'type': 'video'
                        # 这类搜索结果仅会在搜索词有相关视频时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                                'cover': 'str, 百科封面图片/视频链接',
                                'cover-type': 'str, 百科封面类别，图片是image，视频是video',
                                'des': 'str, 百科简介',
                                'title': 'str, 百科标题',
                                'url': 'str, 百科链接'
                        },
                        'type': 'baike'
                        # 这类搜索结果仅会在搜索词有相关百科时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'result': {
                                'cover': 'str, 贴吧封面图片链接',
                                'des': 'str, 贴吧简介',
                                'title': 'str, 贴吧标题',
                                'url': 'str, 贴吧链接',
                                'followers': 'str, 贴吧关注人数（可能有汉字，如：1万）',
                                'hot': [{  # list, 热门帖子
                                    'clicks': 'str, 帖子点击总数',
                                    'replies': 'str, 帖子回复总数',
                                    'title': 'str, 帖子标题',
                                    'url': 'str, 帖子链接'
                                }],
                                'total': 'str, 贴吧总帖子数（可能有汉字，如：17万）'
                        },
                        'type': 'tieba'
                        # 这类搜索结果仅会在搜索词有相关贴吧时出现，不一定每个搜索结果都会出现的
                    },
                    {
                        'des': 'str, 搜索结果简介',
                        'origin': 'str, 搜索结果的来源，可能是域名，也可能是名称',
                        'time': 'str, 搜索结果的发布时间',
                        'title': 'str, 搜索结果标题',
                        'type': 'result',  # 正经的搜索结果
                        'url': 'str, 搜索结果链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 总计的搜索结果页数，可能会因为当前页数的变化而随之变化
            }

        - 带页码：
            >>> BaiduSpider().search_web('搜索词', pn=2)
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要爬取的query
            pn (int, optional): 爬取的页码. Defaults to 1.

        Returns:
            dict: 爬取的返回值和搜索结果
        """
        error = None
        try:
            text = quote(query, 'utf-8')
            url = 'https://www.baidu.com/s?wd=%s&pn=%d' % (text, (pn - 1) * 10)
            content = self._get_response(url)
            results = self.parser.parse_web(content)
        except Exception as err:
            error = err
        finally:
            self._handle_error(error)
        return {
            'results': results['results'],
            'total': results['pages']
        }

    def search_pic(self, query: str, pn: int = 1) -> dict:
        """百度图片搜索

        - 实例：
            >>> BaiduSpider().search_pic('搜索词')
            {
                'results': [
                    {
                        'host': 'str, 图片来源域名',
                        'title': 'str, 图片标题',
                        'url': 'str, 图片链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 搜索结果总计页码，可能会变化
            }

        - 带页码的搜索：
            >>> BaiduSpider().search_pic('搜索词', pn=2)
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要爬取的query
            pn (int, optional): 爬取的页码. Defaults to 1.

        Returns:
            dict: 爬取的搜索结果
        """
        error = None
        try:
            url = 'http://image.baidu.com/search/flip?tn=baiduimage&word=%s&pn=%d' % (
                quote(query), (pn - 1) * 20)
            content = self._get_response(url)
            result = self.parser.parse_pic(content)
        except Exception as err:
            error = err
        finally:
            self._handle_error(error)
        return {
            'results': result['results'],
            'total': result['pages']
        }

    def search_zhidao(self, query: str, pn: int = 1) -> dict:
        """百度知道搜索

        - 普通搜索：
            >>> BaiduSpider().search_zhidao('搜索词')
            {
                'results': [
                    {
                        'count': int, 回答总数,
                        'date': 'str, 发布日期',
                        'des': 'str, 简介',
                        'title': 'str, 标题',
                        'url': 'str, 链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 搜索结果最大页数，可能会变化
            }

        - 带页码的搜索：
            >>> BaiduSpider().search_zhidao('搜索词', pn=2)  # `pn` !!
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索结果的页码. Defaults to 1.

        Returns:
            dict: 搜索结果以及总页码
        """
        url = 'https://zhidao.baidu.com/search?pn=%d&word=%s' % (
            (pn - 1) * 10, quote(query))
        source = requests.get(url, headers=self.headers)
        # 转化编码
        source.encoding = 'gb2312'
        code = source.text
        bs = BeautifulSoup(self._minify(code), 'html.parser')
        # 所有搜索结果
        list_ = bs.find('div', class_='list').findAll('dl')
        results = []
        for item in list_:
            # 屏蔽企业回答
            if 'ec-oad' in item['class']:
                continue
            # 标题
            title = item.find('dt').text.strip('\n')
            # 链接
            url = item.find('dt').find('a')['href']
            # 简介
            des = item.find('dd', class_='answer').text.split('答：', 1)[-1]
            tmp = item.find('dd', class_='explain').findAll(
                'span', class_='mr-8')
            # 发布日期
            date = item.find('dd', class_='explain').find('span', class_='mr-7').text
            # 回答总数
            count = int(str(tmp[-1].text).strip('\n').strip('个回答'))
            # 生成结果
            result = {
                'title': title,
                'des': des,
                'date': date,
                'count': count,
                'url': url
            }
            results.append(result)  # 加入结果
        # 获取分页
        wrap = bs.find('div', class_='pager')
        pages_ = wrap.findAll('a')[:-2]
        pages = []
        for _ in pages_:
            # 暴力
            try:
                pages.append(int(_.text))
            except ValueError:
                pass
        return {
            'results': results,
            # 取最大页码
            'total': max(pages)
        }

    def search_video(self, query: str, pn: int = 1) -> dict:
        """百度视频搜索

        - 普通搜索：
            >>> BaiduSpider().search_video('搜索词')
            {
                'results': [
                    {
                        'img': 'str, 视频封面图片链接',
                        'time': 'str, 视频时长',
                        'title': 'str, 视频标题',
                        'url': 'str, 视频链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                'total': int, 搜索结果最大页数，可能因搜索页数改变而改变
            }

        - 带页码：
            >>> BaiduSpider().search_video('搜索词', pn=2)  # <=== `pn`
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索结果的页码. Defaults to 1.

        Returns:
            dict: 搜索结果及总页码
        """
        url = 'http://v.baidu.com/v?no_al=1&word=%s&pn=%d&ie=utf-8&db=0&s=0&fbl=800' % (
            quote(query), (60 if pn == 2 else (pn - 1) * 20))
        # 获取源码
        source = requests.get(url, headers=self.headers)
        code = self._minify(source.text)
        bs = BeautifulSoup(code, 'html.parser')
        # 锁定结果div
        data = bs.findAll('li', class_='result')
        results = []
        for res in data:
            # 标题
            title = res.find('a')['title']
            # 链接
            url = 'https://v.baidu.com' + res.find('a')['href']
            # 封面图片链接
            img = res.find('img', class_='img-normal-layer')['src']
            # 时长
            time = res.find('span', class_='info').text
            # 生成结果
            result = {
                'title': title,
                'url': url,
                'img': img,
                'time': time
            }
            results.append(result)  # 加入结果
        # 分页
        wrap = bs.find('div', class_='page-wrap')
        pages_ = wrap.findAll('a', class_='filter-item')[:-1]
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        return {
            'results': results,
            # 获取最大值
            'total': max(pages) if pages else 0
        }

    def search_news(self, query: str, pn: int = 1) -> dict:
        """百度资讯搜索

        - 获取资讯搜索结果：
            >>> BaiduSpider().search_news('搜索词')
            {
                'results': [
                    {
                        'author': 'str, 资讯来源（作者）',
                        'date': 'str, 资讯发布时间',
                        'des': 'str, 资讯简介',
                        'title': 'str, 资讯标题',
                        'url': 'str, 资讯链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 搜索结果最大页码，可能会因为当前页数变化而变化
            }

        - 带页码：
            >>> BaiduSpider().search_news('搜索词', pn=2)
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 搜索query
            pn (int, optional): 搜索结果的页码. Defaults to 1.

        Returns:
            dict: 爬取的搜索结果与总页码。
        """
        url = 'https://www.baidu.com/s?rtt=1&bsst=1&tn=news&word=%s&pn=%d' % (
            quote(query), (pn - 1) * 10)
        # 源码
        source = requests.get(url, headers=self.headers)
        # 压缩
        code = self._minify(source.text)
        bs = BeautifulSoup(self._format(code), 'html.parser')
        # 搜索结果容器
        data = bs.find('div', id='content_left').findAll('div')[1].findAll('div', class_='result-op')
        # print(len(data))
        results = []
        for res in data:
            # 标题
            title = self._format(
                res.find('h3').find('a').text)
            # 链接
            url = res.find('h3').find('a')['href']
            # 简介
            des = res.find('div', class_='c-span-last').find('span', class_='c-color-text').text
            # 作者
            author = res.find('div', class_='c-span-last').find('div', class_='news-source').find('span', class_='c-gap-right').text
            # 发布日期
            date = res.find('div', class_='c-span-last').find('div', class_='news-source').find('span', class_='c-color-gray2').text
            # 生成结果
            result = {
                'title': title,
                'author': author,
                'date': date,
                'des': des,
                'url': url
            }
            results.append(result)  # 加入结果
        # 获取所有页数
        pages_ = bs.find('div', id='page').findAll('a')
        # 过滤页码
        if '< 上一页' in pages_[0].text:
            pages_ = pages_[1:]
        if '下一页 >' in pages_[-1].text:
            pages_ = pages_[:-1]
        pages = []
        for _ in pages_:
            pages.append(int(_.find('span', class_='pc').text))
        return {
            'results': results,
            # 最大页数值
            'total': max(pages)
        }

    def search_wenku(self, query: str, pn: int = 1) -> dict:
        """百度文库搜索

        - 普通搜索：
            >>> BaiduSpider().search_wenku('搜索词')
            {
                'results': [
                    {
                        'date': 'str, 文章发布日期',
                        'des': 'str, 文章简介',
                        'downloads': int, 文章下载量,
                        'pages': int, 文章页数,
                        'title': 'str, 文章标题',
                        'type': 'str, 文章格式，为全部大写字母',
                        'url': 'str, 文章链接'
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 总计搜索结果的页数
            }

        - 带页码的搜索：
            >>> BaiduSpider().search_wenku('搜索词', pn=2)
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要搜索的query
            pn (int, optional): 搜索的页码. Defaults to 1.

        Returns:
            dict: 搜索结果和总计页数
        """
        url = 'https://wenku.baidu.com/search?word=%s&pn=%d' % (
            quote(query), (pn - 1) * 10)
        source = requests.get(url, headers=self.headers)
        source.encoding = 'gb2312'
        code = self._minify(source.text)
        bs = BeautifulSoup(code, 'html.parser')
        data = bs.findAll('dl')
        results = []
        for res in data:
            dt = res.find('dt')
            type_ = self._format(dt.find('p', class_='fl').find(
                'span', class_='ic')['title']).upper()
            tmp = dt.find('p', class_='fl').find('a')
            title = self._format(tmp.text)
            url = tmp['href']
            try:
                quality = float(self._format(
                    res.find('p', class_='fr').findAll('span', class_='ib')[1].text))
            except:
                quality = None
            dd = res.find('dd', class_='clearfix').find(
                'div', class_='summary-box')
            des = self._format(dd.find('p', class_='summary').text)
            try:
                dd_tags = res.find('dd', class_='tag-tips')
                tags = []
                for a in dd_tags.findAll('a'):
                    tags.append(self._format(a.text))
            except AttributeError:
                tags = []
            detail = dd.find('div', class_='detail').find(
                'div', class_='detail-info')
            date = self._format(detail.text.split('|')[0])
            pages = int(self._format(detail.text.split('|')[
                        1].replace('共', '').replace('页', '')))
            downloads = int(self._format(
                detail.text.split('|')[2].strip('次下载')))
            result = {
                'title': title,
                'type': type_,
                'url': url,
                'des': des,
                'date': date,
                'pages': pages,
                'downloads': downloads
            }
            results.append(result)
        pages_ = bs.find('div', class_='page-content').findAll('a')
        if '尾页' in pages_[-1].text:
            total = int(int(pages_[-1]['href'].split('&')
                            [-1].strip('pn=')) / 10 + 1)
        else:
            total = int(
                bs.find('div', class_='page-content').find('span', class_='cur').text)
        return {
            'results': results,
            'total': total
        }

    def search_jingyan(self, query: str, pn: int = 1) -> dict:
        """百度经验搜索

        - 例如：
            >>> BaiduSpider().search_jingyan('关键词')
            {
                'results': [
                    {
                        'title': 'str, 经验标题',
                        'url': 'str, 经验链接',
                        'des': 'str, 经验简介',
                        'date': 'str, 经验发布日期',
                        'category': 'str, 经验分类',
                        'votes': int, 经验的支持票数
                    },
                    { ... },
                    { ... },
                    { ... },
                    ...
                ],
                'total': int, 总计搜索结果页数
            }

        - 带页码的：
            >>> BaiduSpider().search_jingyan('搜索词', pn=2) # `pn` 是页码
            {
                'results': [ ... ],
                'total': ...
            }

        Args:
            query (str): 要搜索的关键词
            pn (int, optional): 搜索结果的页码. Defaults to 1.

        Returns:
            dict: 搜索结果以及总计的页码.
        """
        url = 'https://jingyan.baidu.com/search?word=%s&pn=%d&lm=0' % (
            quote(query), (pn - 1) * 10)
        # 获取网页源代码
        source = requests.get(url, headers=self.headers)
        # 最小化代码
        code = self._minify(source.text)
        bs = BeautifulSoup(code, 'html.parser')
        # 加载搜索结果
        data = bs.find('div', class_='search-list').findAll('dl')
        results = []
        for res in data:
            # 标题
            title = self._format(res.find('dt').find('a').text)
            # 链接
            url = 'https://jingyan.baidu.com/' + \
                res.find('dt').find('a')['href']
            # 简介
            des = self._format(res.find('dd').find(
                'div', class_='summary').find('span', class_='abstract').text)
            # 获取发布日期和分类，位于`<span class="cate"/>`中
            tmp = self._format(res.find('dd').find('div', class_='summary').find(
                'span', class_='cate').text).split('-')
            # 发布日期
            date = self._format(tmp[1])
            # 分类
            category = self._format(tmp[-1]).strip('分类：')
            # 支持票数
            votes = int(self._format(res.find('dt').find(
                'span', class_='succ-times').text).strip('得票'))
            # 生成结果
            result = {
                'title': title,
                'url': url,
                'des': des,
                'date': date,
                'category': category,
                'votes': votes
            }
            results.append(result)  # 加入结果到集合中
        # 获取分页
        pages_ = bs.find('div', id='pg').findAll('a')[-1]
        # 既不是最后一页也没有超出最后一页
        if '尾页' in pages_.text:
            # 获取尾页并加一
            total = int(int(pages_['href'].split(
                '&')[-1].strip('pn=')) / 10) + 1
        # 是最后一页或者是超过了最后一页
        else:
            # 重新获取分页
            pages_ = bs.find('div', id='pg').findAll('a')[1]
            # 获取尾页并加一
            total = int(int(pages_['href'].split(
                '&')[-1].strip('pn=')) / 10) + 1
        return {
            'results': results,
            'total': total
        }

    def search_baike(self, query: str) -> dict:
        """百度百科搜索

        - 使用方法：
            >>> BaiduSpider().search_baike('搜索词')
            {
                'results': {
                    [
                        'title': 'str, 百科标题',
                        'des': 'str, 百科简介',
                        'date': 'str, 百科最后更新时间',
                        'url': 'str, 百科链接'
                    ],
                    [ ... ],
                    [ ... ],
                    [ ... ]
                },
                'total': int, 搜索结果总数
            }

        Args:
            query (str): 要搜索的关键词

        Returns:
            dict: 搜索结果和总页数
        """
        # 获取源码
        source = requests.get(
            'https://baike.baidu.com/search?word=%s' % quote(query), headers=self.headers)
        code = self._minify(source.text)
        # 创建BeautifulSoup对象
        soup = BeautifulSoup(code, 'html.parser').find(
            'div', class_='body-wrapper').find('div', class_='searchResult')
        # 获取百科总数
        total = int(
            soup.find('div', class_='result-count').text.strip('百度百科为您找到相关词条约').strip('个'))
        # 获取所有结果
        container = soup.findAll('dd')
        results = []
        for res in container:
            # 链接
            url = 'https://baike.baidu.com' + \
                self._format(res.find('a', class_='result-title')['href'])
            # 标题
            title = self._format(res.find('a', class_='result-title').text)
            # 简介
            des = self._format(res.find('p', class_='result-summary').text)
            # 更新日期
            date = self._format(res.find('span', class_='result-date').text)
            # 生成结果
            results.append({
                'title': title,
                'des': des,
                'date': date,
                'url': url
            })
        return {
            'results': results,
            'total': total
        }
