#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'

import re
import base64

# 英文字母
re_alpha = r"^[a-zA-Z]+$"
# 英文和数字
re_alphanumeric = r"^[a-zA-Z0-9]+$"
#
re_numeric = r"^[-+]?[0-9]+$"
# 整数
re_int = r"^(?:[-+]?(?:0|[1-9][0-9]*))$"
# 正整数
re_positive_int = r"^[1-9][0-9]*$"
# 浮点数
re_float = r"^(?:[-+]?(?:[0-9]+))?(?:\.[0-9]*)?(?:[eE][\+\-]?(?:[0-9]+))?$"
# Base64
# TODO 校验规则需要调整
re_base64 = r"^(?:[A-Za-z0-9+\/]{4})*(?:[A-Za-z0-9+\/]{2}==|[A-Za-z0-9+\/]{3}=|[A-Za-z0-9+\/]{4})$"

def not_empty(val):
    if not val:
        return False
    # str or list
    return len(val) > 0


def equals(val, comparison):
    if not val:
        return False
    # 先以字符串对待
    return val == comparison


def is_alpha(val):
    if not val:
        return True
    return bool(re.match(re_alpha, val))


def is_alphanumeric(val):
    if not val:
        return True
    return bool(re.match(re_alphanumeric, val))


def is_numeric(val):
    if not val:
        return True
    return bool(re.match(re_numeric, val))


def is_int(val):
    if not val:
        return True
    return bool(re.match(re_int, val))


def is_positive_int(val):
    if not val:
        return True
    return bool(re.match(re_positive_int, val))


def is_float(val):
    if not val:
        return True
    return bool(re.match(re_float, val))


def is_in(val, values):
    if not val:
        return True
    return val.lower() in values


def is_base64(val):
    if not val:
        return True

    return bool(re.match(re_base64, val))
