"""
read parkleitsystem data and write
it into a .csv file
"""
import csv
import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup


def main():
    """
    read parkleitsystem data and write
    it into a .csv file
    """
    # get current date and time
    now = datetime.datetime.today()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M')

    # connect with website
    result = requests.get('https://www.stadt-muenster.de/ms/tiefbauamt/pls/PLS-INet.xml', timeout=60)
    result.encoding = result.apparent_encoding
    if result.status_code != 200:
        print("Request failed with status code: {:d}!".format(result.status_code), file=sys.stderr)

    # get parking table
    soup = BeautifulSoup(result.content, 'xml')
    parking_list = soup.find('parkhaeuser')('parkhaus')

    titles_mapping = {
        'Parkhaus PH Coesfelder Kreuz': 'PH Coesfelder Kreuz',
        'Parkhaus Theater': 'PH Theater',
        'Parkplatz Hörster Platz': 'PP Hörsterplatz',
        'Parkhaus Alter Steinweg': 'PH Alter Steinweg',
        'Parkplatz Busparkplatz': 'Busparkplatz',
        'Parkplatz Schlossplatz Nord': 'PP Schlossplatz Nord',
        'Parkplatz Schlossplatz Süd': 'PP Schlossplatz Süd',
        'Parkhaus Aegidii': 'PH Aegidii',
        'Parkplatz Georgskommende': 'PP Georgskommende',
        'Parkhaus Münster-Arkaden': 'PH Münster Arkaden',
        'Parkhaus Karstadt': 'PH Karstadt',
        'Parkhaus Stubengasse': 'PH Stubengasse',
        'Parkhaus Bremer Platz': 'PH Bremer Platz',
        'Parkhaus Engelenschanze': 'PH Engelenschanze',
        'Parkhaus Bahnhofstraße': 'PH Bahnhofstraße',
        'Parkhaus Cineplex': 'PH Cineplex',
        'Parkhaus PH Stadthaus 3': 'PH Stadthaus 3'
    }

    titles = []
    scores = []
    capacities = []
    titles.append("Datum und Uhrzeit")
    scores.append(date + " " + time)
    capacities.append("Anzahl Parkplätze gesamt")


    scores_cache = {}
    gesamt_cache = {}
    for row in parking_list:
        title = row.bezeichnung.text.strip()
        score = int(row.frei.text.strip())
        status = row.status.text.strip()
        capa = row.gesamt.text.strip()
        if status != "frei":
            score = status[0:3]
        if title in titles_mapping:
            scores_cache[title] = score
            gesamt_cache[title] = capa
        else:
            print("UNKNOWN TITLE " + title)
            raise ValueError("beep")

    for key, val in titles_mapping.items():
        titles.append(val)
        scores.append(scores_cache[key])
        capacities.append(f'({gesamt_cache[key]})')

    print("scores:")
    print(scores)
    print("titles:")
    print(titles)


    # write/append to .csv-file
    filename = date + ".csv"
    print("filename:", filename)
    filename_long = "data/" + filename
    print("time:", time)
    exists = os.path.exists(filename_long)
    print("exists:", exists)

    writer = csv.writer(open(filename_long, "a"), quoting=csv.QUOTE_NONNUMERIC)
    if not exists:
        writer.writerow(titles)
        writer.writerow(capacities)
    writer.writerow(scores)


if __name__ == "__main__":
    main()
