import requests
import sys
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup
from vulners import Vulners

requests.packages.urllib3.disable_warnings()

__author__ = 'worlak2 & Cibvetr'
__version__ = '0.1'

parser = \
    argparse.ArgumentParser(description='Command-line tool for Cacti version check'
                            )
parser.add_argument('-H', '--host', help='Host to check', type=str)
parser.add_argument('-p', '--port',
                    help='Port on which Cacti is located', type=str)
args = parser.parse_args()
vulners_api = Vulners()

if args.host is None:
    print(
        'See help -h --help')
    sys.exit()
else:
    yourHost = args.host
if args.port is None:
    port = '80'
else:
    port = args.port

url = 'https://www.cacti.net/'
r = requests.get(url, verify=False)
versionText = 'version='
start = r.text.find(versionText)
end = r.text.find('"', start)
finalVersion = r.text[start + len(versionText):end]
url = 'https://www.cacti.net/changelog.php'
r = requests.get(url, verify=False)


# noinspection PyShadowingNames

def get_all_version(html):
    soup = BeautifulSoup(html, 'lxml')
    version = soup.find_all('td', class_='textParagraphHeading')
    return version


ark = get_all_version(r.text)
textt = ''
textt += str(ark)
new = textt.replace('</td>, <td class="textParagraphHeading">', '')
new1 = new.replace('</td>]', '')
new = new1.replace('[<td class="textParagraphHeading">', '')
final = new.replace('\t', '')
final1 = final.replace(' ', '')
final = final1.split('\n')
final.insert(0, finalVersion)
final.remove('')
i = 0
d = 0
final.reverse()

cactiversion = ''
version = ''
end = final.index('1.1.0')


# before 1.0.1

# noinspection PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames

def before(your_host):
    global cactiversion
    for i in tqdm(range(end)):
        d = 0
        if final[i] == finalVersion:
            break
        if final[i] == '0.8.8':
            while d != 8:
                sendtourl = '0_8_8' + '_' + 'to_' + final[i
                                                          + 1].replace('.', '_') + '.php'
                r = requests.get('http://' + your_host
                                 + sendtourl.replace(' ', ''))
                if r.status_code == 200:
                    cactiversion = sendtourl.replace(' ', '')
                d += 1
                i += 1
        sendtourl = final[i].replace('.', '_') + '_' + 'to_' + final[i
                                                                     + 1].replace('.', '_') + '.php'
        r = requests.get('http://' + your_host + sendtourl.replace(' ',
                                                                   ''))
        if r.status_code == 200:
            cactiversion = sendtourl.replace(' ', '')

    totext = cactiversion.find('to_')
    print(
        'your version\n' + cactiversion[totext + 3:-4].replace('_',
                                                               '.'))
    version = cactiversion[totext + 3:-4].replace('_', '.')
    return version


# noinspection PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames,PyShadowingNames

def new_fast(your_host):
    global cactiversion
    for i in tqdm(range(end, final.__len__())):
        sendtourl = final[i].replace('.', '_') + '.php'
        r = requests.get('http://' + your_host + sendtourl.replace(' ',
                                                                   ''))
        if r.status_code == 200:
            cactiversion = sendtourl.replace(' ', '')
    finalise = cactiversion.replace('_', '.')
    finalise = finalise.replace('.php', '')
    preend = final.index(finalise)

    # print('your version\n' + final[preend + 1])

    version = final[preend + 1]
    return version


def fastcheck(yourhost):
    fastcheck = requests.get(yourhost, verify=False)
    position = fastcheck.text.find('Version')
    if position != -1:
        maybeversion = fastcheck.text[position + 8:position + 15]
        return maybeversion


def bugs(version):
    exceptions = 0
    end = final.index(version)
    for i in range(end, end + 7):
        try:
            results = vulners_api.softwareVulnerabilities('Cacti',
                                                          final[i])
            vulnerabilities_list = [results.get(key) for key in results
                                    if key not in ['info', 'blog',
                                                   'bugbounty']]
            for i in vulnerabilities_list:
                for j in i:
                    print(
                        j['description'] + '\n' + j['href'] + '\n')
        except Exception:
            exceptions += 1
    if exceptions == 7:
        print(
            'Nothing')


if requests.get('http://' + yourHost + ':' + port + '/cacti/install/'
                ).status_code == 200:
    maybe = fastcheck('http://' + yourHost + ':' + port + '/cacti/')
    if requests.get('http://' + yourHost + ':' + port
                            + '/cacti/install/upgrades/').status_code == 200:
        yourHost = yourHost + ':' + port + '/cacti/install/upgrades/'
        version = new_fast(yourHost)
    else:
        yourHost = yourHost + ':' + port + '/cacti/install/'
        version = before(yourHost)
else:

    maybe = fastcheck('http://' + yourHost + ':' + port + '/')
    if requests.get('http://' + yourHost + ':' + port
                            + '/install/upgrades/').status_code == 200:
        yourHost = yourHost + ':' + port + '/install/upgrades/'
        version = new_fast(yourHost)
    else:
        yourHost = yourHost + ':' + port + '/install/'
        version = before(yourHost)

# noinspection PyBroadException

print(
    '\nVersion to fast Check ' + str(maybe) \
    + '\nVersion to file check ' + str(version))

if str(version) != str(maybe):
    try:

        results = vulners_api.softwareVulnerabilities('Cacti',
                                                      str(maybe))
        vulnerabilities_list = [results.get(key) for key in results
                                if key not in ['info', 'blog',
                                               'bugbounty']]
        print
        '\n' + 'Vulnerability' + '\n'
        for i in vulnerabilities_list:
            for j in i:
                print(
                    j['description'] + '\n' + j['href'] + '\n')
    except Exception:
        None

try:
    print(
        '\n' + 'Vulnerability' + '\n')
    results = vulners_api.softwareVulnerabilities('Cacti', str(version))
    vulnerabilities_list = [results.get(key) for key in results if key
                            not in ['info', 'blog', 'bugbounty']]
    for i in vulnerabilities_list:
        for j in i:
            print(
                j['description'] + '\n' + j['href'] + '\n')
except Exception:
    print(
        'Nothing for this version')
    print(
        '\nCan you want to know about bugs in new versions of cacti?')
    somebugs = str(input('Enter Y if you want , or N' + '\n'))
    if somebugs == 'Y' or somebugs == 'y':
        bugs(version)
    elif somebugs == 'N' or somebugs == 'n':
        print(
            'No')
    else:
        print(
            'not work this command')
