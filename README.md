# parking-decks-muenster
History of parking deck data

### Steps for reading the parkleitsystem data from [here](https://www.stadt-muenster.de/tiefbauamt/parkleitsystem) and writing the data into a .csv file:
* Install dependencies, i.e. the python package BeautifulSoup:
  ```
  pip3 install bs4
  ```
* Call the read_parkleitsystem_data script:
  ```
  python3 read_parkleitsystem_data.py
  ```

### Steps for commiting the .csv file into the "data" folder on GitHub:
* Generate a "personal access token" on GitHub: <br />
  Go to your GitHub account "Settings", then "Developer Settings", "Personal access tokens" and "Generate new token".
* Generate a file "config.py" (like [config.dist.py](https://github.com/codeformuenster/parking-decks-muenster/blob/master/config.dist.py)) and copy your personal access token into the file. <br />
  **Note: Treat your personal access token like a password and NEVER check in your config.py.**
* Switch the remote URL of your cloned parking-decks-muenster repository to HTTPS (if cloned with SSH): <br />
  command is ``git remote set-url``; see [this explanation](https://help.github.com/en/articles/changing-a-remotes-url#switching-remote-urls-from-ssh-to-https))
* Call the auto_commit script:
  ```
  python3 auto_commit.py
  ```

