import json
from datetime import datetime, time
from typing import Dict

from baiduspider._spider import BaseSpider
from baiduspider.util import handle_err
from bs4 import BeautifulSoup, Comment


class WebSubParser(BaseSpider):
    """网页搜索子解析模块。

    此模块为`BaiduSpider.search_web`函数的子模块，用于解析网页搜索子模块的HTML代码
    并返回Python字典。
    """

    def __init__(self) -> None:
        super().__init__()
        self.spider_name = "WebSubSpider"

    @handle_err
    def parse_news_block(self, news: BeautifulSoup) -> Dict:
        """解析资讯子块

        Args:
            news (BeautifulSoup): 从源HTML代码中提取的资讯块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
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
        return news_detail

    @handle_err
    def parse_video_block(self, video: BeautifulSoup) -> Dict:
        """解析视频子块

        Args:
            video (BeautifulSoup): 从源HTML代码中提取的视频块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
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
        return video_results

    @handle_err
    def parse_baike_block(self, baike: BeautifulSoup) -> Dict:
        """解析百科子块

        Args:
            baike (BeautifulSoup): 从源HTML代码中提取的百科块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
        if baike:
            b_title = self._format(baike.find("h3").text)
            b_url = baike.find("a")["href"]
            b_des = self._format(
                baike.find("div", class_="c-span-last")
                .find("div", class_="c-font-normal")
                .text
            )
            try:
                b_cover = baike.find("div", class_="c-span3").find("img")["src"]
                b_cover_type = "image"
            except (TypeError, AttributeError):
                try:
                    b_cover = (
                        baike.find("div", class_="op-bk-polysemy-imgWrap")
                        .find("div", class_="c-img")["style"]
                        .split("url", 1)[-1]
                        .split(")", 1)[0]
                        .strip("(")
                    )
                    b_cover_type = "video"
                except (TypeError):
                    b_cover = None
                    b_cover_type = None
            baike = {
                "title": b_title,
                "url": b_url,
                "des": b_des,
                "cover": b_cover,
                "cover-type": b_cover_type,
            }
        return baike

    @handle_err
    def parse_tieba_block(self, tieba: BeautifulSoup) -> Dict:
        """解析贴吧子块

        Args:
            tieba (BeautifulSoup): 从源HTML代码中提取的贴吧块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
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
            t_hot_ = tieba.findAll("div", class_="c-row")[1:-1]
            t_hot = []
            i = 1
            for hot in t_hot_:
                t_h_title = self._format(hot.find("a").text)
                t_h_url = hot.find("a")["href"]
                t_h_clicks = self._format(
                    hot.find("div", class_="c-color-gray2").find("span").text
                )
                t_h_replies = self._format(
                    hot.findAll("div", class_="c-color-gray2")[-1].find("span").text
                )
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
        return tieba

    @handle_err
    def parse_blog_block(self, blog: BeautifulSoup) -> Dict:
        """解析博客子块

        Args:
            blog (BeautifulSoup): 从源HTML代码中提取的博客块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
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
        return blog

    @handle_err
    def parse_gitee_block(self, gitee: BeautifulSoup) -> Dict:
        """解析Gitee仓库子块

        Args:
            gitee (BeautifulSoup): 从源HTML代码中提取的码云仓库块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
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
        return gitee

    @handle_err
    def parse_music_block(self, music: BeautifulSoup) -> Dict:
        """解析音乐子块

        Args:
            music (BeautifulSoup): 从源HTML代码中提取的音乐块BeautifulSoup对象

        Returns:
            Dict: 解析后自动生成的Python结果字典对象
        """
        if music is not None:
            # 从注释中获取结果JSON
            music = json.loads(
                music.find(text=lambda text: isinstance(text, Comment)).strip(
                    "s-data: "
                )
            )
            m_title = music["title"].replace("<em>", "").replace("</em>", "")  # 搜索结果标题
            m_url = music["url"]  # 搜索结果链接
            m_songs = []  # 搜索结果歌曲
            for song in music["data"]["site"]:
                # 歌手信息
                s_singer = [
                    {"url": i["singerUrl"], "name": i["singerName"]}
                    for i in song["singer"]
                ]
                # 预处理歌曲发布时间
                try:
                    __ = song["publishTime"].split("-")
                except KeyError:
                    __ = None
                # 预处理歌曲时长
                _ = int(song["duration"])
                # 歌曲信息
                s_song = {
                    "name": song["displaySongName"],  # 歌曲名称
                    "url": song["songUrl"],  # 歌曲链接
                    "poster": song["poster"],  # 歌曲海报图片链接
                    "is_original": bool(int(song["isOriginal"])),  # 是否为原唱
                    "pub_date": datetime(int(__[0]), int(__[1]), int(__[2]))
                    if __ is not None
                    else None,  # 歌曲发布时间
                    "labels": [i["txt"] for i in song["labels"]],  # 歌曲标签
                    "copyright": bool(int(song["copyRight"])),  # 歌曲是否有版权
                    "site": song["sitePinyin"],  # 歌曲发布站点（拼音）
                    "duration": time(
                        hour=int(_ / 60 / 60), minute=int(_ / 60), second=int(_ % 60)
                    ),  # 歌曲时长
                    "other_sites": song["allWapPlayFile"],  # 歌曲其他网站链接
                }
                # 歌曲发布公司
                try:
                    s_song["pub_company"] = song["pubCompany"]
                    if song["pubCompany"] == "null":
                        s_song["pub_company"] = None
                except KeyError:
                    s_song["pub_company"] = None
                # 歌曲专辑
                try:
                    s_album = {
                        "url": song["album"]["albumUrl"],
                        "name": song["album"]["albumName"],
                    }
                except KeyError:
                    s_album = None
                m_songs.append({"song": s_song, "singer": s_singer, "album": s_album})
            music = {"title": m_title, "url": m_url, "songs": m_songs}
        return music
