import os
import twstock

class Define:
    FILE_PATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
    LIST_PATH_FMT = FILE_PATH + '/res/list{}.csv'
    TEST_HTML_PATH = FILE_PATH + '/res/test/stock_list.txt'
    SECRET_PATH = FILE_PATH + '/auth/client_secret.json'
    XLS_PATH = FILE_PATH + '/res/StockGradingSystem.xlsx'
    MARGIN_PATH_FMT = FILE_PATH + '/res/margin/{0}_M{1}.csv'

    TSE_MARGIN_URL_FMT = 'http://www.twse.com.tw/exchangeReport/MI_MARGN?response=csv&date={0}&selectType=ALL'
    TSE_MARGIN_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "Referer":"http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal.php?l=zh-tw",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Cookie":"_ga=GA1.3.315440950.1514384378; _gid=GA1.3.2008630621.1524582057",
        "Host":"www.tpex.org.tw",
        "Upgrade-Insecure-Requests":"1"
    }
    
    OTC_MARGIN_URL_FMT = 'http://www.tpex.org.tw/web/stock/margin_trading/margin_balance/margin_bal_result.php?l=zh-tw&o=csv&d={0}&s=0'
    OTC_MARGIN_REQ_HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection":"keep-alive",
        "Cookie":"_ga=GA1.3.315440950.1514384378; _gid=GA1.3.2008630621.1524582057",
        "Host":"www.tpex.org.tw",
        "Upgrade-Insecure-Requests":"1",
        "Cache-Control": "max-age=0"
    }

    STOCK_LIST_SHEET_NAME = 'ID'

    @staticmethod
    def get_list_path(data_type):
        return Define.LIST_PATH_FMT.format(data_type)
    
    @staticmethod
    def get_margin_file_path(market, date):
        date = date.replace('/', '')
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