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
                            self.mysql.insert(MYSQL_TABLE, result)
                            # pass
                else:
                    self.error(tmall_request)
            else:
                self.error(tmall_request)

    def run(self):
        self.start()
        self.schedule()


class TianMaoSpider(SpiderFather):
    params = {
        "auctionNumId": 609686548905,
        'userNumId': 2888885899,
        'currentPageNum': 1,
        'callback': 'jsonp_tbcrate_reviews_list',
        "orderType": "feedbackdate"
    }
    # params = {
    #     "itemId": "529565826078",
    #     "sellerId": "1105025069",
    #     "currentPage": 1,
    #     "callback": "jsonp2917",
    # }

    # url = 'https://rate.tmall.com/list_detail_rate.htm'
    url = 'https://rate.taobao.com/feedRateList.htm'
    headers = {
        "referer": "https://item.taobao.com/item.htm?spm=a21ag.11815245.0.0.166650a5lNrw5d&id=602934064500",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        'cookie': '_samesite_flag_=true; cookie2=197204d89b811e7032ee2ec24faab2f1; t=f00c7cc2057f74996a9ee6848b152f8f; _tb_token_=5eb136153fb89; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; enc=a3QYWM2193KKQGSPRDOSk1Co%2FB5ZkiwgN5fMDESOA2pmSrH8UK1IU7mPhN42cHPYCPaWtzW15TsztQdEEM9cVQ%3D%3D; UM_distinctid=17208a86f75306-0066be0c184d45-d373666-144000-17208a86f765a8; _m_h5_tk=fc2a8c1dc347026f3d2ecd7ecfff28f7_1589293820091; _m_h5_tk_enc=13ddee0f52bf1f53399346c72a00079b; cna=hIU+FwjXu1ACAXr3v+ExOn8B; v=0; sgcookie=Eq8ItydCo8QiUp%2F%2FkQiLz; unb=2647741626; uc3=vt3=F8dBxGXEmSE1wjwSjBc%3D&id2=UU6lSsVzSQr4dQ%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D&nk2=saDP0XwOr7Dno1yn; csg=f7760f1b; lgc=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; cookie17=UU6lSsVzSQr4dQ%3D%3D; dnk=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; skt=fa8d5968cbebea14; existShop=MTU4OTI4NjkyNw%3D%3D; uc4=nk4=0%40s8WPMo5F5rAibkF75DMF87TdAhLhVMQ%3D&id4=0%40U2xo%2Bvmd%2BvRtFNxpw09spJV8h%2Fhb; tracknick=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; _cc_=Vq8l%2BKCLiw%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%A4%B463; _nk_=%5Cu4E00%5Cu76F4%5Cu6C38%5Cu8FDC%5Cu4E2B%5Cu5934; cookie1=W5%2FQVXrhb2qJGOA9xJYKLLZ6qZhtRFPY6UpnGf5tgy0%3D; tfstk=c2jfBwOtSjcfntjq41wy7GTjHvxNZkNWErOAhamvG-o7NpBfi0neOgpFSbmJJL1..; uc1=cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&cookie21=UtASsssmeW6lpyd%2BB%2B3t&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTUM2LG4ZwZ2A%3D%3D; mt=ci=46_1; x5sec=7b22726174656d616e616765723b32223a226466653338313239356432333062306538396232353932623931643633353536434a537736765546454c4433693862647739486939674561444449324e4463334e4445324d6a59374d513d3d227d; l=eBOmI5RPQl3FUEN3BO5Zhurza77TBBRf1sPzaNbMiInca1k5iLv6KNQc7mSHrdtjgt5bCetzEdARfRUDSj438xTjGO0qOC0eQMpe8e1..; isg=BCcnBHUPNYTdkrEIhfSFSYE6tlvxrPuOfwzMhPmSubfY6ESqAX-H3wCuCuj2ANMG'
    }

    def parse_index(self, response):
        try:
            req = response.content.decode('utf-8')[29:-2]
            req = json.loads(req)
        except Exception:
            raise ArithmeticError
        # results = req.get("rateDetail").get("rateList")
        results = req.get("comments")

        for result in results:
            yield {
                "auctionSku": result.get("auction").get('sku'),
                "rateContent": result.get("content"),
                "rateDate": result.get("date")
            }
            # yield {
            #     "auctionSku": result.get("content"),
            #     "rateContent": result.get("rateContent"),
            #     "rateDate": result.get("date")
            # }

        # paginator = req.get('rateDetail').get("paginator")
        # page = paginator.get("page")
        # print(page)
        # lastPage = paginator.get("lastPage")
        page = req.get("currentPageNum")
        lastPage = req.get('maxPage')
        print("page:",page, "lastpage:", lastPage)
        if page < lastPage:
            params = self.params
            # params['currentPage'] = page + 1
            params['currentPageNum'] = page + 1
            request = TianMaoRequest(url=self.url, callback=self.parse_index, need_proxy=NEED_PROXY, headers=self.headers,
                                     params=params)
            yield request
