from stocks import Stock, StockManager, User
from time import sleep
from datetime import datetime


if __name__ == '__main__':
    
    tesla = Stock('TSLA')
    microsoft = Stock('MSFT')

    ammons_stocks = StockManager([tesla, microsoft])

    ammon = User(ammons_stocks, 'ammonx9@gmail.com')

    while True:

        print('Running...')
        rsi_changes = ammon.getStockManager().checkRSI()
        macd_changes = ammon.getStockManager().checkMACD()
        email_message = 'Subject: StockBot Update ' + str(datetime.now()) + ': \n'
        updates = False

        if len(rsi_changes) != 0:
            for change in rsi_changes:
                stock = change['stock']
                value = change['status']
                message = stock.getName() + ' is now ' + value + '!\n'
                price = stock.getName() + ' price is currently $' + str(round(stock.getPrice(), 2)) + '\n'
                email_message += message
                email_message += price
            updates = True
                
        if len(macd_changes) != 0:
            for change in macd_changes:
                stock = change['stock']
                value = change['status']
                message = stock.getName() + ' is now ' + value + ' momentum!\n'
                price = stock.getName() + ' price is currently $' + str(round(stock.getPrice(), 2)) + '\n'
                email_message += message
                email_message += price
            updates = True

        if updates:
            print('New message information!')
            print('Sending email...')
            ammon.sendEmail(email_message)
            print('Email sent successfully.')
        else:
            print('No message to send at this moment.')
        print('Going to sleep now.')
        sleep(60)