#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2021/3/30 17:41
# @Author: luolf
# @File  : json2file.py

import json
from config import task_file
import time
single_blogger_big = [

    {
        'name': 'bg收录',
        'task_type': 'agg_nest',
        'task_period': 'day',
        'datetime': 0,
        'data_source_type': 'es',
        'data_source': 'canal_ins_blogger',
        'data_target_type': 'es',
        'data_target': 'ins_monitor_event',
        'sql_type': 'aggregations',
        'sql': '''  {
                "aggs": {
                    "first": {
                        "range": {
                            "field": "followerCount",
                            "ranges": [
                               {
                                    "from": 0,
                                    "to": 10000
                                },
                                {
                                    "from": 10000,
                                    "to": 50000
                                },
                                {
                                    "from": 50000
                                }
                            ],
                            "keyed": true
                        },
                        "aggs": {
                            "two": {
                                "date_histogram": {
                                    "field": "createTime",
                                    "interval": "1d", 
                                    "min_doc_count": 1
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": [     
                    ]
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {

                },                
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "createTime": {
                                        "gte": "now-3d/d",
                                        "lt": "now"
                                    }
                                }
                            }
                        ]
                    }
                },
                "timeout": "30000ms"
            }''',
        'filed_map': '{}'
    },
    {
        'name': 'uid',
        'task_type': 'agg_nest',
        'task_period': 'day',
        'datetime': 0,
        'data_source_type': 'es',
        'data_source': 'canal_ins_blogger_main',
        'data_target_type': 'es',
        'data_target': 'ins_monitor_event',
        'sql_type': 'aggregations',
        'sql': '''  {
                    "aggs": {
                        "first": {
                            "range": {
                                "field": "followerCount",
                                "ranges": [
                                    {
                                        "from": 10000,
                                        "to": 50000
                                    },
                                    {
                                        "from": 50000
                                    }
                                ],
                                "keyed": true
                            },
                            "aggs": {
                                "two": {
                                    "date_histogram": {
                                        "field": "lastCollectTime",
                                        "interval": "1d", 
                                        "min_doc_count": 1
                                    }
                                }
                            }
                        }
                    },
                    "size": 0,
                    "_source": {
                        "excludes": [     
                        ]
                    },
                    "stored_fields": [
                        "*"
                    ],
                    "script_fields": {
                        
                    },                
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "range": {
                                        "lastCollectTime": {
                                            "gte": "now-9d/d",
                                            "lt": "now"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "timeout": "30000ms"
                }''',
        'filed_map': '{}'
    },
    {
        'name': '帖子',
        'task_type': 'agg_nest',
        'task_period': 'day',
        'datetime': 0,
        'data_source_type': 'es',
        'data_source': 'canal_ins_blogger_main',
        'data_target_type': 'es',
        'data_target': 'ins_monitor_event',
        'sql_type': 'aggregations',
        'sql': '''  {
                "aggs": {
                    "first": {
                        "range": {
                            "field": "followerCount",
                            "ranges": [
                                {
                                    "from": 10000,
                                    "to": 50000
                                },
                                {
                                    "from": 50000
                                }
                            ],
                            "keyed": true
                        },
                        "aggs": {
                            "two": {
                                "date_histogram": {
                                    "field": "lastMediaCollectTime",
                                    "interval": "1d", 
                                    "min_doc_count": 1
                                }
                            }
                        }
                    }
                },
                "size": 0,
                "_source": {
                    "excludes": [     
                    ]
                },
                "stored_fields": [
                    "*"
                ],
                "script_fields": {

                },                
                "query": {
                    "bool": {
                        "must": [
                            {
                                "range": {
                                    "lastMediaCollectTime": {
                                        "gte": "now-9d/d",
                                        "lt": "now"
                                    }
                                }
                            }
                        ]
                    }
                },
                "timeout": "30000ms"
            }''',
        'filed_map': '{}'
    },
]
with open(task_file.single_blogger_big, 'w', encoding='utf-8') as file:
    file.write(json.dumps(single_blogger_big, indent=2, ensure_ascii=False))

print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), time.time())





