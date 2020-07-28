"""百度爬虫

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
from htmlmin import minify

__all__ = ['BaiduSpider']


class BaseSpider(object):
    def __init__(self) -> None:
        r"""所有爬虫的基类

        此类包括了常用的util和自定义方法，继承自`object`。
        """
        super().__init__()
        self.spider_name = 'BaseSpider'
        self.headers = {}

    def _format(self, s: str) -> str:
        r"""去除字符串中不必要的成分并返回

        Args:
            s (str): 要整理的字符串

        Returns:
            str: 处理后的字符串
        """
        return s.replace('\n', '').strip().replace('\n\r    \xa0', '').replace('  ', '').replace('\xa0', '')

    def _remove_html(self, s: str) -> str:
        r"""从字符串中去除HTML标签

        Args:
            s (str): 要处理的字符串

        Returns:
            str: 处理完的去除了HTML标签的字符串
        """
        pattern = re.compile(r'<[^*>]+>', re.S)
        removed = pattern.sub('', s)
        return removed

    def _minify(self, html: str) -> str:
        r"""压缩HTML代码

        Args:
            html (str): 要压缩的代码

        Returns:
            str: 压缩后的HTML代码
        """
        return minify(html, remove_all_empty_space=True, remove_comments=True, remove_optional_attribute_quotes=True)

    def __repr__(self) -> str:
        return '<Spider %s>' % self.spider_name

    def __str__(self) -> str:
        return self.__repr__()


class BaiduSpider(BaseSpider):
    def __init__(self) -> None:
        r"""爬取百度的搜索结果

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
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'Referer': 'https://www.baidu.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Cookie': 'BAIDUID=BB66E815C068DD2911DB67F3F84E9AA5:FG=1; BIDUPSID=BB66E815C068DD2911DB67F3F84E9AA5; PSTM=1592390872; BD_UPN=123253; BDUSS=RQa2c4eEdKMkIySjJ0dng1ZDBLTDZEbVNHbmpBLU1rcFJkcVViaTM5NUdNaDFmRVFBQUFBJCQAAAAAAAAAAAEAAAAPCkwAZGF5ZGF5dXAwNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEal9V5GpfVebD; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=2; COOKIE_SESSION=99799_0_5_2_8_0_1_0_5_0_0_0_99652_0_3_0_1593609921_0_1593609918%7C9%230_0_1593609918%7C1; H_PS_PSSID=1457_31326_32139_31660_32046_32231_32091_32109_31640; sug=3; sugstore=0; ORIGIN=0; bdime=0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_645EC=1375sSQTgv84OSzYM3CN5w5Whp9Oy7MkdGdBcw5umqOIFr%2FeFZO4D952XrS0pC1kVwPI; BDSVRTM=223'
        }

    def search_web(self, query: str, pn: int = 1) -> dict:
        r"""百度网页搜索

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
                                'url': 'str, 新闻链接'
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
        text = quote(query, 'utf-8')
        url = 'https://www.baidu.com/s?&wd=%s&pn=%d' % (
            text, (pn - 1) * 10)
        # 获取响应
        response = requests.get(url, headers=self.headers)
        text = bytes(response.text, response.encoding).decode('utf-8')
        soup = BeautifulSoup(self._minify(text), 'html.parser')
        # 尝试获取搜索结果总数
        try:
            num = int(str(soup.find('span', class_='nums_text').text).strip(
                '百度为您找到相关结果约').strip('个').replace(',', ''))
        except:
            num = 0
        # 查找运算窗口
        calc = soup.find('div', class_='op_new_cal_screen')
        # 定义预结果（运算以及相关搜索）
        pre_results = []
        # 预处理相关搜索
        try:
            _related = soup.find('div', id='rs').find('table').find_all('th')
        except:
            _related = []
        related = []
        # 预处理新闻
        news = soup.find('div', class_='result-op',
                         tpl='sp_realtime_bigpic5', srcid='19')
        # 确认是否有新闻块
        try:
            news_title = self._format(
                news.find('h3', class_='t').find('a').text)
        except:
            news_title = None
            news_detail = []
        else:
            news_rows = news.findAll('div', class_='c-row')
            news_detail = []
            for row in news_rows:
                # 因为新闻会有介绍，但是不是每个都有，所以碰到介绍这里用try-except捕获
                try:
                    row_title = self._format(row.find('a').text)
                except AttributeError:
                    continue
                else:
                    row_time = self._format(
                        row.find('span', class_='c-color-gray2').text)
                    row_author = self._format(
                        row.find('span', class_='c-color-gray2').text)
                    row_url = self._format(row.find('a')['href'])
                    news_detail.append({
                        'title': row_title,
                        'time': row_time,
                        'author': row_author,
                        'url': row_url
                    })
        # 预处理短视频
        video = soup.find('div', class_='op-short-video-pc')
        if video:
            video_rows = video.findAll('div', class_='c-row')
            video_results = []
            for row in video_rows:
                row_res = []
                videos = row.findAll('div', class_='c-span6')
                for v in videos:
                    v_link = v.find('a', class_='op-short-video-pc-link')
                    v_title = v_link['title']
                    v_url = self._format(v_link['href'])
                    v_img = v_link.find(
                        'img', class_='op-short-video-pc-img')['src']
                    v_len = self._format(
                        v.find('div', class_='op-short-video-pc-duration-wrap').text)
                    v_from = self._format(
                        v.find('div', class_='op-short-video-pc-source').text)
                    row_res.append({
                        'title': v_title,
                        'url': v_url,
                        'cover': v_img,
                        'length': v_len,
                        'origin': v_from
                    })
                video_results += row_res
        else:
            video_results = []
        # 一个一个append相关搜索
        for _ in _related:
            if _.text:
                related.append(_.text)
        # 加载搜索结果总数
        if num != 0:
            pre_results.append(dict(type='total', result=num))
        # 加载运算
        if calc:
            pre_results.append(dict(type='calc', process=str(calc.find('p', class_='op_new_val_screen_process').find(
                'span').text), result=str(calc.find('p', class_='op_new_val_screen_result').find('span').text)))
        # 加载相关搜索
        if related:
            pre_results.append(dict(type='related', results=related))
        # 加载资讯
        if news_detail:
            pre_results.append(dict(type='news', results=news_detail))
        # 加载短视频
        if video_results:
            pre_results.append(dict(type='video', results=video_results))
        # 预处理源码
        try:
            soup = BeautifulSoup(minify(soup.find_all(id='content_left')[
                0].prettify(), remove_all_empty_space=True), 'html.parser')
        # 错误处理
        except IndexError:
            return {
                'results': None,
                'total': None
            }
        results = BeautifulSoup(self._minify(response.text), 'html.parser').findAll(class_='c-container')
        res = []
        for result in results:
            des = None
            soup = BeautifulSoup(self._minify(
                result.prettify()), 'html.parser')
            # 链接
            href = soup.find_all('a', target='_blank')[0].get('href').strip()
            # 标题
            title = self._format(soup.find_all('a', target='_blank')[0].text)
            try:
                time = self._format(soup.find_all('div', class_='c-abstract')[0].find('span', class_='c-color-gray2').text)
            except (AttributeError, IndexError):
                time = None
            try:
                # 简介
                des = soup.find_all('div', class_='c-abstract')[0].text
                soup = BeautifulSoup(result.prettify(), 'html.parser')
                des = self._format(des).lstrip(str(time)).strip()
            except IndexError:
                try:
                    des = des.replace('\n', '')
                except (UnboundLocalError, AttributeError):
                    des = None
            # 因为百度的链接是加密的了，所以需要一个一个去访问
            # 由于性能原因，分析链接部分暂略
            # if href is not None:
            #     try:
            #         # 由于性能原因，这里设置1秒超时
            #         r = requests.get(href, timeout=1)
            #         href = r.url
            #     except:
            #         # 获取网页失败，默认换回原加密链接
            #         href = href
            #     # 分析链接
            #     if href:
            #         parse = urlparse(href)
            #         domain = parse.netloc
            #         prepath = parse.path.split('/')
            #         path = []
            #         for loc in prepath:
            #             if loc != '':
            #                 path.append(loc)
            #     else:
            #         domain = None
            #         path = None
            # 获取可见的域名
            try:
                is_not_news_or_video = result['tpl'] != 'short_video_pc' and result['tpl'] != 'sp_realtime_bigpic5'
            except KeyError:
                try:
                    is_not_news_or_video = result['tpl'] != 'short_video_pc'
                except KeyError:
                    try:
                        is_not_news_or_video = result['tpl'] != 'sp_realtime_bigpic5'
                    except:
                        is_not_news_or_video = False
            if is_not_news_or_video:  # 确保不是视频和资讯
                try:
                    domain = self._format(result.find('div', class_='c-row').find('div', class_='c-span-last').find(
                        'div', class_='se_st_footer').find('a', class_='c-showurl').text)
                except Exception as error:
                    try:
                        domain = self._format(result.find(
                            'div', class_='c-row').find('div', class_='c-span-last').find('p', class_='op-bk-polysemy-move').find('span', class_='c-showurl').text)
                    except Exception as error:
                        try:
                            domain = self._format(result.find(
                                'div', class_='se_st_footer').find('a', class_='c-showurl').text)
                        except:
                            domain = None
            else:
                domain = None
            # 加入结果
            if title and href and is_not_news_or_video:
                res.append({
                    'title': title,
                    'des': des,
                    'origin': domain,
                    'url': href,
                    'time': time,
                    'type': 'result'})
        soup = BeautifulSoup(text, 'html.parser')
        soup = BeautifulSoup(soup.find_all('div', id='page')
                             [0].prettify(), 'html.parser')
        # 分页
        pages_ = soup.find_all('span', class_='pc')
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        # 设置最终结果
        result = pre_results
        result.extend(res)
        return {
            'results': result,
            # 最大页数
            'total': max(pages)
        }

    def search_pic(self, query: str, pn: int = 1) -> dict:
        r"""百度图片搜索

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
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&word=%s&pn=%d' % (
            quote(query), (pn - 1) * 20)
        print(url)
        source = requests.get(url, headers=self.headers)
        code = source.text
        # 从JavaScript中加载数据
        # 因为JavaScript很像JSON（JavaScript Object Notation），所以直接用json加载就行了
        # 还有要预处理一下，把函数和无用的括号过滤掉
        data = json.loads(code.split('flip.setData(\'imgData\', ')[1].split(
            'flip.setData(')[0].split(']);')[0].replace(');', '').replace('<\\/strong>', '</strong>').replace('\\\'', '\''))
        results = []
        for _ in data['data'][:-1]:
            if _:
                # 标题
                title = str(_['fromPageTitle']).encode('utf-8').decode('utf-8')
                # 去除标题里的HTML
                pattern = re.compile(r'<[^*>]+>', re.S)
                title = unescape(pattern.sub('', title))
                # 链接
                url = _['objURL']
                # 来源域名
                host = _['fromURLHost']
                # 生成结果
                result = {
                    'title': title,
                    'url': url,
                    'host': host
                }
                results.append(result)  # 加入结果
        # 获取分页
        bs = BeautifulSoup(code, 'html.parser')
        pages_ = bs.find('div', id='page').findAll('span', class_='pc')
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        return {
            'results': results,
            # 取最大页码
            'total': max(pages)
        }

    def search_zhidao(self, query: str, pn: int = 1) -> dict:
        r"""百度知道搜索

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
        url = 'https://zhidao.baidu.com/search?pn=%d&tn=ikaslis&word=%s' % (
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
            title = item.find('dt').text
            # 链接
            url = item.find('dt').find('a')['href']
            # 简介
            des = item.find('dd').text.strip('答：')
            tmp = item.find('dd', class_='explain').findAll(
                'span', class_='mr-8')
            # 发布日期
            date = tmp[0].text
            # 回答总数
            count = int(str(tmp[-1].text).strip('个回答'))
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
        r"""百度视频搜索

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
        url = 'http://v.baidu.com/v?no_al=1&word=%s&pn=%d' % (
            quote(query), (60 if pn == 2 else (pn - 1) * 20))
        print(url)
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
            'total': max(pages)
        }

    def search_news(self, query: str, pn: int = 1) -> dict:
        r"""百度资讯搜索

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
        url = 'https://www.baidu.com/s?rtt=1&tn=news&word=%s&pn=%d' % (
            quote(query), (pn - 1) * 10)
        # 源码
        source = requests.get(url, headers=self.headers)
        # 压缩
        code = self._minify(source.text)
        bs = BeautifulSoup(self._format(code), 'html.parser')
        # 搜索结果容器
        data = bs.findAll('div', class_='result')
        results = []
        for res in data:
            # 标题
            title = self._format(
                res.find('h3', class_='c-title').find('a').text)
            # 链接
            url = res.find('h3', class_='c-title').find('a')['href']
            # 简介
            des = res.find('div', class_='c-summary')
            # 获取作者容器
            tmp = des.find('p', class_='c-author')
            # 另一种格式
            if tmp is None:
                tmp = des.find(
                    'div', class_='c-span-18').find('p', class_='c-author')
            tmp = self._format(str(tmp.text)).split(' ')
            # 作者
            author = tmp[0]
            # 发布日期
            if tmp[1] != tmp[-1]:
                date = tmp[1] + ' ' + tmp[-1]
            else:
                date = tmp[-1]
            tmp = des.find('div', class_='c-span-18')
            if tmp is None:
                tmp = des
            # 简介
            des = self._format(tmp.text.replace(
                author, '').replace(date, '').strip('百度快照'))
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
        pages_ = bs.find('p', id='page').findAll('a')[:-1]
        # 过滤页码
        if '上一页' in pages_[0].text:
            pages_ = pages_[1:]
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        return {
            'results': results,
            # 最大页数值
            'total': max(pages)
        }

    def search_wenku(self, query: str, pn: int = 1) -> dict:
        r"""百度文库搜索

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
        r"""百度经验搜索

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
        r"""百度百科搜索

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
        code = minify(source.text)
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
