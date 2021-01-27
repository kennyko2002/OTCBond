#main program to get similar bond yield
import datetime
import pandas as pd
import sys
import streamlit as st
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
bondfromcsv=pd.read_csv('twbond',names=['ID','Name','Duration','MaturityYear','High','Low','Average','recorddate'],parse_dates=['recorddate'],infer_datetime_format='%Y-%M-%D')
bondfromcsv=bondfromcsv.astype({"ID":str, "Name":str})
querybond=st.text_input('input the bond id')
st.write("No trade record")
if (st.button('Hit me')):
  
  govtcondition=bondfromcsv.ID.map(lambda x: x.startswith('A'))
  target=bondfromcsv[bondfromcsv['ID']==querybond]
  if target.size==0:
    st.write("No trade record")
  else:
    pyplot.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    st.table(target)
    targetduration=target['Duration'].values[-1]
    upper=bondfromcsv[ (bondfromcsv['Duration']>targetduration) & (bondfromcsv['Duration']<(targetduration+1)) & (bondfromcsv['ID']!=querybond) & govtcondition]
    lower=bondfromcsv[ (bondfromcsv['Duration']<targetduration) & (bondfromcsv['Duration']>(targetduration-1)) & (bondfromcsv['ID']!=querybond) & govtcondition]
    
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
#    axes[0,0].tick_params(labelrotation=45)
    ax.scatter(target.recorddate,target.Average,c='g')
    ax.scatter(upper.recorddate,upper.Average,c='r')
    ax.scatter(lower.recorddate,lower.Average,c='b')
    
    
    st.pyplot(fig)
    st.table(upper)

