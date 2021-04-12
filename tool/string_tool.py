#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/3/31 19:03
# @Author: luolf
# @File  : string_tool.py


def list2str(lst):
    rst = list()
    for i in range(len(lst)):
        if isinstance(lst[i], list):
            rst.append(list2str(lst[i]))
        else:
            rst.append(str(lst[i]))
    return '\n'.join(rst)





