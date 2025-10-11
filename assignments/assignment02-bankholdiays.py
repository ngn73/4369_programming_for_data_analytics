'''
accounts.py
Author  Niall Naughton
Date    05/10/2025

----------------------------------------------------------------------------------
Description     Weekly Task #2 Northern bank holdays
Write a program called assignment02-bankholdiays.py
The program should print out the dates of the bank holidays that happen in northern Ireland.
Last few marks (ie this is more tricky)
Modify the program to print the bank holidays that are unique to northern Ireland (i.e. do not happen elsewhere in the UK) you can choose if you want to use the name or the date of the holiday to decide if it is unique.

----------------------------------------------------------------------------------
Approach:
Use Requests Module to get CSV Bank Holiday data from https://www.gov.uk/bank-holidays.json

Load Full Details for Northern Ireland
Load just the dates for England/Scotland/Wales ... use these for comparison

Iterate thru NI Data and compare Dates with England/Scotland/Wales dates
Whenever we find a date that does not match ... then add this data record to an "Unique dates" Array

Note:This call returns 3 years of data (previous/present/future)
So, prompt the user to enter the specific year
'''


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

#Print Results
if(len(unique_ni_events) > 0):
    for ni_event in unique_ni_events:
        print(f"{ni_event['date']} - {ni_event['title']}")
else:
    print("no data for that year")