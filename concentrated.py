#%%
# -*- encoding: utf8-*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
from io import open
import re
import json

f = open("res/result.txt", "r", encoding='utf-8')
l = f.read()
f.close()

soup = BeautifulSoup(l, 'html.parser')
pattern = re.compile(r'var jsonDatas', re.MULTILINE | re.DOTALL)
script = soup.find("script", text=pattern)

start = script.string.find('eval(')+5
end = script.string.find('});')+1
json_s = script.string[start:end]

json_obj = json.load(json_s)


print('done')

