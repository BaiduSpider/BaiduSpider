import json
import math
from datetime import datetime, time
from html import unescape
from time import localtime, strftime

from baiduspider._spider import BaseSpider
from baiduspider.errors import ParseError
from baiduspider.parser.subparser import WebSubParser
from baiduspider.util import handle_err
from bs4 import BeautifulSoup


class Parser(BaseSpider):
    def __init__(self) -> None:
        """百度搜索解析器"""
        super().__init__()
        self.webSubParser = WebSubParser()

    def parse_web(self, content: str, exclude: list) -> dict:
        """解析百度网页搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度网页搜索HTML源码.
            exclude (list): 要屏蔽的控件.

        Returns:
            dict: 解析后的结果
        """
        soup = BeautifulSoup(content, "html.parser")
        if not soup.find("div", id="content_left"):
            return {"results": [], "pages": 0, "total": 0}
        # 获取搜索结果总数
        tmp1 = soup.findAll("div", class_="result-molecule")
        idx_ = 0
        ele = None
        while not ele and idx_ < len(tmp1):
            tmp = tmp1[idx_].findAll("span")
            found = False
            for t in tmp:
                if "百度为您找到相关结果" in t.text:
                    ele = t
                    found = True
                    break
            if found:
                break
            idx_ += 1
        num = int(
            str(ele.text).strip("百度为您找到相关结果").strip("约").strip("个").replace(",", "")
        )
        # 定义预结果（运算以及相关搜索）
        pre_results = []
        # 预处理新闻
        if "news" not in exclude:
            news = soup.find("div", class_="result-op", srcid="19")
            news_detail = self.webSubParser.parse_news_block(news)
        # 预处理短视频
        if "video" not in exclude:
            video = soup.find("div", class_="op-short-video-pc")
            video_results = self.webSubParser.parse_video_block(video)
        # 预处理运算
        if "calc" not in exclude:
            calc = soup.find("div", class_="op_new_cal_screen")
        # 预处理相关搜索
        if "related" not in exclude:
            try:
                _related = soup.findAll("table")[-1].findAll("td")
            except AttributeError:
                _related = []
            related = []
            # 一个一个append相关搜索
            for _ in _related:
                if _.text:
                    related.append(self._format(_.text))
        # 预处理百科
        if "baike" not in exclude:
            baike = soup.find("div", class_="c-container", tpl="bk_polysemy")
            baike = self.webSubParser.parse_baike_block(baike)
        # 预处理贴吧
        if "tieba" not in exclude:
            tieba = BeautifulSoup(content, "html.parser").find("div", srcid="10")
            tieba = self.webSubParser.parse_tieba_block(tieba)
        if "music" not in exclude:
            music = BeautifulSoup(content, "html.parser").find(
                "div", class_="result-op", tpl="yl_music_song"
            )
            music = self.webSubParser.parse_music_block(music)
        # 预处理博客
        article_tags = BeautifulSoup(content, "html.parser").findAll("article")
        if "blog" not in exclude:
            blog = None
            for tmp in article_tags:
                if tmp["class"][-1].startswith("open-source-software-blog"):
                    blog = tmp
                    break
            blog = self.webSubParser.parse_blog_block(blog)
        # 预处理码云
        if "gitee" not in exclude:
            gitee = None
            for tmp in article_tags:
                if tmp["class"][-1].startswith("osc-gitee"):
                    gitee = tmp
                    break
            gitee = self.webSubParser.parse_gitee_block(gitee)
        # 加载贴吧
        if "tieba" not in exclude and tieba:
            pre_results.append(dict(type="tieba", result=tieba))
        # 加载博客
        if "blog" not in exclude and blog:
            pre_results.append(dict(type="blog", result=blog))
        # 加载码云
        if "gitee" not in exclude and gitee:
            pre_results.append(dict(type="gitee", result=gitee))
        # 加载搜索结果总数
        # 已经移动到根字典中
        # if num != 0:
        #     pre_results.append(dict(type="total", result=num))
        # 加载运算
        if "calc" not in exclude and calc:
            pre_results.append(
                dict(
                    type="calc",
                    process=str(
                        calc.find("p", class_="op_new_val_screen_process")
                        .find("span")
                        .text
                    ),
                    result=str(
                        calc.find("p", class_="op_new_val_screen_result")
                        .find("span")
                        .text
                    ),
                )
            )
        # 加载相关搜索
        if "related" not in exclude and related:
            pre_results.append(dict(type="related", results=related))
        # 加载资讯
        if "news" not in exclude and news_detail:
            pre_results.append(dict(type="news", results=news_detail))
        # 加载短视频
        if "video" not in exclude and video_results:
            pre_results.append(dict(type="video", results=video_results))
        # 加载百科
        if "baike" not in exclude and baike:
            pre_results.append(dict(type="baike", result=baike))
        # 加载音乐
        if "music" not in exclude and music:
            pre_results.append(dict(type="music", result=music))
        # 预处理源码
        soup = BeautifulSoup(content, "html.parser")
        results = []
        for res in soup.findAll("div", class_="result"):
            try:
                if res["srcid"] in ["1599"]:
                    results.append(res)
            except KeyError:
                pass
        res = []
        for result in results:
            des = None
            try:
                result["tpl"]
            except KeyError:
                continue
            soup = BeautifulSoup(self._minify(str(result)), "html.parser")
            # 链接
            href = soup.find("a").get("href").strip()
            # 标题
            title = self._format(str(soup.find("a").text))
            # 时间
            try:
                _ = soup.find("div", class_="c-span-last")
                if not _:
                    _ = soup.find("div", class_="c-gap-top-small")
                if _:
                    time = self._format(
                        _.find("span", class_="c-color-gray2")
                        .text
                    )
            except (AttributeError, IndexError):
                time = None
            try:
                # 简介
                des = None
                _ = soup.find("div", class_="c-span-last")
                if _:
                    for des_ in _.findAll("span"):
                        try:
                            if des_["class"][0].startswith("content-right"):
                                des = des_.text
                                break
                        except KeyError:
                            pass
                else:
                    _ = soup.find("div", class_="c-gap-top-small")
                    if _:
                        for des_ in _.findAll("span"):
                            try:
                                if des_["class"][0].startswith("content-right"):
                                    des = des_.text
                                    break
                            except KeyError:
                                pass
                soup = BeautifulSoup(str(result), "html.parser")
                if des:
                    des = self._format(des)
            except IndexError:
                try:
                    des = des.replace("mn", "")
                except (UnboundLocalError, AttributeError):
                    des = None
            if time:
                time = time.split("-")[0].strip()
            # 因为百度的链接是加密的了，所以需要一个一个去访问
            # 由于性能原因，分析链接部分暂略
            # if href:
            #     try:
            #         # 由于性能原因，这里设置1秒超时
            #         r = requests.get(href, timeout=1)
            #         href = r.url
            #     except Exception:
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
            try:
                result["tpl"]
            except KeyError:
                pass
            is_not_special = (
                result["tpl"]
                not in [
                    "short_video_pc",
                    "sp_realtime_bigpic5",
                    "bk_polysemy",
                    "tieba_general",
                    "yl_music_song",
                ]
                and not result.find("article")
            )
            domain = None
            domain_ = result.findAll("div", class_="c-row")
            for _ in domain_:
                flag = False
                if _.has_attr("class"):
                    for __ in _["class"]:
                        if __.startswith("source"):
                            domain = _
                            flag = True
                            break
                if flag:
                    break
            domain = self._format(domain.find("a").text)
            # 百度快照
            snapshot = result.find("a", class_="kuaizhao")
            if snapshot:
                snapshot = self._format(snapshot["href"].replace("\n", "").replace(" ", ""))
            # 加入结果
            if title and href and is_not_special:
                res.append(
                    {
                        "title": title,
                        "des": des,
                        "origin": domain,
                        "url": href,
                        "time": time,
                        "snapshot": snapshot,
                        "type": "result",
                    }
                )
        soup = BeautifulSoup(content, "html.parser")
        soup = BeautifulSoup(str(soup.findAll("div", id="page")[0]), "html.parser")
        # 分页
        # pages_ = soup.findAll("span", class_="pc")
        # pages = []
        # for _ in pages_:
        #     pages.append(int(_.text))
        # # 如果搜索结果仅有一页时，百度不会显示底部导航栏
        # # 所以这里直接设置成1，如果不设会报错`TypeError`
        # if not pages:
        #     pages = [1]
        # 设置最终结果
        result = pre_results
        result.extend(res)
        return {
            "results": result,
            # 最大页数
            # "pages": max(pages),
            "total": num,
        }

    @handle_err
    def parse_pic(self, content: str) -> dict:
        """解析百度图片搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度图片搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        # 从JavaScript中加载数据
        # 因为JavaScript很像JSON（JavaScript Object Notation），所以直接用json加载就行了
        # 还有要预处理一下，把函数和无用的括号过滤掉
        error = None
        try:
            data = json.loads(
                content.split("flip.setData('imgData', ")[1]
                .split("flip.setData(")[0]
                .split("]);")[0]
                .replace(");", "")
                .replace("<\\/strong>", "</strong>")
                .replace("\\'", "'")
                .replace('\\"', "'"),
                strict=False,
            )
        except Exception as err:
            error = err
            if type(err) in [IndexError, AttributeError]:
                raise ParseError("Invalid HTML content.")
        finally:
            if error:
                raise ParseError(str(error))
        soup = BeautifulSoup(content, "html.parser")
        total = "".join(re.findall('\d', soup.find("div", id="resultInfo").text))
        if total:
            total = int(total)
        else:
            total = 0
        results = []
        for _ in data["data"][:-1]:
            if _:
                # 标题
                title = str(_["fromPageTitle"]).encode("utf-8").decode("utf-8")
                # 去除标题里的HTML
                title = unescape(self._remove_html(title))
                # 链接
                url = _["objURL"]
                # 来源域名
                host = _["fromURLHost"]
                # 生成结果
                result = {"title": title, "url": url, "host": host}
                results.append(result)  # 加入结果
        # 获取分页
        # bs = BeautifulSoup(content, "html.parser")
        # pages_ = bs.find("div", id="page").findAll("span", class_="pc")
        # pages = []
        # for _ in pages_:
        #     pages.append(int(_.text))
        return {
            "results": results,
            # 取最大页码
            # "pages": max(pages),
            "total": total,
        }

    def parse_zhidao(self, content: str) -> dict:
        """解析百度知道搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度知道搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._minify(content), "html.parser")
        # 搜索结果总数
        try:
            total = int(
                bs.find("div", class_="wgt-picker")
                .find("span", class_="f-lighter")
                .text.split("共", 1)[-1]
                .split("条结果", 1)[0]
                .replace(",", "")
            )
        except AttributeError:
            # 没有搜索结果
            return {
                "results": [],
                "total": 0
            }
        # 所有搜索结果
        list_ = bs.find("div", class_="list").findAll("dl")
        results = []
        for item in list_:
            # 屏蔽企业回答
            if "ec-oad" in item["class"]:
                continue
            # print(item.prettify() + '\n\n\n\n\n\n\n')
            # 标题
            title = item.find("dt").text.strip("\n")
            # 链接
            try:
                url = item.find("dt").find("a")["href"]
            except KeyError:
                url = item.find("dt").find("a")["data-href"]
            if item.find("dd", class_="video-content"):
                # 问题
                __ = item.find("dd", class_="summary")
                question = __.text.strip("问：") if __ else None
                item = item.find("div", class_="right")
                tmp = item.findAll("div", class_="video-text")
                # # 简介
                # des = self._format(tmp[2].text)
                answer = None
                # 回答者
                answerer = tmp[0].text.strip("\n").strip("回答:\u2002")
                # 发布日期
                date = self._format(tmp[1].text.strip("时间:"))
                # 回答总数
                count = None
                # 赞同数
                try:
                    agree = int(tmp[2].text.strip("获赞:\u2002").strip("次"))
                except ValueError:
                    agree = 0
                    answer = tmp[2].text.strip()
                # type_ = "video"
            else:
                # 回答
                __ = item.find("dd", class_="answer")
                answer = __.text.strip("答：") if __ else None
                # 问题
                __ = item.find("dd", class_="summary")
                question = __.text.strip("问：") if __ else None
                tmp = item.find("dd", class_="explain").findAll("span", class_="mr-8")
                # 发布日期
                date = (
                    item.find("dd", class_="explain").find("span", class_="mr-7").text
                )
                # 回答总数
                try:
                    count = int(str(tmp[-1].text).strip("\n").strip("个回答"))
                except Exception:
                    count = None
                # 回答者
                answerer = tmp[(-2 if len(tmp) >= 2 else -1)].text.strip("\n").strip("回答者:\xa0")
                # 赞同数
                __ = item.find("dd", class_="explain").find("span", class_="ml-10")
                agree = int(__.text.strip()) if __ else 0
                # type_ = "normal"
            # 生成结果
            result = {
                "title": title,
                "question": question,
                "answer": answer,
                "date": date,
                "count": count,
                "url": url,
                "agree": agree,
                "answerer": answerer,
                # "type": type_
            }
            results.append(result)  # 加入结果
        # 获取分页
        # wrap = bs.find("div", class_="pager")
        # pages_ = wrap.findAll("a")[:-2]
        # if "下一页" in pages_[-1].text:
        #     pages = pages_[-2].text
        # else:
        #     pages = pages_[-1].text
        return {
            "results": results,
            # 取最大页码
            # "pages": int(pages),
            "total": total,
        }

    def parse_video(self, content: str) -> dict:
        """解析百度视频搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度视频搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(content, "html.parser")
        # 锁定结果div
        data = bs.findAll("div", class_="video_short")
        if len(data) == 0:
            return {"results": None}
        results = []
        for res in data:
            __ = res.find("div", class_="video_small_intro")
            _ = __.find("a")
            # 标题
            title = self._format(_.text)
            # 链接
            url = _["href"]
            # 封面图片链接
            img = res.find("img", class_="border-radius")["src"].rsplit("?", 1)[0]
            # 时长
            length_ = res.find("span", class_="video_play_timer").text
            _ = [int(i) for i in length_.split(":")]
            if len(_) < 3:
                length_ = time(minute=_[0], second=_[1])
            else:
                length_ = time(_[0], _[1], _[2])
            # 简介
            try:
                des = __.find("div", class_="c-color-text").text
            except AttributeError:
                des = None
            # 来源
            try:
                origin = self._format(__.find("span", class_="wetSource").text).strip(
                    "来源："
                )
            except AttributeError:
                origin = None
            # 发布时间
            pub_time: str = __.findAll("span", class_="c-font-normal")[-1].text.strip(
                "发布时间："
            )
            try:
                __ = [int(i) for i in pub_time.split("-")]
            except ValueError:
                __ = self._convert_time(pub_time, True)
            pub_time = datetime(__[0], __[1], __[2])
            # 生成结果
            result = {
                "title": title,
                "url": url,
                "img": img,
                "length": length_,
                "des": des,
                "origin": origin,
                "pub_time": pub_time,
            }
            results.append(result)  # 加入结果
        return {"results": results}

    def parse_news(self, content: str) -> dict:
        """解析百度资讯搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度资讯搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._format(content), "html.parser")
        # 搜索结果总数
        total = int(
            bs.find("div", id="wrapper_wrapper")
            .find("span", class_="nums")
            .text.split("资讯", 1)[-1]
            .split("篇", 1)[0]
            .replace(",", "")
        )
        # 搜索结果容器
        data = (
            bs.find("div", id="content_left")
            .findAll("div")[1]
            .findAll("div", class_="result-op")
        )
        results = []
        for res in data:
            # 标题
            title = self._format(res.find("h3").find("a").text)
            # 链接
            url = res.find("h3").find("a")["href"]
            # 简介
            des = (
                res.find("div", class_="c-span-last")
                .find("span", class_="c-color-text")
                .text
            )
            _ = res.find("div", class_="c-span-last")
            # 作者
            author = _.find("span", class_="c-gap-right").text
            # 发布日期
            try:
                date = _.find("span", class_="c-color-gray2").text
            except AttributeError:
                date = None
            # 封面图片
            try:
                cover = res.find("div", class_="c-img-radius-large").find("img")["src"]
            except Exception:
                cover = None
            # 生成结果
            result = {
                "title": title,
                "author": author,
                "date": date,
                "des": des,
                "url": url,
                "cover": cover,
            }
            results.append(result)  # 加入结果
        # 获取所有页数
        # pages_ = bs.find("div", id="page").findAll("a")
        # # 过滤页码
        # if "< 上一页" in pages_[0].text:
        #     pages_ = pages_[1:]
        # if "下一页 >" in pages_[-1].text:
        #     pages_ = pages_[:-1]
        return {"results": results, "total": total}

    def __get_wenku_doc_type(self, t: int) -> str:
        if t in [1, 4, 10, 11, 9]:
            return "DOC"
        if t in [3, 6, 14, 15]:
            return "PPT"
        if t in [2, 5]:
            return "XLS"
        if t in [12]:
            return "VSD"
        if t in [7]:
            return "PDF"
        if t in [8]:
            return "TXT"
        if t in [16]:
            return "EPUB"
        if t in [19]:
            return "CAD"
        if t in [13]:
            return "RTF"
        if t in [20]:
            return "XMIND"
        return "UNKNOWN"

    def parse_wenku(self, content: str) -> dict:
        """解析百度文库搜索的页面源代码。

        Args:
            content (str): 已经转换为UTF-8编码的百度文库搜索API接口JSON数据

        Returns:
            dict: 解析后的结果
        """
        results = []
        pages = 0
        _ = json.loads(content)
        if _["status"]["msg"] != "success":
            raise RuntimeError
        for res in _["data"]["normalResult"]:
            info = res["docInfo"]
            author = res["authorInfo"]
            title = (
                info["title"]
                .replace("<em>", "")
                .replace("</em>", "")
                .replace(" - 百度文库", "")
            )
            des = info["content"].replace("<em>", "").replace("</em>", "")
            pub_date = strftime(r"%Y-%m-%d", localtime(int(info["createTime"])))
            page_num = info["pageNum"]
            score = info["qualityScore"]
            downloads = info["downloadCount"]
            url = info["url"]
            is_vip = info["flag"] == 28
            u_name = author["uname"]
            u_url = f"https://wenku.baidu.com/u/{u_name}?uid={author['uid']}"
            results.append(
                {
                    "title": title,
                    "des": des,
                    "pub_date": pub_date,
                    "pages": page_num,
                    "quality": score,
                    "downloads": downloads,
                    "url": url,
                    "is_vip": is_vip,
                    "uploader": {"name": u_name, "url": u_url},
                }
            )
        pages = math.ceil(
            (_["data"]["total"] - len(_["data"]["normalResult"])) / 10 + 1
        )
        return {"results": results, "pages": pages}

    def parse_jingyan(self, content: str) -> dict:
        """解析百度经验搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度经验搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        # 最小化代码
        code = self._minify(content)
        bs = BeautifulSoup(code, "html.parser")
        total = int(
            bs.find("div", class_="result-num")
            .text.split("约", 1)[-1]
            .split("个", 1)[0]
            .replace(",", "")
        )
        # 加载搜索结果
        data = bs.find("div", class_="search-list").findAll("dl")
        results = []
        for res in data:
            # 标题
            title = self._format(res.find("dt").find("a").text)
            # 链接
            url = "https://jingyan.baidu.com/" + res.find("dt").find("a")["href"]
            # 简介
            des = self._format(
                res.find("dd")
                .find("div", class_="summary")
                .find("span", class_="abstract")
                .text
            )
            # 获取发布日期和分类，位于`<span class="cate"/>`中
            _ = res.find("dd").find("div", class_="summary").find("span", class_="cate")
            tmp = self._format(_.text).split("-")
            # 发布日期
            pub_date = self._format(tmp[1]).replace("/", "-")
            # 分类
            category = self._format(tmp[-1]).strip("分类：").split(">")
            # 发布者
            publisher = {
                "name": self._format(_.find("a").text),
                "url": "https://jingyan.baidu.com" + _.find("a")["href"],
            }
            # 支持票数
            votes = int(
                self._format(
                    res.find("dt").find("span", class_="succ-times").text
                ).strip("得票")
            )
            # 是否为原创经验
            try:
                res.find("span", class_="i-original").text
                original = True
            except Exception:
                original = False
            # 是否为优秀经验
            try:
                res.find("span", class_="i-good-exp").text
                outstanding = True
            except Exception:
                outstanding = False
            # 生成结果
            result = {
                "title": title,
                "url": url,
                "des": des,
                "pub_date": pub_date,
                "category": category,
                "votes": votes,
                "publisher": publisher,
                "is_original": original,
                "is_outstanding": outstanding,
            }
            results.append(result)  # 加入结果到集合中
        # 获取分页
        # pages_ = bs.find("div", class_="pager-wrap").findAll("a", class_="pg-btn")
        # if not pages_:
        #     return {"results": results, "pages": 1}
        # if "下一页" in pages_[-1].text:
        #     pages_ = pages_[:-1]
        # pages = int(self._format(pages_[-1].text))
        return {"results": results, "total": total}

    def parse_baike(self, content: str) -> dict:
        """解析百度百科搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度百科搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        code = self._minify(content)
        # 创建BeautifulSoup对象
        soup = (
            BeautifulSoup(code, "html.parser")
            .find("div", class_="body-wrapper")
            .find("div", class_="searchResult")
        )
        # 获取百科总数
        total = int(
            soup.find("div", class_="result-count")
            .text.strip("百度百科为您找到相关词条约")
            .strip("个")
        )
        # 获取所有结果
        container = soup.findAll("dd")
        results = []
        for res in container:
            if res.select(".ad-footer"):
                continue
            # 链接
            url_pre = self._format(res.find("a", class_="result-title")["href"])
            url = (
                "https://baike.baidu.com"
                if url_pre.startswith("https://baike.baidu.com")
                else ""
            ) + url_pre
            # 标题
            title = self._format(res.find("a", class_="result-title").text)
            # 简介
            des = self._format(res.find("p", class_="result-summary").text)
            # 更新日期
            upd_date = self._format(res.find("span", class_="result-date").text)
            # 生成结果
            results.append(
                {"title": title, "des": des, "upd_date": upd_date, "url": url}
            )
        return {"results": results, "total": total}
