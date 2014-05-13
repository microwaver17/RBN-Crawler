__author__ = 'fujita'

import sys
import io
import urllib.request
from urllib.error import *
import json

def load_station_detail(callsign,latestid=0):
    url = 'http://www.reversebeacon.net/dxsd1/sk.php?s='+str(latestid)+'&r=15&cdx='+callsign
    response = urllib.request.urlopen(url)
    rbnjson = response.readall().decode()
    rbndata = json.loads(rbnjson)
    if 's' not in rbndata:
        return None

    stations = list()
    for sta in rbndata['s'].items():
        stations += (sta[1],)

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
        print('-->freq:'+sta[1]+' time:'+sta[5]+' callsign:'+sta[0])
        pass
    print('')

if __name__  == "__main__":
    print('input callsign')
    for line in sys.stdin:
        callsign = line.replace('\n','')
        print_latest(callsign)
        print('input callsign')
    pass
