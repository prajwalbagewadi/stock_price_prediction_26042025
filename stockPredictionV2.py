# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 13:52:55 2025

@author: bagew

"""
import yfinance as yf
import datetime as dt


#data collection
# define stock_symbol and date range
stock_symbol='AAPL'
start_date='2024-01-01'
end_date='2024-12-31'

# download stock data
df=yf.download(stock_symbol,start=start_date,end=end_date)

#test
print(f"dataframe:\n{df.head()}")

#save to csv file
csv_filename=f"{stock_symbol}_{start_date}_to_{end_date}.csv"
df.to_csv(csv_filename)

