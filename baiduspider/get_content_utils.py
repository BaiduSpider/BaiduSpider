import os
import re
from collections import OrderedDict
from datetime import datetime
from urllib.parse import unquote
import warnings

import requests
from bs4 import BeautifulSoup
from scrapy.item import Field, Item
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule



# 通过浏览器获取真实url
def get_real_url(url: str, driver=None):
    #等待时间5秒
    driver.get(url)
    url = driver.current_url
    #获取当前网页的html
    html = driver.page_source
    return url,html


class EncyclopediaItem(Item):
    name = Field()  # 此词条名称
    name_en = Field()  # 英文名称
    name_other = Field()  # 其他名称
    original_url = Field()  # 词条链接
    summary = Field()  # 简介
    source_site = Field()  # 词条来源网站
    edit_number = Field()  # 词条被编辑次数
    fetch_time = Field()  # 词条抓取时间
    update_time = Field()  # 词条更新时间
    item_tag = Field()  # 词条分类标签
    thumbnail_url = Field()  # 词条缩率图url
    album_url = Field()  # 词条缩率图url
    keywords_url = Field()  # 此词条内容所包含的其他词条
    polysemous = Field()  # 多义词，本词条不包含任何内容

    text_content = Field()  # 正文内容，是一个dict
    basic_info = Field()  # 属性内容，是一个dict
    text_image = Field()  # 正文内容中包含的图片dict


    def to_text(self,keep_reference=False):
        # 将name、name_en、name_other转换为文本
        name_text = ' '.join(name for name in [self['name'], self['name_en'], self['name_other']] if name)

        # 将summary转换为文本
        summary_text = str(self['summary'])

        # 将basic_info转换为文本
        basic_info = self['basic_info']
        basic_info_text = ''
        for key, value in basic_info.items():
            basic_info_text += key + ': ' + value + '\n'

        # 将text_content转换为文本
        text_content = self['text_content']
        text_content_text = ''
        for key, value in text_content.items():
            # 不包括参考资料或学术论文
            if keep_reference == False and key == '参考资料' or key == '学术论文':
                continue
            text_content_text += key + ': ' + value + '\n'

        # 将text拼接
        text = "名称: " + name_text + "\n\n" + "简介: " + summary_text + "\n\n" + "基本信息: " + basic_info_text + "\n\n" + "正文: " + text_content_text + "\n\n"
        # 删除所有 [数字]\xa0
        # text=re.sub(r'\[\d+\]\xa0','',text)
        return text


class BaiduBaikeParser():
    proxy_mode = 0  # not use proxy
    base_url = "https://baike.baidu.com"
    allowed_domains = ['baike.baidu.com']
    rules = (
        Rule(LinkExtractor(allow=('https://baike.baidu.com/item/',)), callback='parse', follow=True),
    )

    #输入html，解析返回item
    def parse(self, html)->EncyclopediaItem:
        basic_info_dict = OrderedDict()  # 词条基本信息值
        content_h2_dict = OrderedDict()  # 词条正文内容值
        img_dict = OrderedDict()  # 表示子标题中出现的图片url
        items = EncyclopediaItem()  # 基础信息

        #如果html已经是BeautifulSoup对象，则不需要再次转换
        if isinstance(html,BeautifulSoup):
            soup=html
        else:
            soup = BeautifulSoup(html, "html.parser")
        # 词条是否为多义词
        items['polysemous'] = '/view/10812277.htm' in html
        # 词条名称
        name = soup.title.get_text()
        items['name'] = name.split('_百度百科')[0] if name else None
        # name = soup.find('dd', attrs={'class': 'lemmaWgt-lemmaTitle-title'}).find('h1')
        # items['name'] = name.get_text() if name else None
        # 百科解释
        summary = soup.find('div', attrs={'class': 'lemma-summary'})
        items['summary'] = re.sub(r'\r|\n', '', summary.get_text()) if summary else None
        # 词条来源
        items['source_site'] = '百度百科'
        # 词条被编辑次数
        desc_text = soup.find('dl', attrs={'class': 'side-box lemma-statistics'})
        edit_number = re.compile(r'编辑次数：([\d]+)次').findall(desc_text.get_text())[0] if desc_text else None
        items['edit_number'] = int(edit_number) if edit_number else 1
        # 词条最近更新时间
        latest = soup.find('span', attrs={'class': 'j-modified-time'})
        items['update_time'] = latest.get_text().replace('（', '').replace('）', '') if latest else None
        # 词条抓取时间
        items['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 词条的分类标签（路径）
        item_tag = soup.find('dd', attrs={'id': 'open-tag-item'})
        items['item_tag'] = re.sub(r'\r|\n|\s', '', item_tag.get_text()) if item_tag else None
        # 词条缩率图链接
        thumbnail_url = soup.find('div', attrs={'class': 'summary-pic'})
        items['thumbnail_url'] = thumbnail_url.find('img').get('src') if thumbnail_url else None
        # 获得下一步需要采集的关键词
        kw_urls = list()
        for tag_obj in soup.findAll('div', attrs={'class': 'para'}):
            try:
                kw_urls.append(unquote(tag_obj.find('a', attrs={'target': '_blank'}).get('href')))
            except (AttributeError, TypeError):
                pass
        items['keywords_url'] = list(set(filter(lambda x: 'item' in x, kw_urls)))
        # 词条的简要简介
        items['name_en'] = None
        items['name_other'] = None
        basic_info_item_name = soup.findAll('dt', attrs={'class': 'basicInfo-item name'})
        basic_info_item_value = soup.findAll('dd', attrs={'class': 'basicInfo-item value'})
        for basic_info in zip(basic_info_item_name, basic_info_item_value):
            dict_key = ''.join(basic_info[0].get_text(strip=True).split())
            dict_value = basic_info[1].get_text(strip=True).strip()
            if '英文名称' == dict_key:
                items['name_en'] = dict_value
            elif dict_key in ['外文名', '外文名称']:
                items['name_other'] = dict_value
            else:
                basic_info_dict[dict_key] = dict_value

        # 找到第一个class为para-title且class为level-2的div标签
        sibling = soup.find('div', attrs={'class': lambda x: x and 'para-title' in x and 'level-2' in x})

        # 如果没有二级标题，那么就是正文
        if not sibling:
            h2_title = '正文'
            content_h2_dict[h2_title] = ''
            img_dict[h2_title] = list()
            for para in soup.find_all('div', attrs={'class': 'para'}):
                content_h2_dict[h2_title] += '<p>' + re.sub(r'\r|\n', '', para.get_text()) + '</p>'
                try:
                    img_url = para.find('img').get('data-src')
                    if img_url:
                        img_dict[h2_title].append(img_url)
                except AttributeError:
                    pass

        # 如果有二级标题，分别获取每个二级标题下的内容
        else:
            while sibling is not None:
                if 'para-title level-2' in str(sibling):
                    h2_title = sibling.find('h2', attrs={'class': 'title-text'}).get_text('$$').split('$$')[-1]  # h2标题
                    content_h2_dict[h2_title] = ''
                    img_dict[h2_title] = list()
                # elif 'para' in str(sibling):
                elif 'para-title level-3' in str(sibling):
                    # 3级标题名称
                    content_h2_dict[h2_title] += '<h3>' + sibling.find('h3').get_text('$$').split('$$')[-1] + '</h3>'
                elif 'class=\"para' in str(sibling):
                    # 对应的正文内容
                    content_h2_dict[h2_title] += '<p>' + re.sub(r'\r|\n', '', sibling.get_text()).strip() + '</p>'
                    try:
                        img_url = sibling.find('img').get('data-src')
                        if img_url:
                            img_dict[h2_title].append(img_url)
                    except AttributeError:
                        pass
                try:
                    sibling = next(sibling.next_siblings)
                except StopIteration:
                    sibling = None
        # 参考资料
        try:
            reference_key = soup.find('dt', attrs={'class': 'reference-title'}).get_text()
            reference_value = ''
            reference_urls = []
            lis = soup.find('ul', attrs={'class': 'reference-list'}).find_all('li')
            for index, li in enumerate(lis):
                reference_value += '<p>'.format(index) + re.sub(r'\r|\n', '', li.get_text()) + '</p>'
                url = li.find('a', attrs={'rel': 'nofollow'})
                if url:
                    reference_urls.append(self.base_url + url.get('href'))
            content_h2_dict[reference_key] = reference_value if reference_value else None
            img_dict[reference_key] = reference_urls
        except (AttributeError, TypeError):
            pass
        # 词条图册链接
        album_url = soup.find('div', attrs={'class': 'album-list'})
        if album_url:
            album_url = album_url.find('a', attrs={'class': 'more-link'}).get('href')
        items['album_url'] = self.base_url + album_url if album_url else None
        # 简要信息
        items['basic_info'] = basic_info_dict
        # 正文内容
        items['text_content'] = content_h2_dict
        # 正文中包含的图片
        items['text_image'] = img_dict
        # print(items['name'], items['polysemous'])
        return items  # 深拷贝的目的是默认浅拷贝item会在后面的pipelines传递过程中会出现错误，比如串数据了


# 根据url获取百度百科内容
def get_baike_item(baike, headers=None):
    url=baike.url
    if hasattr(baike,'html'):
        html=baike.html
    else:
        # 获取response
        res = requests.get(url, headers=headers,timeout=10)
        res.encoding = 'utf-8'
        html=res.text
        res.close()
    # 实例化Parser
    spider = BaiduBaikeParser()
    # 解析
    item = spider.parse(html)
    return item


#获取杂类网页的文本
def parse_other_normal_text(bs: BeautifulSoup,title='') -> str:

    #寻找class包含“title”的h1或div。如果找到，且长度大于title，则更新title
    title_tag=bs.find('h1',attrs={'class':lambda x:x and 'title' in x})
    if title_tag:
        if len(title_tag.get_text())>len(title):
            title=title_tag.get_text()

    #寻找class为“article”的div或name为“article”的标签
    article=bs.find('div',attrs={'class':'article'})
    if article:
        text="标题: "+title+"\n\n"+"内容: "+article.get_text()+"\n\n"
        return text
    article=bs.find('article')
    if article:
        text="标题: "+title+"\n\n"+"内容: "+article.get_text()+"\n\n"
        return text

    #寻找class中包含"content"的div
    content=bs.find('div',attrs={'class':lambda x:x and 'content' in x})
    if content:
        text="标题: "+title+"\n\n"+"内容: "+content.get_text()+"\n\n"
        return text

    #寻找class中包含“question”的div和class中包含“answer”的div
    question=bs.find('div',attrs={'class':lambda x:x and 'question' in x})
    answer=bs.find('div',attrs={'class':lambda x:x and 'answer' in x})
    if question and answer:
        text="标题: "+title+"\n\n"+"问题: "+question.get_text()+"\n\n"+"回答: "+answer.get_text()+"\n\n"
        return text

    #如果不属于任何类型，则获取网页的所有文本
    text=bs.get_text()
    #把标题加到最前面
    text=title+"\n\n"+text
    return text


#解析百度百科内容
def parse_baidu_baike(bs: BeautifulSoup) -> str:
    # 实例化Parser
    spider = BaiduBaikeParser()
    # 解析
    item = spider.parse(bs)
    text=item.to_text()
    return text

#解析百度百科内容
def parse_baidu_baike_simple(bs: BeautifulSoup) -> str:
    #获取第一个h1标签
    title=bs.find('h1').get_text()
    #获取class为“J-summary”的div
    summary=bs.find('div',attrs={'class':'J-summary'}).get_text()

    text=title+"\n\n"+"简介: "+summary
    return text

# 解析百度知道
def parse_baidu_zhidao(bs: BeautifulSoup) -> str:

    # 获取问题,class为“ask-title”的span
    question = bs.find('span', attrs={'class': 'ask-title'}).get_text()
    # 获取答案，id为wgt-best的div下的class为“rich-content-container”的div
    answer = bs.find('div', attrs={'id': 'wgt-best'}).find('div', attrs={'class': 'rich-content-container'}).get_text()
    # 返回文本
    text = "问题: " + question + "\n\n" + "回答: " + answer + "\n\n"
    return text

#解析百家号内容
def parse_baijiahao(bs: BeautifulSoup) -> str:
    # 获取标题,class为“sKHSJ”的div
    title = bs.find('div', attrs={'class': 'sKHSJ'}).get_text()
    # 获取文本，class为“_18p7x”的div
    content = bs.find('div', attrs={'class': '_18p7x'}).get_text()
    # 返回文本
    text = "标题: " + title + "\n\n" + "内容: " + content + "\n\n"
    return text

#解析csdn内容
def parse_csdn(bs: BeautifulSoup) -> str:
    # 获取标题,class为“title-article”的h1
    title = bs.find('h1', attrs={'class': 'title-article'}).get_text()
    # 获取文本，class为“article_content”的div
    content = bs.find('div', attrs={'class': 'article_content'}).get_text()
    # 返回文本
    text = "标题: " + title + "\n\n" + "网页内容: " + content + "\n\n"
    return text


# 为WebBaike增加一个函数，get_text()
def get_baike_text(self, headers=None) -> str:
    url=self.url
    if hasattr(self,'html'):
        html=self.html
    else:
        # 获取response
        res = requests.get(url, headers=headers,timeout=10)
        res.encoding = 'utf-8'
        html=res.text
        res.close()

    bs = BeautifulSoup(html, 'html.parser')
    text=parse_baidu_baike(bs)
    self.web_content=text
    return text


def get_normal_text(self, headers=None)->str:
    # 获取url
    url = self.url
    # 获取摘要
    summary = self.des
    # 获取网页标题
    title = self.title

    if hasattr(self,'html'):
        html=self.html
    else:
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        html=res.text
        self.html=html
        res.close()
    bs = BeautifulSoup(html, 'html.parser')

    try:
        # 如果标题包含“百度知道”，则调用parse_baidu_zhidao
        if '百度知道' in title:
            text= parse_baidu_zhidao(bs)
        #如果包含百度百科，则调用get_baike_content
        elif '百度百科' in title:
            text= parse_baidu_baike_simple(bs)

        #如果url中包含“baijiahao”，说明是百家号,则调用parse_baijiahao
        elif 'baijiahao' in url:
            text=parse_baijiahao(bs)
        #如果url中包含"blog.csdn",则调用parse_csdn
        elif 'blog.csdn' in url:
            text=parse_csdn(bs)
        else:
            # 如果是杂类，则调用get_other_normal_text
            text = parse_other_normal_text(bs,title=title)
    except:
        #判断是否是DEBUG模式
        if os.environ.get('DEBUG')=='1':
            raise
        else:
            warnings.warn("解析网页出错，返回空字符串")
            text=''

    self.web_content=text #将文本保存到web_content中
    return text

