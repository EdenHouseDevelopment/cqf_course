# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""l
import numpy as np
import pandas as pd
from pylab import plt
plt.style.use('seaborn')

import tpqoa

api = tpqoa.tpqoa('oanda.cfg')

#api.get_instruments()[:5]

instrument = 'EUR_USD'
data = api.get_history(instrument, '2016-01-01', '2018-11-01', 'D', 'A')

#data.info()

data['c'].plot(figsize=(15,10))

data = api.get_history(instrument, '2018-10-20', '2018-11-01', 'M10', 'A')

#data.info()

data = api.get_history(instrument, '2018-11-14', '2018-11-15', 'S5', 'A')

#data.info()

data['c'].plot(figsize=(15,10))

from sklearn.neural_network import MLPClassifier

data = api.get_history(instrument, '2018-10-01', '2018-11-15', 'M5', 'A')

#data.info()

data = pd.DataFrame(data['c'])
data.columns = [instrument]

#data.info()

data['r'] = np.log(data / data.shift(1))

data.dropna(inplace=True)

lags = 5

cols = []
for lag in range(1, lags + 1):
    col = 'lag_{}'.format(lag)
    data[col] = data['r'].shift(1)
    cols.append(col)
    
data.dropna(inplace=True)

data[cols] = np.where(data[cols] > 0, 1, 0)

model = MLPClassifier(hidden_layer_sizes=[100, 100], max_iter=500)

model.fit(data[cols], np.sign(data['r']))

data['p'] = model.predict(data[cols])

data['s'] = data['p'] * data['r']

data[['r', 's']].cumsum().apply(np.exp).plot(figsize=(15,10))
