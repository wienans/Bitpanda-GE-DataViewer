import websocket
import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import pprint
import urllib3
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        #self.mainWcolor = '#4D4D4D'
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.root.title("Bitpanda-GE-DataViewer")
        self.root.minsize(640,400)
        #self.root.configure(background = self.mainWcolor)

        self.tabcontrol = ttk.Notebook(self.root)
        self.tabHome = tk.Frame(self.tabcontrol)
        self.tabcontrol.add(self.tabHome, text="Home")
        self.tabMarketView = tk.Frame(self.tabcontrol)
        self.tabMarketView.columnconfigure(0,pad=3)
        self.tabMarketView.columnconfigure(1,pad=3)
        self.tabMarketView.rowconfigure(0,pad=3)
        self.tabMarketView.rowconfigure(1,pad=3)
        self.tabcontrol.add(self.tabMarketView, text="Market View")
        self.tabLiveTraiding = tk.Frame(self.tabcontrol)
        self.tabcontrol.add(self.tabLiveTraiding, text="Live Traiding")
        self.tabLocalData = tk.Frame(self.tabcontrol)
        self.tabcontrol.add(self.tabLocalData, text="Local Data")
        self.tabBacktest = tk.Frame(self.tabcontrol)
        self.tabcontrol.add(self.tabBacktest, text="Backtest")
        self.tabConfig = tk.Frame(self.tabcontrol)
        self.tabcontrol.add(self.tabConfig, text="Config")
        self.matplotCanvas()
        self.tabcontrol.pack(expan = 1, fill = "both")



        self.root.mainloop()

    def matplotCanvas(self):
        f = Figure(figsize=(5,5),dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6],[1,2,3,4,5,6])
        canvas = FigureCanvasTkAgg(f,master=self.tabMarketView)
        canvas._tkcanvas.grid(row=0,column=1)
        f = Figure(figsize=(5,5),dpi=100)
        a = f.add_subplot(111)
        a.plot([6,4,3,2,5,6],[1,2,3,4,5,6])
        canvas = FigureCanvasTkAgg(f,master=self.tabMarketView)
        canvas._tkcanvas.grid(row=0,column=0)

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

def startWS():
    ws.run_forever(suppress_origin=1,ping_timeout = 20)

if __name__ == "__main__":
    global ws
    global ffile
    app = App()

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

    socketThread = threading.Thread(target=startWS)
    #socketThread.start()
    ffile=open("recv.txt", "a+")
    check = 1
    while check == 0:
        inp=input()
        if inp == "close":
            check=1
            ws.close()
            ffile.close()
            
    print("All closed")