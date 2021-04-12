#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/3/30 19:18
# @Author: luolf
# @File  : collectDataService.py
import time
import types

from elasticsearch import Elasticsearch
import json
from config import task_file
from tool import my_date
from tool import string_tool

# elasticsearch集群服务器的地址
ES = ["10.1.1.51:9611", "10.1.1.52:9611", "10.1.1.53:9611"]
# 创建elasticsearch客户端
es = Elasticsearch(
    ES,
    # 启动前嗅探es集群服务器
    sniff_on_start=True,
    # es集群服务器结点连接异常时是否刷新es节点信息
    sniff_on_connection_fail=True,
    # 每60秒刷新节点信息
    sniffer_timeout=60
)


def count_process(rst):
    lst = list()
    buckets = rst["buckets"]
    print(rst["name"], buckets)
    return lst


def agg_process(rst):
    lst = list()
    buckets = rst["buckets"]
    # buckets = result["aggregations"]["rst"]["buckets"]
    for i in range(len(buckets)):
        buckets[i]["key_as_string"] = my_date.get_date_from_seconds(buckets[i]["key"] / 1000)
        print(rst["name"], buckets[i])
    return lst


def agg_nest_process(rst):
    buckets = rst["buckets"]
    # print(buckets)
    # buckets = result["aggregations"]["2"]["buckets"]
    keys = buckets.keys()
    lst = list()
    for i in keys:
        date_count = buckets[i]["two"]["buckets"]
        head_key = '{}#{}'.format(rst["name"], i)
        head_element = dict()
        head_element[head_key] = buckets[i]["doc_count"]
        lst.append(head_element)

        for j in range(len(date_count)):
            element = dict()
            # element["name"] = '{}:{}:{}'.format(rst["name"], i, buckets[i]["doc_count"])
            # element["time"] = my_date.get_date_from_seconds(date_count[j]["key"] / 1000)
            # element["cnt"] = date_count[j]["doc_count"]
            k = my_date.get_date_from_seconds(date_count[j]["key"] / 1000)
            element[k] = '{:8d}#{:>4.3f}'.format(date_count[j]["doc_count"],
                                            date_count[j]["doc_count"] / buckets[i]["doc_count"])
            # print(element)
            lst.append(element)
    return lst


def save_event_2_es(es_idx, lst):
    if isinstance(lst, list):
        msg = string_tool.list2str(lst)
        mill_seconds = int(round(time.time() * 1000))
        # print(mill_seconds)
        # print(msg)
        if es_idx == "ins_monitor_event":
            es_idx = es_idx + "_" + my_date.get_now_month()
        es.index(index=es_idx, id=mill_seconds, body={"id": mill_seconds, "eventTime": mill_seconds, "content": msg,
                                                      "eventType": "report", "eventStatus": "NORMAL",
                                                      "owner": "day-report"})


def main():
    with open(task_file.single_blogger_big, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
        all_rst = list()
        for i in range(len(data)):
            # time.sleep(2)
            body = data[i]["sql"]
            if data[i]["task_period"] == "day":
                body = body.replace("${startTime}", my_date.get_day(data[i]["datetime"]))
                body = body.replace("${endTime}", my_date.get_today())

            rst_data = es.search(index=data[i]["data_source"], body=body)
            if data[i]["task_type"] == "count":
                rst_tmp = rst_data["aggregations"]["rst"]
                rst_tmp["name"] = data[i]["name"]
                rst = count_process(rst_tmp)
            if data[i]["task_type"] == "agg":
                rst_tmp = rst_data["aggregations"]["rst"]
                rst_tmp["name"] = data[i]["name"]
                rst = agg_process(rst_tmp)
            if data[i]["task_type"] == "agg_nest":
                rst_tmp = rst_data["aggregations"]["first"]
                rst_tmp["name"] = data[i]["name"]
                rst = agg_nest_process(rst_tmp)
                all_rst.append(rst)
        save_event_2_es("ins_monitor_event", all_rst)
        # es_results.append(rst)
        # for i in range(len(es_results)):
        #     print(es_results[i]["name"], es_results[i]["rst"])
        # for j in range(len(es_results[i]["rst"])):
        #     sub = es_results[i]["rst"][j]
        #     sub["key_as_string"] = my_date.get_date_from_seconds(sub["key_as_string"])
        #     print("------------------", sub)

