import json

from baiduspider._spider import BaseSpider
from baiduspider.util import handle_err
from bs4 import BeautifulSoup


class WebSubParser(BaseSpider):
    """网页搜索子解析模块。

    此模块为`BaiduSpider.mobile.search_web`函数的子模块，用于解析网页搜索子模块的HTML代码
    并返回Python字典。
    """

    def __init__(self) -> None:
        super().__init__()
        self.spider_name = "WebSubSpider"

    @handle_err
    def parse_video_block(self, video: BeautifulSoup) -> dict:
        """解析视频子块

        Args:
            video (BeautifulSoup): 从源HTML代码中提取的视频块BeautifulSoup对象

        Returns:
            dict: 解析后自动生成的Python结果字典对象
        """
        if video is None:
            return []
        video = video.find("article")
        tags_container = (
            video.find("section")
            .find("div", class_="c-tags-scroll-wrapper")
            .findAll("li")
        )
        v_url = video["rl-link-href"]
        results = []
        tags = []
        for tag in tags_container:
            text = self._format(tag.text)
            url = tag.find("a")["href"]
            tags.append({"text": text, "url": url})
        vid_container = video.findAll("div", class_="c-span")
        for vid in vid_container:
            vid = vid.find("div", class_="c-touchable-feedback-content")
            url = vid.find("a")["href"]
            _ = vid.find("div", class_="c-img")
            poster = _.find("img")["src"]
            labels = []
            __ = _.find("span", class_="c-label-radius")
            if __ is not None:
                labels.append(self._format(__.text))
            duration = None
            video_num = None
            __ = _.find("div", class_="c-img-info-br")
            if "视频" in __.text:
                video_num = int(self._format(__.text.strip("个视频")))
            elif ":" in __.text:
                duration = __.text
            title = self._format(vid.find("div", role="text").text)
            _ = vid.findAll("div", class_="c-line-clamp1")[-1]
            try:
                author_avatar = _.find("img")["src"]
                __ = _.findAll("span")
                author = self._format(__[0].text)
                if len(__) > 1 and "vid-scroll-pubtime" in __[1]["class"][0]:
                    pub_time = self._format(__[1].text)
                else:
                    pub_time = None
                __ = _.find("span", class_="c-label-radius")
                if __ is not None:
                    labels.append(__.text)
            except:
                author_avatar = None
                author = None
                pub_time = None
            results.append(
                {
                    "poster": poster,
                    "labels": labels,
                    "duration": duration,
                    "video_num": video_num,
                    "title": title,
                    "author_avatar": author_avatar,
                    "author": author,
                    "pub_time": pub_time,
                    "url": url,
                }
            )
        return {"results": results, "tags": tags, "url": v_url}

    @handle_err
    def parse_short_video_block(self, short_video: BeautifulSoup) -> dict:
        """解析短视频子块

        Args:
            short_video (BeautifulSoup): 从源HTML代码中提取的短视频块BeautifulSoup对象

        Returns:
            dict: 解析后自动生成的Python结果字典对象
        """
        if short_video is None:
            return []
        s_total = self._reformat_big_num(
            short_video.find("div", class_="middle")
            .find("span", class_="text")
            .text.strip("条\ue734"),
            "全部",
        )
        s_url = short_video.find("article")["rl-link-href"]
        short_video = short_video.find("section")
        short_video_container = short_video.findAll("div", class_="vid-pocket-item")
        results = []
        for vid in short_video_container:
            poster = vid.find("img")["data-lazy-src"]
            url = vid.parent.parent["href"]
            _ = vid.find("div", class_="c-color-white")
            try:
                author_avatar = _.find("img")["src"]
            except:
                author_avatar = None
            author = _.find("span", class_="c-color-white").text
            play_times = _.findAll("span")[-1].text
            if play_times is not None and "次播放" in play_times:
                delta = 1
                if "万" in play_times:
                    delta = 10000
                elif "亿" in play_times:
                    delta = 100000000
                play_times = int(
                    float(
                        play_times.replace("次播放", "").replace("万", "").replace("亿", "")
                    )
                    * delta
                )
            else:
                play_times = None
            title = vid.find("div", class_="c-gap-bottom-small").text
            results.append(
                {
                    "title": title,
                    "poster": poster,
                    "url": url,
                    "author_avatar": author_avatar,
                    "author": author,
                    "play_times": play_times,
                }
            )
        return {"results": results, "total": s_total, "url": s_url}

    @handle_err
    def parse_baike_block(self, baike: BeautifulSoup) -> dict:
        """解析百科子块

        Args:
            baike (BeautifulSoup): 从源HTML代码中提取的百科块BeautifulSoup对象

        Returns:
            dict: 解析后自动生成的Python结果字典对象
        """
        if baike is None:
            return []
        b_url = json.loads(baike["data-log"])["mu"]
        baike = baike.find("article")
        title = baike.find("h3", class_="c-title").text
        baike = baike.find("section")
        try:
            poster = baike.find("img", class_="c-img-img")["src"]
        except:
            poster = None
        des = baike.find("div", class_="c-abstract").text
        section_container = baike.findAll("a", class_="c-slink")
        sections = []
        for section in section_container:
            text = section.text
            url = section["href"]
            sections.append({"text": text, "url": url})
        _ = baike.find("div", class_="c-source")
        origin = _.find("span", class_="c-color-source").text
        label_container = _.findAll("span", class_="c-label-radius")
        labels = [l.text for l in label_container]
        result = {
            "title": title,
            "poster": poster,
            "des": des,
            "sections": sections,
            "origin": origin,
            "labels": labels,
            "url": b_url,
        }
        return {"result": result}

    @handle_err
    def parse_reyi_block(self, reyi: BeautifulSoup) -> dict:
        """解析热议子块

        Args:
            reyi (BeautifulSoup): 从源HTML代码中提取的热议块BeautifulSoup对象

        Returns:
            dict: 解析后自动生成的Python结果字典对象
        """
        if reyi is None:
            return []
        reyi = reyi.find("section")
        r_url = reyi.find("a", class_="c-blocka")["href"]
        r_total = self._reformat_big_num(
            reyi.find("a", class_="middle").text.strip("条\ue734"), "全部"
        )
        post_container = reyi.findAll("div", class_="tts-b-item")
        posts = []
        for post in post_container:
            _ = post.find("div", role="text")
            author_avatar = _.find("img")["src"]
            __ = _.find("div", class_="c-line-clamp1").findAll("span")
            author = __[0].text
            site = __[1].text
            pub_time = __[-1].text
            _ = post.find("div", role="option")
            des = _.find("p", class_="text-container").text.replace("\ue60b", "")
            __ = _.findAll("img", class_="c-img-img")
            images = []
            for img in __:
                try:
                    images.append(img["data-lazy-src"])
                except:
                    pass
            try:
                origin = _.find("div", class_="origin-content-new").text
            except:
                origin = None
            ___ = post.findAll("i", class_=["c-icon", "c-gap-inner-right-small"])
            __ = []
            for t in ___:
                for c in t["class"]:
                    if "zk-icon-size" in c:
                        __.append(t)
                        break
            __ = __[1:]
            try:
                comments = int(__[0].find_next_sibling("span").text.strip())
            except:
                comments = 0
            try:
                likes = int(__[1].find_next_sibling("span").text.strip())
            except:
                likes = 0
            posts.append(
                {
                    "author_avatar": author_avatar,
                    "author": author,
                    "site": site,
                    "pub_time": pub_time,
                    "des": des,
                    "images": images,
                    "origin": origin,
                    "comments": comments,
                    "likes": likes,
                }
            )
        return {"results": posts, "url": r_url, "total": r_total}

    @handle_err
    def parse_knowledge_block(self, knowledge: BeautifulSoup) -> dict:
        """解析相关知识子块

        Args:
            knowledge (BeautifulSoup): 从源HTML代码中提取的相关知识块BeautifulSoup对象

        Returns:
            dict: 解析后自动生成的Python结果字典对象
        """
        from pprint import pprint

        if knowledge is None:
            return []
        knowledge = knowledge.find("article")
        k_title = knowledge.find("header").find("h3").text
        knowledge_container = knowledge.findAll("div", class_="c-scroll-item")
        results = []
        for kl in knowledge_container:
            url = kl.find("a")["href"].replace("&amp;", "&")
            image = kl.find("img")["data-lazy-src"]
            title = kl.find("div", class_="c-color-link").text
            try:
                des = kl.find("div", class_="c-color-gray").text
                if not des.strip():
                    des = None
            except AttributeError:
                des = None
            results.append({"url": url, "image": image, "title": title, "des": des})
        return {"results": results, "title": k_title}
