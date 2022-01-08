"""BaiduSpider 自定义错误

本文件定义了 BaiduSpider 的自定义错误。
"""


class ParseError(Exception):  # pragma: no cover
    def __init__(self, msg: str = "", *args, **kwargs) -> None:
        """分析HTML的自定义错误

        Args:
            msg (str, optional): 错误信息. Defaults to "".
        """
        super().__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self) -> str:  # pragma: no cover
        return self.msg


class UnknownError(Exception):  # pragma: no cover
    def __init__(self, msg: str = "", *args, **kwargs) -> None:
        """未知错误

        Args:
            msg (str, optional): 错误信息. Defaults to "".
        """
        super().__init__(*args, **kwargs)
        self.msg = msg

    def __str__(self) -> str:  # pragma: no cover
        return self.msg
