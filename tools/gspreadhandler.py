#%%
# -*- encoding: utf8-*-

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from define import Define

scope = ['https://spreadsheets.google.com/feeds', 
        'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name(Define.SECRET_PATH, scope)
client = gspread.authorize(creds)

c = client.open('StockGradingSystem')
sheet = c.worksheet('Main')


pp = pprint.PrettyPrinter()
records = sheet.row_values(1)
pp.pprint(records)


