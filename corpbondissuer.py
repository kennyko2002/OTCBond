import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
urls=['https://www.tpex.org.tw/web/bond/publish/corporate_bond_search/memo_professional.php?l=zh-tw','https://www.tpex.org.tw/web/bond/publish/corporate_bond_search/memo.php?l=zh-tw']
for url in urls:
  response = urllib.request.urlopen(url)
  html = response.read()
  sp = BeautifulSoup(html) 
  tbls=sp.find_all('table')
  x=tbls[0].find_all('td')
  y=[]
  for s in x : 
    y.append(s.text)
  y_sublists = [y[i:i+9] for i in range(0, len(y), 9)]
  yy=pd.DataFrame(y_sublists )
  yy=yy[[0,1,2]]
  yy.to_csv('corplistpro',mode='a',index=False,header=None)


