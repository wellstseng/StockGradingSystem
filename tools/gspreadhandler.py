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
    
    start_date_str = '2018/04/09'
    stock_id_str = '5478'
    
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    s = stockinfo.StockInfoManager(stock_id_str, start_date, 120)
   
    price = s.get_price(start_date)    
    ma20 = s.get_average(start_date, 20)
    ma60 = s.get_average(start_date, 60)
    ma120 = s.get_average(start_date, 120)
    leader1 =s.get_concentrate(start_date, 1)
    leader20 = s.get_concentrate(start_date, 20)
    leader60 = s.get_concentrate(start_date, 60)
    leader120 = s.get_concentrate(start_date, 120)
    rgz = s.get_rgzratio(start_date)[0]
    daytrading = s.get_daytrade_ratio(start_date)

    handler = GoogleSheetHandler('StockGradingSystem')
    sheet = handler.get_sheet('Main')
    new_cell_row = int(sheet.row_count) +1

    new_row_data = [
        start_date_str,
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
        leader1[0],
        '=if(N{0}<Score!$B$26,Score!$C$26,VLOOKUP(N{0},Score!$A$2:$C$6,3,TRUE))'.format(new_cell_row),
        leader20[0],
        '=if(P{0}<Score!$B$29,Score!$C$29,VLOOKUP(P{0},Score!$E$2:$G$6,3,TRUE))'.format(new_cell_row),
        leader60[0],
        '=if(R{0}<Score!$B$27,Score!$C$27,VLOOKUP(R{0},Score!$E$2:$G$6,3,TRUE))'.format(new_cell_row),
        leader120[0],
        '=if(T{0}<Score!$B$28, Score!$C$28,if(T{0}=\"\",\"\",VLOOKUP(T{0},Score!$E$20:$G$22,3,TRUE)))'.format(new_cell_row),
        daytrading,
        '=if(V{0}>=Score!$B$32,Score!$C$32, VLOOKUP(V{0},Score!$I$2:$K$8,3,TRUE))'.format(new_cell_row),
        rgz,
        '=if(X{0}>Score!$B$33, Score!$C$33,VLOOKUP(X{0},Score!$M$2:$O$6,3,TRUE))'.format(new_cell_row),
        "O" if leader1[1] > 0 else "X",
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
    


