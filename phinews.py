import datetime
import pandas as pd
import sys
import numpy as np
import urllib.request
import os
import re
from bs4 import BeautifulSoup
html_string = '''
<html>
  <head><title>HTML Pandas Dataframe with CSS</title>
<link rel="stylesheet" href="https://kennyko2002.github.io/OTCBond/style.css">
  </head>
  <body>
    {table}
  </body>
</html>.
'''
urls = 'https://asianbondsonline.adb.org/economy/?economy=PH#news'
response = urllib.request.urlopen(urls)
html = response.read()
sp = BeautifulSoup(html)
sp.original_encoding
tbls = sp.find('table', id="Commentary")
x = tbls.find_all('td')
res = []
for s in x:

    td_check = s.find('a')
    bond_check = s.find('td', text=re.compile('.bond.'))
    bond_row_data = []
    row_data = []
    if td_check is not None:
        link = s.find('a')
        linku = str(link).replace("â\x80\x99", "'")
        linku = str(linku).replace("â\x80\x94", "-")
        row_data.append(linku)
        if bond_check is not None:
            bond_row_data.append(linku)
    else:
        not_link = ''.join(s.stripped_strings)
        if not_link == '':
            not_link = None
        row_data.append(not_link)
    res.append(row_data)

yy = pd.DataFrame(np.array(res).reshape(-1, 3))
bond = yy[yy[0].str.contains('bonds', regex='False')]
html_str = yy[0:10][[0, 2]].to_html(index=False, render_links=True,
                                    escape=False, max_rows=10, header=False, classes='mystyle')
bond_str = bond[0:10][[0, 2]].to_html(index=False, render_links=True,
                                      escape=False, max_rows=10, header=False, classes='mystyle')

Html_file = open("phinews.html", "w")
Html_file.write(html_string.format(table=html_str))
Html_file.close()

Html_file2 = open("phibondnews.html", "w")
Html_file2.write(html_string.format(table=bond_str))
Html_file2.close()
# yy.to_csv('phinews', mode='w', index=False, header=None)
