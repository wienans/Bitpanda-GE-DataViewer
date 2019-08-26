import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import random
import numpy as np
from mplwidget import MplWidget
import websocket
import threading
import json
import pprint
import urllib3
import csv
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
import re


class Dialog(QtWidgets.QMainWindow):
    def __init__(self):
        global pair24hVolume
        pair24hVolume = np.array(['0'])
        QtWidgets.QMainWindow.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        loadUi(os.path.join(ui_path,"ui/Main.ui"),self)
        self.StatusMessage = "No Connection to Bitpanda API"
        self.statusBar.showMessage(self.StatusMessage)
        self.bDeapthPlus.clicked.connect(self.zoomInDeapthChart)
        self.bDeapthMinus.clicked.connect(self.zoomOutDeapthChart)
        self.tabWidget.currentChanged.connect(self.tabWidgetChanged)
        self.cBTraidPairs.currentIndexChanged.connect(self.cBTraidPairsChanged)
        self.chBNow.stateChanged.connect(self.checkBoxNowChanged)
        self.bImport.clicked.connect(self.csvImport)
        self.zoomDeapthChart = 0.1
        self.dateFormat = re.compile('.{4}-.{2}-.{2}')
        self.time = '2019-08-07T11:00:00.080Z'
        self.RepeatingEventTimer = QtCore.QTimer()
        self.RepeatingEventTimer.timeout.connect(self.RepeatingEvents)
        self.RepeatingEventTimer.start(10000)

        self.getServerTime()
        self.fillInitial()
        # sub=json.dumps({'type': 'SUBSCRIBE','channels': [{'name': 'MARKET_TICKER','instrument_codes': ['PAN_BTC','BTC_EUR','MIOTA_BTC','MIOTA_EUR','ETH_EUR']}]})
        # ws.send(sub)

    def RepeatingEvents(self):
        if self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabHome):
            print("Home")
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabDataView):
            self.cBTraidPairsChanged()
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabDataImport):
            print("DataImport")
        elif self.tabWidget.currentIndex() == self.tabWidget.indexOf(self.tabConfig):
            print("Config")

    def tabWidgetChanged(self,i):
        if i == self.tabWidget.indexOf(self.tabHome):
            print("Home")
        elif i == self.tabWidget.indexOf(self.tabDataView):
            print("DataView")
            #self.plotDeapthChart(self.zoomDeapthChart)
        elif i == self.tabWidget.indexOf(self.tabDataImport):
            print("DataImport")
        elif i == self.tabWidget.indexOf(self.tabConfig):
            print("Config")

    def cBTraidPairsChanged(self):
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/'+self.cBTraidPairs.currentText()+'?unit=DAYS&period=1&from=2019-08-07T11:00:00.080Z&to='+self.time)
        data=json.loads(res.data.decode('utf-8'))
        currency = self.cBTraidPairs.currentText()
        [_,csell]=currency.split("_")
        self.lVolume24h.setText(str(float(data[-1]['volume']))+' '+csell)
        self.lVolume1Days.setText(str(float(data[-2]['volume']))+' '+csell)
        self.lVolume2Days.setText(str(float(data[-3]['volume']))+' '+csell)
        self.lVolume3Days.setText(str(float(data[-4]['volume']))+' '+csell)
        self.lVolume4Days.setText(str(float(data[-5]['volume']))+' '+csell)
        self.lVolume5Days.setText(str(float(data[-6]['volume']))+' '+csell)
        #self.lVolume24h.setText(str(pair24hVolume[self.cBTraidPairs.currentIndex()]))
        self.plotDeapthChart(self.zoomDeapthChart)
        self.plotCandleChart(data)
    
    def plotCandleChart(self,data):
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/'+self.cBTraidPairs.currentText()+'?unit=HOURS&period=4&from=2019-08-08T11:00:00.080Z&to='+self.time)
        data=json.loads(res.data.decode('utf-8'))
        n=len(data)
        quotes = np.empty((n,0)).tolist()
        i=0
        for instance in data:
            quotes[i].append(mdates.datestr2num(str(instance['time'][0:19].replace('T',' '))))
            quotes[i].append(float(instance['open']))
            quotes[i].append(float(instance['high']))
            quotes[i].append(float(instance['low']))
            quotes[i].append(float(instance['close']))
            i+=1
        self.mplCandleChart.canvas.axes.clear()
        candlestick_ohlc(self.mplCandleChart.canvas.axes, quotes,width=0.05)
        self.mplCandleChart.canvas.axes.set_xlabel('Date')
        self.mplCandleChart.canvas.axes.set_ylabel('Price')
        self.mplCandleChart.canvas.draw()

    def plotDeapthChart(self,cmdZoom):
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/order-book/'+self.cBTraidPairs.currentText()+'?level=2')
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
        #prices=np.append(bidprices,askprices)
        #amount=np.append(bidamount,askamount)

        self.mplDeapthChart.canvas.axes.clear()
        self.mplDeapthChart.canvas.axes.plot(bidprices,bidamount,'g',askprices,askamount,'r')
        self.mplDeapthChart.canvas.axes.set_xlim([(1-cmdZoom)*middleprice,(1+cmdZoom)*middleprice])
        self.mplDeapthChart.canvas.axes.set_ylim([0,np.maximum(bidamount[self.findNearestIndex(bidprices,(1-cmdZoom)*middleprice)]*1.1,1.1*askamount[self.findNearestIndex(askprices,(1+cmdZoom)*middleprice)])])
        #self.mplDeapthChart.canvas.axes.set_title('Deapth-Chart '+ currency+'\nMiddle Price:'+ str(middleprice)+csell)
        self.lDeapthPrice.setText(str(middleprice)+' '+csell)
        self.mplDeapthChart.canvas.axes.set_xlabel('Price ['+csell+']')
        self.mplDeapthChart.canvas.axes.set_ylabel('Amount ['+cbuy+']')
        self.mplDeapthChart.canvas.draw()
    
    def zoomInDeapthChart(self):
        if (self.zoomDeapthChart-0.1) > 0.001:
            self.zoomDeapthChart-=0.1
        self.plotDeapthChart(self.zoomDeapthChart)
        print(self.zoomDeapthChart)

    def zoomOutDeapthChart(self):
        self.zoomDeapthChart+=0.1
        self.plotDeapthChart(self.zoomDeapthChart)
        print(self.zoomDeapthChart)

    def csvImport(self):
        self.pBImport.setValue(0)
        [number, period] = self.cBCandlestickPeriod.currentText().split(' ')
        if self.dateFormat.match(self.tBFrom.displayText()) and self.dateFormat.match(self.tBTo.displayText()) and len(self.tBFrom.displayText())==10 and len(self.tBTo.displayText())==10:
            [j,m,d]=self.tBFrom.displayText().split('-')
            [j1,m1,d1]=self.tBTo.displayText().split('-')
            try:
                int(j)
                int(j1)
                int(m)
                int(m1)
                int(d)
                int(d1)
            except:
                print("No Int")
                return
            fromDateNum = mdates.datestr2num(self.tBFrom.displayText())
            toDateNum = mdates.datestr2num(self.tBTo.displayText())
        else:
            print("No Valid Pattern")
            return
        csvDatei=open('import/'+self.cBTraidPairs_2.currentText()+'p'+number+period+'f'+self.tBFrom.displayText()+'t'+self.tBTo.displayText()+'.csv','w+',newline='')
        csvwriter = csv.writer(csvDatei)
        csvwriter.writerow(['high','low','open','close','volume','time'])
        diffDays = toDateNum-fromDateNum
        itterations = np.ceil(diffDays)
        print(itterations)
        if itterations == 1:
            stop = toDateNum
            start = fromDateNum
        else:
            start = fromDateNum
            stop = start+1    
        if self.chBNow.checkState() == 2:
            itterations +=1
        for i in range(0,int(itterations)):
            print(str(mdates.num2date(start))[0:10])
            print(str(mdates.num2date(stop))[0:10])
            if self.chBNow.checkState() == 2 and i == int(itterations)-1:
                self.getServerTime()
                res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/'+self.cBTraidPairs_2.currentText()+'?unit='+period+'&period='+number+'&from='+self.time[0:10]+'T00:00:00.080Z&to='+self.time)
                stop = start
            else:
                res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/candlesticks/'+self.cBTraidPairs_2.currentText()+'?unit='+period+'&period='+number+'&from='+str(mdates.num2date(start))[0:10]+'T00:00:00.080Z&to='+str(mdates.num2date(stop))[0:10]+'T00:00:00.090Z')
                start = stop
                if start+1<toDateNum:
                    stop = start+1
                else:
                    stop = toDateNum
            data=json.loads(res.data.decode('utf-8'))
            try:
                if data['error'] == 'CANDLESTICKS_TIME_RANGE_TOO_BIG':
                    print("CANDLESTICKS_TIME_RANGE_TOO_BIG")
                    return
            except:
                pass
            for interval in data:
                interval.pop('last_sequence')
                interval.pop('granularity')
                interval.pop('instrument_code')
                interval['time']=interval['time'][11:23]
                csvwriter.writerow(interval.values())
            self.pBImport.setValue(int((i+1)/float(itterations)*100))
        csvDatei.close()
 

    def fillInitial(self):
        # Fill Candlestick Periods
        self.cBCandlestickPeriod.addItem("1 MINUTES")
        self.cBCandlestickPeriod.addItem("5 MINUTES")
        self.cBCandlestickPeriod.addItem("15 MINUTES")
        self.cBCandlestickPeriod.addItem("30 MINUTES")
        self.cBCandlestickPeriod.addItem("1 HOURS")
        self.cBCandlestickPeriod.addItem("4 HOURS")
        self.cBCandlestickPeriod.addItem("1 DAYS")
        self.cBCandlestickPeriod.addItem("1 WEEKS")
        self.cBCandlestickPeriod.addItem("1 MONTHS")
        # Fill textBoxes
        self.tBFrom.setText("2019-08-07")
        self.tBTo.setText(self.time[0:10])
        # Fill Traiding Pairs
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/instruments')
        data=json.loads(res.data.decode('utf-8'))
        for pair in data:
            self.cBTraidPairs.addItem(pair['base']['code']+"_"+pair['quote']['code'])
            self.cBTraidPairs_2.addItem(pair['base']['code']+"_"+pair['quote']['code'])
    
    def getServerTime(self):
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/time')
        data=json.loads(res.data.decode('utf-8'))
        self.time = data['iso']

    def findNearestIndex(self,array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        # return (array[idx],idx)
        return idx  
    
    def checkBoxNowChanged(self):
        if self.chBNow.checkState() == 2:
            self.tBTo.setEnabled(False)
            self.tBTo.setText(self.time[0:10])
        else:
            self.tBTo.setEnabled(True)

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

def startWebSocket():
    ws.run_forever(suppress_origin=1,ping_timeout = 20)
    
def startWindow():
    window.show()

if __name__ == "__main__":
    global ws,ffile,window,check
    #load Config
    config=open("config.json","r")
    cdata=json.load(config)
    #Starting
    http=urllib3.PoolManager()
    #websocket Config and Start
    websocket.enableTrace(cdata['enableWebsocketTrace'])
    ws = websocket.WebSocketApp(cdata['url'],
                            on_open = on_open,
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)

    socketThread = threading.Thread(target=startWebSocket)
    socketThread.start()
    ffile=open("recv.txt", "a+")
    #App Start                        
    app = QtWidgets.QApplication(sys.argv)
    window = Dialog()
    windowThread = threading.Thread(target=window.show())
    windowThread.start()
    check = 0
    while check == 0:
        inp=input()
        if inp == "sub":
            sub=json.dumps({"type": "SUBSCRIBE","channels": [{"name": "PRICE_TICKS","instrument_codes": ["BTC_EUR","ETH_EUR"]}]})
            ws.send(sub)
        if inp == "unsub":
            unsub=json.dumps({"type": "UNSUBSCRIBE","channels": ["PRICE_TICKS"]})
            ws.send(unsub)
        if inp == "close":
            check=1
            ws.close()
            ffile.close()

    #sys.exit(app.exec_())
