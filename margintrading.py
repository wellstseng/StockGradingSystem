#%%
# -*- encoding:utf8 -*-
import twstock
import os.path
import os
import requests
import csv
import pandas as pd
from define import *
from fake_useragent import UserAgent

class MarginTrading:
    __ua = UserAgent()
    def get_data(self, data_type:int, stock_id:str, date:str):
        '''
        載入信用交易資料
        回傳DataFrame
        '''
        #取得市場類型
        market = Define.get_market_type(stock_id)

        #未知市場不處理
        if market == MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return MarketType.UNKNOWN,None

        #檢查是否需從網路下載資料表
        file_path = self.check_load_margin_data(market, date) if data_type == MarginTradingType.MARGIN else self.check_load_daytrading_data(market, date) 
        #產生data frame回傳
        df =pd.read_csv(file_path, encoding='utf-8', header=0, index_col=0)        
        return market, df        

    def get_daytrade(self, stock_id:str, date:str):
        market, margin_df = self.get_data(MarginTradingType.MARGIN, stock_id, date)
        _, daytrading_df = self.get_data(MarginTradingType.DAYTRADING, stock_id, date)
        if market == MarketType.UNKNOWN:
            return None
        short_selling = int(margin_df.at[stock_id, '資券互抵' if market == MarketType.TSE else '資券相抵(張)'])
        day_trading = int(int(daytrading_df.at[stock_id, '當日沖銷交易成交股數'].replace(',',''))/1000) #換算張

        return short_selling+day_trading, short_selling, day_trading

    def get_rgzratio(self, stock_id:str, date:str):
        #print(margin_data.at[stock_id, '資券相抵(張)'])
        market, df = self.get_data(MarginTradingType.MARGIN, stock_id, date)
        if market == MarketType.UNKNOWN:
            return None

        securities = int(df.at[stock_id, '券今餘' if market == MarketType.TSE else '券餘額'].replace(',',''))
        financing = int(df.at[stock_id, '資今餘' if market == MarketType.TSE else '資餘額'].replace(',',''))

        if financing == 0:
            return 0
        return round(securities/financing*100, 2), securities, financing

    def check_load_margin_data(self, market:str, date:str):        
        '''
        檢查下載信用交易資料
        '''

        if market == MarketType.UNKNOWN:
            print('unknown market')
            return None

        #檢查檔案是否存在，不存在先從網路上下載
        file_path = Define.get_margin_file_path(market, date)
        if not os.path.isfile(file_path):
#region 透過網路下載資料並儲存
            #TSE市場下載           
            if market == MarketType.TSE:
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(Define.TSE_MARGIN_URL_FMT.format(fixed_date), {"User-Agent":self.__ua.random}) 
                #標準化分析，刪除多餘的文字               
                title_text = "\"股票代號\",\"股票名稱\",\"資買進\",\"資賣出\",\"資現償\",\"資前餘額\",\"資今餘\",\"資限額\",\"券買進\",\"券賣出\",\"券現償\",\"券前餘\",\"券今餘\",\"券限額\",\"資券互抵\",\"註記\",\n"
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                        for i in text.split('\n') 
                        if len(i.split('",')) == 17 and (not "代號" in i and not "名稱" in i)])
                            
                #寫入CSV檔案
                self.__save_text(file_path, title_text+initialize_text)
            else: #OTC市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(Define.OTC_MARGIN_URL_FMT.format(roc_date), {"User-Agent":self.__ua.random})
                #標準化，移除多餘的文字                
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                                for i in text.split('\n') 
                                if len(i.split('",')) == 20 or ("代號" in i and "名稱" in i)])
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
#endregion
        return file_path

    def check_load_daytrading_data(self, market:str, date:str):
        '''
        檢查下載現股當沖資料
        '''
        if market == MarketType.UNKNOWN:
            print('unknown market')
            return None
        file_path = Define.get_daytrading_file_path(market, date)
        self.__check_make_dir(file_path)

        #檢查是否需重新下載
        if not os.path.isfile(file_path):
            #TSE市場下載           
            if market == MarketType.TSE:            
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(Define.TSE_DAYTRADING_URL_FMT.format(fixed_date), Define.TSE_DAYTRADING_REQ_HEADERS) 
                #標準化分析，刪除多餘的文字  
                text_arr = [i.translate({ord(' '): None}) 
                            for i in text.split('\n') 
                                if len(i.split('",')) == 7]
                #移除前2行多餘的字串
                del text_arr[0]
                del text_arr[0]                            
                initialize_text = "\n".join(text_arr)                            
                       
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
            else: #OTC市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(Define.OTC_DAYTRADING_URL_FMT.format(roc_date), Define.OTC_DAYTRADING_REQ_HEADERS)
                #標準化，移除多餘的文字   
                text_arr = [i.translate({ord(' '): None}) 
                            for i in text.split('\n') 
                            if len(i.split('",')) == 6 ]
                del text_arr[0]
                title_text = '"證券代號","證券名稱","暫停現股賣出後現款買進當沖註記","當日沖銷交易成交股數","當日沖銷交易買進成交金額","當日沖銷交易賣出成交金額"\n'
                initialize_text = "\n".join(text_arr)
                #寫入CSV檔案
                self.__save_text(file_path, title_text+initialize_text)
        return file_path

    def __check_make_dir(self, file_path:str):
        dir_name = os.path.dirname(file_path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    def __load_text(self, url:str, headers:dict):
        '''
        使用request下載CSV字串
        '''       
        r = requests.post(url, headers = headers)
        r.encoding = 'big5'        
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
    t = MarginTrading()
    print(t.get_daytrade('3546', '2018/04/25'))
    #t.check_load_daytrading_data(MarketType.OTC, '2018/04/25')