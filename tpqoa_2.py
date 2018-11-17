# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:55:46 2018

@author: Admin
"""

import numpy as np
import pandas as pd
from pylab import plt
plt.style.use('seaborn')

import tpqoa

api = tpqoa.tpqoa('oanda.cfg')

instrument = 'EUR_USD'
data = api.get_history(instrument, '2016-01-01', '2018-11-01', 'D', 'A')

## streaming data

api.stream_data(instrument, stop=25)