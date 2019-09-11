"""
automatic commit of daily parkleitsystem and waiting time data .csv file
"""
import os
import datetime
import config as cfg


def main():
    """
    automatic commit of daily parkleitsystem data
    and of daily waiting time data in the citizen center of Muenster
    to github
    """
    # get current date and time
    now = datetime.datetime.today()
    yesterday = now - datetime.timedelta(days=1)
    date = yesterday.strftime('%Y-%m-%d')
    filename = date + ".csv"
    filename_long_parkleitsystem = "data/" + filename
    filename_long_waiting_time = "data_citizen_center/" + filename
    add_command = 'git add ' + filename_long_parkleitsystem + ' ' + filename_long_waiting_time
    commit_command = 'git commit -m "added parkleitsystem and waiting time data files"'
    push_command = 'git push https://' + cfg.token + '@github.com/codeformuenster/parking-decks-muenster.git'

    os.system(add_command)
    os.system(commit_command)
    os.system(push_command)


if __name__ == "__main__":
    main()
