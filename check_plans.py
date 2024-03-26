import requests
import re

basic = True


def check():
    url = 'http://wmii.uwm.edu.pl/~mirek/PLANY/'
    path = './data/plany'
    changes = []
    pdf_time = []
    pdf_r_time = []
    response = requests.get(url)
    try:
        with open(f'{path}/time.txt', 'r') as f:
            for lines in f.readlines():
                pdf_r_time.append(lines)
    except Exception as e:
        print(f'Error {e}')
    if response.status_code == 200:
        html_content = response.text
        url_match = re.findall('<a.*?href="(.*?)">(.*?)</a>.*?align="right">(.*?)</td>.*?&nbsp;', html_content)
        for i, link in enumerate(url_match):
            if i == 0:
                continue
            else:
                pdf_time.append(f'{link[0]} {link[2]}\n')
                if not basic:
                    try:
                        pdf_response = requests.get(
                            f'{url}{link[0]}')  # to można usunąć w wersji basic ale jak już tu jest to niech zosdtanie
                        if pdf_response.status_code == 200:
                            pdf_content = pdf_response.content
                            with open(f'{path}/{link[0]}', 'wb') as f:
                                f.write(pdf_content)
                    except Exception as e:
                        print(f'Error {e}')
                try:
                    for iv, line in enumerate(pdf_r_time):  # enumerate na przyszłość
                        link_r = line.split(' ')
                        if link[0] == link_r[0] and link[2].split(' ')[0] != link_r[1]:
                            changes.append(f'{url}{link[0]}+{link[1]}+{link[2]}')
                except Exception as e:
                    print(f'Error {e}')
        with open(f'{path}/time.txt', 'w') as f:
            f.writelines(pdf_time)
    else:
        print(f'Error, response status: {response.status_code}')
    if changes:
        print(f'Changes found: {len(changes)}')
    return changes


def main():
    check()


if __name__ == '__main__':
    main()