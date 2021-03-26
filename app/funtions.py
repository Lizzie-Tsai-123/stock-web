# -*- coding: UTF-8 -*-
import requests
import time
import numpy as np
import pandas as pd
import json
from datetime import datetime
import time # 引入time
import talib
import pandas as pd
import mplfinance as mpf
#inputs = np.array([['120','2330.TW']])
#print(inputs[0])
def pullData(inputs):
    d = int(inputs[0][0])
    stock = inputs[0][1]
    try:
        nowTime = int(time.time()) # 取得現在時間
        struct_time = time.localtime(nowTime) # 轉換成時間元組

        time_stamp = int(time.mktime(struct_time)) # 轉成時間戳
        print("time_stamp: ",time_stamp)
        present_time = time_stamp
        print("present_time: ", present_time)
        past2m = present_time - (d*24*60*60)
        print("past_two_month: ", past2m)
        m = int(d/30)


        site = 'https://query1.finance.yahoo.com/v8/finance/chart/'+stock+'?period1='+str(past2m)+'&period2='+str(present_time)+'&interval=1d&events=history&=hP2rOschxO0'
        response = requests.get(site)
        data = json.loads(response.text)

        df = pd.DataFrame(data['chart']['result'][0]['indicators']['quote'][0])
        df['date'] = pd.DataFrame(pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'],dtype='int64')*1000*1000*1000).strftime("%Y-%m-%d"))
        #df1 = pd.DataFrame(pd.to_datetime(np.array(data['chart']['result'][0]['timestamp'],dtype='int64')*1000*1000*1000).strftime("%Y-%m-%d"))
        #df2 = pd.DataFrame(data['chart']['result'][0]['timestamp'])
        #joined_df = df1.join(df)
        #joined_df['otime'] = df2
        df['MA5'] = talib.MA(df['close'], timeperiod=5)
        df['MA10'] = talib.MA(df['close'], timeperiod=10)
        print(df.head())
        #print(df1.head())
        #print(joined_df.head())
        df.close.plot()

        df.to_csv('C://Users//FJUSER200921H//Desktop//stock_web//web_design//'+stock+str(m)+'m.csv', mode='a')


    except Exception as e:
        print('main loop ', str(e))

#pullData(inputs)

def drawGraph(inputs):
    d = int(inputs[0][0])
    stock = inputs[0][1]
    file = stock+str(int(d/30))+'m.csv'
    data = pd.read_csv(file)
    data.date = pd.to_datetime(data.date)
    data = data.set_index('date')
    save = dict(fname='picture.jpg',dpi=100,pad_inches=0.25)
    mpf.plot(data,figratio=(20,12), type='candle', title = stock, mav=(10,5), volume=True, tight_layout=True,style='yahoo',savefig=save)
    return '..//picture.jpg'
#drawGraph(inputs)

def drawGraph_s(inputs):
    d = int(inputs[0][0])
    stock = inputs[0][1]
    file = stock+str(int(d/30))+'m.csv'
    data = pd.read_csv(file)
    data.date = pd.to_datetime(data.date)
    data = data.set_index('date')
    signal = []
    for i in range(len(data)):
        if i != 0:
            if data.MA5[i] >= data.MA10[i] and data.MA5[i-1] < data.MA10[i-1]:
                signal.append(data.close[i]*0.98)
            else:
                signal.append(np.nan)
        else:
            signal.append(np.nan)
    data['signal'] = signal
    apd = mpf.make_addplot(signal,type='scatter',markersize=200,marker='^')
    save = dict(fname='picture_s.jpg',dpi=100,pad_inches=0.25)
    mpf.plot(data,figratio=(20,12), type='candle', title = stock, mav=(10,5), volume=True, tight_layout=True,style='yahoo', addplot=apd,savefig=save)

    print(data.head())
    return '..//picture_s.jpg'

#drawGraph_s(inputs)
