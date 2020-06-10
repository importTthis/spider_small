TIMEOUT = 60
MAX_FAILED_COUNT = 3
REDIS_KEY = 'tmall'
NEED_PROXY = False

REDIS_CONN = {
    "host": 'localhost',
    "port": 6379,
    "password": 'xzwz0502',
    'db': 1
}


# MYSQL_TABLE = "jd_bad_review"
MYSQL_TABLE = "jd_praise"

MYSQL_CONN = {
    "host": 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'xzwz0502',
    'database': 'test'
}

MONGO_CONN = "175.147.70.29:20674"