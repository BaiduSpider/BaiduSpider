import re
from htmlmin import minify
import requests
from baiduspider.errors import ParseError, UnknownError
import os


class BaseSpider(object):  # pragma: no cover
    def __init__(self) -> None:
        """所有爬虫的基类

        此类包括了常用的util和自定义方法，继承自`object`。
        """
        super().__init__()
        self.spider_name = "BaseSpider"
        self.headers = {}

    def _format(self, s: str) -> str:
        """去除字符串中不必要的成分并返回

        Args:
            s (str): 要整理的字符串

        Returns:
            str: 处理后的字符串
        """
        return s.strip()

    def _remove_html(self, s: str) -> str:
        """从字符串中去除HTML标签

        Args:
            s (str): 要处理的字符串

        Returns:
            str: 处理完的去除了HTML标签的字符串
        """
        pattern = re.compile(r"<[^*>]+>", re.S)
        removed = pattern.sub("", s)
        return removed

    def _minify(self, html: str) -> str:
        """压缩HTML代码

        Args:
            html (str): 要压缩的代码

        Returns:
            str: 压缩后的HTML代码
        """
        return html.replace("\u00a0", "")

    def _get_response(self, url: str) -> str:
        """获取网站响应，并返回源码

        Args:
            url (str): 要获取响应的链接

        Returns:
            str: 获取到的网站HTML代码
        """
        response = requests.get(url, headers=self.headers)
        content = bytes(response.text, response.encoding).decode("utf-8")
        return content

    def _handle_error(self, err: Exception, parent: str, cause: str) -> None:
        if err is None:
            return None
        if bool(int(os.environ.get("DEBUG", 0))):
            raise err
        else:
            print(
                f"\033[33mWARNING: An error occurred while executing function {parent}.{cause}, "
                "which is currently ignored. However, the rest of the parsing process is still being executed normally. "
                "This is most likely an inner parse failure of BaiduSpider. For more details, please set the environment "
                "variable `DEBUG` to `1` to see the error trace and open up a new issue at https://github.com/BaiduSpider/"
                "BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D.\033[0m"
            )
            # 错误日志中文输出
            # print(f'\n\033[1;31m警告：在执行函数{parent}.{cause}时发生了一个错误，并且已被忽略。尽管如此，剩余的解析过程仍被正常执行。'
            #     '这很有可能是一个BaiduSpider内部错误。请将环境变量`DEBUG`设为`1`并查看Traceback。'
            #     '请在https://github.com/BaiduSpider/BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md'
            #     '&title=%5BBUG%5D%20%E6%AD%A4%E5%A4%84%E5%A1%AB%E5%86%99%E4%BD%A0%E7%9A%84%E6%A0%87%E9%A2%98 提交一个新的issue。\033[31;m')
            return None

    def __repr__(self) -> str:
        return "<Spider %s>" % self.spider_name

    def __str__(self) -> str:
        return self.__repr__()
