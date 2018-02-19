import requests
from bs4 import BeautifulSoup
import pymongo
import re
#----------MongoDB Part------------------
#set up connection between mongodb
client = pymongo.MongoClient('localhost',27017)

#Get Database in MongoDB
scrapy_db = client['scrapy_db']

#Get a collection in scrapy_db
scrapy_collection = scrapy_db['scrapy_collection']
#----------MongoDB Part Finished----------

#----------Request Part ----------
page_url = 'http://txzb.miit.gov.cn/DispatchAction.do?efFormEname=POIX14&pagesize=11&page=1'
page_req = requests.get(page_url)
page_soup = BeautifulSoup(page_req.text, 'lxml')
# Get total number of pages
page_number = page_soup.find_all('td', class_="page STYLE1 STYLE4")[1]["page"]
# print(page_number)

url = 'http://txzb.miit.gov.cn/DispatchAction.do?efFormEname=POIX14&pagesize=11&page='
for i in range(1, int(page_number)):
    req = requests.get(url+str(i))
    soup = BeautifulSoup(req.text,'lxml')
    items = soup.select('td.STYLE1 > a')
    for item in items:
        subLink = item['href']
        subUrl = 'http://txzb.miit.gov.cn' + subLink
        subReq = requests.get(subUrl)
        subSoup = BeautifulSoup(subReq.text.strip(),'html.parser')
        soup_utf = subSoup.decode('utf8')

        rm_soup = re.compile(r'<[^>]+>', re.S)
        sub_compile1 = rm_soup.sub('', soup_utf)

        rm_space = re.compile(' ')
        sub_compile2 = rm_space.sub('', sub_compile1)

        #----------------------Search Address-------------------------------
        try:
            address = re.findall(r"(建设地点：|项目所在地区：|服务地点：|工程地点分布在|交货地点：)(.*?)([\u3002|\uff0c|<])", subSoup.decode('utf8'))
            if((address != None) & (address[0][1] == '')):
                address = re.findall(r"(服务地点：)(.*?</.*?)([\u3002])", subSoup.decode('utf8'))
                #print(address)
                address = re.findall(r"(\">)(.*)",address[0][1])
            #print(address[0][1])
            data_address = address[0][1]
        except IndexError as indexerr:
            data_address = 'IndexError:' + str(indexerr)

        # ----------------------Search Address Finished----------------------
        # ----------------------Search time for sale-------------------------
        try:
            sale_time = re.findall(r"(\d{4}年\d{1,2}月\d{1,2}日(\d{1,2}时)?(\d{1,2}：)?(\d{1,2})?分?)(至|到)(\d{4}年\d{1,2}月\d{1,2}日((\d{1,2}：)?\d{1,2}时)?(\d{1,2}：)?(\d{1,2})?分?)", sub_compile2)
            #print(sale_time)
            sale_time_range = sale_time[0][0]+sale_time[0][4]+sale_time[0][5]
            #print(sale_time[0][0]+sale_time[0][4]+sale_time[0][5])
        except IndexError as indexerr:
            sale_time_range = 'IndexError:' + str(indexerr)
        # ----------------------Search time for sale Finished---------------

        # ----------------------Search time for sale end---------------------
        try:
            sale_end = re.findall(r"(投标|递交)?截止时间(.*?)(\d{4}年\d{1,2}月\d{1,2}日(\d{1,2}时)?(\d{1,2}：)?(\d{1,2})?分?)", sub_compile2)
            #print(sale_end[0][2])
            data_sale_end = sale_end[0][2]
        except IndexError as indexerr:
            data_sale_end = 'IndexError:' + str(indexerr)
        # ----------------------Search time for sale end finished------------

        #---------------------Prepare Date for MongoDB---------------
        try:
            data = {
                "name" : item.get_text().strip().split('\xa0\xa0\xa0')[0],
                "release_time" : item.get_text().strip().split('\xa0\xa0\xa0')[1],
                "address" : data_address,
                "sale_time_range" : sale_time_range,
                "sale_end" : data_sale_end,
            }
            print(data)
            #scrapy_collection.insert_one(data)
        except IndexError as indexerr:
            print('IndexError:' + str(indexerr))
        #---------------------Prepare Date for MongoDB Finished-------
