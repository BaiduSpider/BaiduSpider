from baiduspider._spider import BaseSpider
from baiduspider.mobile.parser.subparser import WebSubParser
from baiduspider.util import handle_err
from bs4 import BeautifulSoup


class MobileParser(BaseSpider):
    def __init__(self) -> None:
        """百度移动端搜索解析器"""
        super().__init__()
        self.webSubParser = WebSubParser()
        self.WEB_NORMAL = "1599"
        self.WEB_VIDEO_NORMAL = "1508"
        self.WEB_VIDEO = "4295"
        self.WEB_SHORT_VIDEO = "4660"
        self.WEB_BAIKE = "1547"
        self.WEB_REYI = "201"
        self.WEB_KNOWLEDGE = "28339"

    @handle_err
    def parse_web(self, content: str) -> dict:
        """解析百度网页搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度网页搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        soup = BeautifulSoup(content, "html.parser")
        res_normal_container = soup.findAll(
            "div", class_="c-result", new_srcid=self.WEB_NORMAL
        )
        res_normal = []
        for res in res_normal_container:
            _ = res.find("div", class_="c-result-content").find("article")
            header = _.find("header")
            # 标签
            labels = []
            # 标题
            title = header.find("h3").find("span", class_="c-title-text").text
            # 链接
            try:
                url = _["rl-link-href"]
            except:
                url = header.find("a")["href"]
            __ = header.find("h3").find("span", class_="c-text-public")
            # “官方”标签
            if __ is not None:
                labels.append(__.text)
            section = _.find("section").find("section")
            _ = section.find("div", role="text")
            # （更新）日期
            try:
                date_ = _.find("span", class_="c-color-gray").text
                date = date_.replace("年", "-").replace("月", "-").replace("日", "")
            except:
                date = None
            __ = res.find("section").find("div", class_="c-flexbox")
            ___ = __.find("span", class_="c-text-box")
            # 热度标签
            if ___ is not None:
                labels.append(___.text)
            # 简介
            des = ""
            # 可能有多个`span`标签，需要依次解析
            for s in _.findAll("div"):
                for t in s.findAll("span"):
                    try:
                        if t.find("span").text:
                            continue
                    except:
                        pass
                    try:
                        if "c-color-gray" in t["class"]:
                            continue
                    except:
                        pass
                    des += t.text
                des += "\n"
            des = des.strip("\n")
            # 来源（作者）
            origin = __.find("span", class_="c-footer-showurl")
            if origin is not None:
                origin = origin.text
            else:
                origin = __.find("div", class_="single-text")
                if origin is not None:
                    origin = origin.text
            _ = section.find("a").find("div", role="img")
            # 封面图片链接
            if _ is not None and _.find("img") is not None:
                try:
                    img = _.find("img")["data-lazy-src"].replace("&amp;", "&")
                except:
                    img = _.find("img")["src"].replace("&amp;", "&")
            else:
                img = None
            section_container = res.findAll("a", class_="c-slink")
            sections = []
            for section in section_container:
                text = section.text
                url = section["href"]
                sections.append({"text": text, "url": url})
            res_normal.append(
                {
                    "title": title,
                    "url": url,
                    "labels": labels,
                    "date": date,
                    "des": des,
                    "origin": origin,
                    "img": img,
                    "sections": sections,
                    "type": "result",
                }
            )
        res_video_normal_container = soup.findAll(
            "div", class_="c-result", new_srcid=self.WEB_VIDEO_NORMAL
        )
        res_video_normal = []
        for res in res_video_normal_container:
            title = res.find("span", class_="c-title-text").text
            url = res.find("article")["rl-link-href"].replace("&amp;", "&")
            poster = res.find("img", class_="c-img-img")["src"]
            duration = res.find("div", class_="c-img-info-br").text
            video_num = None
            if "个" in duration:
                video_num = int(duration.strip("个视频"))
                duration = None
            info_container = res.findAll("a", class_="c-blocka")[-1].findAll(
                class_="c-color"
            )
            info = []
            for i in info_container:
                if i.text.startswith("作者："):
                    info.append({"data": i.text.strip("作者：").strip(), "type": "author"})
                elif i.text.startswith("简介："):
                    info.append({"data": i.text.strip("简介：").strip(), "type": "des"})
                elif i.text.startswith("时间："):
                    info.append({"data": i.text.strip("时间：").strip(), "type": "time"})
                elif i.text.startswith("播放："):
                    info.append(
                        {
                            "data": self._reformat_big_num(
                                i.text.strip("播放：").strip("次播放").strip()
                            ),
                            "type": "play_times",
                        }
                    )
                else:
                    info.append({"data": i.text.strip(), "type": "unknown"})
            labels = []
            _ = res.find("div", class_="c-img-radius-tl")
            __ = _.find("span", class_="c-label-radius")
            if __ is not None:
                labels.append(self._format(__.text))
            _ = res.find("div", class_="c-source-new")
            origin = _.find("div", class_="single-text").text
            __ = res.find("section").find("div", class_="c-flexbox")
            ___ = __.find("span", class_="c-text-box")
            # 热度标签
            if ___ is not None:
                labels.append(___.text)
            res_video_normal.append(
                {
                    "title": title,
                    "url": url,
                    "poster": poster,
                    "duration": duration,
                    "info": info,
                    "origin": origin,
                    "labels": labels,
                    "video_num": video_num,
                    "type": "video_normal",
                }
            )
        # 预处理视频子块
        video = soup.find("div", class_="c-result", new_srcid=self.WEB_VIDEO)
        video = self.webSubParser.parse_video_block(video)
        # 预处理短视频子块
        short_video = soup.find(
            "div", class_="c-result", new_srcid=self.WEB_SHORT_VIDEO
        )
        short_video = self.webSubParser.parse_short_video_block(short_video)
        # 预处理百科子块
        baike = soup.find("div", class_="c-result", new_srcid=self.WEB_BAIKE)
        baike = self.webSubParser.parse_baike_block(baike)
        # 预处理相关知识子块
        knowledge = soup.find("div", class_="c-result", new_srcid=self.WEB_KNOWLEDGE)
        knowledge = self.webSubParser.parse_knowledge_block(knowledge)
        pre_results = []
        # 预处理热议子块
        reyi = soup.find("div", class_="c-result", new_srcid=self.WEB_REYI)
        reyi = self.webSubParser.parse_reyi_block(reyi)
        # 加载视频子块
        if video:
            pre_results.append(
                dict(results=video["results"], tags=video["tags"], type="video")
            )
        # 加载短视频子块
        if short_video:
            pre_results.append(
                dict(
                    results=short_video["results"],
                    total=short_video["total"],
                    type="short_video",
                )
            )
        # 加载百科子块
        if baike:
            pre_results.append(dict(result=baike["result"], type="baike"))
        # 加载热议子块
        if reyi:
            pre_results.append(
                dict(
                    results=reyi["results"],
                    url=reyi["url"],
                    total=reyi["total"],
                    type="reyi",
                )
            )
        # 加载相关知识子块
        if knowledge:
            pre_results.append(
                dict(
                    results=knowledge["results"],
                    title=knowledge["title"],
                    type="knowledge",
                )
            )
        results = pre_results
        results.extend(res_normal)
        results.extend(res_video_normal)
        return {"results": results}
