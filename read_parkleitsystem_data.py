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
    result = requests.get('https://www.stadt-muenster.de/tiefbauamt/parkleitsystem')
    if result.status_code != 200:
        print("Request failed with status code: {:d}!".format(result.status_code), file=sys.stderr)

    # get parking table
    soup = BeautifulSoup(result.text, 'html.parser')
    parking_table = soup.find('div', id='parkingList')('table')
    parking_list = None
    for table in parking_table:
        parking_list = table('tr')[1:]

    titles_for_comparison = ['Datum und Uhrzeit', 'PH Theater', \
                             'PP Hörsterplatz', 'PH Alter Steinweg', \
                             'Busparkplatz', 'PP Schlossplatz Nord', \
                             'PP Schlossplatz Süd', 'PH Aegidii', \
                             'PP Georgskommende', 'PH Münster Arkaden', \
                             'PH Karstadt', 'PH Stubengasse', \
                             'PH Bremer Platz', 'PH Engelenschanze', \
                             'PH Bahnhofstraße', 'PH Cineplex', 'PH Stadthaus 3']
    titles = []
    scores = []
    titles.append("Datum und Uhrzeit")
    scores.append(date + " " + time)

    for row in parking_list:
        title = row('td', class_='name')[0].text.strip()
        score = row('td', class_='freeCount')[0].text.strip()
        titles.append(title)
        scores.append(score)
    print("titles:")
    print(titles)
    print("scores:")
    print(scores)
    if titles != titles_for_comparison:
        if len(titles) > len(titles_for_comparison):
            print("Number of parking decks increased!", file=sys.stderr)
        elif len(titles) < len(titles_for_comparison):
            print("Number of parking decks decreased!", file=sys.stderr)
        else:
            print("Order or of parking decks changed!", file=sys.stderr)

    # write/append to .csv-file
    filename = date + ".csv"
    print("filename:", filename)
    exists = os.path.exists(filename)
    print("exists:", exists)

    writer = csv.writer(open(filename, "a"))
    if not exists:
        writer.writerow(titles)
    writer.writerow(scores)


if __name__ == "__main__":
    main()
