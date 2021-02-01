import datetime
import pandas as pd
import sys
for i in range(120):
    
    time_delta = datetime.timedelta(days=i)
    record=datetime.date.today()-time_delta
    url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdys01a.'+ record.strftime("%Y%m%d") +'-C.xls'
    try:
        x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,2,3,9,10,11],names=['ID','Name','Duration','MaturityYear','High','Low','Average'])
        y=x[x.Name.notna()]
        y['recorddate']=record
        y.to_csv('twbond',mode='a',index=False,header=False)
    except:
        print("no data"+record.strftime("%Y%m%d"))
    url='https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + record.strftime("%Y") + '/'+ record.strftime("%Y%m") + '/BDdcs001.'+ record.strftime("%Y%m%d") +'-C.xls'
    try:
        x=pd.read_excel(url,skiprows=4,header=None,usecols=[0,1,2,3,9,10,11],names=['ID','Name','Duration','MaturityYear','High','Low','Average'])
        y=x[x.Name.notna()]
        y['recorddate']=record
        y.to_csv('twbond',mode='a',index=False,header=False)
    except:
        print("no data"+record.strftime("%Y%m%d"))
