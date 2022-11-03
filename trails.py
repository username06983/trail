import requests
import numpy as np
import pandas as pd
from datetime import date
from datetime import timedelta
import streamlit as st

st.set_page_config(layout = "wide")

@st.experimental_memo()
def nse():
  today = date.today()  #date
  yesterday = today - timedelta(days = 1)
  daten = []
  url1 = []
  for i in range(45):
    d = yesterday - timedelta(days=i)
    if d.weekday() < 5:
      s = d.strftime("%d%b%Y").upper()
      m = d.strftime("%b").upper()
      y = d.strftime("%Y")
      url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}.zip".format(y,m,s,"bhav.csv")
      proxies = { 'http://example.org': 'http://10.10.1.10:3128', 'http://something.test': 'http://10.10.1.10:1080' }
      try:
        r = requests.get(url,timeout=2,proxies = proxies)
        if r.status_code == 200:
          url1.append(url)
      except:
        pass
#url1
  
  st.write("stock dashboard")
  st.write("nse 7 days")

  l1 = url1[0]
  l1 = pd.read_csv(l1)
  l1 = l1.loc[l1['SERIES'].isin(['EQ','BE'])]
  l1 = l1[['SYMBOL','CLOSE']]
  link1 = l1.set_index('SYMBOL')


  present_url = url1[0:7]
  df = pd.DataFrame()
  for k in present_url:
    dff = pd.read_csv(k)
    df = df.append(dff)
  df = df.loc[df['SERIES'].isin(['EQ','BE'])]
  df = df.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
  p = df.groupby('SYMBOL')['CLOSE'].mean().rename('Present price MA')
  df_price_present7 = pd.DataFrame(p)


  df = df[(df['TOTTRDQTY'] > 100000)]
  v = df.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('present Volume MA')
  df_volume_present7 = pd.DataFrame(v)


  past_url = url1[7:14]
  df1 = pd.DataFrame()
  for k in past_url:
    dff = pd.read_csv(k)
    df1 = df1.append(dff)
  df1 = df1.loc[df1['SERIES'].isin(['EQ','BE'])]
  df1 = df1.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
  t = df1.groupby('SYMBOL')['CLOSE'].mean().rename('past price MA')
  df_price_past7 = pd.DataFrame(t)


  df1 = df1[(df1['TOTTRDQTY'] > 100000)]
  s = df1.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('past Volume MA')
  df_volume_past7 = pd.DataFrame(s)

  df = pd.merge(df_price_past7,df_price_present7,on = 'SYMBOL')
  df0 = pd.merge(df_volume_present7, df_volume_past7, on = 'SYMBOL')

  volume_ma = (df0['present Volume MA'] - df0['past Volume MA']) / df0['past Volume MA'] *100
  volume_ma = pd.DataFrame(volume_ma)
  volume_ma.columns = ['volume7']
  volume_MA = volume_ma[volume_ma.volume7 > 20]

  close_MA = (df['Present price MA'] - df['past price MA']) / df['past price MA'] *100
  close_MA = pd.DataFrame(close_MA)
  close_MA.columns = ['close_price7']
  close_MA = close_MA[close_MA.close_price7 > 20]

  df_01 = pd.merge(volume_MA, close_MA, on='SYMBOL', how='inner')
  df_1 = pd.merge(df_01, link1, on='SYMBOL', how='inner')
  df_1 = df_1[df_1.CLOSE > 50]
  df_1

  st.write("nse 13 days")

  present_url = url1[0:13]
  df2 = pd.DataFrame()
  for k in present_url:
    dff = pd.read_csv(k)
    df2 = df2.append(dff)
  df2 = df2.loc[df2['SERIES'].isin(['EQ','BE'])]
  df2 = df2.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
  p = df2.groupby('SYMBOL')['CLOSE'].mean().rename('Present price MA')
  df_price_present13 = pd.DataFrame(p)

  df2 = df2[(df2['TOTTRDQTY'] > 100000)]
  v = df2.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('present Volume MA')
  df_volume_present13 = pd.DataFrame(v)


  past_url = url1[13:26]
  df3 = pd.DataFrame()
  for k in past_url:
    dff = pd.read_csv(k)
    df3 = df3.append(dff)
  df3 = df3.loc[df3['SERIES'].isin(['EQ','BE'])]
  df3 = df3.drop(columns=["OPEN","HIGH","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
  t = df3.groupby('SYMBOL')['CLOSE'].mean().rename('past price MA')
  df_price_past13 = pd.DataFrame(t)


  df3 = df3[(df3['TOTTRDQTY'] > 100000)]
  s = df3.groupby('SYMBOL')['TOTTRDQTY'].mean().rename('past Volume MA')
  df_volume_past13 = pd.DataFrame(s)


  df13p = pd.merge(df_price_past13,df_price_present13,on = 'SYMBOL')
  df13v = pd.merge(df_volume_present13, df_volume_past13, on = 'SYMBOL')

  volume_ma = (df13v['present Volume MA'] - df13v['past Volume MA']) / df13v['past Volume MA'] *100
  volume_ma = pd.DataFrame(volume_ma)
  volume_ma.columns = ['volume13']
  volume_MA = volume_ma[volume_ma.volume13 > 20]

  close_MA = (df13p['Present price MA'] - df13p['past price MA']) / df13p['past price MA'] *100
  close_MA = pd.DataFrame(close_MA)
  close_MA.columns = ['close_price13']
  close_MA = close_MA[close_MA.close_price13 > 20]

  df_02 = pd.merge(volume_MA, close_MA, on='SYMBOL', how='inner')
  df_2 = pd.merge(df_02, link1, on='SYMBOL', how='inner')
  df_2 = df_2[df_2.CLOSE > 50]
  df_2

  st.write("nse close price")

  m1 = pd.merge(df_1, df_2, on='SYMBOL', how='inner')
  m2 = pd.merge(m1, link1, on='SYMBOL', how='inner')
  merg1 = m2[['CLOSE']]
  merg1[merg1.CLOSE > 50]

@st.experimental_memo()
def bse():
  today = date.today()
  yesterday = today - timedelta(days = 1)
  daten = []
  for i in range(40):
    d = yesterday - timedelta(days=i)
    if d.weekday() < 5:
      s = d.strftime("%d%m%y")
      daten.append(s)
#print(daten)
  url2 = []
  for i in daten:
    url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}{}{}.ZIP".format(i,"_","CSV")
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    r = requests.get(url, headers= hdr)
    if(r.status_code == 200):
       pass
       url2.append(url)

  l2 = url2[0]
  hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
  l2 = pd.read_csv(l2,storage_options=hdr)
  l2 = l2.loc[l2['SC_GROUP'].isin(['X ','XT'])]
  l2 = l2[['SC_NAME','CLOSE']]
  link2 = l2.set_index('SC_NAME')

  st.write("BSE 7 days")

  present_link = url2[0:7]
  df = pd.DataFrame()
  for k in present_link:
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    dff = pd.read_csv(k,storage_options=hdr)
    df = df.append(dff)
  df = df.loc[df['SC_GROUP'].isin(['X ','XT'])]
  df = df.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
  a = df.groupby('SC_NAME')['CLOSE'].mean().rename('present close MA')
  df_price_present7p = pd.DataFrame(a)

  df = df[(df['NO_OF_SHRS'] > 75000)]
  b = df.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('Present volume MA')
  df_volume_present7v = pd.DataFrame(b)



  past_link = url2[7:14]
  df01 = pd.DataFrame()
  for k in past_link:
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    dff = pd.read_csv(k,storage_options=hdr)
    df01 = df01.append(dff)
  df1 = df01.loc[df01['SC_GROUP'].isin(['X ','XT'])]
  df1 = df1.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
  c = df1.groupby('SC_NAME')['CLOSE'].mean().rename('past close MA')
  df_price_past7p = pd.DataFrame(c)

  df1 = df1[(df1['NO_OF_SHRS'] > 75000)]
  d = df1.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('past volume MA')
  df_volume_past7v = pd.DataFrame(d)

  df00 = pd.merge(df_price_present7p,df_price_past7p,on = 'SC_NAME')
  df01 = pd.merge(df_volume_present7v,df_volume_past7v,on = 'SC_NAME')

  volume_MA = (df01['Present volume MA'] - df01['past volume MA']) / df01['past volume MA'] *100
  volume_MA = pd.DataFrame(volume_MA)
  volume_MA.columns = ['volume7']
  volume_MA = volume_MA[volume_MA.volume7 > 20]

  close_MA = (df00['present close MA'] - df00['past close MA']) / df00['past close MA'] *100
  close_MA = pd.DataFrame(close_MA)
  close_MA.columns = ['close_price7']
  close_MA = close_MA[close_MA.close_price7 > 20]

  df_03 = pd.merge(volume_MA, close_MA, on='SC_NAME', how='inner')
  df_3 = pd.merge(df_03, link2, on='SC_NAME', how='inner')
  df_3 = df_3[df_3.CLOSE > 50]
  df_3

  st.write("BSE 13 days")

  present_link = url2[0:13]
  df3 = pd.DataFrame()
  for k in present_link:
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    dff = pd.read_csv(k,storage_options=hdr)
    df3 = df3.append(dff)
  df3 = df3.loc[df3['SC_GROUP'].isin(['X ','XT'])]
  df3 = df3.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
  e = df3.groupby('SC_NAME')['CLOSE'].mean().rename('present close MA')
  df_price_present13p = pd.DataFrame(e)

  df3 = df3[(df3['NO_OF_SHRS'] > 75000)]
  f = df3.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('Present volume MA')
  df_volume_present13v = pd.DataFrame(f)

  past_link = url2[13:26]
  df4 = pd.DataFrame()
  for k in past_link:
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    dff = pd.read_csv(k,storage_options=hdr)
    df4 = df4.append(dff)
  df4 = df4.loc[df4['SC_GROUP'].isin(['X ','XT'])]
  df4 = df4.drop(columns=["SC_CODE","SC_TYPE","OPEN","LAST","PREVCLOSE","HIGH","LOW","NO_TRADES","NET_TURNOV","TDCLOINDI","SC_GROUP"])
  g = df4.groupby('SC_NAME')['CLOSE'].mean().rename('past close MA')
  df_price_past13p = pd.DataFrame(g)

  df4 = df4[(df4['NO_OF_SHRS'] > 75000)]
  h = df4.groupby('SC_NAME')['NO_OF_SHRS'].mean().rename('past volume MA')
  df_volume_past13v = pd.DataFrame(h)

  df02 = pd.merge(df_price_present13p,df_price_past13p,on = 'SC_NAME')
  df03 = pd.merge(df_volume_present13v,df_volume_past13v,on = 'SC_NAME')

  volume_MA = (df03['Present volume MA'] - df03['past volume MA']) / df03['past volume MA'] *100
  volume_MA = pd.DataFrame(volume_MA)
  volume_MA.columns = ['volume13']
  volume_MA = volume_MA[volume_MA.volume13 > 20]

  close_MA = (df02['present close MA'] - df02['past close MA']) / df02['past close MA'] *100
  close_MA = pd.DataFrame(close_MA)
  close_MA.columns = ['close_price13']
  close_MA = close_MA[close_MA.close_price13 > 20]

  df_04 = pd.merge(volume_MA, close_MA, on='SC_NAME', how='inner')
  df_4 = pd.merge(df_04, link2, on='SC_NAME', how='inner')
  df_4 = df_4[df_4.CLOSE > 50]
  df_4

  st.write("bse close price")

  m3 = pd.merge(df_3, df_4, on='SC_NAME', how='inner')
  m4 = pd.merge(m3, link2, on='SC_NAME', how='inner')
  merg2 = m4[['CLOSE']]
  merg2[merg2.CLOSE > 50]
  

@st.experimental_memo()
def williams():
  st.write("WILLIAMS R")
  today = date.today()  #date
  yesterday = today - timedelta(days = 1)
  daten = []
  url1 = []
  for i in range(365):
    d = yesterday - timedelta(days=i)
    if d.weekday() < 5:
      s = d.strftime("%d%b%Y").upper()
      m = d.strftime("%b").upper()
      y = d.strftime("%Y")
      url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}.zip".format(y,m,s,"bhav.csv")
      proxies = { 'http://example.org': 'http://10.10.1.10:3128', 'http://something.test': 'http://10.10.1.10:1080' }
      try:
        r = requests.get(url,timeout=2,proxies = proxies)
        if r.status_code == 200:
          url1.append(url)
      except:
        pass

  link = url1[0:21]
  df = pd.DataFrame()
  for k in link:
    dff = pd.read_csv(k)
    df = df.append(dff)
  df = df.loc[df['SERIES'].isin(['EQ','BE'])]
  #df = df.drop(columns=["OPEN","CLOSE","LOW","LAST","PREVCLOSE","TOTTRDVAL","TOTTRDQTY","TOTALTRADES","ISIN","SERIES","Unnamed: 13"])
  l = df.groupby(["SYMBOL"])["HIGH"].nlargest(1)
  s = df.groupby(["SYMBOL"])["LOW"].nsmallest(1)
  
  l1 = url1[0]
  l1 = pd.read_csv(l1)
  l1 = l1.loc[l1['SERIES'].isin(['EQ','BE'])]
  l1 = l1[['SYMBOL','CLOSE']]
  link1 = l1.set_index('SYMBOL')

  df1 = pd.merge(l,s,on='SYMBOL')
  df2 = pd.merge(df1,link1,on='SYMBOL')
  a = df2['HIGH'] - df2['CLOSE']
  b = df2['HIGH'] - df2['LOW']
  result = -100 * (a / b) 
  result = pd.DataFrame(result)
  final = pd.merge(df2,result,on='SYMBOL')

  def william(row):
    if row[0] > -20 and row[0] <= -0.0 :
      return 'overbought'
    else:
      return 'None'
  final['Check'] = final.apply(william,axis=1)

  final = final.loc[final['Check'].isin(['overbought'])]
  final = final.drop(columns=['Check','LOW'])
  final = final.rename(columns = {'HIGH':'High', 'CLOSE':'Close', 0 : 'Williams%r'})
  final
  

@st.experimental_memo()
def top():
  st.write("TOP 25")
  today = date.today()  #date
  yesterday = today - timedelta(days = 1)
  daten = []
  url1 = []
  for i in range(365):
    d = yesterday - timedelta(days=i)
    if d.weekday() < 5:
      s = d.strftime("%d%b%Y").upper()
      m = d.strftime("%b").upper()
      y = d.strftime("%Y")
      url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/cm{}{}.zip".format(y,m,s,"bhav.csv")
      proxies = { 'http://example.org': 'http://10.10.1.10:3128', 'http://something.test': 'http://10.10.1.10:1080' }
      try:
        r = requests.get(url,timeout=2,proxies = proxies)
        if r.status_code == 200:
          url1.append(url)
      except:
        pass
        
  #present
  l1 = url1[0]
  l1 = pd.read_csv(l1)
  l1 = l1.loc[l1['SERIES'].isin(['EQ','BE'])]
  l1 = l1[['SYMBOL','CLOSE','TOTTRDQTY']]
  link1 = l1.set_index('SYMBOL')
  

  #top25
  df = pd.DataFrame()
  for k in url1:
    dff = pd.read_csv(k)
    df = df.append(dff)
  df = df.loc[df['SERIES'].isin(['EQ','BE'])]
  s = df.groupby(["SYMBOL"])["HIGH"].nlargest(1)
  df = pd.DataFrame(s)
  df1 = link1['CLOSE'] * 1.25
  df2 = pd.merge(df,df1, on = 'SYMBOL', how = 'inner')
  df = pd.merge(link1,df2,on = 'SYMBOL', how = 'inner')

  def selector(row):
    if row['CLOSE_y'] > row['HIGH'] :
      return 'TRUE'
    else:
      return 'FALSE'
  df['check'] = df.apply(selector,axis=1)

  final = df[df['check']== 'TRUE'][['CLOSE_x','HIGH','check']]
  final = final.drop(columns=['check'])
  
  #williams_r
  link = url1[0:21]
  df = pd.DataFrame()
  for k in link:
    dff = pd.read_csv(k)
    df = df.append(dff)
  df = df.loc[df['SERIES'].isin(['EQ','BE'])]
  l = df.groupby(["SYMBOL"])["HIGH"].nlargest(1)
  s = df.groupby(["SYMBOL"])["LOW"].nsmallest(1)

  df1 = pd.merge(l,s,on='SYMBOL')
  df2 = pd.merge(df1,link1,on='SYMBOL')

  a = df2['HIGH'] - df2['CLOSE']
  b = df2['HIGH'] - df2['LOW']
  result = -100 * (a / b) 
  result = pd.DataFrame(result)
  final1 = pd.merge(df2,result,on='SYMBOL')

  def william(row):
    if row[0] > -20 and row[0] <= -0.0 :
      return 'overbought'
    elif  row[0] > -100 and row[0] < -80:
      return 'oversold'
    else:
      return 'None'
  final1['Check'] = final1.apply(william,axis=1)

  final1 = final1.loc[final1['Check'].isin(['overbought'])]
  final1 = final1.drop(columns = 'Check')
  final1 = final1.rename(columns = {'HIGH':'High21', 'CLOSE':'Close','LOW':'Low', 0 : 'williams%r'})

  #intersection
  new = pd.merge(final1,final,on='SYMBOL',how='inner')
  new = new.drop(columns=['High21','Low','CLOSE_x'])
  new = new.rename(columns = {'HIGH':'High', 'TOTTRDQTY':'Volume'})
  new[new.Close > 30]


page = st.sidebar.selectbox('select page',['NSE','BSE','Williams R','Top25'])
if page == 'NSE':
  nse()
elif page == 'BSE':
  bse()
elif page == 'Top25':
  top()
else:
  williams()
