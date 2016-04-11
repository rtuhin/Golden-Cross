# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:09:39 2016

@author: tuhrak
"""


import numpy as np
import pandas as pd
import pandas.io.data as web
from dateutil.relativedelta import relativedelta
#import matplotlib as plt

from datetime import datetime
 
def rand_date(duration_years):
    year = np.random.randint(1950, 2015)
    month = np.random.randint(1, 12)
    day = np.random.randint(3, 28)
    dt = datetime(year, month, day)
    #print dt.strftime('%Y-%m-%d')
    dt1 = datetime(2015, 12, 30)

    if (dt < dt1 - relativedelta(years=duration_years)):
        dt = dt - relativedelta(years=duration_years)
    
    #print dt.strftime('%m-%d-%Y')
    return dt
#######################################################
#
#  Main program
#
#######################################################

if __name__ == "__main__":
    
    duration_years = 5
    st = 50
    lt = 200
    sd = 15
    N = 5000
    count = 0
    dfList = []

    print N
    for i in xrange(N):
        start_date = rand_date(duration_years)
        #print start_date.strftime('%m-%d-%Y')
        end_date = start_date + relativedelta(years=duration_years)
        #print start_date.strftime('%m-%d-%Y'),  end_date.strftime('%m-%d-%Y')
        figName = start_date.strftime('%m-%d-%Y') + '_' + end_date.strftime('%m-%d-%Y') + '.png'
    
        sp500 = web.DataReader('^GSPC', data_source='yahoo',start=start_date, end=end_date)
        #print sp500.info()
    #
        #ax = sp500['Close'].plot(grid=True, figsize=(8, 5))

        
        
    #
        sp500['st'] = np.round(pd.rolling_mean(sp500['Close'], window=st), 2)
        sp500['lt'] = np.round(pd.rolling_mean(sp500['Close'], window=lt), 2)
        
        #print sp500.info()
        #
        #sp500[['Close', 'st', 'lt']].plot(grid=True, figsize=(8, 5))
        sp500['st-lt'] =  sp500['st'] - sp500['lt']
        sp500['Regime'] = np.where(sp500['st-lt'] > sd, 1, 0)
        sp500['Regime'] = np.where(sp500['st-lt'] < -sd, -1, sp500['Regime'])
        #print sp500['Regime'].value_counts()
        #
        #sp500['Regime'].plot(lw=1.5)
        sp500['Market'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
        sp500['Strategy'] = sp500['Regime'].shift(1) * sp500['Market']
        cumRet = sp500[['Market', 'Strategy']].cumsum().apply(np.exp)
        
        dfList.append([start_date.strftime('%m-%d-%Y'),  
                end_date.strftime('%m-%d-%Y'), 
                cumRet['Strategy'][-1] - cumRet['Market'][-1]])             
                                        
        if ((cumRet['Strategy'][-1] - cumRet['Market'][-1]) > 0):
            count += 1
            ax = cumRet.plot(grid=True, figsize=(8, 5))
            fig = ax.get_figure()
        #print cumRet[-1]
            fig.savefig(figName)
        #market_returns = sp500['Market'].cumsum().apply(np.exp)
        #strat_returns = sp500['Strategy'].cumsum().apply(np.exp)
        #print 'Market returns:', market_returns
        
        
        # determine the first golden cross date
    outDf = pd.DataFrame(dfList, columns=['Start Date', 'End Date', 'Abnormal Return'])
    #print outDf
    #writer = ExcelWriter('result.xlsx')
    writer = pd.ExcelWriter('result.xls')
    outDf.to_excel(writer, sheet_name='Sheet1')
    writer.save()
print float(count)/float(N)
print 'Done!'