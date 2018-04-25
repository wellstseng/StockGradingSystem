#%%
# -*- encoding:utf8 -*-
import twstock
import os.path
import requests
import csv
import pandas as pd
from define import *


class MarginTrading:
    def get_data(self, stock_id:str, date:str):
        '''
        取得所有信用交易資料，包含融資融券，現股當沖
        '''
        #取得市場類型
        market = Define.get_market_type(stock_id)

        #未知市場不處理
        if market == MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return None

        #取得信用交易資料data frame
        margin_data = self.__get_margin_data(market, stock_id, date)

        #取得現股當沖資料data frame

        #合併data frame

    
    def __get_margin_data(self, market:str, stock_id:str, date:str):        
        '''
        取得信用交易資料
        '''

        #檢查檔案是否存在，不存在先從網路上下載
        file_path = Define.get_margin_file_path(market, date)
        if not os.path.isfile(file_path):
#region 透過網路下載資料並儲存
            #TSE市場下載           
            if market == MarketType.TSE:
                #格式化日期
                fixed_date = date.replace('/', '')
                #取得網路下載的字串
                text = self.__load_text(Define.TSE_MARGIN_URL_FMT.format(fixed_date), Define.TSE_MARGIN_REQ_HEADERS) 
                #標準化分析，刪除多餘的文字               
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                        for i in text.split('\n') 
                        if len(i.split('",')) == 17 and i[0] != '='])
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
            else: #OTC市場下載
                #轉換西元為民國
                roc_date = '/'.join([str(int(date.split('/')[0]) - 1911)] + date.split('/')[1:])
                #取得網路下載的字串
                text = self.__load_text(Define.OTC_MARGIN_URL_FMT.format(roc_date), Define.OTC_MARGIN_REQ_HEADERS)
                #標準化，移除多餘的文字                
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                                for i in text.split('\n') 
                                if len(i.split('",')) == 20 or ("代號" in i and "名稱" in i)])
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
#endregion

#region 產生data frame
        df =pd.read_csv(file_path, encoding='utf-8', header=0, index_col=0)
        print(df)
        pass
#endregion
        pass

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
        f = open(file_path, "w", encoding='utf8', newline='')        
        f.write(text)
        f.close()
    

if __name__ == '__main__':
    t = MarginTrading()
    t.get_data('2353', '2018/04/25')