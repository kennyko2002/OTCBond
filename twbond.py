import datetime
import pandas as pd
import sys
from tabula import read_pdf
import numpy as np
import urllib.request
import os
from bs4 import BeautifulSoup
record=datetime.date.today()
#等殖
url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdys01a.'+ record.strftime("%Y%m%d") +'-C.xls'
try:
  x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,2,3,9,11,15],names=['ID','Name','Duration','TimeToMaturity','High','Average','Volume'])
  y=x[x.Name.notna()]
  y['recorddate']=record
  y.to_csv('twbond',mode='a',index=False,header=False)
except:
  print("no data"+record.strftime("%Y%m%d"))
#處所
url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdcs001.'+ record.strftime("%Y%m%d") +'-C.xls'
try:
  x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,3,4,8,10,13],names=['ID','Name','Duration','TimeToMaturity','High','Average','Volume'])
  y=x[x.Name.notna()]
  y['recorddate']=record
  y['Volume']=y['Volume']/100000000
  y.to_csv('twbond',mode='a',index=False,header=False)
except:
  print("no data"+record.strftime("%Y%m%d"))


#清單
url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdys503.'+ record.strftime("%Y%m%d") +'-C.xls'  
try:
  x=pd.read_excel(url,skiprows=3,header=None,usecols=[0,1,2,3,4,5,13],names=['ID','Name','Maturity','TimeToMaturity','Duration','Coupon','Yield'])
  y=x[x.Name.notna()]
  y['recorddate']=record
  y.to_csv('twgovbondlist',mode='w',index=False)
except:
  print("no gov list to retrived"+record.strftime("%Y%m%d"))

url='https://nweb.tpex.org.tw/bbg/bndcrvpx_'+ record.strftime("%Y%m%d") +'.pdf'
try:
  df = read_pdf(url,multiple_tables=False,pages = 'all',pandas_options={'header': None})
  df=pd.DataFrame(df[0])
  df.columns=['ID','Name','TimeToMaturity','CouponRating','Price','Yield']
  df['Coupon']=df['CouponRating'].map(lambda x :x.split(' ')[0])
  df['Rating']=df['CouponRating'].map(lambda x :x.split(' ')[1])

  df.to_csv('twcorpbondlist',mode='w',index=False,columns=['ID','Name','TimeToMaturity','Yield','Rating'])
except:
  print("no data"+record.strftime("%Y%m%d"))
#phi gov
url='https://www.pds.com.ph/wp-content/uploads/'+record.strftime("%Y")+'/'+record.strftime("%m")+'/FI-Board-Report-as-of-'+record.strftime("%B")+'-'+record.strftime("%d")+'-'+record.strftime("%Y")+'.pdf'
try:
  df = read_pdf(url,multiple_tables=False,pages = 'all')
  df=pd.DataFrame(df[0])
  df['recorddate']=record
  df=df[['Global ID', 'Local ID', 'Domestic No.', 'CPN','YRS','Maturity', 'D. Vol (MM)', 'Last Yield','recorddate']]
  df=df.dropna(subset=['Last Yield'])
  df=df[df['Global ID']!='Global ID']
  df.to_csv('phigovt',mode='a',index=False,header=None)
except:
  print("no data"+record.strftime("%Y%m%d"))
#phi corp
url='https://www.pds.com.ph/wp-content/uploads/'+record.strftime("%Y")+'/'+record.strftime("%m")+'/corp_board_summary_'+record.strftime("%Y")+'-'+record.strftime("%m")+'-'+record.strftime("%d")+'.csv'
try:
  df=pd.read_csv(url)
  df['recorddate']=record    
  df=df[['Global ID', 'Local ID', 'Domestic No.', 'Coupon Rate','YTM','Maturity', 'D.Vol(MM)', 'Last Yield','recorddate']]
  df.replace('-',np.NaN,inplace=True)
  df=df.dropna(subset=['Last Yield'])    
  df.to_csv('phicorp',mode='a',index=False,header=None) 
except:
  print("no corp data"+record.strftime("%Y%m%d"))


urls=['https://www.tpex.org.tw/web/bond/publish/corporate_bond_search/memo_professional.php?l=zh-tw','https://www.tpex.org.tw/web/bond/publish/corporate_bond_search/memo.php?l=zh-tw']
os.remove("demofile.txt") 
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

#phi issur list
url='https://www.pds.com.ph/wp-content/uploads/'+record.strftime("%Y")+'/'+record.strftime("%m")+'/Listed-Securities-as-of-'+record.strftime("%b")+'-'+record.strftime("%d")+'-'+record.strftime("%Y")+'.pdf'
try:
  df = read_pdf(url,multiple_tables=False,pages = 'all',lattice=True)
  df=pd.DataFrame(df[0])
  df['recorddate']=record
  df=df.iloc[5:,[0,2]]
  df=df.dropna()
  df2=df.replace({r'\r': ''}, regex=True)
  df2.rename(columns={'Unnamed: 0':'Corpname','Unnamed: 2':'key'},inplace=True)
  df2['key']=df2['key'].str.replace(' ','')
  df2.to_csv('phitest',header=None)
except:
  print("no phi issur list"+record.strftime("%Y%m%d"))






