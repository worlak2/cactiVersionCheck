import requests
import sys
import argparse
from tqdm import tqdm
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup

__author__ = 'worlak2 & Cibvetr'
__version__ = '0.1'

parser = argparse.ArgumentParser(
    description='Command-line tool for Cacti version check')
parser.add_argument('-H', '--host', help='Host to check', type=str)
parser.add_argument(
    '-p',
    '--port',
    help='Port on which Cacti is located',
    type=str)
args = parser.parse_args()

if args.host is None:
    print('See help -h --help')
    sys.exit()
else:
    yourHost = args.host
if args.port is None:
    port = '80'
else:
    port = args.port

url = 'https://www.cacti.net/'
r = requests.get(url,verify=False)
versionText = 'version='
start = r.text.find(versionText)
end = r.text.find('"', start)
finalVersion = r.text[start + len(versionText):end]
url = 'https://www.cacti.net/changelog.php'
r = requests.get(url,verify=False)


def get_all_version(html):
    soup = BeautifulSoup(html, 'lxml')
    version = soup.find_all('td', class_='textParagraphHeading')
    return version


if requests.get('http://' + yourHost + ':' + port +
                '/cacti/install/').status_code == 200:
    yourHost = yourHost + ':' + port + '/cacti/install/'
else:
    yourHost = yourHost + ':' + port + '/install/'

ark = get_all_version(r.text)
textt = ''
textt += str(ark)
new = textt.replace('</td>, <td class="textParagraphHeading">', '')
new1 = new.replace('</td>]', '')
new = new1.replace('[<td class="textParagraphHeading">', '')
final = new.replace('\t', '')
final = final.split('\n')
final.insert(0, finalVersion)
final.remove('')
i = 0
d = 0
final.reverse()
cactiversion = ''

for i in tqdm(range(final.__len__())):

    if final[i] == finalVersion:
        break
    if final[i] == '0.8.8':
        while d != 8:
            sendtourl = '0_8_8' + '_' + 'to_' + \
                final[i + 1].replace('.', '_') + '.php'
            r = requests.get('http://' + yourHost + sendtourl.replace(' ', ''))
            if r.status_code == 200:
                cactiversion = sendtourl.replace(' ', '')
            d += 1
            i += 1
    sendtourl = final[i].replace('.', '_') + '_' + \
        'to_' + final[i + 1].replace('.', '_') + '.php'
    r = requests.get('http://' + yourHost + sendtourl.replace(' ', ''))
    if r.status_code == 200:
        cactiversion = sendtourl.replace(' ', '')
    i += 1

totext = cactiversion.find('to_')
print("\n"+cactiversion)
print('your version\n' + cactiversion[totext + 3:-4].replace('_', '.'))
