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
            Stock('BABA')
        ]
    )
    ammon = User(ammons_stocks, 'ammonx9@gmail.com')

    while True:
        # checks all stocks in StockManager, cycles every minute
        ammon.checkStocks()
        sleep(60)
