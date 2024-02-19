import requests
from bs4 import BeautifulSoup

url = 'http://wmii.uwm.edu.pl/~mirek/PLANY/'

def check():
    changes = []
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text().split('\n')
    text = [x for x in text if x != '']

    links = []
    for a in soup.find_all('a', href=True):
        links.append(url + a['href'])
    links.pop(2)
    with open("data.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip().split('\t')
            if line[1][-3:] != text[i].strip()[-3:]:
                if line[1][:4] == "I-io":
                    changes.append("I-io: " + links[i])
                elif line[1][:5] == "I-isi":
                    changes.append("I-isi: " + links[i])
                elif line[1][:5] == "II-io":
                    changes.append("II-io: " + links[i])
                elif line[1][:6] == "II-isi":
                    changes.append("II-isi: " + links[i])
                elif line[1][:6] == "III-io":
                    changes.append("III-io: " + links[i])
                elif line[1][:7] == "III-isi":
                    changes.append("III-isi: " + links[i])

    if(changes):
        with open("data.txt", "w", encoding='utf-8') as f:
            for i in range(len(links)):
                f.write(links[i] + '\t' + text[i] + '\n')

    return changes