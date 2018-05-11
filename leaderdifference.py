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
from fake_useragent import FakeUserAgent
import time
import randomproxy
class LeaderDifference:
    __ua = FakeUserAgent()

    def get_data(self, stock_id, begin, end, test=False):
        try:
            if test == True:
                print('Test mode')
                f = open("res/test/result.txt", "r", encoding='utf-8')
                l = f.read()
                f.close()
            else:          
                begin_date = begin.strftime('%Y%m%d')
                end_date = end.strftime('%Y%m%d')
                url = 'https://histock.tw/stock/branch.aspx?no={}&from={}&to={}'.format(str(stock_id), end_date, begin_date) #end date is earlier than begin date
                
                time.sleep(1)
                for _ in range(0, 5):
                    proxy_index = randomproxy.random_proxy()
                    proxy = randomproxy.proxies[proxy_index]
                    # Make the call
                    try:                       
                        r = requests.get(url, headers= {'User-Agent':self.__ua.random}, proxies = {'http': '{0}:{1}'.format(proxy['ip'], proxy['port'])})
                        r.encoding = 'utf-8'
                        l = r.text
                        break
                    except: # If error, delete this proxy and find another one
                        del randomproxy.proxies[proxy_index]
                        print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
                        

            soup = BeautifulSoup(l, 'html.parser')
            pattern = re.compile(r'var jsonDatas', re.MULTILINE | re.DOTALL)
            script = soup.find("script", text=pattern)

            start = script.string.find('eval(')+5
            end = script.string.find('});')+1
            json_s = script.string[start:end]

            json_obj = json.loads(json_s, encoding='utf-8')
            
            return json_obj
        except Exception as e:
            print("except: {}".format(str(e)))
            return None


if __name__=='__main__':
    o = LeaderDifference()
    data = o.get_data('2353', datetime.datetime(2018, 4, 30), datetime.datetime(2018, 3, 9), False)
    for i in range(500):
        time.sleep(3)
        print("id:{}  d:{}".format(i, "Success" if data != None else "Fail"))
