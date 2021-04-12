#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/3/31 10:00
# @Author: luolf
# @File  : my_date.py

import time


def get_yesterday():
    seconds = time.time()-86400
    time_array = time.localtime(seconds)
    yesterday = time.strftime("%Y-%m-%d 00:00:00", time_array)
    return yesterday


def get_last_hour():
    seconds = time.time()-3600
    time_array = time.localtime(seconds)
    last_hour = time.strftime("%Y-%m-%d %H:00:00", time_array)
    return last_hour


def get_today():
    seconds = time.time()
    time_array = time.localtime(seconds)
    today = time.strftime("%Y-%m-%d 00:00:00", time_array)
    return today


def get_date_from_seconds(seconds):
    time_array = time.localtime(seconds)
    today = time.strftime("%Y%m%d%H", time_array)
    return today


def get_day(days):
    if days > 15:
        days = 15
    if days < -15:
        days = -15
    seconds = time.time()+86400*days
    time_array = time.localtime(seconds)
    today = time.strftime("%Y-%m-%d 00:00:00", time_array)
    return today


def get_now_hour():
    seconds = time.time()
    time_array = time.localtime(seconds)
    last_hour = time.strftime("%Y-%m-%d %H:00:00", time_array)
    return last_hour


def get_now_month():
    seconds = time.time()
    time_array = time.localtime(seconds)
    now_month = time.strftime("%Y%m", time_array)
    return now_month


# 输出
# print("欢迎使用时间工具")
# print(get_now_month())
# print(get_day(-30))


