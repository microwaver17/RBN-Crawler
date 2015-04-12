__author__ = 'yuya'

import sys
from threading import Thread

from PyQt5 import QtWidgets

import latest
import main_window
import time

window = None
latestRBN = None
refresh_thread = None

def refresh():
    while True:
        latestRBN.reload()
        main_window.set_latest_rbn(latestRBN.rbn_list)
        time.sleep(60)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    window = main_window.create_window()
    window.show()

    latestRBN = latest.LatestRBN(('JA1YGX', 'JA1ZLO'))

    refresh_thread = Thread(target=refresh)
    refresh_thread.daemon = True
    refresh_thread.start()


    ret = app.exec_()
    sys.exit(ret)