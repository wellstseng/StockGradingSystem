#%%
# -*- encoding:utf8 -*-
import twstock
from define import *

class MarginTrading:
    def get_data(self, stock_id:str, date:str):
        market = Define.get_market_type(stock_id)
        if market == MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return None
        
        file_path = Define.get_margin_file_path(market, date.replace('/', ''))
        
        '''
        http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=csv&d=107/04/24&s=0
        http://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date=20180424&selectType=MS
        '''
        return file_path

if __name__ == '__main__':
    t = MarginTrading()
    print(t.get_data('2353', '2018/04/20'))