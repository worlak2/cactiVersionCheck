import requests
import sys

from bs4 import BeautifulSoup

yourHost = str(input("vvedite host without http\n"))
url = 'https://www.cacti.net/'
r = requests.get(url)
versionText = 'version='
start = r.text.find(versionText)
end = r.text.find('"', start)
finalVersion = r.text[start + len(versionText):end]
url = 'https://www.cacti.net/changelog.php'
r = requests.get(url)


def get_all_vrsion(html):
    soup = BeautifulSoup(html, 'lxml')
    version = soup.find_all('td', class_='textParagraphHeading')
    return version


if (requests.get("http://" + yourHost + "/cacti/install/").status_code == 200):
    yourHost = yourHost + "/cacti/install/"
else:
    yourHost = yourHost + "/install/"
ark = get_all_vrsion(r.text)
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
cactiversion = ""

while i < final.__len__():
    sys.stderr.write('%d\r' % i)
    if final[i] == finalVersion:
        break
    if final[i] == "0.8.8":
        while d != 8:
            sendtourl = "0_8_8" + "_" + "to_" + final[i + 1].replace(".", "_") + ".php"
            r = requests.get("http://" + yourHost + sendtourl.replace(" ", ""))
            if r.status_code == 200:
                cactiversion = sendtourl.replace(" ", "")
            d += 1
            i += 1
    sendtourl = final[i].replace(".", "_") + "_" + "to_" + final[i + 1].replace(".", "_") + ".php"
    r = requests.get("http://" + yourHost + sendtourl.replace(" ", ""))
    if r.status_code == 200:
        cactiversion = sendtourl.replace(" ", "")
    i += 1

totext = cactiversion.find("to_")
print(cactiversion)
print("your version\n" + cactiversion[totext + 3:-4].replace("_", "."))
