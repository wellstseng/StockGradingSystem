import os

class Define:
    FILE_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
    LIST_PATH_FMT = FILE_PATH + '/res/list{}.csv'
    TEST_HTML_PATH = FILE_PATH + '/res/test/stock_list.txt'

    XLS_PATH = FILE_PATH + '/res/StockGradingSystem.xlsx'

    STOCK_LIST_SHEET_NAME = 'ID'

    @staticmethod
    def get_list_path(data_type):
        return Define.LIST_PATH_FMT.format(data_type)

class MarketType:
    TSE = '2'
    OTC = '4'

if __name__=='__main__':
    print("hello "+Define.FILE_PATH)