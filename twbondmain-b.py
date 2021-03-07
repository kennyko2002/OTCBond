#main program to get similar bond yield
import datetime
import pandas as pd
import sys
import streamlit as st
import numpy as np
from matplotlib import pyplot
from matplotlib.font_manager import FontProperties
import streamlit.components.v1 as components  # Import Streamlit
import urllib.request
# Render the h1 block, contained in a frame of size 200x200.
st.markdown("""

<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
table .dataframe mystyle {
    font-size: 20pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

}

.mystyle td, th {
    padding: 5px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}

</style>



""", unsafe_allow_html=True)


page = open("phinews.html").read()
components.html(page,width=800,height=300)

st.title('台債市場交易查詢')
bondfromcsv=pd.read_csv('https://raw.githubusercontent.com/kennyko2002/OTCBond/master/twbond',names=['ID','Name','Duration','MaturityYear','High','Low','Average','recorddate'],parse_dates=['recorddate'],infer_datetime_format='%Y-%M-%D')
bondfromcsv=bondfromcsv.astype({"ID":str, "Name":str})
twgovbondlist=pd.read_csv('twgovbondlist')
twcorpbondlist=pd.read_csv('twcorpbondlist')
bondfromcsv=pd.merge(bondfromcsv,twcorpbondlist,how='left',on='ID')
bondfromcsv=bondfromcsv[['ID','Name_x','Rating','Duration','MaturityYear','Average','recorddate']]
bondfromcsv=bondfromcsv.fillna('twAAA')
bondfromcsv.rename(columns={"Name_x":"Name"},inplace=True)
bondfromcsv.sort_values(by='recorddate',ascending=False,inplace=True)
querybond=st.sidebar.text_input('請輸入券號')
duration_diff=st.sidebar.slider("存續期間差異", min_value=0.0, max_value=5.0, value=1.0,step=0.1)
start_date=st.sidebar.slider("資料期間", min_value=0, max_value=90, value=30,step=1)

st.markdown("""
<link rel="stylesheet" type="text/css" href="style.css"/>
<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
</style>
""", unsafe_allow_html=True)


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
#  target=bondfromcsv[bondfromcsv['ID']==querybond & bondfromcsv['recorddate']>=(np.datetime64((datetime.date.today()-datetime.timedelta(start_date))))]
  target=bondfromcsv[(bondfromcsv['ID']==querybond) & (bondfromcsv['recorddate']>=first_record_date)]
  if target.size==0:
    st.write("No trade record")
  else:
    pyplot.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    st.subheader("本券近期成交記錄")
    st.table(target)
    
    if querybond.startswith('A'):
      targetduration=inbond.Duration.item()
    else :
      targetduration=target['Duration'].values[0]
    upper=bondfromcsv[ (bondfromcsv['Duration']>targetduration) & (bondfromcsv['Duration']<(targetduration+duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition & (bondfromcsv['recorddate']>=first_record_date) & (bondfromcsv['Rating']==target['Rating'].values[0])]
    lower=bondfromcsv[ (bondfromcsv['Duration']<targetduration) & (bondfromcsv['Duration']>(targetduration-duration_diff)) & (bondfromcsv['ID']!=querybond) & govtcondition &(bondfromcsv['recorddate']>=first_record_date) & (bondfromcsv['Rating']==target['Rating'].values[0])]
    st.subheader("相近(存續)天期成交記錄")
  #  col1,col2=st.beta_columns(2)
  #  with col1:
  #    st.table(upper[['ID','Name','Duration','Average']])
  #  with col2:
  #    st.table(lower[['ID','Name','Duration','Average']])
    st.table(upper[['ID','Name','Duration','Average','recorddate']])
    st.table(lower[['ID','Name','Duration','Average','recorddate']])
    fig = pyplot.figure()
    
    ax = fig.add_subplot(1,1,1)
    ax.set_xlabel("日期")
    ax.set_ylabel('Yield%')
    
    #ax.tick_params(labelrotation=30)
    s1=ax.scatter(target.recorddate,target.Average,c='g',s=5**2,marker='D')
    s2=ax.scatter(upper.recorddate,upper.Average,c='r',s=2**2,marker='X')
    s3=ax.scatter(lower.recorddate,lower.Average,c='b',s=2**2,marker='X')
    ax.grid(axis='y')
    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
    fig.legend(
    handles=(s1, s2, s3),labels=(querybond, 'longer bond', 'short bond'),loc='upper left',bbox_to_anchor=(0.13,0.87))
    
    
    st.pyplot(fig)
    st.markdown("""

<style>
table td:nth-child(1) {
    display: none
}
table th:nth-child(1) {
    display: none
}
table .dataframe mystyle {
    font-size: 20pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

}

.mystyle td, th {
    padding: 5px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}

</style>



""", unsafe_allow_html=True)
   
