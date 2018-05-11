#%%
# -*- encoding:utf8 -*-
import requests
import randomproxy
from fake_useragent import FakeUserAgent


__ua = FakeUserAgent()
def get(url, params=None, encoding='utf8'):   
    try:
        proxies = None
        proxy_index = randomproxy.random_proxy()
        if proxy_index != -1:
            proxy = randomproxy.proxies[proxy_index]
            proxies = {'http': '{0}:{1}'.format(proxy['ip'], proxy['port'])}
      
        r = requests.get(url, headers= {'User-Agent':__ua.random}, proxies = proxies)
        r.encoding = encoding
        return r, proxy_index
    except: # If error, delete this proxy and find another one
        remove_proxy(proxy_index)
        
        return None, proxy_index

def remove_proxy(index):
    if index != None:
        print('Proxy ' + randomproxy.proxies[index]['ip'] + ':' + randomproxy.proxies[index]['port'] + ' deleted.')
        del randomproxy.proxies[index]