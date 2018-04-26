#%%
# -*- encoding:utf8 -*-
import twstock
import os.path
import os
import requests
import csv
import pandas as pd
from define import *


class MarginTrading:
    def get_margin_data(self, stock_id:str, date:str):
        '''
        載入信用交易資料
        回傳DataFrame
        '''
        #取得市場類型
        market = Define.get_market_type(stock_id)

        #未知市場不處理
        if market == MarketType.UNKNOWN:
            print('unknown stock id: {}'.format(stock_id))
            return None

        #檢查是否需從網路下載資料表
        file_path = self.check_load_margin_data(market, date);
        
        #產生data frame回傳
        df =pd.read_csv(file_path, encoding='utf-8', header=0, index_col=0)        
        return market, df        

    def get_rgzratio(self, stock_id:str, date:str):
        #print(margin_data.at[stock_id, '資券相抵(張)'])
        market, df = self.get_margin_data(stock_id, date)
        if market == MarketType.UNKNOWN:
            return None

        securities = int(df.at[stock_id, '券今餘' if market == MarketType.TSE else '券餘額'].replace(',',''))
        financing = int(df.at[stock_id, '資今餘' if market == MarketType.TSE else '資餘額'].replace(',',''))

        if financing == 0:
            return 0
        return round(securities/financing*100, 2)

    def check_load_margin_data(self, market:str, date:str):        
        '''
        檢查下載信用交易資料
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
                text = self.__load_text(Define.OTC_MARGIN_URL_FMT.format(roc_date), Define.OTC_MARGIN_REQ_HEADERS)
                #標準化，移除多餘的文字                
                initialize_text = "\n".join([i.translate({ord(' '): None}) 
                                for i in text.split('\n') 
                                if len(i.split('",')) == 20 or ("代號" in i and "名稱" in i)])
                #寫入CSV檔案
                self.__save_text(file_path, initialize_text)
#endregion
        return file_path

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
        dir_name = os.path.dirname(file_path)
        print('dir name {}'.format(dir_name))
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        f = open(file_path, "w", encoding='utf8', newline='')        
        f.write(text)
        f.close()
    

if __name__ == '__main__':
    t = MarginTrading()
    print(t.get_rgzratio('5478', '2018/04/25'))