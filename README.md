# GTFObonch

lk.sut.ru *study* Automation

# Install:

Clone repo: `git clone https://github.com/videobitva/GTFObonch.git`

Run install sequence: `sudo bash setup.sh`

Open main.py and fill in BONCH_USERNAME, BONCH_PASSWORD, GOOGLE_USERNAME and GOOGLE_PASSWORD constants.

# Run

Activate venv: `source venv/bin/activate`

Run it: `python -m main.py`

Sample crontabs (from Monday to Saturday, from January to July, from September to December):

`5 9 * 1-7,9-12 1-6`  # every 9:05

`50 10 * 1-7,9-12 1-6`  # every 10:50

`5 13 * 1-7,9-12 1-6`  # every 13:05

`50 14 * 1-7,9-12 1-6`  # every 14:50

`35 16 * 1-7,9-12 1-6`  # every 16:35

To build our own schedule use crontab.guru
