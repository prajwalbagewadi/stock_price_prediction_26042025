# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 19:49:22 2025

@author: bagew

Stock Market Prediction and Forecasting Using Stacked LSTM
"""
"""
Keras and Tensorflow->2.0
"""
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
import requests as req
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
from io import StringIO

#df = pdr.get_data_tiingo("stock_name","api_key")
#startDate=dt.datetime(2024,1,1)
#endDate=dt.datetime(2024,12,31)
#df = pdr.get_data_yahoo('AAPL',start=startDate,end=endDate)
#print(f"df-head:\n {df.head}")

def date_to_unix(date_str):
    
    print(f"inputDate-{date_str}")
    
    dte = dt.datetime.strptime(date_str, "%Y-%m-%d")
    data = int(time.mktime(dte.timetuple()))
    
    print(f"Date-{data}")
    return data


def get_cookie_crumb_selenium(ticker):
    
    service = Service(executable_path=r"C:\Users\bagew\Downloads\Testing\chromedriver_win32\chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    url = f"https://finance.yahoo.com/quote/{ticker}/history"
    driver.get(url)
    time.sleep(5)#wait for javascript to load
    
    page_source = driver.page_source
    
    #Extract crumb
    pattern = re.compile(r'"CrumbStore":\{"crumb":"(.*?)"\}')
    match = pattern.search(page_source)
    if not match:
        driver.quit()
        raise Exception("Crumb not found in page source")
        
    crumb = match.group(1)
    cookie = driver.get_cookie()
    
    driver.quit()
    print(f"Crumb: {crumb}")
    print(f"Cookie: {cookie}")
    
"""
def fetchYahooStockData(stock_name,start,end):
    
    start_unix = date_to_unix(start)
    end_unix = date_to_unix(end)
    
    # https://finance.yahoo.com/quote/ITC.NS/
    
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock_name}?period1={start_unix}&period2={end_unix}&interval=1d&events=history&includeAdjustedClose=true"
    #url = f"https://finance.yahoo.com/quote/{stock_name}/history/?period1={start_unix}&period2={end_unix}"

    headers = {
        "User-Agent":"Mozilla/5.0"    
    }
    
    response = req.get(url=url,headers=headers,timeout=10)
    response.raise_for_status()
    
    if response.status_code == 200:
        #df = pd.read_csv(pd.compat.StringIO(response.text))
        df = pd.read_csv(StringIO(response.text))
        #print(f"df-head:\n{df.head()}")
        print("Response content:")
        print(response.text[:500])  # Print first 500 chars to check

        return df
    else:
        print(f"Failed to fetch data:{response.status_code}")
        return None
"""
if __name__ == '__main__':
    #date_to_unix("2024-01-01")
    data = get_cookie_crumb_selenium('AAPL')
    #print(data)
    #df = fetchYahooStockData('AAPL', "2024-01-01", "2024-12-31")
    #print(f"df_head:\n{df.head()}")
    
"""
import requests
import re
import pandas as pd
import datetime as dt
import time
from io import StringIO

def date_to_unix(date_str):
    dte = dt.datetime.strptime(date_str, "%Y-%m-%d")
    return int(time.mktime(dte.timetuple()))

def get_cookie_and_crumb(stock_name):
    session = requests.Session()
    url = f"https://finance.yahoo.com/quote/{stock_name}/history"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to get Yahoo Finance page")

    # Extract crumb
    pattern = re.compile(r'"CrumbStore":\{"crumb":"(.*?)"\}')
    match = pattern.search(response.text)
    if not match:
        raise Exception("Crumb not found")
    
    crumb = match.group(1)
    cookie = session.cookies.get_dict()
    return session, crumb

def fetch_yahoo_stock_data(stock_name, start, end):
    session, crumb = get_cookie_and_crumb(stock_name)
    start_unix = date_to_unix(start)
    end_unix = date_to_unix(end)
    
    download_url = f"https://query1.finance.yahoo.com/v7/finance/download/{stock_name}?period1={start_unix}&period2={end_unix}&interval=1d&events=history&includeAdjustedClose=true&crumb={crumb}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = session.get(download_url, headers=headers)
    response.raise_for_status()
    
    # Now read the CSV data
    df = pd.read_csv(StringIO(response.text))
    return df

if __name__ == "__main__":
    df = fetch_yahoo_stock_data('AAPL', '2024-01-01', '2024-12-31')
    print(df.head())
"""
   
