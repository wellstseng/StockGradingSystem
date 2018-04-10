#%%
# -*- encoding: utf8-*-

import twstock
from datetime import datetime
from datetime import timedelta
from leaderdifference import LeaderDifference
import pandas as pd

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
                print('count:{}'.format(len(self.__stock.date)))    
        except ValueError:
            print("date format error '%Y/%m/%d'")
    
    def get_date(self, begin, period):
        self.init_date(begin, period)
        i = self.__stock.date.index(begin)
        return self.__stock.date[i-period+1]

    def get_leader_difference(self, begin_date, end_date):
        print('begin:{}   end:{}'.format(str(begin_date), str(end_date)))
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
        

def test():
    start_date = datetime.strptime('2018/04/09', '%Y/%m/%d')
    s = StockInfoManager('2353', start_date, 120)
    e = start_date
    b = s.get_date(e, 60)
    o = s.get_leader_difference(b, e)
    
    print('observe date:{}'.format(start_date.strftime('%Y/%m/%d')))
    print('price:{}'.format(s.get_price(start_date)))
    print('20ma:{}'.format(s.get_average(start_date, 20)))
    print('60ma:{}'.format(s.get_average(start_date, 60)))
    print('120ma:{}'.format(s.get_average(start_date, 120)))
    #print('{}'.format(o['Buy']['BSSum'].sum()))

if __name__ == '__main__':
   test()