import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import json
import pprint
import urllib3
import csv
import matplotlib.pyplot as plt
import numpy as np

def findNearestIndex(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    # return (array[idx],idx)
    return idx

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

    plt.style.use('dark_background')
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
        cmd=inp.split(' ')
        if cmd[0] == "unsub":
            unsub()
        if cmd[0] == "sub":
            sub()
        if cmd[0] == "time":
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/time')
            print(json.loads(res.data.decode('utf-8')))

        if cmd[0] == "readData":
            print("This may take a while")
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/BTC_EUR?unit=HOURS&period=4&from=2019-08-07T11:00:00.080Z&to=2019-08-14T16:01:41.090Z')
            data=json.loads(res.data.decode('utf-8'))
            csvDatei=open('data.csv','w+',newline='')
            csvwriter = csv.writer(csvDatei)
            count = 0
            for interval in data:
                interval.pop('last_sequence')
                interval.pop('granularity')
                interval.pop('instrument_code')
                interval['time']=interval['time'][11:23]
                if count == 0:
                    header = interval.keys()
                    csvwriter.writerow(header)
                    count+=1
                csvwriter.writerow(interval.values())
            csvDatei.close()
            print("Finished DataGrabbing")

        if cmd[0] == "OrderBook":
            print("This may take a while")
            try:
                cmdcurrency =cmd[1]
            except:
                cmdcurrency='BTC_EUR'
            cmdZoom = 0.2
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/order-book/'+cmdcurrency+'?level=2')
            data=json.loads(res.data.decode('utf-8'))
            currency=data['instrument_code']
            [cbuy,csell]=currency.split("_")
            bids=data['bids']
            asks=data['asks']
            bidprices = np.array([])
            askprices = np.array([])
            bidamount = np.array([])
            askamount = np.array([])
            for bid in bids:
                bidprices=np.insert(bidprices,0,float(bid['price']))
                try:
                    bidamount=np.insert(bidamount,0,bidamount[0]+float(bid['amount']))
                except:
                   bidamount=np.insert(bidamount,0,float(bid['amount'])) 
            for ask in asks:
                askprices=np.append(askprices,float(ask['price']))
                try:
                    askamount=np.append(askamount,askamount[-1]+float(ask['amount']))
                except:
                    askamount=np.append(askamount,float(ask['amount']))
            middleprice=(bidprices[-1]+askprices[0])/2
            prices=np.append(bidprices,askprices)
            amount=np.append(bidamount,askamount)
            plt.plot(bidprices,bidamount,'g',askprices,askamount,'r')
            plt.axis([(1-cmdZoom)*middleprice,(1+cmdZoom)*middleprice,0,np.maximum(bidamount[findNearestIndex(bidprices,(1-cmdZoom)*middleprice)]*1.1,1.1*askamount[findNearestIndex(askprices,(1+cmdZoom)*middleprice)])])
            plt.suptitle('Tiefendiagram '+ currency+'\nMittlerer Preis:'+ str(middleprice))
            plt.ylabel('Amount ['+cbuy+']')
            plt.xlabel('Price ['+csell+']')
            plt.show()
            print("Finished OrderBook Grabbing")  

        if cmd[0] == "DayVolume":
            try:
                cmdcurrency =cmd[1]
            except:
                cmdcurrency='BTC_EUR'
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/time')
            data=json.loads(res.data.decode('utf-8'))
            time = data['iso']
            res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/'+cmdcurrency+'?unit=DAYS&period=1&from=2019-08-07T11:00:00.080Z&to='+time)
            data=json.loads(res.data.decode('utf-8'))
            for interval in data:
                print(float(interval['volume']))

        if cmd[0] == "close":
            check=1
            ws.close()
            ffile.close()
    print("All closed")