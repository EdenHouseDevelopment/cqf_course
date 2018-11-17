# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 10:34:39 2018

@author: Admin
"""

import zmq
import datetime
import pandas as pd

context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Creating ZMQ Client")
socket.connect('tcp://127.0.0.1:4242')

instrument = 'AAPL'

socket.setsockopt_string(zmq.SUBSCRIBE, u'')

raw = pd.DataFrame()

SMA1 = 5
SMA2 = 10

min_length = SMA2 + 1

position = 0

while True:
    
    msg = socket.recv_string()
    
    t = datetime.datetime.now()
    
    print(' {} '.format(str(t)) + msg)
    
    symbol, price = msg.split()
    
    raw = raw.append(pd.DataFrame({symbol: float(price)},index=[t]))
    
    data = raw.resample('5s', label='right').last()
    
    if len(data) > min_length:
        min_length += 1
        
        data['SMA1'] = data[symbol].rolling(SMA1).mean()
        data['SMA2'] = data[symbol].rolling(SMA2).mean()
        
        if position in [0,-1]:
            if data['SMA1'].iloc[-2] > data['SMA2'].iloc[-2]: # this is because the last number might actually not be the right one
                print(55 * '=')
                print("Buy order ...")
                print(55 * '=')
                position = 1
                print(data.tail())
                ### this is where you place your trade
        elif position in [0,1]:
             if data['SMA1'].iloc[2] < data['SMA2'].iloc[-2]:
                print(55 * '=')
                print("Sell order ...")
                print(55 * '=')
                position = -1
                print(data.tail())
                ### this is where you put your trade code
        



#this means you've overwritten the on_success method of tpqoa such that rather
#capture the time, bid, ask as original, you can get it to do anything you're
#after doing 9 ie, trigger your 'do I want to trade' algo
        #it wont really work in this bit tho coz this is 0MQ rather than Oanda
        




        