# Copyright(c) 2020  Max Planck Gesellschaft
# Author: Vincent Berenz

from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from collections import deque
import threading,math,time

pg.setConfigOptions(antialias=True)

class Config:

    def __init__(self):
        self.channels = []
        self.slots = {}
        self.slots_colors = {}
        self.data_size = 200
        self.title = "untitled"
        self.windows_size = [800,800]
        self.start = False
        self.limits = {}

        
_APPLICATION = QtGui.QApplication([])
_WIN = pg.GraphicsWindow(title="pasta")
_WIN.resize(1,1)
_WIN.setWindowTitle("")


_FIRST_ITERATION = True
_CHANNELS = {}
_PLOTS = {} # key : channel , value : {slot:(plot,curve)}
_CONFIG = None

class _channel_data:
    
    def __init__(self,slots,data_size,y_range=[-math.pi,+math.pi]):

        self.data = {slot:deque([0 for _ in range(data_size)],data_size) for slot in slots }

        for slot in slots:
            self.data[slot][-2] = y_range[0]
            self.data[slot][-1] = y_range[1]
        self.lock = threading.Lock()

    def update(self,values):

        with self.lock:

            for slot,value in values.items():
                self.data[slot].append(value)

                
    def get(self):
        with self.lock:
            r = {}
            for slot,queue in self.data.items():
                r[slot] = [v for v in queue]
            return r

        
def _init():
    
    timer.timeout.connect(_update_plot)
    global _CONFIG,_CHANNELS,_PLOTS,_WIN
    _WIN.resize(_CONFIG.windows_size[0],_CONFIG.windows_size[1])
    _WIN.setWindowTitle(_CONFIG.title)
    if isinstance(_CONFIG.channels[0],str):
        _CONFIG.channels = [_CONFIG.channels]

    all_channels = []
    for channel_set in _CONFIG.channels:
        all_channels.extend(channel_set)

    def _get_y_range(channel):
        try : return _CONFIG.limits[channel]
        except : return None

    _CHANNELS = {channel:_channel_data(_CONFIG.slots[channel],
                                       _CONFIG.data_size,
                                       y_range=_get_y_range(channel))
                 for channel in all_channels}

    for channel_set in _CONFIG.channels:
        for channel in channel_set:
            p = _WIN.addPlot(title=channel)
            data = _CHANNELS[channel].get()
            curves = {}
            for slot in _CONFIG.slots[channel]:
                curve = p.plot(pen=_CONFIG.slots_colors[slot],name=slot)
                curves[slot]=(p,curve)
            _PLOTS[channel]=curves
        _WIN.nextRow()

    _CONFIG.start = True

    
def set_data(data):
    global _CHANNELS
    for channel,d in data.items():
        _CHANNELS[channel].update(d)

        
def _update_plot():
    global  _CHANNELS,_FIRST_ITERATION,_PLOTS,win
    if not _CONFIG.start : return
    for channel in _CHANNELS.keys():
        curves = _PLOTS[channel]
        data = _CHANNELS[channel].get()
        for slot in _CONFIG.slots[channel]:
            plot,curve = curves[slot]
            d = data[slot]
            curve.setData(d)
            if _FIRST_ITERATION : plot.enableAutoRange('xy', False)
    _FIRST_ITERATION = False

    
timer = QtCore.QTimer()
timer.start(50)


def _start(target_function):
    _init()
    t = threading.Thread(target=target_function)
    t.start()

    
def start_plotting(config,target_function):
    global _CONFIG
    _CONFIG = config
    _start(target_function)
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()


    


