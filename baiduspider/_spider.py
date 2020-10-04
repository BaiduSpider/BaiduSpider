import re
from htmlmin import minify
import requests
from baiduspider.errors import ParseError, UnknownError

class BaseSpider(object):  # pragma: no cover
    def __init__(self) -> None:
        """所有爬虫的基类

        此类包括了常用的util和自定义方法，继承自`object`。
        """
        super().__init__()
        self.spider_name = 'BaseSpider'
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
        pattern = re.compile(r'<[^*>]+>', re.S)
        removed = pattern.sub('', s)
        return removed

    def _minify(self, html: str) -> str:
        """压缩HTML代码

        Args:
            html (str): 要压缩的代码

        Returns:
            str: 压缩后的HTML代码
        """
        return html.replace('\u00a0', '')

    def _get_response(self, url: str) -> str:
        """获取网站响应，并返回源码

        Args:
            url (str): 要获取响应的链接

        Returns:
            str: 获取到的网站HTML代码
        """
        response = requests.get(url, headers=self.headers)
        content = bytes(response.text, response.encoding).decode('utf-8')
        return content

    def _handle_error(self, err: Exception) -> None:
        if err is None:
            return None
        if type(err) in [ParseError]:
            error = err
        else:
            error = UnknownError(str(err))
        raise error

    def __repr__(self) -> str:
        return '<Spider %s>' % self.spider_name

    def __str__(self) -> str:
        return self.__repr__()