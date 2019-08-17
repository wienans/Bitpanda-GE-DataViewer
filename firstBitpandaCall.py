import json
import pprint
import websocket
from websocket import create_connection

msg=json.dumps({'type': 'SUBSCRIBE','channels': [{'name': 'MARKET_TICKER','instrument_codes': ['BTC_EUR','ETH_EUR']}]})
unsub=json.dumps({"type": "UNSUBSCRIBE","channels": ["MARKET_TICKER"]})
print(msg)
websocket.enableTrace(True)
print("Starting Websocket connection")
ws = create_connection("wss://streams.exchange.bitpanda.com/",suppress_origin=1)
print("got Connection")

#result = ws.recv()
#print('Result: {}'.format(result))

#result = ws.recv()
#print('Result: {}'.format(result))

ws.send(msg)
result = ws.recv()
print('Result: {}'.format(result))
ws.send(unsub)
result = ws.recv()
print('Result: {}'.format(result))
ws.close()