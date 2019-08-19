from bs4 import BeautifulSoup
import requests
import csv
import os
import datetime


# get current date and time
now=datetime.datetime.today()
date = now.strftime('%Y-%m-%d')
time = now.strftime('%H:%M')
german_date = now.strftime('%d.%m.%Y')

# connect with website
r = requests.get('https://www.stadt-muenster.de/tiefbauamt/parkleitsystem')
print("status of request (should be 200):")
print(r.status_code)

# get content of interest
soup = BeautifulSoup(r.text, 'html.parser')
parking_table = soup.find('table')('tr')[1:]

titles = []
scores = []
titles.append("Datum und Uhrzeit")
scores.append(german_date + ", " + time)

for i in range(0, len(parking_table)):
  title = parking_table[i]('td', class_='name')[0].text.strip()
  score = parking_table[i]('td', class_='freeCount')[0].text.strip()
  titles.append(title)
  scores.append(score)
print("titles:")
print(titles)
print("scores:")
print(scores)

# write/append to .csv-file
filename = date + ".csv"
print("filename:", filename)
exists = False
if os.path.exists(filename) :
  exists = True
print("exists:", exists)

writer = csv.writer(open(filename, "a"))
if not exists :
  writer.writerow(titles)
  writer.writerow(scores)
else :
  writer.writerow(scores)

