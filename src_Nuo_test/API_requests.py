import requests
import json

r = requests.get("https://api.fda.gov/food/enforcement.json?search=report_date:[20040101+TO+20131231]&limit=1", auth=('enforcement', 'report_date'))

r.headers
r.encoding