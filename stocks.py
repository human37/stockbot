import yahoo_fin.stock_info as yf
from pandas import DataFrame 
from stockstats import StockDataFrame
from warnings import catch_warnings, simplefilter
import numpy as np
from datetime import datetime, timedelta


# class requires the stock ticker as a parameter, for example 'MSFT' for microsoft
# allows for functionality including getting the current price, cashflow, etc.
class Stock:

    def __init__(self, stock):
        self.stock = stock

    def getPrice(self):
        return yf.get_live_price(self.stock)

    def getEarnings(self):
        return yf.get_earnings(self.stock)

    # set yearly=False for quarterly data
    def getCashFlow(self, yearly):
        return yf.get_cash_flow(self.stock, yearly)

    # returns the income statement, balancesheet, and cashflow. requires boolean parameters for yearly or quarterly data
    def getFinancials(self, yearly, quarterly):
        return yf.get_financials(self.stock, yearly, quarterly)

    # returns all daily price information about the stock
    def getData(self, start_date, end_date):
        return yf.get_data(self.stock, start_date=start_date, end_date=end_date)

    # set rsi_12 to false for rsi 6 day calculation, defaults to 12 day calculation
    def getRSI(self, n = 200, rsi_12 = True):
        # returns the current rsi indicator of the stock (uses the past 200 business days for calculation)
        with catch_warnings():
            # suppresses default warning from pandas
            simplefilter('ignore')
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days = n)
            stock_data = self.getData(start_date, end_date)
            if rsi_12:
                rsi = StockDataFrame(stock_data).get('rsi_12')[-1]
            else:
                rsi = StockDataFrame(stock_data).get('rsi_6')[-1]
        return rsi

    def getMACD(self, n = 200):
        # returns the current macd indicator of the stock (uses the past 200 business days for calculation)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days = n)
        stock_data = self.getData(start_date, end_date)
        macd = StockDataFrame(stock_data).get('macd')[-1]
        return macd


# example for using the above class
if __name__ == '__main__':
    microsoft = Stock('MSFT')
    print('price:', microsoft.getPrice())
    print('rsi:', microsoft.getRSI())
    print('macd:', microsoft.getMACD())