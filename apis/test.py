import yfinance as yf
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
import pandas as pd
import numpy as np
import os

import warnings
warnings.filterwarnings("ignore")

def get_stock_data(userInput):
    return yf.download(
        userInput,
        start = '2000-01-01',
        end = f'{date.today()}',
        progress = False
    )
    
def showStockNames():
    print(os.getcwd()) 
    path = os.path.join(os.getcwd(), 'apis\Data\stockNames.csv')
    print(path)
    return pd.read_csv(
        path, 
        index_col = 0, 
        usecols= ['Symbol', 'Name']
        )

def data_preprocess(forecastDays, userInput):
    if forecastDays < 0:
        return {'error': 'CHECK NUMBER INPUT'}
    else:
        stock_df = showStockNames()
        if userInput not in stock_df.index:
            return {'error':'Not a valid stock'}
        else:
            stock_info = get_stock_data(userInput)
            stock_prediction = stock_info[['Adj Close']]
            stock_prediction['Stock Price'] = stock_prediction.loc[:, 'Adj Close'].shift(-forecastDays)
            return stock_prediction

def data_prep(forecastDays, userInput):
    if forecastDays < 0 or forecastDays == 0:
        return {'error': 'CHECK NUMBER INPUT'}
    else:
        stock_df = showStockNames()
        if userInput not in stock_df.index:
            return {'error':'Not a valid stock'}
        else:
            stock = data_preprocess(forecastDays, userInput)
            X_DATA = np.array(stock.drop('Stock Price',axis=1))
            X_DATA = X_DATA[:-forecastDays]
            Y_DATA = np.array(stock['Stock Price'])
            Y_DATA = Y_DATA[:-forecastDays]
            x_train, x_test, y_train, y_test = train_test_split(X_DATA, Y_DATA, test_size = 0.2)
            return x_train, x_test, y_train, y_test


def svm_model(forecastDays, userInput):
    if forecastDays < 0 or forecastDays == 0:
        return {'error': 'CHECK NUMBER INPUT'}
    else:
        stock_df = showStockNames()
        if userInput not in stock_df.index:
            return {'error':'Not a valid stock'}
        else:
            stock = data_preprocess(forecastDays, userInput)
            x_train, x_test, y_train, y_test = data_prep(forecastDays, userInput)
            svr_clf = SVR(kernel='rbf', C = 1000.0, gamma = 0.0001)
            svr_clf_fit = svr_clf.fit(x_train, y_train)
            stock_price_pred = np.array(stock.drop(['Stock Price'], axis=1))[forecastDays:]
            svr_clf_pred = svr_clf_fit.predict(stock_price_pred)
            return {'result': svr_clf_pred[:forecastDays]}
