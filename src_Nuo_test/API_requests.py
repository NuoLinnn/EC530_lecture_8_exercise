import requests
import json

#Get the top 5 manufacturers with recalls
r = requests.get("https://api.fda.gov/drug/enforcement.json?count=openfda.manufacturer_name.exact&limit=5")

#print(r.json())
print("URL: ", r.url)
print("Status Code: ", r.status_code)

data = r.json()

for item in data.get("results", []):
    #print("Report Date:", item.get("report_date"))
    print("Manufacturer Name:", item.get("term"))
    print("Recall Count:", item.get("count"))
    print()