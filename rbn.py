__author__ = 'yuya'

import sys
import io
import urllib.request
from urllib.error import *
import json
import datetime
import pytz

class RBNData():
    monthword = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'dec': 12}
    bandrange = {'3.5': (135.7, 137.8), '1.9': (1810.0, 1912.5), '3.5': (3500.0, 3687.0), '3.8': (3702.0, 3805.0),
                '7': (7000.0, 7200.0), '10': (10100.0, 10150.0), '14': (14000.0, 14350.0), '18': (18068.0, 18168.0),
                '21': (21000.0, 21450.0), '24': (24890.0, 24990.0), '28': (28000.0, 29700.0), '50': (50000.0, 54000.0),
                '144': (144000.0, 146000.0), '430': (430000.0, 440000.0), '1200': (1260000.0, 1300000.0),
                '2400': (2400000.0, 2450000.0), '5600': (5650000.0, 5850000.0)}
    JST = pytz.timezone('Asia/Tokyo')

    def __init__(self, response):
        self.callsign = response[2]
        self.frequency = float(response[1])
        self.wpm = int(response[4])

        timetext = response[5]
        month = RBNData.monthword[timetext[9:12]]
        day = int(timetext[6:8])
        hour = int(timetext[0:2])
        minute = int(timetext[2:4])
        year = datetime.date.today().year
        utctime = datetime.datetime(year,month,day,hour,minute,tzinfo=pytz.UTC)
        self.time = utctime.astimezone(RBNData.JST)

        self.band = None
        for key in RBNData.bandrange.keys():
            ran = RBNData.bandrange[key]
            if ran[0] <= self.frequency <= ran[1]:
                self.band = key

    def __str__(self):
        strs = "Call:"+self.callsign+" Freq:"+str(self.frequency)+" WPM:"+str(self.wpm)+" Time:"+str(self.get_time())
        return strs


def load_station_detail(callsign,latestid=0):
    url = 'http://www.reversebeacon.net/dxsd1/sk.php?s=' + str(latestid) + '&r=15&cdx='+callsign
    response = urllib.request.urlopen(url)
    rbnjson = response.readall().decode()
    rbndata = json.loads(rbnjson)
    if 's' not in rbndata:
        return None

    stations = list()
    for sta in rbndata['s'].items():
        s = RBNData(sta[1])
        stations.append(s)

    latest_id = 0
    for sta in rbndata['s'].keys():
        print('id='+sta)
        if int(sta) > latest_id:
            latest_id = int(sta)

    return stations, latest_id

def print_latest(callsign):
    retry = 0
    data = None
    for i in range(5):
        try:
            data = load_station_detail(callsign)
        except URLError:
            continue
        break
    if data is None:
        return

    print('['+callsign+']')
    for sta in data[0]:
        print(sta)
        pass
    print('')

if __name__  == "__main__":
    print('input callsign')
    for line in sys.stdin:
        callsign = line.replace('\n','')
        print_latest(callsign)
        print('input callsign')
    pass
