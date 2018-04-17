#%%
# -*- encoding: utf8-*-

import twstock
from datetime import datetime
from datetime import timedelta
from leaderdifference import LeaderDifference
import pandas as pd
import math 
from tools.workbookhandler import WorkBookHandler
from define import * 

class StockInfoManager:  
    __leader_diff = LeaderDifference() 
    def __init__(self, stock_id, start_date, period):
        self.__stock = twstock.Stock(str(stock_id))
        self.init_date(start_date, period)
        #print("{}  c: {}".format(self.__stock.date , len(self.__stock.date)))
            
    def init_date(self, begin, period):
        try:            
            end = begin - timedelta(days=(period*2)+30) 
            if self.__stock.date[0] > end:
                print('date less end')
                self.__stock.fetch_from(end.year, end.month)
        except ValueError as e:
            print("date format error '%Y/%m/%d'   msg:{}".format(str(e)))
    
    def get_date(self, begin, period):
        self.init_date(begin, period)
        i = self.__stock.date.index(begin)
        return self.__stock.date[i-period+1]

    def get_leader_difference(self, begin_date, end_date):
        o = self.__leader_diff.get_data(self.__stock.sid, begin_date, end_date)
        data = {}       
        train = pd.DataFrame.from_dict(o['Buy'])
        train['BSSum'] = train['BSSum'].str.replace(',', '')
        train['BSSum'] = pd.to_numeric(train['BSSum'])
        train['BuySum'] = train['BuySum'].str.replace(',', '')
        train['BuySum'] = pd.to_numeric(train['BuySum'])
        train['SellSum'] = train['SellSum'].str.replace(',', '')
        train['SellSum'] = pd.to_numeric(train['SellSum'])
        data['Buy'] = train

        train = pd.DataFrame.from_dict(o['Sell'])
        train['BSSum'] = train['BSSum'].str.replace(',', '')
        train['BSSum'] = pd.to_numeric(train['BSSum'])
        train['BuySum'] = train['BuySum'].str.replace(',', '')
        train['BuySum'] = pd.to_numeric(train['BuySum'])
        train['SellSum'] = train['SellSum'].str.replace(',', '')
        train['SellSum'] = pd.to_numeric(train['SellSum'])
        data['Sell'] = train
        return data

    def get_price(self, date):
        i = self.get_date_index(date)
        return self.__stock.price[i]     

    def get_date_index(self, date):
        i = self.__stock.date.index(date)
        return i
    
    def get_average(self, date, days):
        t = self.__stock.moving_average(self.__stock.price, days)
        cur = len(t)
        total = len(self.__stock.date)
        for _ in range(0, total-cur):
            t.insert(0, 0)
        i = self.get_date_index(date)
        return t[i]
    
    def get_concentrate(self, start_date, days):
        end_date = self.get_date(start_date, days)
        leader_diff = self.get_leader_difference(start_date, end_date)
        b = leader_diff['Buy']['BSSum'].sum() 
        s = leader_diff['Sell']['BSSum'].sum()
        bs = b + s
        
        start_index = self.get_date_index(start_date)
        end_index = self.get_date_index(end_date)

        volume = 0
        for i in range(start_index, end_index-1, -1):
            c =self.__stock.capacity[i]
            volume +=  c

        volume = math.floor(volume / 1000)
        return round(bs / volume * 100, 1) if volume > 0 else 0
        

def test():
    start_date_str = '2017/05/12'
    stock_id_str = '00655L'

    
    start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
    s = StockInfoManager(stock_id_str, start_date, 120)
   
    price = s.get_price(start_date)    
    ma20 = s.get_average(start_date, 20)
    ma60 = s.get_average(start_date, 60)
    ma120 = s.get_average(start_date, 120)
    cd1 = s.get_concentrate(start_date, 1)
    cd20 = s.get_concentrate(start_date, 20)
    cd60 = s.get_concentrate(start_date, 60)
    cd120 = s.get_concentrate(start_date, 120)
    
    '''
    print('observe date:{}'.format(start_date.strftime('%Y/%m/%d')))
    print('price:{}'.format(price))
    print('20ma:{}'.format(ma20))
    print('60ma:{}'.format(ma60))
    print('120ma:{}'.format(ma120))
    print('1 day concentrate:{}'.format(cd1))
    print('20 day concentrate:{}'.format(cd20))
    print('60 day concentrate:{}'.format(cd60))
    print('120 day concentrate:{}'.format(cd120))
    print(' {}	{}	{}	{}	{}	{}	{}	{}'.format(price, ma20, ma60, ma120, cd1, cd20, cd60, cd120))
    '''

    
    wb = WorkBookHandler.load_workbook(Define.XLS_PATH)
    ws = WorkBookHandler.get_sheet(wb, 'Main')
    wb.active = wb.worksheets.index(ws)
    
    new_cell_index = 0
    for cell in ws['B']:
        if cell.value == None or cell.value == "":
            global new_cell_index
            new_cell_index = int(cell.row)-1
            break
   
    #add cell data
    new_cell_row = new_cell_index + 1
    exit
    
    ws['A'][new_cell_index].value = None
    ws['B'][new_cell_index].value = stock_id_str
    ws['C'][new_cell_index].value = "=if(B{0}=\"\",\"\", VLOOKUP($B{0},ID!$A:$B,2,FALSE))".format(new_cell_row) 
    ws['D'][new_cell_index].value = price
    ws['E'][new_cell_index].value = ma20
    ws['F'][new_cell_index].value = ma60
    ws['G'][new_cell_index].value = ma120
    ws['H'][new_cell_index].value ="=if(min(E{0},F{0}) =0,0,round(ABS(F{0}-E{0})/min(E{0},F{0})*100,2))".format(new_cell_row)
    ws['I'][new_cell_index].value ="=VLOOKUP(H{0},Score!$E$11:$G$14,3,TRUE)".format(new_cell_row)
    ws['J'][new_cell_index].value ="=if(min(G{0},F{0}) =0,0,round(ABS(F{0}-G{0})/min(G{0},F{0})*100,2))".format(new_cell_row)
    ws['K'][new_cell_index].value ="=VLOOKUP(J{0},Score!$E$11:$G$14,3,TRUE)".format(new_cell_row)
    ws['L'][new_cell_index].value ="=if(min(G{0},E{0}) =0,0,round(ABS(E{0}-G{0})/min(G{0},E{0})*100,2))".format(new_cell_row)
    ws['M'][new_cell_index].value ="=VLOOKUP(L{0},Score!$E$11:$G$14,3,TRUE)".format(new_cell_row)
    ws['N'][new_cell_index].value = cd1
    ws['O'][new_cell_index].value ="=if(N{0}<Score!$B$26,Score!$C$26,VLOOKUP(N{0},Score!$A$2:$C$6,3,TRUE))".format(new_cell_row)
    ws['P'][new_cell_index].value = cd20
    ws['Q'][new_cell_index].value ="=if(P{0}<Score!$B$29,Score!$C$29,VLOOKUP(P{0},Score!$E$2:$G$6,3,TRUE))".format(new_cell_row)
    ws['R'][new_cell_index].value = cd60
    ws['S'][new_cell_index].value ="=if(R{0}<Score!$B$27,Score!$C$27,VLOOKUP(R{0},Score!$E$2:$G$6,3,TRUE))".format(new_cell_row)
    ws['T'][new_cell_index].value = cd120
    ws['U'][new_cell_index].value ="=if(T{0}<Score!$B${0}, Score!$C${0},if(T{0}=\"\",\"\",VLOOKUP(T{0},Score!$E$20:$G$22,3,TRUE)))".format(new_cell_row)
    ws['V'][new_cell_index].value =None
    ws['W'][new_cell_index].value ="=if(V{0}>=Score!$B$32,Score!$C$32, VLOOKUP(V{0},Score!$I$2:$K$8,3,TRUE))".format(new_cell_row)
    ws['X'][new_cell_index].value =None
    ws['Y'][new_cell_index].value ="=if(X{0}>Score!$B$33, Score!$C$33,VLOOKUP(X{0},Score!$M$2:$O$6,3,TRUE))".format(new_cell_row)
    ws['Z'][new_cell_index].value =None
    ws['AA'][new_cell_index].value ="=if(Z{0}=\"O\", Score!$B$12, 0)".format(new_cell_row)
    ws['AB'][new_cell_index].value =None
    ws['AC'][new_cell_index].value ="=if(AB{0}=\"O\", Score!$B$11, 0)".format(new_cell_row)
    ws['AD'][new_cell_index].value =None
    ws['AE'][new_cell_index].value ="=if(AD{0}=\"\",\"\", if(AD{0}<>0, Score!$B$10*AD{0}, Score!$B$31))".format(new_cell_row)
    ws['AF'][new_cell_index].value =None
    ws['AG'][new_cell_index].value ="=AF{0}*Score!$B$15".format(new_cell_row)
    ws['AH'][new_cell_index].value =None
    ws['AI'][new_cell_index].value ="=AH{0}*Score!$C$13".format(new_cell_row)
    ws['AJ'][new_cell_index].value =None
    ws['AK'][new_cell_index].value ="=if(B{0}=\"\",\"\",if(AND(AH{0}>=Score!$B$13), ROUND((I{0}+K{0}+M{0}+O{0}+Q{0}+S{0}+U{0}+W{0}+Y{0}+AE{0}+AC{0}+AA{0}+AG{0}+AI{0}),0), 0))".format(new_cell_row)

    wb.save(Define.XLS_PATH)
    wb.close()
    
    
if __name__ == '__main__':
    test()