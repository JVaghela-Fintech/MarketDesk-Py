import websocket
from base64 import b64encode
import os
import json
import random
import string


class MarketDeskSocket():

    def __init__(self, host=None, port=None, username=None, password=None, on_message=None, on_error=None, on_close=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.web_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(8)) + '.'
        self.subscription_id = 0
        self.is_logged_in = False
        self.on_message = on_message
        self.on_error = on_error
        self.on_close = on_close
        

    def __get_headers(self):
        origin = "http://" + self.host + ":" + self.port
        return [
            'Host: %s:%s' % (self.host, self.port),
            'Connection: Upgrade',
            'Upgrade: websocket',
            'Origin: %s' % (origin),
            'Sec-WebSocket-Key: ' + b64encode(os.urandom(16)).decode('utf-8'),
            'Sec-WebSocket-Version: 13',
            'Sec-WebSocket-Protocol: bsws-protocol'
        ]

    
    def __on_open(self, ws):
        print("on connection open")
        loginMessageStructure = {"L": {"S": self.username, "P": self.password}}
        ws.send(json.dumps(loginMessageStructure, indent=2).encode('utf-8'))
    
    
    def __on_error(self, ws, error):
        print("Error", error)
        self._callback(self.on_error, error)


    def __on_close(self, ws, close_status_code, close_msg):
        print("### closed ###", close_status_code, close_msg)
        self._callback(self.on_close, close_status_code, close_msg)
        
    
    def __on_message(self, ws, message):
        print(message.decode('utf-8'))
        decoded_message = message.decode('utf-8')
        decoded_message = json.loads(decoded_message)
        if("L" in decoded_message.keys()):
            self.is_logged_in = True
        elif("R" in decoded_message.keys()):
            print("Got subscription message", decoded_message)
        elif("C" in decoded_message.keys()):
            print("Got contribution response", decoded_message)
        # else:
        #     print(decoded_message)
        self._callback(self.on_message, decoded_message)
            
    
    def connect(self):
        headers = self.__get_headers()
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://" + self.host + ":" + self.port + "/",
                                    header=headers,
                                    on_open=self.__on_open,
                                    on_message=self.__on_message,
                                    on_error=self.__on_error,
                                    on_close=self.__on_close)

        self.ws = ws
        ws.run_forever()
    
    
    def subscribe(self, currency_pair):
        W = self.web_id + str(self.subscription_id)
        I = "MARKETDESK/FX/" + currency_pair
        subscriptionMessageStructure = {"T":{"W":W,"I":I}}
        self.ws.send(json.dumps(subscriptionMessageStructure, indent=2).encode('utf-8'))
        return W
    

    def unsubscribe(self, subscription_id, currency_pair):
        W = subscription_id
        I = "MARKETDESK/FX/" + currency_pair
        unSubscriptionMessageStructure = {"X":{"W":W,"I":I}}
        self.ws.send(json.dumps(unSubscriptionMessageStructure, indent=2).encode('utf-8'))
        

    def unsubscribe_all(self):
        unSubscriptionAllMessageStructure = {"U":{}}
        self.ws.send(json.dumps(unSubscriptionAllMessageStructure, indent=2).encode('utf-8'))
        

    def kill_session(self):
        S = "8437495ED435W"
        killSessionMessageStructure = {"Z":{"S":S,"ID":"ID"}}
        self.ws.send(json.dumps(killSessionMessageStructure, indent=2).encode('utf-8'))
        
        
    def contribution(self, identifier, bids):
        W = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        I = identifier
        bid = bids
        contributionMessageStructure = {"C":{"W":W,"I":I, "BID": bid}}
        self.ws.send(json.dumps(contributionMessageStructure, indent=2).encode('utf-8'))
        
    
    def _callback(self, callback, *args):
        if callback:
            try:
                callback(self, *args)

            except Exception as e:
                print("error from callback {}: {}".format(callback, e))
                if self.on_error:
                    self.on_error(self, e)