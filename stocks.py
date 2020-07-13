import yahoo_fin.stock_info as yf
import numpy as np
import datetime


# class requires the stock ticker as a parameter, for example 'MSFT' for microsoft
# allows for functionality including getting the current price, cashflow, etc.
class Stock:

    def __init__(self, stock):
        self.stock = stock

    def getPrice(self):
        return yf.get_live_price(self.stock)

    def getEarnings(self):
        return yf.get_earnings(self.stock)

    # requires boolean parameter, set yearly=False for quarterly data
    def getCashFlow(self, yearly):
        return yf.get_cash_flow(self.stock, yearly)

    # returns the income statement, balancesheet, and cashflow. requires boolean parameters for yearly or quarterly data
    def getFinancials(self, yearly, quarterly):
        return yf.get_financials(self.stock, yearly, quarterly)

    # returns stats on the stock, including the moving average, return on equity, etc.
    def getStats(self):
        return yf.get_stats(self.stock)

    def getData(self, start_date, end_date):
        return yf.get_data(self.stock, start_date=start_date, end_date=end_date)

    def getRSI(self, n = 14):
        # this method will return the current RSI of the stock
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=n)
        # makes a list of the closing price of the stock each day for the last n days (default 2 weeks)
        prices = self.getData(start_date, end_date)['close'].values.tolist()
        deltas = np.diff(prices)
        seed = deltas[: n + 1]
        up = seed[seed >= 0].sum() / n
        down = -seed[seed < 0].sum() / n
        rs = up / down
        rsi = np.zeros_like(prices)
        rsi[:n] = 100. - 100. / (1. + rs)
        for i in range(n, len(prices)):
            delta = deltas[i - 1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            up = (up * (n - 1) + upval) / n
            down = (down * (n - 1) + downval) / n
            rs = up / down
            rsi[i] = 100. - 100. / (1. + rs)
        return rsi

    def getMACD(self):
        # this method will return the current MACD of the stock
        pass


# example for using the above class
if __name__ == '__main__':
    microsoft = Stock('MSFT')
    print('price:', microsoft.getPrice())
    print('rsi:', microsoft.getRSI())