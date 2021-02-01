import datetime
import pandas as pd
import sys
from tabula import read_pdf
record=datetime.date.today()
#等殖
url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdys01a.'+ record.strftime("%Y%m%d") +'-C.xls'
try:
  x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,2,3,9,10,11],names=['ID','Name','Duration','TimeToMaturity','High','Low','Average'])
  y=x[x.Name.notna()]
  y['recorddate']=record
  y.to_csv('twbond',mode='a',index=False,header=False)
except:
  print("no data"+record.strftime("%Y%m%d"))
#處所
url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdcs001.'+ record.strftime("%Y%m%d") +'-C.xls'
try:
  x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,2,3,9,10,11],names=['ID','Name','Duration','TimeToMaturity','High','Low','Average'])
  y=x[x.Name.notna()]
  y['recorddate']=record
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
  print("no data"+record.strftime("%Y%m%d"))


