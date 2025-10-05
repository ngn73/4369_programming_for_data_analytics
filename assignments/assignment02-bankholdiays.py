import requests
url =" https://www.gov.uk/bank-holidays.json"

response = requests.get(url)
data = response.json()

# Extract Events data for Northern Ireland holidays
ni_bh = data["northern-ireland"]["events"]

# Extract dates for England and Wales holidays
ew_dates = [event['date'] for event in data["england-and-wales"]["events"]]
# Extract dates for Scotland holidays
s_dates = [event['date'] for event in data["scotland"]["events"]]
#loop thru NI event data and print bank holiday dates

#www.gov.uk json returns multiple years of bank holiday data so ask user to specify year
year = input("enter a year (e.g. 2025) :")
unique_ni_events = []
for event in ni_bh:
    if (event['date'].startswith(year) ):
        if (event['date'] not in ew_dates) and (event['date'] not in s_dates):
            unique_ni_events.append({'date' : event['date'], 'title' : event['title']})

if(len(unique_ni_events) > 0):
    for ni_event in unique_ni_events:
        print(f"{ni_event['date']} - {ni_event['title']}")
else:
    print("no data for that year")