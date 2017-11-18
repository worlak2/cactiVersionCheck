# Cacti Version Check
script can fingerprint Cacti monitoring system. It's also trying to get a list of known CVE for this version.

python 3 required

## Dependencies
pip install -r requirements.txt

## Usage
usage: check.py [-h] [-H HOST] [-p PORT]

Command-line tool for Cacti version check

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Host to check
  -p PORT, --port PORT  Port on which Cacti is located, default 80
  
  ## Example of use
  
  python3 check.py --host cacti.version.ru
