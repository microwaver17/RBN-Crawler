__author__ = 'yuya'

import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui

import rbn

window = None
band_table = None
band_scene = None
band_graphics = None

def create_window():
    global window, band_table, band_scene, band_graphics

    if window is None:
        window = uic.loadUi("main.ui")
        band_table = {'3.5': window.table35, '7': window.table7}
        band_graphics = {'3.5': window.graphics35, '7': window.graphics7}
        band_scene = {'3.5': QtWidgets.QGraphicsScene(),
                      '7': QtWidgets.QGraphicsScene()}
        mat = QtGui.QTransform()
        mat.scale(0.5,0.5)
        mat.translate(-950,0)

        for key in band_scene.keys():
            band_graphics[key].setScene(band_scene[key])
            band_graphics[key].setTransform(mat)

    return window


def set_latest_rbn(rbn_list):
    set_table(rbn_list)
    set_graph(rbn_list, window.graphics35)


def add_row_to_table(rbndata, table):
    newrow = table.rowCount()
    table.insertRow(newrow)

    callsign = str(rbndata.callsign)
    freq = str(rbndata.frequency)
    wpm = str(rbndata.wpm)
    time = str(rbndata.time)
    item_callsign = QtWidgets.QTableWidgetItem(callsign)
    item_freq = QtWidgets.QTableWidgetItem(freq)
    item_wpm = QtWidgets.QTableWidgetItem(wpm)
    item_time = QtWidgets.QTableWidgetItem(time)

    table.setItem(newrow, 0, item_callsign)
    table.setItem(newrow, 1, item_freq)
    table.setItem(newrow, 2, item_wpm)
    table.setItem(newrow, 3, item_time)


def set_table(rbn_list):
    # tableを全削除
    for table in band_table.values():
        table.clearContents()
        table.setRowCount(0)

    for rbndata in rbn_list:
        if rbndata.band in band_table.keys():
            table = band_table[rbndata.band]
            add_row_to_table(rbndata, table)

def set_graph(rbn_list, graphics):
    font = QtGui.QFont("Helvetica", 25)
    for key in band_scene.keys():
        scene = band_scene[key]
        freq_min = rbn.RBNData.bandrange[key][0]
        freq_max = rbn.RBNData.bandrange[key][1]
        div = 20
        for i in range(div):
            freq = freq_min + ((freq_max - freq_min) / div) * i
            text = scene.addText(str(freq))
            text.setFont(font)
            text.setPos(-150,1000/div * i)
        scene.addLine(-200, 0.0, 1000, 0.0)
        text = scene.addText("3min")
        scene.addLine(0, -50, 0, 1000)
        text.setFont(font)
        text.setPos(0,-50)
        scene.addLine(200, -50, 200, 1000)
        text = scene.addText("10min")
        text.setFont(font)
        text.setPos(200,-50)
        scene.addLine(400, -50, 400, 1000)
        text = scene.addText("30min")
        text.setFont(font)
        text.setPos(400,-50)
        scene.addLine(600, -50, 600, 1000)
        text = scene.addText("60min or more")
        text.setFont(font)
        text.setPos(600,-50)

    font = QtGui.QFont("Helvetica", 15)
    for rbndata in rbn_list:
        if rbndata.band in band_table.keys():
            band = rbndata.band
            scene = band_scene[band]
            freq_min = rbn.RBNData.bandrange[band][0]
            freq_max = rbn.RBNData.bandrange[band][1]
            text = scene.addText(rbndata.callsign + " " + str(rbndata.frequency))
            text.setFont(font)
            text.setPos(0, (freq_max-rbndata.frequency)/(freq_max-freq_min) * 1000)

