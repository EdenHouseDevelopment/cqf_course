# -*- coding: utf-8 -*-
import numpy
import tpqoa

instrument = 'EUR_USD'

class SMATrader(tpqoa.tpqoa):
    def __init_(self,config_file, SMA1, SMA2, bar_length, units):
        super(SMATrader, self).__init__(config_file)
        self.raw = pd.DataFrame()
        
        self.sma1 = SMA1
        self.sma2 = SMA2
        self.min_length = SMA2 + 1
        self.bar_length = bar_length
        self.position = 0
        
    def on_success(self,time,bid,ask,bar_length, ticks):
        print(self.ticks, end = ' ')
        self.raw = self.raw.append(pd.DataFrame({'bid':bid, 'ask':ask},index=[pd.Timestamp(time)]))
        self.data = self.raw.resample(self.bar_length, label='right').last() 
        self.data['mid'] = self.data.mean(axis=1)
        
        if len(self.data) > self.min_length:
            if self.position in [0,-1]:
                self.min_length += 1
                self.data['SMA1'] = self.data['mid'].rolling(self.SMA1).mean()
                self.data['SMA2'] = self.data['mid'].rolling(self.SMA2).mean()

                if self.data['SMA1'].iloc[-2] > self.data['SMA2'].iloc[-2]: # this is because the last number might actually not be the right one
                    print(55 * '=')
                    print("Buy order ...")
                    print(55 * '=')
                    self.create_order(self.stream_instrument, units = ( 1 - self.position )*self.units)
                    self.position = 1
                    ### this is where you place your trade
                    api.create_order(instrument, units=50)
            elif self.position in [0,1]:
                 if self.data['SMA1'].iloc[2] < self.data['SMA2'].iloc[-2]:
                    print(55 * '=')
                    print("Sell order ...")
                    print(55 * '=')
                    self.create_order(self.stream_instrument, units = -( 1 + self.position )*self.units)
                    self.position = -1        
            
        
sma = SMATrader('oanda.cfg',5, 10, '5s', 200)
sma.stream_data(instrument, stop=150)
sma.print_transactions(tid=0)
sma.get_transactions(tid=0)