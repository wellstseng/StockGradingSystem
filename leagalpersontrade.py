#%%
# -*- encoding:utf8 -*-
import twstock
import os.path
import os
import requests
import csv
import pandas as pd
import math
from define import *
from fake_useragent import UserAgent
from util import Util
from datetime import datetime
import time
class LegalPersonTrading:
    __ua = UserAgent()
    
    def get_legal_person_trade(self, stock_id, date):
        d = Util.date_to_str(date)
        market, df = self.get_data(stock_id, d)
        if market == MarketType.UNKNOWN:
            return None
        return math.floor(int(df.at[stock_id, '三大法人買賣超股數' if market == MarketType.TSE else '三大法人買賣超股數合計'].replace(',',''))/1000)

    def get_data(self, stock_id:str, date:str):
        '''
        載入法人交易資料
        回傳DataFrame
        '''
        #取得市場類型
        market = Define.get_market_type(stock_id)

        #未知市場不處理
        if market == MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return MarketType.UNKNOWN,None

        #檢查是否需從網路下載資料表
        file_path = self.check_load_legal_person_data(market, date)
        df =pd.read_csv(file_path, encoding='utf8', header=0, index_col=0)  
        
        return market, df        
    
    def check_load_legal_person_data(self, market:str, date:str):        
        '''
        檢查下載法人交易資料
        '''

        if market == MarketType.UNKNOWN:
            print('unknown market')
            return None

        #檢查檔案是否存在，不存在先從網路上下載
        file_path = Define.get_legal_person_file_path(market, date)
        if not os.path.isfile(file_path):
#region 透過網路下載資料並儲存
            #TSE市場下載           
            if market == MarketType.TSE:
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(Define.TSE_LEGAL_PERSON_TRADE_FMT.format(fixed_date), {"User-Agent":self.__ua.random}) 
               # title_text = '證券代號,證券名稱,外陸資買進股數(不含外資自營商),外陸資賣出股數(不含外資自營商),外陸資買賣超股數(不含外資自營商),外資自營商買進股數,外資自營商賣出股數,外資自營商買賣超股數,投信買進股數,投信賣出股數,投信買賣超股數,自營商買賣超股數,自營商買進股數(自行買賣),自營商賣出股數(自行買賣),自營商買賣超股數(自行買賣),自營商買進股數(避險),自營商賣出股數(避險),自營商買賣超股數(避險),三大法人買賣超股數\n'
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                        for i in text.split('\n') 
                        if len(i.split('",')) == 20 ])
                            
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
            else: #OTC市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(Define.OTC_LEGAL_PERSON_TRADE_FMT.format(roc_date), {"User-Agent":self.__ua.random})
                #標準化，移除多餘的文字      
                title_text = '代號,名稱,外資及陸資(不含外資自營商)-買進股數,外資及陸資(不含外資自營商)-賣出股數,外資及陸資(不含外資自營商)-買賣超股數,外資自營商-買進股數,外資自營商-賣出股數,外資自營商-買賣超股數,外資及陸資-買進股數,外資及陸資-賣出股數,外資及陸資-買賣超股數,投信-買進股數,投信-賣出股數,投信-買賣超股數,自營商(自行買賣)-買進股數,自營商(自行買賣)-賣出股數,自營商(自行買賣)-買賣超股數,自營商(避險)-買進股數,自營商(避險)-賣出股數,自營商(避險)-買賣超股數,自營商-買進股數,自營商-賣出股數,自營商-買賣超股數,三大法人買賣超股數合計\n'          
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                                for i in text.split('\n') 
                                if len(i.split('",')) == 24 ])
                #寫入CSV檔案
                self.__save_text(file_path, title_text+initialize_text)
#endregion
        return file_path

    
    def __check_make_dir(self, file_path:str):
        dir_name = os.path.dirname(file_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    def __load_text(self, url:str, headers:dict, encode='big5'):
        '''
        使用request下載CSV字串
        '''       
        time.sleep(3)
        r = requests.post(url, headers = headers)
        r.encoding = encode        
        return r.text
    
    def __save_text(self, file_path:str, text:str):
        '''
        存檔
        '''
        self.__check_make_dir(file_path)
        f = open(file_path, "w", encoding='utf8', newline='')
        f.write(text)
        f.close()
    

if __name__ == '__main__':
    t = LegalPersonTrading()
    print(t.get_legal_person_trade('2377', datetime.strptime('2018/04/30', '%Y/%m/%d')))