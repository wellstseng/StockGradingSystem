#%%
# -*- encoding: utf8-*-

import twstock
from datetime import datetime
from datetime import timedelta
from leaderdifference import LeaderDifference
import pandas as pd
import math 

class StockInfoManager:  
    __leader_diff = LeaderDifference() 
    def __init__(self, stock_id, start_date, period):
        self.__stock = twstock.Stock(str(stock_id))
        self.init_date(start_date, period)        
            
    def init_date(self, begin, period):
        try:            
            end = begin - timedelta(days=(period*2)+30) 
            if self.__stock.date[0] > end:
                print('date less end')
                self.__stock.fetch_from(end.year, end.month) 
        except ValueError:
            print("date format error '%Y/%m/%d'")
    
    def get_date(self, begin, period):
        self.init_date(begin, period)
        i = self.__stock.date.index(begin)
        return self.__stock.date[i-period+1]

    def get_leader_difference(self, begin_date, end_date):
        o = self.__leader_diff.get_data(self.__stock.sid, begin_date, end_date)
        data = {}       
        train = pd.DataFrame.from_dict(o['Buy'])
        train['BSSum'] = train['BSSum'].str.replace(',', '')
        train['BSSum'] = pd.to_numeric(train['BSSum'])
        train['BuySum'] = train['BuySum'].str.replace(',', '')
        train['BuySum'] = pd.to_numeric(train['BuySum'])
        train['SellSum'] = train['SellSum'].str.replace(',', '')
        train['SellSum'] = pd.to_numeric(train['SellSum'])
        data['Buy'] = train

        train = pd.DataFrame.from_dict(o['Sell'])
        train['BSSum'] = train['BSSum'].str.replace(',', '')
        train['BSSum'] = pd.to_numeric(train['BSSum'])
        train['BuySum'] = train['BuySum'].str.replace(',', '')
        train['BuySum'] = pd.to_numeric(train['BuySum'])
        train['SellSum'] = train['SellSum'].str.replace(',', '')
        train['SellSum'] = pd.to_numeric(train['SellSum'])
        data['Sell'] = train
        return data

    def get_price(self, date):
        i = self.get_date_index(date)
        return self.__stock.price[i]     

    def get_date_index(self, date):
        i = self.__stock.date.index(date)
        return i
    
    def get_average(self, date, days):
        t = self.__stock.moving_average(self.__stock.price, days)
        cur = len(t)
        total = len(self.__stock.date)
        for _ in range(0, total-cur):
            t.insert(0, 0)
        i = self.get_date_index(date)
        return t[i]
    
    def get_concentrate(self, start_date, days):
        end_date = self.get_date(start_date, days)
        leader_diff = self.get_leader_difference(start_date, end_date)
        b = leader_diff['Buy']['BSSum'].sum() 
        s = leader_diff['Sell']['BSSum'].sum()
        bs = b + s
        
        start_index = self.get_date_index(start_date)
        end_index = self.get_date_index(end_date)

        volume = 0
        for i in range(start_index, end_index-1, -1):
            c =self.__stock.capacity[i]
            volume +=  c

        volume = math.floor(volume / 1000)
        return round(bs / volume * 100, 1) if volume > 0 else 0
        

def test():
    start_date = datetime.strptime('2018/04/09', '%Y/%m/%d')
    s = StockInfoManager('2353', start_date, 120)
   
    
    
    print('observe date:{}'.format(start_date.strftime('%Y/%m/%d')))
    print('price:{}'.format(s.get_price(start_date)))
    print('20ma:{}'.format(s.get_average(start_date, 20)))
    print('60ma:{}'.format(s.get_average(start_date, 60)))
    print('120ma:{}'.format(s.get_average(start_date, 120)))
    print('1 day concentrate:{}'.format(s.get_concentrate(start_date, 1)))
    print('20 day concentrate:{}'.format(s.get_concentrate(start_date, 20)))
    print('60 day concentrate:{}'.format(s.get_concentrate(start_date, 60)))
    print('120 day concentrate:{}'.format(s.get_concentrate(start_date, 120)))

if __name__ == '__main__':
   test()