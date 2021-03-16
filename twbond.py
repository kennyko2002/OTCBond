import datetime
import pandas as pd
import sys
from tabula import read_pdf
import numpy as np
import urllib.request
import os
from bs4 import BeautifulSoup
record = datetime.date.today()
# 等殖
url = 'https://www.tpex.org.tw/storage/bond_zone/tradeinfo/govbond//' + \
    record.strftime("%Y") + '/' + record.strftime("%Y%m") + \
    '/BDdys01a.' + record.strftime("%Y%m%d") + '-C.xls'
x = pd.read_excel(url, skiprows=4, header=None, usecols=[0, 1, 2, 3, 9, 11, 15], names=[
                      'ID', 'Name', 'Duration', 'TimeToMaturity', 'High', 'Average', 'Volume'])
y = x[x.Name.notna()]
y['recorddate'] = record
y.to_csv('twbond', mode='a', index=False, header=False)
