import pymysql.cursors

'''
将数据存入数据库模块
'''


class DbToMysql:
    """封装对数据库的操作"""
    def __init__(self, configs):
        self.con = pymysql.connect(
            host=configs['host'],
            port=configs['port'],
            user=configs['user'],
            password=configs['password'],
            db=configs['db'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        """关闭数据库链接"""
        self.con.close()

    def save_one_data(self, table, data,):
        """
        将一条记录保存到数据库
        Args:
            table: 表名字 str
            data:  记录 dict
        return:
            成功： dict 保存的记录
            失败： -1
        每条记录都以一个字典的形式传进来
        """
        # key_map = {}
        if len(data) == 0:
            return -1
        fields = ''
        values = ''
        datas = {}
        for k, v in data.items():
            # 防止sql注入
            if type(v) == str:
                datas.update({k: pymysql.converters.escape_string(v)})

            elif v is None:
                # datas.update({k: v})
                var = None
            else:
                datas.update({k: v})

        for d in datas:
            fields += "`{}`,".format(str(d))
            # values += "'{}',".format(str(datas[d]))
            if type(datas[d]) == int:
                values += "{},".format(datas[d])
            elif type(datas[d]) == bool:
                values += "{},".format(datas[d])
            else:
                values += "'{}',".format(str(datas[d]))

        if len(fields) <= 0 or len(values) <= 0:
            return -1
        # 生成sql语句
        sql = "insert into {}({}) values({})".format(
            table, fields[:-1], values[:-1])

        try:
            with self.con.cursor() as cursor:
                # 执行语句
                cursor.execute(sql)
                self.con.commit()
                res = cursor.fetchone()
                return res
        except AttributeError as e:
            print('数据库保存错误', e, sql)
            return -1
        except Exception as e:
            print('数据库保存错误', e, sql)
        # finally:
        #     self.close()

    def find_all(self, table, limit):
        """
        从数据库里查询所有记录
        Args:
            table: 表名字 str
            limit: 限制数量
        return:
            成功： [dict] 保存的记录
            失败： -1
        """
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} limit 0,{}".format(table, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('数据查询存错误', e, sql)
            return -1
        finally:
            self.close()

    def find_by_field(self, table, field, field_value):
        """
        从数据库里查询指定条件的记录
        Args:
            table: 表名字 str
            field: 字段名
            field_value: 字段值
        return:
            成功： [dict] 保存的记录
            失败： -1
        """
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} where {} = '{}'".format(
                    table, field, field_value)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('数据查询存错误', e, sql)
            return -1
        finally:
            self.close()

    def find_by_fields(self, table, queryset=None):
        """
        从数据库里查询 符合多个条件的记录
        Args:
            table: 表名字 str
            queryset : key 字段 value 值 dict
        return:
            成功： [dict] 保存的记录
            失败： -1
        """

        if queryset is None:
            queryset = {}
        try:
            with self.con.cursor() as cursor:
                query = ""
                for k, v in queryset.items():
                    query += "{} = '{}' and ".format(k, v)
                sql = "select * from {} where {} ".format(
                    table, query[:-4])
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('数据查询存错误', e, sql)
            return -1
        finally:
            self.close()

    def find_by_sort(self, table, field, limit=1000, order='DESC'):
        """
        从数据库里查询排序过的数据
        Args:
            table: 表名字 str
            field: 字段名
            limit: 限制数量
            order: 降序DESC/升序ASC 默认为降序
        return:
            成功： [dict] 保存的记录
            失败： -1
        """
        try:
            with self.con.cursor() as cursor:
                sql = "select * from {} order by {} {} limit 0,{}".format(
                    table, field, order, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('数据查询存错误', e, sql)
            return -1
        finally:
            self.close()

    def query(self, sql):
        """
        根据sql查询
        Args:
            sql: sql 语句 str
        return:
            成功： 查询的结果
            失败： -1 并打印返回报错信息
        """

        try:
            with self.con.cursor() as cursor:
                # 执行语句

                cursor.execute(sql)
                self.con.commit()
                res = cursor.fetchall()
                return res
        except Exception as e:
            print('query 数据库查询错误', e, sql)
            return []
        # finally:
        #     self.close()
