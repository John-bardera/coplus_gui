# coding:utf-8

"""
def now_time_datetime():
    import datetime
    from time import ctime
    import ntplib
    datetime_now = datetime.datetime.strptime(ctime(ntplib.NTPClient().request("ntp.nict.jp").tx_time), "%a %b %d %H:%M:%S %Y")
    return datetime_now
"""


def now_time_datetime():
    import datetime
    import requests
    import simplejson
    req = requests.get("https://ntp-b1.nict.go.jp/cgi-bin/json")
    datetime_now = datetime.datetime.fromtimestamp(simplejson.loads(req.text)["st"])
    return datetime_now
