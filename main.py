import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import pprint
import urllib3
def on_message(ws, message):
    msg=json.loads(message)
    print(msg)
    if msg['type']!="HEARTBEAT" and msg['type']!="PRICE_POINT_UPDATES" :
        ffile.write('\n{}'.format(message))
    

def on_error(ws, error):
    print("Error")
    print('ERROR: {}'.format(error))

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### conection opend ###")

def sub ():
    sub=json.dumps({'type': 'SUBSCRIBE','channels': [{'name': 'MARKET_TICKER','instrument_codes': ['BTC_EUR','ETH_EUR']}]})
    ws.send(sub)

def unsub():
    unsub=json.dumps({"type": "UNSUBSCRIBE","channels": ["MARKET_TICKER"]})
    ws.send(unsub)

def startWS():
    ws.run_forever(suppress_origin=1,ping_timeout = 20)

if __name__ == "__main__":
    global ws
    global ffile
    #load Config
    config=open("config.json","r")
    cdata=json.load(config)
    #Starting
    http=urllib3.PoolManager()
    websocket.enableTrace(cdata['enableWebsocketTrace'])

    ws = websocket.WebSocketApp(cdata['url'],
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    thread.start_new_thread(startWS, ())
    ffile=open("recv.txt", "a+")
    check=0
    while check == 0:
        inp=input()
        if inp == "unsub":
            unsub()
        if inp == "sub":
            sub()
        if inp == "res":
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/time')
            print(json.loads(res.data.decode('utf-8')))
        if inp == "res2":
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/order-book/BTC_EUR?level=1')
            print(json.loads(res.data.decode('utf-8')))
        if inp == "close":
            check=1
            ws.close()
            ffile.close()
    print("All closed")