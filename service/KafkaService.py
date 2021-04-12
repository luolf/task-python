#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/4/1 18:30
# @Author: luolf
# @File  : KafkaService.py
from pykafka import KafkaClient

host = '10.1.1.48:9092'
client = KafkaClient(hosts=host)
event_topic = client.topics[b'ins_monitor_event']  # 指定topic,没有就新建

producer = event_topic.get_producer()


def send_msg(msg):
    producer.produce(msg)

