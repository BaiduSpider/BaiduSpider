import inspect
import os
import re
from datetime import datetime, timedelta
from functools import wraps
from typing import Union


def handle_err(func):  # pragma: no cover
    """处理报错"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            if bool(int(os.environ.get("DEBUG", 0))):  # DEBUG 模式开启
                raise err
            func_name = (
                func.__name__.strip("parse_").strip("_block")
                if "block" in func.__name__
                else None
            )
            if func_name is not None:
                print(
                    f"\033[33mWARNING: An error occurred while parsing the {func_name} subcomponent of BaiduSpider.{inspect.stack()[1][0].f_code.co_name}, "
                    "which is currently ignored. However, the rest of the parsing process is still being executed normally. "
                    "This is most likely an inner parse failure of BaiduSpider. For more details, please set the environment "
                    "variable `DEBUG` to `1` to see the error trace and open up a new issue at https://github.com/BaiduSpider/"
                    "BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D.\033[0m"
                )
            else:
                print(
                    f"\033[33mWARNING: An error occurred while executing function BaiduSpider.{inspect.stack()[1][0].f_code.co_name}, "
                    "which is currently ignored. However, the rest of the parsing process is still being executed normally. "
                    "This is most likely an inner parse failure of BaiduSpider. For more details, please set the environment "
                    "variable `DEBUG` to `1` to see the error trace and open up a new issue at https://github.com/BaiduSpider/"
                    "BaiduSpider/issues/new?assignees=&labels=bug%2C+help+wanted&template=bug_report.md&title=%5BBUG%5D.\033[0m"
                )

    return wrapper


def convert_time(t: str, as_list: bool = False) -> Union[datetime, bool]:
    """转换有时间差的汉字表示的时间到`datetime.datetime`形式的时间

    Args:
        t (str): 要转换的字符串
        as_list (bool): 是否以列表形式返回

    Returns:
        datetime: 转换后的`datetime.datetime`结果
    """
    if not t:
        return None

    t = t.strip()
    days_in_chinese = {"昨天": 1, "前天": 2, "今天": 0}
    if t in days_in_chinese:
        return datetime.now() - timedelta(days=days_in_chinese[t])

    delta = int(re.findall(r"\d+", t)[0])
    # print( t.replace(str(delta), "").strip(), delta)
    if "秒" in t:
        s = datetime.now() - timedelta(seconds=delta)
    elif "分钟" in t:
        s = datetime.now() - timedelta(minutes=delta)
    elif "小时" in t:
        s = datetime.now() - timedelta(hours=delta)
    elif t.replace(str(delta), "").split(":")[0].strip() in days_in_chinese:
        _ = int(re.findall(r"\d+", t)[-1])
        __ = t.replace(str(delta), "").split(":")[0].strip()
        s = datetime.now() - timedelta(days=days_in_chinese[__])
        s = datetime(s.year, s.month, s.day, delta, _)
    elif "天" in t:
        s = datetime.now() - timedelta(days=delta)
    # elif '年' in t:
    #     s = (datetime.now() - timedelta(days=365 * delta))
    elif "年" in t and "月" in t and "日" in t:
        s = datetime.strptime(t, "%Y年%m月%d日")
    else:
        s = datetime.now()

    if not as_list:
        return s
    else:
        return (s.year, s.month, s.day, s.hour, s.minute, s.second)
