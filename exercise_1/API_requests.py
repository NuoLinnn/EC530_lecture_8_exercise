import requests
import json

#Get the top 5 manufacturers with recalls
r = requests.get("https://api.fda.gov/drug/enforcement.json?count=openfda.manufacturer_name.exact&limit=5")

# Print the URL and staus code to make sure the user is accessing the right place and has success.
print("URL: ", r.url)
print("Status Code: ", r.status_code)

# Assign the JSON data
data = r.json()

# Return the data in a readable form
for item in data.get("results", []):
    print("Manufacturer Name:", item.get("term"))
    print("Recall Count:", item.get("count"))
    print()