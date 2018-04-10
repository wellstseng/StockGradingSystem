#%%
# -*- encoding: utf8-*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import open
from io import StringIO
import re
import json
import requests
import datetime

class LeaderDifference:
    def get_data(self, stock_id, begin, end, test=False):
        if test == True:
            print('Test mode')
            f = open("res/test/result.txt", "r", encoding='utf-8')
            l = f.read()
            f.close()
        else:          
            begin_date = begin.strftime('%Y%m%d')
            end_date = end.strftime('%Y%m%d')
            url = 'https://histock.tw/stock/branch.aspx?no={}&from={}&to={}'.format(str(stock_id), begin_date, end_date)
            print('url:{}'.format(url))
            r = requests.get(url)
            r.encoding = 'utf-8'
            l = r.text
        soup = BeautifulSoup(l, 'html.parser')
        pattern = re.compile(r'var jsonDatas', re.MULTILINE | re.DOTALL)
        script = soup.find("script", text=pattern)

        start = script.string.find('eval(')+5
        end = script.string.find('});')+1
        json_s = script.string[start:end]

        json_obj = json.loads(json_s, encoding='utf-8')
        
        return json_obj


if __name__=='__main__':
    o = LeaderDifference()
    print(o.get_data('2353', datetime.datetime(2018, 1, 3), datetime.datetime(2018, 4, 9), True))
