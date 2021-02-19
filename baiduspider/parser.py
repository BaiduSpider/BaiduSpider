import json
from html import unescape

from bs4 import BeautifulSoup, ResultSet

from baiduspider._spider import BaseSpider
from baiduspider.errors import ParseError


class Parser(BaseSpider):
    def __init__(self) -> None:
        super().__init__()

    def parse_web(self, content: str) -> dict:
        """解析百度网页搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度网页搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        soup = BeautifulSoup(content, "html.parser")
        if soup.find("div", id="content_left") is None:
            raise ParseError("Invalid HTML content.")
        # 获取搜索结果总数
        num = int(
            str(soup.find("span", class_="nums_text").text)
            .strip("百度为您找到相关结果约")
            .strip("个")
            .replace(",", "")
        )
        # 查找运算窗口
        calc = soup.find("div", class_="op_new_cal_screen")
        # 定义预结果（运算以及相关搜索）
        pre_results = []
        # 预处理相关搜索
        try:
            _related = soup.find("div", id="rs").find("table").find_all("th")
        except AttributeError:
            _related = []
        related = []
        # 预处理新闻
        news = soup.find(
            "div", class_="result-op", tpl="sp_realtime_bigpic5", srcid="19"
        )
        # 确认是否有新闻块
        try:
            self._format(news.find("h3", class_="t").find("a").text)
        except:
            news_detail = []
        else:
            news_rows = news.findAll("div", class_="c-row")
            news_detail = []
            prev_row = {}
            for row in news_rows:
                try:
                    row_title = self._format(row.find("a").text)
                except AttributeError:
                    prev_row["des"] = self._format(row.text)
                    continue
                row_time = self._format(row.find("span", class_="c-color-gray2").text)
                row_author = self._format(row.find("span", class_="c-color-gray").text)
                row_url = self._format(row.find("a")["href"])
                news_detail.append(
                    {
                        "title": row_title,
                        "time": row_time,
                        "author": row_author,
                        "url": row_url,
                        "des": None,
                    }
                )
                prev_row = news_detail[-1]
        # 预处理短视频
        video = soup.find("div", class_="op-short-video-pc")
        if video:
            video_rows = video.findAll("div", class_="c-row")
            video_results = []
            for row in video_rows:
                row_res = []
                videos = row.findAll("div", class_="c-span3")
                for v in videos:
                    v_link = v.find("a")
                    v_title = v_link["title"]
                    v_url = self._format(v_link["href"])
                    v_img = v_link.find("img")["src"]
                    v_len = self._format(
                        v.find("div", class_="op-short-video-pc-duration-wrap-new").text
                    )
                    v_from = self._format(
                        v.find("div", class_="op-short-video-pc-clamp1").text
                    )
                    row_res.append(
                        {
                            "title": v_title,
                            "url": v_url,
                            "cover": v_img,
                            "length": v_len,
                            "origin": v_from,
                        }
                    )
                video_results += row_res
        else:
            video_results = []
        # 一个一个append相关搜索
        for _ in _related:
            if _.text:
                related.append(_.text)
        # 预处理百科
        baike = soup.find("div", class_="c-container", tpl="bk_polysemy")
        if baike:
            b_title = self._format(baike.find("h3").text)
            b_url = baike.find("a")["href"]
            b_des = self._format(baike.find("div", class_="c-span-last").find("p").text)
            try:
                b_cover = baike.find("div", class_="c-span3").find("img")["src"]
                b_cover_type = "image"
            except (TypeError, AttributeError):
                try:
                    b_cover = baike.find("video", class_="op-bk-polysemy-video")[
                        "data-src"
                    ]
                    b_cover_type = "video"
                except TypeError:
                    b_cover = None
                    b_cover_type = None
            baike = {
                "title": b_title,
                "url": b_url,
                "des": b_des,
                "cover": b_cover,
                "cover-type": b_cover_type,
            }
        # 预处理贴吧
        tieba = BeautifulSoup(content, "html.parser").find("div", srcid="10")
        if tieba:
            t_title = self._format(tieba.find("h3").text)
            t_url = tieba["mu"]
            try:
                t_info_ = tieba.find(
                    "div", class_="op-tieba-general-col-top-xs"
                ).findAll("p")
                t_des = self._format(t_info_[0].text)
            except AttributeError:
                t_des = None
            t_followers = self._format(
                tieba.find("div", class_="c-span-last").find("span").find("span").text
            )
            t_total = self._format(
                tieba.find("div", class_="c-span-last").findAll("span")[-1].text
            )
            try:
                t_cover = tieba.find("a", class_="op-tieba-general-photo-link").find(
                    "img"
                )["src"]
            except AttributeError:
                t_cover = None
            t_hot_ = tieba.findAll("div", class_="c-row")[1:]
            t_hot = []
            i = 1
            for hot in t_hot_:
                t_h_title = self._format(hot.find("a").text)
                t_h_url = hot.find("a")["href"]
                t_h_clicks = self._format(hot.find("span").find("span").text)
                t_h_replies = self._format(hot.findAll("span")[2].find("span").text)
                t_hot.append(
                    {
                        "title": t_h_title,
                        "url": t_h_url,
                        "clicks": t_h_clicks,
                        "replies": t_h_replies,
                    }
                )
                i += 1
            del i
            tieba = {
                "title": t_title,
                "url": t_url,
                "des": t_des,
                "followers": t_followers,
                "total": t_total,
                "cover": t_cover,
                "hot": t_hot,
            }
        # 预处理博客
        article_tags = BeautifulSoup(content, "html.parser").findAll("article")
        blog = None
        for tmp in article_tags:
            if tmp["class"][-1].startswith("open-source-software-blog"):
                blog = tmp
                break
        if blog is not None:
            blog = blog.find("section")
            b_title = blog.find("h3", class_="c-title").text
            b_url = blog.find("a")["href"]
            b_blogs_ = blog.findAll("div", class_="c-row")
            b_blogs = []
            for b in b_blogs_:
                b_current_blog_header = b.find("div")
                b_blog_title = b_current_blog_header.find("a").text
                b_blog_url = b_current_blog_header.find("a")["href"]
                b_blog_origin = b_current_blog_header.find(
                    "span", class_="nor-src-wrap"
                ).text
                try:
                    b_current_blog_tags = b.findAll("div")[1].findAll("span")
                    b_blog_tags = [tag.text for tag in b_current_blog_tags]
                except IndexError:
                    b_blog_tags = []
                b_blog_parent = b.find_parent("div").findAll("div")
                b_blog_des = None
                for p in b_blog_parent:
                    if p["class"][0].startswith("blog-summary"):
                        b_blog_des = p.text
                        break
                b_blogs.append(
                    {
                        "title": b_blog_title,
                        "url": b_blog_url,
                        "origin": b_blog_origin,
                        "tags": b_blog_tags,
                        "des": b_blog_des,
                    }
                )
            blog = {"title": b_title, "url": b_url, "blogs": b_blogs}
        # 预处理码云
        gitee = None
        for tmp in article_tags:
            if tmp["class"][-1].startswith("osc-gitee"):
                gitee = tmp
                break
        if gitee is not None:
            g_title = gitee.find("h3", class_="c-title").text
            g_url = gitee.find("a", class_="c-blocka")["href"]
            gitee = gitee.find("section").find("div", class_="c-tabs-content-wrapper")
            g_tabs = gitee.findAll("div", class_="c-tabs-content")
            g_intro = g_tabs[0].find("div", class_="c-tabs-item").find("div")
            g_des = g_intro.find("div").text
            g_license = (
                g_intro.findAll("div")[1].text.lstrip("开源协议：")
                if len(g_intro.findAll("div")) >= 2
                and g_intro.findAll("div")[1].text.startswith("开源协议：")
                else None
            )
            g_lang = (
                g_intro.findAll("div")[2].text.lstrip("开发语言：")
                if len(g_intro.findAll("div")) >= 2
                and g_intro.findAll("div")[1].text.startswith("开发语言：")
                or len(g_intro.findAll("div")) >= 3
                and g_intro.findAll("div")[2].text.startswith("开发语言：")
                else None
            )
            g_temp = g_intro.findAll("span")
            g_star = int(g_temp[0].text.strip("Star："))
            g_fork = int(g_temp[1].text.strip("Fork："))
            g_watch = int(g_temp[2].text.strip("Watch："))
            g_status = g_tabs[-1].find("img")["src"]
            gitee = {
                "title": g_title,
                "url": g_url,
                "des": g_des,
                "license": g_license,
                "lang": g_lang,
                "star": g_star,
                "fork": g_fork,
                "watch": g_watch,
                "status": g_status,
            }
        # 加载贴吧
        if tieba:
            pre_results.append(dict(type="tieba", result=tieba))
        # 加载博客
        if blog:
            pre_results.append(dict(type="blog", result=blog))
        # 加载码云
        if gitee:
            pre_results.append(dict(type="gitee", result=gitee))
        # 加载搜索结果总数
        if num != 0:
            pre_results.append(dict(type="total", result=num))
        # 加载运算
        if calc:
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
        if related:
            pre_results.append(dict(type="related", results=related))
        # 加载资讯
        if news_detail:
            pre_results.append(dict(type="news", results=news_detail))
        # 加载短视频
        if video_results:
            pre_results.append(dict(type="video", results=video_results))
        # 加载百科
        if baike:
            pre_results.append(dict(type="baike", result=baike))
        # 预处理源码
        soup = BeautifulSoup(content, "html.parser")
        results = soup.findAll("div", class_="result")
        res = []
        for result in results:
            des = None
            try:
                result["tpl"]
            except:
                continue
            soup = BeautifulSoup(self._minify(str(result)), "html.parser")
            # 链接
            href = soup.find("a").get("href").strip()
            # 标题
            title = self._format(str(soup.find("a").text))
            # 时间
            try:
                time = self._format(
                    soup.findAll("div", class_="c-abstract")[0]
                    .find("span", class_="newTimeFactor_before_abs")
                    .text
                )
            except (AttributeError, IndexError):
                time = None
            try:
                # 简介
                des = soup.find_all("div", class_="c-abstract")[0].text
                soup = BeautifulSoup(str(result), "html.parser")
                des = self._format(des).lstrip(str(time)).strip()
            except IndexError:
                try:
                    des = des.replace("mn", "")
                except (UnboundLocalError, AttributeError):
                    des = None
            if time:
                time = time.split("-")[0].strip()
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
            try:
                result["tpl"]
            except:
                print(result.prettify())
            is_not_special = (
                result["tpl"]
                not in [
                    "short_video_pc",
                    "sp_realtime_bigpic5",
                    "bk_polysemy",
                    "tieba_general",
                ]
                and result.find("article") is None
            )
            domain = None
            if is_not_special:  # 确保不是特殊类型的结果
                # 获取可见的域名
                try:
                    domain = (
                        result.find("div", class_="c-row")
                        .find("div", class_="c-span-last")
                        .find("div", class_="se_st_footer")
                        .find("a", class_="c-showurl")
                        .text
                    )
                except Exception:
                    try:
                        domain = (
                            result.find("div", class_="c-row")
                            .find("div", class_="c-span-last")
                            .find("p", class_="op-bk-polysemy-move")
                            .find("span", class_="c-showurl")
                            .text
                        )
                    except Exception:
                        try:
                            domain = (
                                result.find("div", class_="se_st_footer")
                                .find("a", class_="c-showurl")
                                .text
                            )
                        except:
                            domain = None
                if domain:
                    domain = domain.replace(" ", "")
            # 加入结果
            if title and href and is_not_special:
                res.append(
                    {
                        "title": title,
                        "des": des,
                        "origin": domain,
                        "url": href,
                        "time": time,
                        "type": "result",
                    }
                )
        soup = BeautifulSoup(content, "html.parser")
        soup = BeautifulSoup(str(soup.findAll("div", id="page")[0]), "html.parser")
        # 分页
        pages_ = soup.findAll("span", class_="pc")
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        # 如果搜索结果仅有一页时，百度不会显示底部导航栏
        # 所以这里直接设置成1，如果不设会报错`TypeError`
        if not pages:
            pages = [1]
        # 设置最终结果
        result = pre_results
        result.extend(res)
        return {
            "results": result,
            # 最大页数
            "pages": max(pages),
        }

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
        bs = BeautifulSoup(content, "html.parser")
        pages_ = bs.find("div", id="page").findAll("span", class_="pc")
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        return {
            "results": results,
            # 取最大页码
            "pages": max(pages),
        }

    def parse_zhidao(self, content: str) -> dict:
        """解析百度知道搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度知道搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._minify(content), "html.parser")
        # 所有搜索结果
        list_ = bs.find("div", class_="list").findAll("dl")
        results = []
        for item in list_:
            # 屏蔽企业回答
            if "ec-oad" in item["class"]:
                continue
            # 标题
            title = item.find("dt").text.strip("\n")
            # 链接
            try:
                url = item.find("dt").find("a")["href"]
            except KeyError:
                url = item.find("dt").find("a")["data-href"]
            # 简介
            des = item.find("dd", class_="dd").text
            tmp = item.find("dd", class_="explain").findAll("span", class_="mr-8")
            # 发布日期
            date = item.find("dd", class_="explain").find("span", class_="mr-7").text
            # 回答总数
            count = int(str(tmp[-1].text).strip("\n").strip("个回答"))
            # 生成结果
            result = {
                "title": title,
                "des": des,
                "date": date,
                "count": count,
                "url": url,
            }
            results.append(result)  # 加入结果
        # 获取分页
        wrap = bs.find("div", class_="pager")
        pages_ = wrap.findAll("a")[:-2]
        if "下一页" in pages_[-1].text:
            total = pages_[-2].text
        else:
            total = pages_[-1].text
        return {
            "results": results,
            # 取最大页码
            "pages": int(total),
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
        data = bs.findAll("li", class_="result")
        results = []
        for res in data:
            # 标题
            title = res.find("a")["title"]
            # 链接
            url = "https://v.baidu.com" + res.find("a")["href"]
            # 封面图片链接
            img = res.find("img", class_="img-normal-layer")["src"]
            # 时长
            time = res.find("span", class_="info").text
            # 生成结果
            result = {"title": title, "url": url, "img": img, "time": time}
            results.append(result)  # 加入结果
        # 分页
        wrap = bs.find("div", class_="page-wrap")
        pages_ = wrap.findAll("a", class_="filter-item")[:-1]
        try:
            pages = int(pages_[-1].text)
        except:
            pages = 0
        return {"results": results, "pages": pages}

    def parse_news(self, content: str) -> dict:
        """解析百度资讯搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度资讯搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._format(content), "html.parser")
        # 搜索结果容器
        data = (
            bs.find("div", id="content_left")
            .findAll("div")[1]
            .findAll("div", class_="result-op")
        )
        # print(len(data))
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
            # 作者
            author = (
                res.find("div", class_="c-span-last")
                .find("div", class_="news-source")
                .find("span", class_="c-gap-right")
                .text
            )
            # 发布日期
            date = (
                res.find("div", class_="c-span-last")
                .find("div", class_="news-source")
                .find("span", class_="c-color-gray2")
                .text
            )
            # 生成结果
            result = {
                "title": title,
                "author": author,
                "date": date,
                "des": des,
                "url": url,
            }
            results.append(result)  # 加入结果
        # 获取所有页数
        pages_ = bs.find("div", id="page").findAll("a")
        # 过滤页码
        if "< 上一页" in pages_[0].text:
            pages_ = pages_[1:]
        if "下一页 >" in pages_[-1].text:
            pages_ = pages_[:-1]
        return {"results": results, "pages": int(pages_[-1].text)}

    def parse_wenku(self, content: str) -> dict:
        """解析百度文库搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度文库搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(content, "html.parser")
        data = bs.findAll("dl")
        results = []
        for res in data:
            dt = res.find("dt")
            type_ = self._format(
                dt.find("p", class_="fl").find("span", class_="ic")["title"]
            ).upper()
            tmp = dt.find("p", class_="fl").find("a")
            title = self._format(tmp.text)
            url = tmp["href"]
            try:
                quality = float(
                    self._format(
                        res.find("p", class_="fr").findAll("span", class_="ib")[1].text
                    )
                )
            except:
                quality = None
            dd = res.find("dd", class_="clearfix").find("div", class_="summary-box")
            des = self._format(dd.find("p", class_="summary").text)
            try:
                dd_tags = res.find("dd", class_="tag-tips")
                tags = []
                for a in dd_tags.findAll("a"):
                    tags.append(self._format(a.text))
            except AttributeError:
                tags = []
            detail = dd.find("div", class_="detail").find("div", class_="detail-info")
            date = self._format(detail.text.split("|")[0])
            pages = int(
                self._format(
                    detail.text.split("|")[1].replace("共", "").replace("页", "")
                )
            )
            downloads = int(self._format(detail.text.split("|")[2].strip("次下载")))
            result = {
                "title": title,
                "type": type_,
                "url": url,
                "des": des,
                "date": date,
                "pages": pages,
                "downloads": downloads,
            }
            results.append(result)
        pages_ = bs.find("div", class_="page-content").findAll("a")
        if "尾页" in pages_[-1].text:
            total = int(int(pages_[-1]["href"].split("&")[-1].strip("pn=")) / 10 + 1)
        else:
            total = int(
                bs.find("div", class_="page-content").find("span", class_="cur").text
            )
        return {"results": results, "pages": total}
