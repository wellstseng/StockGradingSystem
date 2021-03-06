
#%%
# -*- encoding: utf8-*-

from io import open
import requests
from bs4 import BeautifulSoup

from define import *
import json
import csv

class StockListHolder:
    @staticmethod
    def __load_data(data_type, test):
        if test == False:
            url = "http://isin.twse.com.tw/isin/C_public.jsp?strMode={}".format(data_type)
            print('load list from url {}'.format(url))
            res = requests.get(url, verify = False)
            return res.text
        else:
            f = open(Define.TEST_HTML_PATH, 'r', encoding='utf-8')
            text = f.read()
            f.close()
            return text

    @staticmethod
    def __save_data(data_type, data):   
        json_str = str(data).replace(' ','').replace('\'','"')
        data_parsed = json.loads(json_str)
        
        f = open(Define.get_list_path(data_type), "w", encoding='utf-8', newline='')
        csv_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['id', 'name'])

        for key in data_parsed:
            csv_writer.writerow(["{} ".format(key),data_parsed[key]])

        f.close()
    
    @staticmethod
    def get_list(data_type, test=False):
        src = StockListHolder.__load_data(data_type, test)    
        soup = BeautifulSoup(src, 'html.parser')    
        table = soup.find("table", {"class" : "h4"})
    
        datas = {}
        for row in table.find_all("tr"):
            cols = row.find_all('td')
            split_r = cols[0].text.split('\u3000')
            if len(split_r) >= 2:
                datas[split_r[0]] = split_r[1].strip('\u3000')
            else:
                print("warn: {}".format(split_r))
        
        StockListHolder.__save_data(data_type, datas)

if __name__ == '__main__':
    StockListHolder.get_list(MarketType.TSE)
    StockListHolder.get_list(MarketType.OTC)
    

