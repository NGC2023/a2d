#coding=utf-8
#!/usr/bin/env python

from utils.decr_usrinfo import retrieve_usrinfo
import requests

data = retrieve_usrinfo()
APRSAPI_KEY = data['aprsapi_key']
callsign_nossid = data['callsign_nossid']

def get_aprs(c):
    if c[2] == '0':
        url = "https://api.aprs.fi/api/get?what=msg&dst=" + c[1] + "&apikey="+APRSAPI_KEY+"&format=json"
        trgcall = c[2]
    else:
        url = "https://api.aprs.fi/api/get?what=msg&dst=" + c[1] + "-" + c[2] + "&apikey="+APRSAPI_KEY+"&format=json"
        trgcall = c[2]

    aprs = requests.get(url)
    aprs = aprs.json()

    try: #If ARPS server returns "Get failed, query ratelimit" (because of too frequent requests)
        entries = aprs['entries']
    except KeyError:
        return None

    return entries, trgcall

def aprs_check():
    url = "https://api.aprs.fi/api/get?what=msg&dst="+callsign_nossid+"&apikey="+APRSAPI_KEY+"&format=json"

    try:
        aprs_check = requests.get(url)
        entries_check = aprs_check.json()
    except KeyError:
        return None

    return entries_check
