# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 13:52:55 2025

@author: bagew

"""
import yfinance as yf
import datetime as dt
import pandas as pd
import  matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

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

df=pd.read_csv(csv_filename)
print(df)

#extract close column
#df2=df.reset_index()['Close']
close_prices=df['Close']
# convert to float
close_prices=pd.to_numeric(close_prices,errors='coerce')
print(close_prices)

plt.figure(figsize=(10, 5))
plt.plot(close_prices, label='Closing Price')
plt.title(f'{stock_symbol} Closing Price from {start_date} to {end_date}')
plt.xlabel('Days')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

#transform and scale the values(from 0 to 1)
scaler=MinMaxScaler(feature_range=(0,1))#scale down from 0to1
df3=scaler.fit_transform(np.array(close_prices).reshape(-1,1))
print(df3)

#split data into train and test
train_size=int(len(df3)*0.65) #65%
test_size=len(df3)-train_size #35%
train_data,test_data=df3[0:train_size,:],df3[train_size:len(df3),:1]
print(f"size of training data:{np.size(train_data)}")
print(f"size of test data:{np.size(test_data)}")

#timesteps how many days to consider to get next day output 
#dataset = 120,130,125,140,134,150   160,190,154
#x_train(independent) y_train(dependent)  
#f1=120 f2=130 f3=125 o/p=140
#f2=130 f3=125 f4=140 o/p=134
#test data should be processed in same way training dataset

#convert an arr of val to dataset matrix
def createDataset(dataset,time_step=1):
    dataX,dataY=[],[]
    for i in range(len(dataset)-time_step-1):
        a=dataset[i:(i+time_step),0] # i=0 0,1,2,3---99 100
        dataX.append(a)
        dataY.append(dataset[i+time_step,0])
    return np.array(dataX),np.array(dataY)

time_step=3
x_train,y_train=createDataset(train_data,time_step)
x_test,y_test=createDataset(test_data,time_step)

print(f"x_train.shape={x_train.shape}")
print(f"y_train.shape={y_train.shape}")
print(f"x_test.shape={x_test.shape}")
print(f"y_test.shape={y_test.shape}")

#reshape input into 3d [samples,time steps,features] which is required for lstm

#preprocess the Data- train and test
#create a stacked lstm model
#predict the test data and plot the output
#predict the future 30 days and plot the output
