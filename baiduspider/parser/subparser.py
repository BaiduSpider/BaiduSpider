from bs4 import BeautifulSoup

from baiduspider._spider import BaseSpider
from baiduspider.util import handle_err


class WebSubParser(BaseSpider):
    def __init__(self) -> None:
        super().__init__()
        self.spider_name = "WebSubSpider"

    @handle_err
    def parse_news_block(self, news: BeautifulSoup):
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
    def parse_video_block(self, video: BeautifulSoup):
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
    def parse_baike_block(self, baike: BeautifulSoup):
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
        return baike

    @handle_err
    def parse_tieba_block(self, tieba: BeautifulSoup):
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
        return tieba

    @handle_err
    def parse_blog_block(self, blog: BeautifulSoup):
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
    def parse_gitee_block(self, gitee: BeautifulSoup):
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
