#main program to get similar bond yield
import datetime
import pandas as pd
import sys
import streamlit as st
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
bondfromcsv=pd.read_csv('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/twbond',names=['ID','Name','Duration','MaturityYear','High','Low','Average','recorddate'],parse_dates=['recorddate'],infer_datetime_format='%Y-%M-%D')
bondfromcsv=bondfromcsv.astype({"ID":str, "Name":str})
twgovbondlist=pd.read_csv('twgovbondlist')
twcorpbondlist=pd.read_csv('twcorpbondlist')
querybond=st.text_input('input the bond id')

if (st.button('Hit me')):
  intwgovbond=twgovbondlist[twgovbondlist['ID']==querybond]
  intwcorpbond=twcorpbondlist[twcorpbondlist['ID']==querybond]
  st.header("Bloomberg 公平市價")
  st.table(intwgovbond)
  govtcondition=bondfromcsv.ID.map(lambda x: x.startswith('A'))
  target=bondfromcsv[bondfromcsv['ID']==querybond]
  if target.size==0:
    st.write("No trade record")
  else:
    pyplot.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    st.subheader("本券近期成交記錄")
    st.table(target)
    targetduration=target['Duration'].values[-1]
    upper=bondfromcsv[ (bondfromcsv['Duration']>targetduration) & (bondfromcsv['Duration']<(targetduration+1)) & (bondfromcsv['ID']!=querybond) & govtcondition]
    lower=bondfromcsv[ (bondfromcsv['Duration']<targetduration) & (bondfromcsv['Duration']>(targetduration-1)) & (bondfromcsv['ID']!=querybond) & govtcondition]
    st.subheader("相近天期成交記錄")
    col1,col2=st.betacolumns(2)
    with col1:
      st.table(upper)
    with col2:
      st.table(lower)
    pyplot.ion()
    fig = pyplot.figure()
    
    ax = fig.add_subplot(1,1,1)
    #ax.tick_params(labelrotation=30)
    s1=ax.scatter(target.recorddate,target.Average,c='g',s=5**2)
    s2=ax.scatter(upper.recorddate,upper.Average,c='r',s=2**2)
    s3=ax.scatter(lower.recorddate,lower.Average,c='b',s=2**2)
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    fig.legend(
    handles=(s1, s2, s3),labels=(querybond, 'longer bond', 'shortbond'),loc='upper right')
    
    
    st.pyplot(fig)
   
