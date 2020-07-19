from stocks import Stock, StockManager, User
from time import sleep


if __name__ == '__main__':

    ammons_stocks = StockManager(
        [
            Stock('TSLA'),
            Stock('TWTR'),
            Stock('F'),
            Stock('AAPL'),
            Stock('ACB'),
            Stock('SNAP'),
            Stock('SPOT')
        ]
    )
    tanners_stocks = StockManager(
        [
            Stock('TSLA'),
            Stock('XSPA'),
            Stock('AMD'),
            Stock('AAPL'),
            Stock('SPOT')
        ]
    )
    ammon = User(ammons_stocks, 'ammonx9@gmail.com')
    tanner = User(tanners_stocks, 'tannernthorne@gmail.com')

    while True:
        # checks all stocks in StockManager, cycles every minute
        ammon.checkStocks()
        tanner.checkStocks()
        sleep(600)
