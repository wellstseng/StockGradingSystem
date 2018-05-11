#%%
# -*- encoding:utf8 -*-

import requests
from fake_useragent import FakeUserAgent
from io import open
from define import Define
from bs4 import BeautifulSoup
import pandas as pd
import time
ua = FakeUserAgent()

class LeaderTrade():
    test = True
    def get_data(self, stock_id, branch_id):
        if self.test == True:
            f = open(Define.TEST_LEADER_TRADE_PATH, 'r', encoding='utf8')
            text = f.read()
            f.close()
        else:
            time.sleep(3)
            r = requests.get('https://histock.tw/stock/brokertrace.aspx?bno={0}&no={1}'.format(branch_id, stock_id), 
                                headers = {"User-Agent":ua.random})
            r.encoding = 'utf8'
            text = r.text
        df = pd.read_html(text, attrs={"class":"tbTable tb-stock tbChip"}, index_col=0)[0]
        df.columns = df.iloc[0]
        df = df.drop(df.index[0])
        print(df)

if __name__ == "__main__":
    lt = LeaderTrade()
    lt.get_data('2377', '9136')