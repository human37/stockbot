import yahoo_fin.stock_info as yf


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

    def getRSI(self):
        # this method will return the current RSI of the stock
        pass

    def getMACD(self):
        # this method will return the current MACD of the stock
        pass
