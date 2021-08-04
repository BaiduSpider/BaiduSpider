import re
from datetime import datetime, timedelta
from typing import Union
from baiduspider.util import convert_time


def get_attr(d: dict, t: str):
    """获取字典`d`下的`t`"""
    try:
        return d[t]
    except:
        return None
