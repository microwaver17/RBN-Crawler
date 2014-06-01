__author__ = 'yuya'

import rbn
from urllib.error import *

class LatestRBN:

    def __init__(self, watch_callsigns):
        self.rbn_list = list()
        self.watch_callsigns = list()
        self.last_id_set = dict()

        self.set_watch_callsign(watch_callsigns)

    '''
        監視コールサインの設定
    '''
    def set_watch_callsign(self, watch_callsigns):

        for callsign in watch_callsigns:
            if callsign not in self.watch_callsigns:
                self.last_id_set[callsign] = None
        self.watch_callsigns = watch_callsigns[:]

    def reload(self):
        for callsign in self.watch_callsigns:

            detail = None
            for i in range(5):
                try:
                    if self.last_id_set[callsign] is None:
                        detail = rbn.load_station_detail(callsign)
                    else:
                        detail = rbn.load_station_detail(callsign, self.last_id_set[callsign])
                except URLError:
                    print('Retry...')
                    continue

            if detail is not None:
                self.rbn_list.extend(detail[0])
                self.last_id_set[callsign] = detail[1]
