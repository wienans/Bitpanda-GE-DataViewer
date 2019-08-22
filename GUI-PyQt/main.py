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

class Dialog(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ui_path = os.path.dirname(os.path.abspath(__file__))
        loadUi(os.path.join(ui_path,"ui/Main.ui"),self)
        self.StatusMessage = "No Connection to Bitpanda API"
        self.statusBar.showMessage(self.StatusMessage)
        self.bDeapthPlus.clicked.connect(self.zoomInDeapthChart)
        self.bDeapthMinus.clicked.connect(self.zoomOutDeapthChart)
        self.tabWidget.currentChanged.connect(self.tabWidgetChanged)
        self.cBTraidPairs.currentIndexChanged.connect(self.cBTraidPairsChanged)
        self.zoomDeapthChart = 0.1

        self.fillTraidingPairs()


    def tabWidgetChanged(self,i):
        if i == self.tabWidget.indexOf(self.tabHome):
            print("Home")
        elif i == self.tabWidget.indexOf(self.tabDataView):
            print("DataView")
            self.plotDeapthChart(self.zoomDeapthChart)
        elif i == self.tabWidget.indexOf(self.tabConfig):
            print("Config")

    def cBTraidPairsChanged(self,i):
        self.plotDeapthChart(self.zoomDeapthChart)

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
        self.zoomDeapthChart+=0.1
        self.plotDeapthChart(self.zoomDeapthChart)
        print(self.zoomDeapthChart)

    def zoomOutDeapthChart(self):
        if (self.zoomDeapthChart-0.1) > 0.001:
            self.zoomDeapthChart-=0.1
        self.plotDeapthChart(self.zoomDeapthChart)
        print(self.zoomDeapthChart)
    
    def fillTraidingPairs(self):
        res = http.request('GET','https://api.exchange.bitpanda.com/public/v1/instruments')
        data=json.loads(res.data.decode('utf-8'))
        for pair in data:
            self.cBTraidPairs.addItem(pair['base']['code']+"_"+pair['quote']['code'])

    def findNearestIndex(self,array, value):
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

def startWebSocket():
    ws.run_forever(suppress_origin=1,ping_timeout = 20)
def startWindow():
    window.show()

if __name__ == "__main__":
    global ws,ffile,window
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
        if inp == "close":
            check=1
            ws.close()
            ffile.close()

    #sys.exit(app.exec_())
