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
    A perfect tool for crawling Baidu
    <br />
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README.md"><strong>简体中文</strong></a>
    |
    <a href="https://github.com/BaiduSpider/BaiduSpider/blob/dev/README-zh-tw.md"><strong>繁體中文</strong></a>
    |
    <span>English</span>
    <br />
    <a href="https://baiduspider.github.io/"><strong>Getting Started »</strong></a>
    <br />
    <br />
    <a href="https://baiduspider.github.io/usage/get-started/">View Demo</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">Report Issue</a>
    ·
    <a href="https://github.com/BaiduSpider/BaiduSpider/issues">Feature Request</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#License">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#disclaimer">Disclaimer</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- ## WARNING

This is the `dev` branch, which is the development branch. All code or features may be unstable, it is for reference only. We do NOT recommend using this version of BaiduSpider in open source projects. -->


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product screenshot][product-screenshot]](https://baiduspider.github.io)

Search engine is a very powerful tool. However, if other tools could implant the most features of the search engine, then it will be even more powerful. But, I have not found any web spider to extract the search results accurately. So, with that goal in mind, I developed this project to crawl Baidu: BaiduSpider.

Here's why:
* Makes the time of extracting data less, which speeds up the development of projects like deep-learning.

* Extract data accurately, without Ads.

* Provides in-detailed search results, supports multiple search types and return models.

Of course, nothing is perfect, including this project. Any open-source project needs the community's help. You can help BaiduSpider by opening an issue or submit a PR! :smile:

Some of the helpful documentations and tools will be listed in the acknowledgements.

### Built With

Some open-source packages used in BaiduSpider.

* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
* [requests](https://docs.python-requests.org/zh_CN/latest/)



<!-- GETTING STARTED -->
## Getting Started

Please follow the steps below in order to install BaiduSpider.

### Prerequisites

Before installing BaiduSpider, please make sure you have `Python3.6+` installed:

```sh
$ python --version
```

If the version is lower than `3.6.0`, please go to [python.org](https://www.python.org/downloads/) to download and install a higher version of Python.

### Installation

#### Installing Using `pip`

Please enter the following commands in the terminal:

```sh
$ pip install baiduspider
```

#### Installing Manually Using GitHub

```sh
$ git clone git@github.com:BaiduSpider/BaiduSpider.git

# ...

$ python setup.py install
```


<!-- USAGE EXAMPLES -->
## Usage

You can get the search result by using one simple command using BaiduSpider:

```python
# Import BaiduSpider
from baiduspider import BaiduSpider
from pprint import pprint

# Generate the BaiduSpider object
spider = BaiduSpider()

# Search the web
pprint(spider.search_web(query='Python'))
```

_For more examples and configurations, please refer to the [documentation](https://baiduspider.github.io)._



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/BaiduSpider/BaiduSpider/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b NewFeatures`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin username/BaiduSpider`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-V3 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

samzhangjy - [@samzhangjy](https://twitter.com/samzhangjy) - samzhang951@outlook.com

Project Link: [https://github.com/BaiduSpider/BaiduSpider](https://github.com/BaiduSpider/BaiduSpider)


## Disclaimer

This project can only be used for learning purposes and cannot be used in commercial projects or crawl a lot of data. Also, BaiduSpider is distributed under the `GPL-V3` license, meaning any project using BaiduSpider must be open-source and link to this project. The author of this project will not afford any legal risks. It is hereby stated that offenders are responsible for the consequences.


## Contributors

<a href="https://github.com/baiduspider/baiduspider/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=baiduspider/baiduspider" />
</a>


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
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