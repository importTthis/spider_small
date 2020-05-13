TIMEOUT = 60
MAX_FAILED_COUNT = 3
REDIS_KEY = 'tmall'
PROXY_POOL_URL = 'http://localhost:5000/get_proxy'
NEED_PROXY = True

REDIS_CONN = {
    "host": 'localhost',
    "port": 6379,
    "password": '',
    'db': 1
}


MYSQL_TABLE = "taobao_6"

MYSQL_CONN = {
    "host": 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'spider_test'
}

MONGO_CONN = ""