#%%
# -*- encoding: utf8-*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from define import Define
import stockinfo
from datetime import datetime, timedelta

class GoogleSheetHandler:
    __client = None
    __spread = None

    def __init__(self, spread_name):
        self.open(spread_name)        

    def open(self, spread_name):
        scope = ['https://spreadsheets.google.com/feeds', 
                'https://www.googleapis.com/auth/drive']
           
        creds = ServiceAccountCredentials.from_json_keyfile_name(Define.SECRET_PATH, scope)
        self.__client = gspread.authorize(creds)
        self.__spread = self.__client.open(spread_name)
        
    def get_sheet(self, sheet_name):
        if self.__spread == None:
            print("Client didn't init yet")
            return
        return self.__spread.worksheet(sheet_name)

if __name__ == "__main__":
    
    start_date_str = '2018/03/21'
    stock_id_str = '6533'
    
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    s = stockinfo.StockInfoManager(stock_id_str, start_date, 120)
   
    price = s.get_price(start_date)    
    ma20 = s.get_average(start_date, 20)
    ma60 = s.get_average(start_date, 60)
    ma120 = s.get_average(start_date, 120)
    cd1 = s.get_concentrate(start_date, 1)
    cd20 = s.get_concentrate(start_date, 20)
    cd60 = s.get_concentrate(start_date, 60)
    cd120 = s.get_concentrate(start_date, 120)
    
    handler = GoogleSheetHandler('StockGradingSystem')
    sheet = handler.get_sheet('Main')
    new_cell_row = int(sheet.row_count) +1

    new_row_data = [
        None,
        stock_id_str,
        '=if(B{0}="","", VLOOKUP(if(IsText($B{0}),$B{0}, Text($B{0},"0")),ID!$A:$B,2,FALSE))'.format(new_cell_row) ,
        price,
        ma20,
        ma60,
        ma120,
        '=if(min(E{0},F{0}) =0,0,round(ABS(F{0}-E{0})/min(E{0},F{0})*100,2))'.format(new_cell_row),
        '=VLOOKUP(H{0},Score!$E$11:$G$14,3,TRUE)'.format(new_cell_row),
        '=if(min(G{0},F{0}) =0,0,round(ABS(F{0}-G{0})/min(G{0},F{0})*100,2))'.format(new_cell_row),
        '=VLOOKUP(J{0},Score!$E$11:$G$14,3,TRUE)'.format(new_cell_row),
        '=if(min(G{0},E{0}) =0,0,round(ABS(E{0}-G{0})/min(G{0},E{0})*100,2))'.format(new_cell_row),
        '=VLOOKUP(L{0},Score!$E$11:$G$14,3,TRUE)'.format(new_cell_row),
        cd1,
        '=if(N{0}<Score!$B$26,Score!$C$26,VLOOKUP(N{0},Score!$A$2:$C$6,3,TRUE))'.format(new_cell_row),
        cd20,
        '=if(P{0}<Score!$B$29,Score!$C$29,VLOOKUP(P{0},Score!$E$2:$G$6,3,TRUE))'.format(new_cell_row),
        cd60,
        '=if(R{0}<Score!$B$27,Score!$C$27,VLOOKUP(R{0},Score!$E$2:$G$6,3,TRUE))'.format(new_cell_row),
        cd120,
        '=if(T{0}<Score!$B$28, Score!$C$28,if(T{0}=\"\",\"\",VLOOKUP(T{0},Score!$E$20:$G$22,3,TRUE)))'.format(new_cell_row),
        None,
        '=if(V{0}>=Score!$B$32,Score!$C$32, VLOOKUP(V{0},Score!$I$2:$K$8,3,TRUE))'.format(new_cell_row),
        None,
        '=if(X{0}>Score!$B$33, Score!$C$33,VLOOKUP(X{0},Score!$M$2:$O$6,3,TRUE))'.format(new_cell_row),
        None,
        '=if(Z{0}=\"O\", Score!$B$12, 0)'.format(new_cell_row),
        None,
        '=if(AB{0}=\"O\", Score!$B$11, 0)'.format(new_cell_row),
        None,
        '=if(AD{0}=\"\",\"\", if(AD{0}<>0, Score!$B$10*AD{0}, Score!$B$31))'.format(new_cell_row),
        None,
        '=AF{0}*Score!$B$15'.format(new_cell_row),
        None,
        '=AH{0}*Score!$C$13'.format(new_cell_row),
        '=if(B{0}=\"\",\"\",if(AND(AH{0}>=Score!$B$13), ROUND((I{0}+K{0}+M{0}+O{0}+Q{0}+S{0}+U{0}+W{0}+Y{0}+AE{0}+AC{0}+AA{0}+AG{0}+AI{0}),0), 0))'.format(new_cell_row)
    ]          
    sheet.append_row(new_row_data, 'USER_ENTERED')
    


