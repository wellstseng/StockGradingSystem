import os
import twstock

class Define:
    FILE_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
    LIST_PATH_FMT = FILE_PATH + '/res/list{}.csv'
    TEST_HTML_PATH = FILE_PATH + '/res/test/stock_list.txt'
    SECRET_PATH = FILE_PATH + '/auth/client_secret.json'
    XLS_PATH = FILE_PATH + '/res/StockGradingSystem.xlsx'
    MARGIN_PATH_FMT = FILE_PATH + '/res/margin/{0}_M{1}.csv'

    STOCK_LIST_SHEET_NAME = 'ID'

    @staticmethod
    def get_list_path(data_type):
        return Define.LIST_PATH_FMT.format(data_type)
    
    @staticmethod
    def get_margin_file_path(market, date):
        return Define.MARGIN_PATH_FMT.format(date, market)

    @staticmethod
    def get_market_type(stock_id: str):
        if stock_id in twstock.twse and not stock_id in twstock.tpex:
            return MarketType.TSE
        elif not stock_id in twstock.twse and stock_id in twstock.tpex:
            return MarketType.OTC
        else:
            return MarketType.UNKNOWN

class MarketType:
    UNKNOWN = '0'
    TSE = '2'
    OTC = '4'

if __name__=='__main__':
    print("hello "+Define.FILE_PATH)