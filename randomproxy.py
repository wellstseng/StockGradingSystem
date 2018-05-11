from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import json
import re
ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]


def get_randome_proxies():
  # Retrieve latest proxies
  proxies_req = Request('http://www.gatherproxy.com/proxylist/country/?c=Taiwan')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find('table', id='tblproxy')
  proxies_s = proxies_table.find_all('script', type="text/javascript");
  
  for row in proxies_s:
    test = row.string
    b = test.find('insertPrx(')+10
    e = test.find('});')+1
    t = test[b:e]
    j = json.loads(t)
    
    proxies.append({
      'ip' : j["PROXY_IP"],
      'port' : int('0x{}'.format(j["PROXY_PORT"]),16),
    })
    
  
  return proxies

def test(proxies):
  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 100):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 10 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  if len(proxies) == 0:
        return -1
  return random.randint(0, len(proxies) - 1)

get_randome_proxies()

if __name__ == '__main__':
  get_randome_proxies()