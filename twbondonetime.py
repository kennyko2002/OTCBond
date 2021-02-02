import datetime
import pandas as pd
import sys
import numpy as np
for i in range(120):
    
    time_delta = datetime.timedelta(days=i)
    record=datetime.date.today()-time_delta
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


