import requests
import json
import os
from googleMapsApi import GoogleMapsApi
from dotenv import load_dotenv
import time
from datetime import datetime, timezone

gMaps = GoogleMapsApi()

# gMaps.googleMapsApiRequest("Filderstadt Uhlbergstraße", "Stuttgart Rosenberg/ Seidenstraße", 'walking')

obj = time.gmtime(0)
epoch = time.asctime(obj)
print("The epoch is:",epoch)
curr_time = round(time.time()*1000)
print("Milliseconds since epoch:",curr_time)

def timestamp(dt):
    return int(dt.replace(tzinfo=timezone.utc).timestamp() * 1000)

dt = datetime(2023, 3, 12, 3)
print(timestamp(dt))
