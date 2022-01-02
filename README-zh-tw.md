<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/BaiduSpider/BaiduSpider">
    <img src="https://baiduspider.github.io/assets/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BaiduSpider</h3>

  <p align="center">
    一個爬取百度的利器
    <br />
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README.md"><strong>简体中文</strong></a>
    |
    <span>繁體中文</span>
    |
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README-en.md"><strong>English</strong></a>
    <br />
    <a href="https://baiduspider.github.io/"><strong>快速上手 »</strong></a>
    <br />
    <br />
    <a href="https://baiduspider.github.io/usage/get-started/">查看示例</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">報告問題</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">請求需求</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>目錄</summary>
  <ol>
    <li>
      <a href="#關於本項目">關於本項目</a>
      <ul>
        <li><a href="#制作依賴">制作依賴</a></li>
      </ul>
    </li>
    <li>
      <a href="#起步">起步</a>
      <ul>
        <li><a href="#預先條件">預先條件</a></li>
        <li><a href="#安裝">安裝</a></li>
      </ul>
    </li>
    <li><a href="#簡單使用">簡單使用</a></li>
    <li><a href="#項目路線圖">項目路線圖</a></li>
    <li><a href="#共同維護">共同維護</a></li>
    <li><a href="#開源協議">開源協議</a></li>
    <li><a href="#聯系方式">聯系方式</a></li>
    <li><a href="#免責聲明">免責聲明</a></li>
    <li><a href="#貢獻者">貢獻者</a></li>
    <li><a href="#致謝">致謝</a></li>
  </ol>
</details>


<!-- ## 警告

此分支為`dev`分支，也就是開發分支。也就是說，所有代碼或功能可能都不穩定，僅供參考。不建議在開源項目中使用此分支的BaiduSpider。 -->


<!-- ABOUT THE PROJECT -->
## 關於本項目

[![項目截圖][product-screenshot]](https://baiduspider.github.io)

搜索引擎是一個十分強大的工具，如果能讓其他工具集成搜索引擎的眾多強大功能，那麼必將變得更加強大。但是，目前我沒有找到一個可以精準提取搜索引擎搜索結果的開源爬蟲。於是，我便編寫了這個爬取百度搜索引擎的項目：BaiduSpider。

BaiduSpider的獨特功能:
* 節省提取數據的時間，對於類似深度學習項目的數據模型建立與訓練起到了良好的幫助。

* 精準提取數據，並刪除廣告。

* 搜索結果大而全，支持多種搜索類型，支持多種返回類型。

當然，沒有一個項目是完美的。任何一個項目的發展都需要社區的幫助。你可以通過發布一個Issue或提交一個PR來幫助BaiduSpider進步！:smile:

一些比較有幫助的文檔或工具我將在最後的致謝部分中列出。

### 制作依賴

一些BaiduSpider使用的主要開源依賴包。

* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/zh_CN/latest/)



<!-- GETTING STARTED -->
## 起步

以安裝BaiduSpider，請按照以下幾個步驟操作。

### 預先條件

在安裝BaiduSpider之前，請確保你安裝了`Python3.6+`：

```sh
$ python --version
```

若版本小於`3.6.0`，請到[Python官網](https://www.python.org/downloads/)下載並安裝Python。

### 安裝

#### 使用`pip`安裝

請在命令行中輸入下列指令：

```sh
$ pip install baiduspider
```

#### 從GitHub手動安裝

```sh
$ git clone git@github.com:BaiduSpider/BaiduSpider.git

# ...

$ python setup.py install
```


<!-- USAGE EXAMPLES -->
## 簡單使用

你可以使用BaiduSpider通過短短的幾行代碼來獲取百度的網頁搜索結果：

```python
# 導入BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# 實例化BaiduSpider
spider = BaiduSpider()

# 搜索網頁
pprint(spider.search_web(query='Python'))
```

_更多樣例和配置，請參照[文檔](https://baiduspider.github.io)_



<!-- ROADMAP -->
## 項目路線圖

請參考[open issues](https://github.com/BaiduSpider/BaiduSpider/issues)以獲取最新的項目規劃以及已知問題。



<!-- CONTRIBUTING -->
## 共同維護

項目貢獻是開源項目的靈魂所在，也是整個開源社區學習、交流、獲得靈感的地方。任何貢獻都將**極力歡迎**。

1. Fork此項目
2. 創建你的feature分支 (`git checkout -b NewFeatures`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送更改 (`git push origin username/BaiduSpider`)
5. 提交一個PR



<!-- LICENSE -->
## 開源協議

此項目的開源協議為`GPL-V3`，詳情請參見`LICENSE`。



<!-- CONTACT -->
## 聯系方式

samzhangjy - [@samzhangjy](https://twitter.com/samzhangjy) - samzhang951@outlook.com

項目鏈接: [https://github.com/BaiduSpider/BaiduSpider](https://github.com/BaiduSpider/BaiduSpider)


## 免責聲明

此項目僅作為學習用途，不可商用或爬取百度大量數據。此外，本項目使用`GPL-V3`版權協議，意味著涉及（使用）此項目的任何其它項目必須開源且註明出處，並且本項目作者將不承擔任何法律風險。特此說明，違者後果自負。


## 貢獻者

<a href="https://github.com/baiduspider/baiduspider/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=baiduspider/baiduspider" />
</a>


<!-- ACKNOWLEDGEMENTS -->
## 致謝
* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/zh_CN/latest/)
* [Img Shields](https://shields.io)
* [Gitmoji](https://gitmoji.dev/)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/BaiduSpider/BaiduSpider?style=for-the-badge
[contributors-url]: https://github.com/BaiduSpider/BaiduSpider/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/BaiduSpider/BaiduSpider?style=for-the-badge
[forks-url]: https://github.com/BaiduSpider/BaiduSpider/network/members
[stars-shield]: https://img.shields.io/github/stars/BaiduSpider/BaiduSpider?style=for-the-badge
[stars-url]: https://github.com/BaiduSpider/BaiduSpider/stargazers
[issues-shield]: https://img.shields.io/github/issues/BaiduSpider/BaiduSpider?style=for-the-badge
[issues-url]: https://github.com/BaiduSpider/BaiduSpider/issues
[license-shield]: https://img.shields.io/github/license/BaiduSpider/BaiduSpider?style=for-the-badge
[license-url]: https://github.com/BaiduSpider/BaiduSpider/blob/master/LICENSE
[product-screenshot]: https://i.loli.net/2021/04/22/V7gGrmTDlfR5U24.png