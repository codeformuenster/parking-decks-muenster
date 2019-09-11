"""
read waiting time data from the citizen center of muenster
and write it into a .csv file
"""
import csv
import os
import sys
import datetime
import requests
from bs4 import BeautifulSoup


def main():
    """
    read waiting time data from the citizen center of muenster
    and write it into a .csv file
    """
    # get current date and time
    now = datetime.datetime.today()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M')

    # connect with website
    result = requests.get('https://www.muenster.de/stadt/buergeramt/mobil-wartezeit.shtml')
    if result.status_code != 200:
        print("Request for waiting times failed with status code: {:d}!".format(result.status_code), file=sys.stderr)

    # get waiting time
    soup = BeautifulSoup(result.text, 'html.parser')

    titles = ['Datum und Uhrzeit', 'Anzahl wartender Personen', \
              'durchschnittliche Wartezeit in Minuten', 'nächste Nummer', 'letzte Aktualisierung']
    scores = []
    scores.append(date + " " + time)

    waiting_block = soup.find('div', class_='kasten')
    waiting_list = waiting_block.find_all('p')
    waiting_list_text = waiting_list[0].text.strip()
    night_message = "Das Bürgerbüro Mitte ist zurzeit geschlossen."
    found = waiting_list_text.find(night_message)
    if found == 0:
        print(night_message)
    else:
        num_persons_and_next_number = waiting_list[0].find_all('strong')
        minutes = waiting_list[1].find('strong')
        updated = waiting_list[2].find('strong')
        num_persons = num_persons_and_next_number[0].text.strip()
        next_number = num_persons_and_next_number[1].text.strip()
        waiting_minutes = minutes.text.strip()
        end_of_waiting_minutes = waiting_minutes.find(" ")
        waiting_time = waiting_minutes[:end_of_waiting_minutes]
        last_update_with_seconds = updated.text.strip()
        end_of_hours = last_update_with_seconds.find(":")
        end_of_minutes = last_update_with_seconds.find(":", end_of_hours+1)
        last_update = last_update_with_seconds[:end_of_minutes]
        scores.append(num_persons)
        scores.append(waiting_time)
        scores.append(next_number)
        scores.append(last_update)
        print(scores)

        # write/append to .csv-file
        filename = date + ".csv"
        print("filename:", filename)
        filename_long = "data_citizen_center/" + filename
        print("time:", time)
        exists = os.path.exists(filename_long)
        print("exists:", exists)

        writer = csv.writer(open(filename_long, "a"))
        if not exists:
            writer.writerow(titles)
        writer.writerow(scores)


if __name__ == "__main__":
    main()
