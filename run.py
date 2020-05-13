from spider import TianMaoSpider

if __name__ == '__main__':
    spider = TianMaoSpider()
    spider.run()

"""MONGO_CONN
    

create table taobao_6(
    id int primary key auto_increment,
    auctionSku varchar(255) not null,
    rateContent text not null,
    rateDate varchar(255) not null)
    default charset = utf8mb4;       
"""
