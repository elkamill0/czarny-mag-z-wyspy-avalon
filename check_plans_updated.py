import requests
from bs4 import BeautifulSoup

url = 'http://wmii.uwm.edu.pl/~mirek/PLANY/'

def check():
    changes = []
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text().split('\n')
    text = [x.strip() for x in text if x != '']

    with open("data.txt", "r", encoding='utf-8') as f:
        lines = f.readlines()

        links = [x.strip().split('\t')[0] for x in lines]
        lines = [x.strip().split('\t')[1] for x in lines]
        print(lines)
        print(text)
        iteration = 0
        for l in lines:
            if l not in text:
                changes.append(l.split(" ")[0] + " " + " " + links[iteration])
            iteration+=1
    if(changes):
        with open("data.txt", "w", encoding='utf-8') as f:
            for i in range(len(links)):
                f.write(links[i] + '\t' + text[i] + '\n')

    return changes