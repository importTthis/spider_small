import requests
import json
import random

from requests import Session
from db import RedisQueue, TianMaoRequest, MySQL, Mongo
from settings import PROXY_POOL_URL, MAX_FAILED_COUNT, NEED_PROXY, MYSQL_TABLE


class SpiderFather:
    headers = ''
    url = ''
    params = {}

    session = Session()
    queue = RedisQueue()
    mysql = MySQL()
    mongo = Mongo()

    def start(self):
        # self.session.headers.update(self.headers)
        request_queue = TianMaoRequest(url=self.url, callback=self.parse_index, need_proxy=NEED_PROXY, headers=self.headers,
                                       params=self.params)
        self.queue.add(request_queue)

    def parse_index(self, response):
        pass

    def request(self, tmall_request):
        try:
            if tmall_request.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    print(proxy)
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    return requests.get(tmall_request.url, params=tmall_request.params, headers=tmall_request.headers,
                                        proxies=proxies)
            return requests.get(tmall_request.url, params=tmall_request.params, headers=tmall_request.headers)
        except Exception as e:
            print(e.args)
            return False

    def get_proxy(self):
        # db = self.mongo.conn.proxy_pool
        # collection = db.proxy
        # results = collection.find({})
        # proxy = random.choice(list(results))
        # return proxy.get("name")
        proxy = '180.127.144.11:23396'

        # try:
        #     r = requests.get(PROXY_POOL_URL)
        #     if r.status_code == 200:
        #         return r.text
        #     return None
        # except:
        #     return None

    def error(self, request):
        request.fail_count += 1
        if request.fail_count < MAX_FAILED_COUNT:
            self.queue.add(request)

    def schedule(self):
        while not self.queue.empty():
            tmall_request = self.queue.pop()
            response = self.request(tmall_request)
            callback = tmall_request.callback
            if response and response.status_code == 200:
                results = list(callback(response))
                print(results, )
                print('-'*50)
                if results:
                    for result in results:
                        if isinstance(result, TianMaoRequest):
                            self.queue.add(result)
                        if isinstance(result, dict):
                            # print(result)
                            # self.mysql.insert(MYSQL_TABLE, result)
                            pass
                else:
                    self.error(tmall_request)
            else:
                self.error(tmall_request)

    def run(self):
        self.start()
        self.schedule()


class TianMaoSpider(SpiderFather):
    # taobao
    # params = {
    #     "auctionNumId": 609686548905,
    #     'userNumId': 2888885899,
    #     'currentPageNum': 1,
    #     'callback': 'jsonp_tbcrate_reviews_list',
    #     "orderType": "feedbackdate"
    # }
    # small
    params = {
        "itemId": "614807100934",
        "sellerId": "2207546970340",
        "currentPage": 1,
        "callback": "jsonp961",
    }
    # small
    url = 'https://rate.tmall.com/list_detail_rate.htm'

    # taobao
    # url = 'https://rate.taobao.com/feedRateList.htm'
    headers = {
        "referer": "https://item.taobao.com/item.htm?spm=a21ag.11815245.0.0.166650a5lNrw5d&id=602934064500",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        'cookie': 't=40899284e69b2da11e7b289c531d6554; _tb_token_=ef8dfebe1b3be; cookie2=121a6a255f71743d98afe9ce943d9be2; cna=OKNKF0o9TnQCAT2ZFcPEJIUs; dnk=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; tracknick=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; lid=%E4%B8%80%E7%9B%B4%E6%B0%B8%E8%BF%9C%E4%B8%AB%E5%A4%B4; _l_g_=Ug%3D%3D; unb=2647741626; lgc=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; cookie1=W5%2FQVXrhb2qJGOA9xJYKLLZ6qZhtRFPY6UpnGf5tgy0%3D; login=true; cookie17=UU6lSsVzSQr4dQ%3D%3D; _nk_=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; sgcookie=EWQIk3SLYKD3gDn6Z%2FHng; sg=%E5%A4%B463; enc=94KfDFnqvkwYWWcVs7UYFa7g15KHy9zvWj0twySMTHUzjVIhz9BRdsXlrvQ4Q6Z0Z3fHBNaYmZq1uDGHlfWDFA%3D%3D; _m_h5_tk=55240510f0ce66ad5054e6e7bc98b182_1589896604785; _m_h5_tk_enc=fd62c18df149b4bd2d0377f9a49892c0; uc1=cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&existShop=false&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&pas=0&cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie14=UoTUM2ji1muPYw%3D%3D; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&nk2=saDP0XwOr7Dno1yn&vt3=F8dBxGZuEXfVY6WJYuc%3D&id2=UU6lSsVzSQr4dQ%3D%3D; uc4=nk4=0%40s8WPMo5F5rAibkF75DMF87TXp6hQnYM%3D&id4=0%40U2xo%2Bvmd%2BvRtFNxpw09srn341yo6; csg=229f818d; x5sec=7b22726174656d616e616765723b32223a22646632373334383761623363313066613734616465623036656663343933393343506d4d6a2f5946454e6d63303637656a652f6259426f4d4d6a59304e7a63304d5459794e6a7378227d; l=eBSJZq3nQZD3ay9MBO5Z-urza77TedOfcsPzaNbMiInca1rlwis9BNQDibikkdtjgtfEJetzEdARfR3k-tUKgZqhuJ1REpZwncJw-; isg=BPT0L0qUFuTMS4Ko_21A1H4jxbJmzRi3cH0ffY5Yv37Y-ZxDttygR9x_eTEhAVAP'
    }

    def parse_index(self, response):
        try:
            req = response.content.decode('utf-8')[11:-1]
            print(req)
            req = json.loads(req)
        except Exception:
            raise ArithmeticError
        # small
        results = req.get("rateDetail").get("rateList")

        # taobao
        # results = req.get("comments")

        for result in results:
            # taobao
            # yield {
            #     "auctionSku": result.get("auction").get('sku'),
            #     "rateContent": result.get("content"),
            #     "rateDate": result.get("date")
            # }

            # small
            yield {
                "auctionSku": result.get("auctionSku"),
                "rateContent": result.get("rateContent"),
                "rateDate": result.get("rateDate")
            }

        paginator = req.get('rateDetail').get("paginator")
        # small
        page = paginator.get("page")
        lastPage = paginator.get("lastPage")

        # taobao
        # page = req.get("currentPageNum")
        # lastPage = req.get('maxPage')
        if page < lastPage:
            params = self.params
            # samll
            params['currentPage'] = page + 1

            # taobao
            # params['currentPageNum'] = page + 1
            request = TianMaoRequest(url=self.url, callback=self.parse_index, need_proxy=NEED_PROXY, headers=self.headers,
                                     params=params)
            yield request
