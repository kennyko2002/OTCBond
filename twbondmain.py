#main program to get similar bond YTM
import datetime
import pandas as pd
import sys
import streamlit as st
import numpy as np
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
country=st.sidebar.radio('Which country?',('Taiwan','Philippines'))
issuername=''
start_date=30
first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
pd.options.display.float_format='{:,.3f}'.format
pyplot.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 


def mycss():           
  st.markdown("""	<style>		
        .main {background:linear-gradient(to top right,#c3c95a,#c4b281);}
table {
background:white;
background:linear-gradient(to bottom right,rgba(255,255,255,0.7),rgba(255,255,255,0.3) );
border-radius:50px; 
font-weight:bold;
white-space:nowrap;
	}

h1,h2,h3{
text-align:center;}
	</style>
	""", unsafe_allow_html=True)

  st.markdown("""	<style>
	table td:nth-child(1) {
	    display: none
	}
	table th:nth-child(1) {
	    display: none
	}
.table-bottom-left > div:nth-child(1){
	    display: none;            
	}

.reportview-container .table-bottom-left,.reportview-container .dataframe.row-header,.reportview-container .dataframe.corner{
background:#ecead0;
font-weight:900;
color:#394a28 ;
}
  	

	</style>
	""", unsafe_allow_html=True)





if country=='Taiwan':
	st.title('台債市場交易查詢')
	bondfromcsv=st.cache(pd.read_csv)('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/twbond',names=['ID','Name','Duration','MaturityYear','High','YTM','VolumeE','Trade_date'],thousands=r',',parse_dates=['Trade_date'],infer_datetime_format='%Y-%M-%D')
	bondfromcsv=bondfromcsv.astype({"ID":str, "Name":str})
	twgovbondlist=st.cache(pd.read_csv)('twgovbondlist')
	twcorpbondlist=st.cache(pd.read_csv)('twcorpbondlist')
	corplistpro=st.cache(pd.read_csv)('corplistpro',names=['ID','Ticker','FullName'])

	bondfromcsv=pd.merge(bondfromcsv,twcorpbondlist,how='left',on='ID')
	bondfromcsv=pd.merge(bondfromcsv,corplistpro,how='left',on='ID')
	bondfromcsv=bondfromcsv[['ID','Name_x','Rating','Duration','MaturityYear','YTM','VolumeE','Trade_date','FullName']]
	#bondfromcsv=bondfromcsv.fillna('twAAA')
	bondfromcsv.Rating.fillna('twAAA',inplace=True)
	bondfromcsv.rename(columns={"Name_x":"Name"},inplace=True)
	bondfromcsv.sort_values(by='Trade_date',ascending=False,inplace=True)
	querytype=st.sidebar.radio('Query type?',('By ID','By Issuer','By Tenor'))	
	if querytype=='By ID':
	  querybond=st.sidebar.text_input('請輸入券號')
	  duration_diff=st.sidebar.slider("存續期間差異", min_value=0.0, max_value=5.0, value=1.0,step=0.1)
	  start_date=st.sidebar.slider("資料期間", min_value=0, max_value=90, value=30,step=1)




	  if (st.sidebar.button('查詢')):   
	    if querybond.startswith('A'):
	      govtcondition=bondfromcsv.ID.map(lambda x: x.startswith('A'))
	      inbond=twgovbondlist[twgovbondlist['ID']==querybond]
	    
	    else:
	      govtcondition=bondfromcsv.ID.map(lambda x: not x.startswith('A'))
	      inbond=twcorpbondlist[twcorpbondlist['ID']==querybond]
	    st.header("Bloomberg 公平市價")
	    st.table(inbond)
	    first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
	#  target=bondfromcsv[bondfromcsv['ID']==querybond & bondfromcsv['Trade_date']>=(np.datetime64((datetime.date.today()-datetime.timedelta(start_date))))]
	    target=bondfromcsv[(bondfromcsv['ID']==querybond) & (bondfromcsv['Trade_date']>=first_record_date)]
	    if target.size==0:
	      st.write("No trade record")
	    else:
	      st.subheader("本券近期成交記錄")
	      st.table(target[['ID','Name','Duration','YTM','Trade_date']])    
	    if querybond.startswith('A'):
	      targetduration=inbond.Duration.item()
	      upper=bondfromcsv[ (bondfromcsv['Duration']>targetduration) & (bondfromcsv['Duration']<(targetduration+duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition & (bondfromcsv['Trade_date']>=first_record_date) ]
	      lower=bondfromcsv[ (bondfromcsv['Duration']<targetduration) & (bondfromcsv['Duration']>(targetduration-duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition &(bondfromcsv['Trade_date']>=first_record_date) ]              
	    else :
	      targetduration=target['Duration'].values[0]
	      upper=bondfromcsv[ (bondfromcsv['Duration']>targetduration) & (bondfromcsv['Duration']<(targetduration+duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition & (bondfromcsv['Trade_date']>=first_record_date) & (bondfromcsv['Rating']==target['Rating'].values[0])]
	      lower=bondfromcsv[ (bondfromcsv['Duration']<targetduration) & (bondfromcsv['Duration']>(targetduration-duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition &(bondfromcsv['Trade_date']>=first_record_date) & (bondfromcsv['Rating']==target['Rating'].values[0])]
	    st.subheader("相近(存續)天期成交記錄")
	  #  col1,col2=st.beta_columns(2)
	  #  with col1:
	  #    st.table(upper[['ID','Name','Duration','YTM']])
	  #  with col2:
	  #    st.table(lower[['ID','Name','Duration','YTM']])
	    st.table(upper[['ID','Name','Duration','YTM','Trade_date']])
	    st.table(lower[['ID','Name','Duration','YTM','Trade_date']])
	    fig = pyplot.figure()
	    
	    ax = fig.add_subplot(1,1,1)
	    ax.set_xlabel("日期")
	    ax.set_ylabel('YTM%')
	    s2=ax.scatter(upper.Trade_date,upper.YTM,c='r',s=2**2,marker='X')
	    s3=ax.scatter(lower.Trade_date,lower.YTM,c='b',s=2**2,marker='X')	    
	    if target.size>0:
	      s1=ax.scatter(target.Trade_date,target.YTM,c='g',s=5**2,marker='D')
	      fig.legend(
	    handles=(s1, s2, s3),labels=(querybond, 'longer bond', 'shorter bond'),loc='upper left',bbox_to_anchor=(0.13,0.87))
	    else:
	      fig.legend(
	    handles=(s2, s3),labels=('longer bond', 'shorter bond'),loc='upper left',bbox_to_anchor=(0.13,0.87))
	    ax.grid(axis='y')
	    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')   
	    st.pyplot(fig)
	elif querytype=='By Issuer':
	  issuername=st.sidebar.selectbox('By Issuer',bondfromcsv.FullName.unique())
	  start_date=st.sidebar.slider("資料期間", min_value=0, max_value=90, value=30,step=1)
	  first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
	  if(st.sidebar.button('查詢')):	  
	    st.table( bondfromcsv[(bondfromcsv.FullName==issuername) & (bondfromcsv['Trade_date']>=first_record_date)])
	else:
	  tenor=st.sidebar.slider("債券天期", min_value=0.0, max_value=30.0, value=(1.0,5.0),step=0.1)
	  start_date=st.sidebar.slider("資料期間", min_value=0, max_value=90, value=30,step=1)	  
	  if (st.sidebar.button('查詢')):
	    first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
	#  target=bondfromcsv[bondfromcsv['ID']==querybond & bondfromcsv['Trade_date']>=(np.datetime64((datetime.date.today()-datetime.timedelta(start_date))))]
	    target=bondfromcsv[(bondfromcsv['Duration']>tenor[0]) & (bondfromcsv['Duration']<tenor[1]) & (bondfromcsv['Trade_date']>=first_record_date)]
	    if target.size==0:
	      st.write("No trade record")
	    else:
	      st.subheader("近期成交記錄")
	      st.table(target[['ID','Name','Duration','YTM','Trade_date']])    
else:
        st.title('Philippines Bond Market')
        bondtype=st.sidebar.radio('Govt/Corp?',('Govt','Corp'))
        if bondtype=='Govt':
          bondfromcsv=st.cache(pd.read_csv)('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/phigovt',thousands=r',',names=['Global ID', 'Local ID', 'Domestic No.', 'CPN','YRS','Maturity', 'D. Vol (MM)', 'YTM','Trade_date'],parse_dates=['Trade_date'],infer_datetime_format='%Y-%M-%D')
          bondfromcsv=bondfromcsv.rename(columns={'D. Vol (MM)':'D.Vol(MM)'})
          querytype=st.sidebar.radio('query type',('By ID','By Tenor'))
        else:
          bondfromcsv=st.cache(pd.read_csv,allow_output_mutation=True)('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/phicorp',thousands=r',',names=['Global ID', 'Local ID', 'Domestic No.', 'Coupon Rate','YRS','Maturity', 'D.Vol(MM)', 'YTM','Trade_date'],parse_dates=['Trade_date'],infer_datetime_format='%Y-%M-%D')
          bondfromcsv['Ticker']=bondfromcsv['Global ID'].map(lambda x :x.split(' ')[0])
          phi_issuer_list=st.cache(pd.read_csv)('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/phitest',names=['corpname','key'])
          bondfromcsv['key']=bondfromcsv['Local ID'].str.replace(' ','')
          bondfromcsv=bondfromcsv.join(phi_issuer_list.set_index('key'),how='left',on='key')
  
          querytype=st.sidebar.radio('Query type?',('By ID','By Issuer','By Tenor'))
        if querytype=='By ID':
          bondfromcsv=bondfromcsv.astype({"YRS":float})
          bondfromcsv.sort_values(by='Trade_date',ascending=False,inplace=True)
          #querybond=st.sidebar.selectbox('Global ID',np.sort(bondfromcsv['Global ID'].unique()))
          querybond=st.sidebar.selectbox('Global ID',bondfromcsv.sort_values('YRS')['Global ID'].unique())
          duration_diff=st.sidebar.slider("tenor_diff", min_value=0.0, max_value=5.0, value=1.0,step=0.1)
          start_date=st.sidebar.slider("number of days", min_value=0, max_value=90, value=30,step=1)

 

          if(st.sidebar.button('submit')):   
           first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
	#  target=bondfromcsv[bondfromcsv['ID']==querybond & bondfromcsv['Trade_date']>=(np.datetime64((datetime.date.today()-datetime.timedelta(start_date))))]
           target=bondfromcsv[(bondfromcsv['Global ID']==querybond) & (bondfromcsv['Trade_date']>=first_record_date)]
           if target.size==0:
              st.write("No trade record")
           else:
              
              st.subheader("Trade record for this issue ")
              st.table(target[['Global ID', 'Local ID', 'YRS', 'D.Vol(MM)', 'YTM','Trade_date']])
              targetduration=target['YRS'].values[0]
              #st.write(type(targetduration))
              upper=bondfromcsv[ (bondfromcsv['YRS']>targetduration) & (bondfromcsv['YRS']<(targetduration+duration_diff)) & (bondfromcsv['Global ID']!=querybond)  & (bondfromcsv['Trade_date']>=first_record_date) ]
              lower=bondfromcsv[ (bondfromcsv['YRS']<targetduration) & (bondfromcsv['YRS']>(targetduration-duration_diff)) & (bondfromcsv['Global ID']!=querybond)  &(bondfromcsv['Trade_date']>=first_record_date)]
              st.subheader("Similar tenor bond")
	  #  col1,col2=st.beta_columns(2)
	  #  with col1:
	  #    st.table(upper[['ID','Name','Duration','YTM']])
	  #  with col2:
	  #    st.table(lower[['ID','Name','Duration','YTM']])
              st.table(upper[['Global ID', 'Local ID', 'YRS', 'D.Vol(MM)', 'YTM','Trade_date']])
              st.table(lower[['Global ID', 'Local ID', 'YRS', 'D.Vol(MM)', 'YTM','Trade_date']])
           fig = pyplot.figure()
           ax = fig.add_subplot(1,1,1)
           ax.set_xlabel("Date")
           ax.set_ylabel('YTM%')
	    
	    #ax.tick_params(labelrotation=30)
           s1=ax.scatter(target.Trade_date,target['YTM'],c='g',s=5**2,marker='D')
           s2=ax.scatter(upper.Trade_date,upper['YTM'],c='r',s=2**2,marker='X')
           s3=ax.scatter(lower.Trade_date,lower['YTM'],c='b',s=2**2,marker='X')
           ax.grid(axis='y')
           fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
           fig.legend(handles=(s1, s2, s3),labels=(querybond, 'longer bond', 'short bond'),loc='upper left',bbox_to_anchor=(0.13,0.87))	    
           st.pyplot(fig)
        elif querytype=='By Issuer':
           issuername=st.sidebar.selectbox('By Issuer',bondfromcsv.corpname.unique())
           start_date=st.sidebar.slider("data period", min_value=0, max_value=90, value=30,step=1)
           first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
           outputtable=bondfromcsv[(bondfromcsv.corpname==issuername) &(bondfromcsv['Trade_date']>=first_record_date)]
           outputtable=outputtable[['Global ID', 'Local ID', 'YRS', 'D.Vol(MM)', 'YTM','Trade_date']]
           if outputtable.size>0:         
             #st.table( outputtable.sort_values(by='Trade_date',ascending=False))
              st.dataframe(outputtable.sort_values(by='Trade_date',ascending=False),width=1000)
           else:
             st.write("No trade record")
        else :
           tenor=st.sidebar.slider("tenor", min_value=0.0, max_value=30.0, value=(1.0,5.0),step=0.1)
           start_date=st.sidebar.slider("data period", min_value=0, max_value=90, value=30,step=1)
           if (st.sidebar.button('Query')):
             first_record_date=np.datetime64((datetime.date.today()-datetime.timedelta(start_date)))
	#  target=bondfromcsv[bondfromcsv['ID']==querybond & bondfromcsv['Trade_date']>=(np.datetime64((datetime.date.today()-datetime.timedelta(start_date))))]
             target=bondfromcsv[(bondfromcsv['YRS']>tenor[0]) & (bondfromcsv['YRS']<tenor[1]) & (bondfromcsv['Trade_date']>=first_record_date)]
             if target.size==0:
               st.write("No trade record")
             else:
               st.subheader("trade record")
               target=target[['Global ID', 'Local ID', 'YRS', 'D.Vol(MM)', 'YTM','Trade_date']]
               st.table(target.sort_values(by='Trade_date',ascending=False))
mycss()
            

