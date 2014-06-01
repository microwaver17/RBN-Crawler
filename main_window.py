__author__ = 'yuya'

import sys
from PyQt5 import uic, QtWidgets

import rbn

window = None
freq_tab = None

def create_window():
    global window, freq_tab

    if window is None:
        window = uic.loadUi("main.ui")
        tab35 = {''}

    return window

def set_latest_rbn(latest_rbn):
    window.table35.setRowCount(len(latest_rbn.rbn_list))

    for i,rbndata in enumerate(latest_rbn.rbn_list):
        callsign = str(rbndata.callsign)
        freq = str(rbndata.frequency)
        wpm = str(rbndata.wpm)
        time = str(rbndata.time)
        item_callsign = QtWidgets.QTableWidgetItem(callsign)
        item_freq = QtWidgets.QTableWidgetItem(freq)
        item_wpm = QtWidgets.QTableWidgetItem(wpm)
        item_time = QtWidgets.QTableWidgetItem(time)

        window.table35.setItem(i, 0, item_callsign)
        window.table35.setItem(i, 1, item_freq)
        window.table35.setItem(i, 2, item_wpm)
        window.table35.setItem(i, 3, item_time)