#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/3/30 17:24
# @Author: luolf
# @File  : dict_to_obj.py

database = [
    {
        "name": "18D_Block",
        "xcc": {
            "component": {
                "core": [],
                "platform": []
            },
        },
        "uefi": {
            "component": {
                "core": [],
                "platform": []
            },
        }
    }
]


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(dictObj):
    if not isinstance(dictObj, dict):
        return dictObj
    inst = Dict()
    for k, v in dictObj.items():
        # 递归完成嵌套的字典对象转换
        inst[k] = dict_to_object(v)
    return inst


# 转换字典成为对象，可以用"."方式访问对象属性
res = dict_to_object(database[0])
# 只有一层字典转换
res1 = Dict(database[0])

print(type(res1))
print(type(database))
print(type(database[0]))
print(type(res))
print(res)
print(res.name)
print(res.xcc)
print(res.xcc.component)
print(res.xcc.component.core)


