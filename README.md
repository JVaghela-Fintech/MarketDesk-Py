# MarketDesk Socket Connection Library

##This is the marketdesk realtime feed library using web socket in python

It require python version >=2.7

#Update package

py -m pip install --upgrade pip
py -m pip install --upgrade build

#Build package

py -m build

#Install package in other project

pip3 install --upgrade {path to package}\marketdesk-0.0.1.tar.gz

#Connect to the Market desk socket

MarketDeskSocket.connect(host=None, port=None, username=None, password=None, on_message=None, on_error=None, on_close=None)

#Subscribe to feed for particular currency pair

MarketDeskSocket.subscribe(currency_pair)

#Contribution

MarketDeskSocket.contribution(identifier, bids)
bids will be a object array of price and hint

#UnSubscribe to feed for particular currency pair

MarketDeskSocket.unsubscribe(subscription_id, currency_pair)

#Unsubscribe to all feed

MarketDeskSocket.unsubscribe_all()

#Kill the session

MarketDeskSocket.kill_session()
