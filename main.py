from stocks import Stock, StockManager, User
from time import sleep


if __name__ == '__main__':

    tesla = Stock('TSLA')
    microsoft = Stock('MSFT')
    ammons_stocks = StockManager([tesla, microsoft])
    ammon = User(ammons_stocks, 'ammonx9@gmail.com')

    while True:
        # checks all stocks in StockManager, cycles every minute
        ammon.checkStocks()
        time.sleep(60)