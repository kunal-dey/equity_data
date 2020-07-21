import pandas as pd
from bs4 import BeautifulSoup
import requests
import datetime as dt
import re

def equity_data(symbol, beg_date, end_date, exchange, interval):
  if exchange == 'NSE':
    symbol = symbol + ".NS"
  elif exchange == 'BSE':
    symbol = symbol + ".BO"
  anchor_date = dt.date(2020,7,21)
  anchor_index = 1595289600
  beg_index = anchor_index - (anchor_date - beg_date).days * 86400
  end_index = anchor_index + (end_date - anchor_date).days * 86400
  link = r'https://query1.finance.yahoo.com/v7/finance/download/' + symbol + r'?period1=' + str(beg_index) + '&period2=' + str(end_index) + '&interval=1' +interval +'&events=history'
  r = requests.get(link)
  data = str(BeautifulSoup(r.text,'html.parser'))
  non_excel = re.split('\n', data)
  column_name = re.split(',', non_excel[0])
  d = {}
  for i in range(len(non_excel)):
    if i < 1:
      for column in column_name:
        d[column] = []
    else:
      arr = re.split(',', non_excel[i])
      if arr[2] != 'null':
        for element in range(len(arr)):
          if element > 0:
            d[column_name[element]].append(float(arr[element]))
          else:
            din = re.split('-',arr[element])
            d[column_name[element]].append(dt.date(int(din[0]),int(din[1]),int(din[2])))
  return pd.DataFrame(d, index= d[column_name[0]])

