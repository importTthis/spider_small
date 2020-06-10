import pickle
import pymysql
import pymongo

from requests import Request
from redis import StrictRedis
from settings import REDIS_CONN, REDIS_KEY, TIMEOUT, MYSQL_CONN, MONGO_CONN


class TianMaoRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, params=None, need_proxy=False, fail_count=0,
                 time_out=TIMEOUT):
        super().__init__(method, url, headers, params=params)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_count = fail_count
        self.time_out = time_out


class RedisQueue:

    def __init__(self):

        self.db = StrictRedis(**REDIS_CONN)

    def add(self, tmall_request):
        if isinstance(tmall_request, TianMaoRequest):
            return self.db.rpush(REDIS_KEY, pickle.dumps(tmall_request))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return pickle.loads(self.db.lpop(REDIS_KEY))
        return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0


class MySQL:
    def __init__(self):
        try:
            self.db = pymysql.connect(**MYSQL_CONN)
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except pymysql.MySQLError as e:
            print("mysql error:",e.args)

    def insert(self, table, data):
        keys = ", ".join('`{}`'.format(k) for k in data.keys())
        values = ', '.join('%({})s'.format(k) for k in data.keys())
        sql = "insert into %s (%s) values(%s)" % (table, keys, values)
        try:
            self.cursor.execute(sql, data)
            self.db.commit()
        except pymysql.MySQLError as e:
            print("mysql insert error",e.args)
            self.db.rollback()

    def insert_many(self, table, data):
        result = data[0]
        keys = ", ".join('`{}`'.format(k) for k in result.keys())
        values = ', '.join('%({})s'.format(k) for k in result.keys())

        sql = "insert into %s (%s) values (%s)" % (table, keys, values)

        self.cursor.executemany(sql, data)
        self.db.commit()




class Mongo:
    def __init__(self):
        self.conn = pymongo.MongoClient(f'mongodb://{MONGO_CONN}/')