# Copyright(c) 2020  Max Planck Gesellschaft
# Author: Vincent Berenz

from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import pyqtgraph as pg
from collections import deque
import threading,math,time

pg.setConfigOptions(antialias=True)

class _Channel:

    __slots__=["_get_function",
               "_color",
               "_curve",
               "_data",
               "_plot",
               "_first"]
    
    def __init__(self,get_function,color,data_size,limits):
        self._get_function = get_function
        self._color = color
        self._data = deque([limits[0]]*data_size,data_size)
        self._data[1]=limits[1]
        self._curve = None
        self._first = True

    def get_color(self):
        return self._color

    def stop(self):
        self._plot.close()
    
    def set_curve(self,curve,plot):
        self._curve = curve
        self._plot = plot
        
    def update(self):
        v = self._get_function()
        self._data.append(v)
        self._curve.setData(self._data)
        if self._first:
            self._plot.enableAutoRange('xy', False)
            self._first=False
        

class _Subplot:

    __slots__= ["_channels","_limits","_data_size"]
    
    def __init__(self,limit_min,limit_max,data_size):
        self._data_size = data_size
        self._channels = []
        self._limits = (limit_min,limit_max)

    def add_channel(self,channel):
        self._channels.append(channel)

    def add_channels(self,function_colors):
        for function,color in function_colors:
            self._channels.append(_Channel(function,
                                           color,self._data_size,
                                           self._limits))
    def get_channels(self):
        return self._channels

    
class Plot():

    def __init__(self,
                 title,
                 period,
                 windows_size):
        self._title = title
        self._period = period
        self._subplots = []
        self._windows_size = windows_size
        self._timer = None

    def add_subplot(self,limits,data_size,function_colors):
        subplot = _Subplot(limits[0],limits[1],data_size)
        subplot.add_channels(function_colors)
        self._subplots.append(subplot)
        
    def _update(self):
        for subplot in self._subplots:
            for channel in subplot.get_channels():
                channel.update()
        
    def _setup(self):
        self._application = QtGui.QApplication([])
        self._win = pg.GraphicsWindow(title=self._title)
        self._win.resize(*self._windows_size)
        self._win.setWindowTitle(self._title)
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self._update)
        self._timer.start(self._period)
        for subplot in self._subplots:
            p = self._win.addPlot()
            for channel in subplot.get_channels():
                curve = p.plot(pen=channel.get_color())
                channel.set_curve(curve,p)
            self._win.nextRow()

    def stop(self):
        self._application.quit()
        self._thread.join()
        
    def _run(self):
        self._setup()
        self._application.exec_()

    def start(self):
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
