import os
import sys
import datetime
import config as cfg


# get current date and time
now = datetime.datetime.today()
yesterday = now - datetime.timedelta(days=1)
date = yesterday.strftime('%Y-%m-%d')
filename = date + ".csv"
filename_long = "data/" + filename
add_command = 'git add ' + filename_long
commit_command = 'git commit -m "added parkleitsystem data file"'
push_command = 'git push https://' + cfg.token + '@github.com/tomsrocket/parking-decks-muenster.git'

os.system(add_command)
os.system(commit_command)
os.system(push_command)
