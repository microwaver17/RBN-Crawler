__author__ = 'yuya'

import sys
import io
import urllib.request
from urllib.error import *
import json
import datetime
import pytz

class RBNData():
    monthword = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "dec": 12}
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

        self.time = datetime.datetime(year,month,day,hour,minute,tzinfo=pytz.UTC)

    def get_time(self):
        return self.time.astimezone(RBNData.JST)

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
        if int(sta) > latest_id:
            latest_id = int(sta)

    return stations, latestid

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
