import os
import csv
import six
import requests
from bs4 import BeautifulSoup
from google.cloud import translate_v2 as google_tl
try:
    from local import cert_path
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cert_path
except ImportError:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = input('Input your GOOGLE_APPLICATION_CREDENTIALS:') or ''


drugs_csv = './drugs.csv'
translator = google_tl.Client()
first_line = ['关键词', '含义', '示例']


def get_wiki(item, lang='en', variation='wiki'):
    result = requests.get(f'https://{lang}.wikipedia.org/{variation}/{item}')
    if result.status_code == 200:
        soup = BeautifulSoup(result.text, features='lxml')
        wiki_link = soup.find('link', rel='canonical')['href']
        return wiki_link
    return ''


def translate_from_wiki(wiki, variation='zh-cn'):
    result = requests.get(wiki)
    soup = BeautifulSoup(result.text, features='lxml')
    tr = soup.find('a', lang='zh', class_='interlanguage-link-target')
    if tr:
        zh_result = requests.get(tr['href'].replace('/wiki/', f'/{variation}/'))
        soup = BeautifulSoup(zh_result.text, features='lxml')
        zh = soup.find('h1', id='firstHeading', lang='zh-Hans-CN')
        if zh:
            print('Get Wikipedia result!')
            return zh.text
    return ''


def translate_word(text, source='en', target='zh-CN', wiki=None, return_type=False):
    text = text.decode("utf-8") if isinstance(text, six.binary_type) else text
    # I don't know why, Google says that.
    result = ''
    tr_type = 'n'

    if wiki and 'wiki' in wiki.lower():
        w_result = translate_from_wiki(wiki)
        if w_result:
            result = w_result
            tr_type = 'w'
    if not result:
        t_result = translator.translate(text, target_language=target, source_language=source)
        result = t_result['translatedText']
        tr_type = 'g'

    if return_type:
        return result, tr_type
    else:
        return result


def translate():
    tmp = []
    with open(drugs_csv, encoding='gbk', newline='') as f:
        content = csv.reader(f)
        next(content)
        for row in content:
            tmp.append(row)
    for j in tmp:
        j[0] = f'? ({j[0].replace("–", "")})'
        j[1] = translate_word(j[1])
        temp_j2 = j[2].split(', ')
        for i in range(len(temp_j2)):
            i_wiki = get_wiki(temp_j2[i])
            temp_j2[i] = translate_word(temp_j2[i], wiki=i_wiki)
        j[2] = '；'.join(temp_j2)
        print('Get:', j[0], j[1], j[2])
    with open('drugs-zh.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(first_line)
        writer.writerows(sorted(tmp))
    print('Done')


if __name__ == '__main__':
    translate()
