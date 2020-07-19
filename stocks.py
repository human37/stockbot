from yahoo_fin import stock_info as yf
from stockstats import StockDataFrame
from warnings import catch_warnings, simplefilter
from datetime import datetime, timedelta
from smtplib import SMTP_SSL
from ssl import create_default_context


# class requires the stock ticker as a parameter, for example 'MSFT' for microsoft
# allows for functionality including getting the current price, cashflow, etc.
class Stock:

    def __init__(self, stock):
        self.stock = stock
        self.undervalued = False
        self.overvalued = False
        self.loosing_momentum = False
        self.gaining_momentum = False

    def setUndervalued(self):
        if self.undervalued == False:
            self.undervalued = True
            return True
        return False

    def setOvervalued(self):
        if self.overvalued == False:
            self.overvalued = True
            return True
        return False

    def resetValue(self):
        self.undervalued = False
        self.overvalued = False

    def setLoosingMomentum(self):
        if self.loosing_momentum == False:
            self.loosing_momentum = True
            self.gaining_momentum = False
            return True
        return False

    def setGainingMomentum(self):
        if self.gaining_momentum == False:
            self.gaining_momentum = True
            self.loosing_momentum = False
            return True
        return False

    def resetMomentum(self):
        self.loosing_momentum = False
        self.gaining_momentum = False

    def getName(self):
        return self.stock

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
        return yf.get_data(self.stock, start_date = start_date, end_date = end_date)

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

    def getSignal(self, n = 200):
        # returns the current macd indicator of the stock (uses the past 200 business days for calculation)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days = n)
        stock_data = self.getData(start_date, end_date)
        macd = StockDataFrame(stock_data).get('macds')[-1]
        return macd

# manages a list of stock objects, sets their respective data members 
class StockManager:

    def __init__(self, stocks):
        self.stocks_list = stocks

    def checkRSI(self):
        stock_changes = []
        for stock in self.stocks_list:
            rsi = float(stock.getRSI())
            if rsi <= 30:
                if stock.setUndervalued():
                    stock_changes.append({'stock' : stock, 'status' : 'undervalued'})
            elif rsi >= 70:
                if stock.setOvervalued():
                    stock_changes.append({'stock' : stock, 'status' : 'overvalued'})
            else:
                stock.undervalued = False
                stock.undervalued = False
        return stock_changes

    def checkMACD(self):
        stock_changes = []
        for stock in self.stocks_list:
            macd = float(stock.getMACD())
            signal = float(stock.getSignal())
            if macd >= signal:
                if stock.setGainingMomentum():
                    stock_changes.append({'stock' : stock, 'status' : 'gaining'})
            else:
                if stock.setLoosingMomentum():
                    stock_changes.append({'stock' : stock, 'status' : 'loosing'})
        return stock_changes
        
class User:

    def __init__(self, stock_manager, email_address):
        self.manager = stock_manager
        self.email = email_address
    
    def sendEmail(self, message):
        # reads in the password for my dev account
        with open('/Users/ammontaylor/logins/passwords.txt', 'r') as f:
            for line in f:
                password = line.strip()
        with SMTP_SSL('smtp.gmail.com', 465, context = create_default_context()) as server:
            server.login('dev.acc3025934@gmail.com', password)
            server.sendmail('dev.acc3025934@gmail.com', self.email, message)
    
    def checkStocks(self):
        # checks the indicators on all the stocks in the stockmanager object, and sends an email if any of them have changed
        print('Running...')
        rsi_changes = self.manager.checkRSI()
        macd_changes = self.manager.checkMACD()
        email_message = 'Subject: StockBot Update ' + str(datetime.now().time()) + ': \n'
        updates = False
        if len(rsi_changes) != 0:
            for change in rsi_changes:
                stock = change['stock']
                value = change['status']
                message = stock.getName() + ' is now ' + value + '!'
                price = ' (price $' + str(round(stock.getPrice(), 2)) + ')\n'
                email_message += message 
                email_message += price
            updates = True
        if len(macd_changes) != 0:
            for change in macd_changes:
                stock = change['stock']
                value = change['status']
                message = stock.getName() + ' is now ' + value + ' momentum!'
                price = ' (price $' + str(round(stock.getPrice(), 2)) + ')\n'
                email_message += message
                email_message += price
            updates = True
        if updates:
            print('New message information!')
            print('Sending email...')
            self.sendEmail(email_message)
            print('Email sent successfully.')
        else:
            print('No message to send at this moment.')