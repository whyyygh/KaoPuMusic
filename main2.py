import requests
import os
import re
import io
from math import ceil
from PIL import Image

requests.packages.urllib3.disable_warnings()

"""
可以下载到文件网站内部定义信息
eopn文件
pdf五线谱和简谱
"""
# todo 可以继续改进下载midi 文件，要录串发现链接

while True:
    song_id = input('input id: ')
    info = requests.get('https://www.everyonepiano.com/members/eopn1.php?id=' + song_id, verify=False).text

    print(info)
    print()

    song_id = int(song_id)
    info_ori = info
    info = info.split('\n')

    title = re.sub('[^a-zA-Z\-]+', '', info[3].split('=')[-1].replace(' ', '-'))
    code = info[-2].split('=')[-1][6:].lower()

    os.makedirs('downloads/%s' % (title.lower()), exist_ok=True)

    with io.open('downloads/%s/%d.txt' % (title.lower(), song_id), 'w', encoding='utf8') as f:
        f.write('\n'.join(info))

    print(title)
    print(code)
    print()

    # eopn midi mid

    url = 'https://www.everyonepiano.com/pianomusic/%03d/%07d/down/%07d-%s.eopn' % (ceil(song_id / 1000), song_id, song_id, code)
    print(url)
    print()
# https://www.everyonepiano.com/midi/001/0000100/down/0000100-02dpn2.mid

    eopn = requests.get(url, verify=False)

    with open('downloads/%s/%s.eopn' % (title.lower(), title.lower()), 'wb') as f:
        f.write(eopn.content)

    print("downloaded eopn successfully")
    print()

    url = 'https://www.everyonepiano.com/Music-%d-%s.html' % (song_id, title)
    print(url)
    page = requests.get(url, verify=False)

    print('html size:', len(page.text))

    sheet_n = len(page.text.split('-w-s-')) - 1
    numeric_n = len(page.text.split('-j-s-')) - 1

    print('sheet pages:', sheet_n)
    print('numeric pages:', numeric_n)
    print()

    sheets = []
    for i in range(1, sheet_n + 1):
        url = 'https://www.everyonepiano.com/pianomusic/%03d/%07d/%07d-w-b-%d.png' % (
        ceil(song_id / 1000), song_id, song_id, i)
        print(url)
        response = requests.get(url, verify=False)
        sheets.append(Image.open(io.BytesIO(response.content)).convert('RGB'))
    print()

    sheets[0].save('./downloads/%s/%s-sheet.pdf' % (title.lower(), title.lower()), save_all=True,
                   append_images=sheets[1:])
    print('downloaded sheet music pdf succesfully')
    print()

    numerics = []
    for i in range(1, numeric_n + 1):
        url = 'https://www.everyonepiano.com/pianomusic/%03d/%07d/%07d-j-b-%d.png' % (
        ceil(song_id / 1000), song_id, song_id, i)
        print(url)
        response = requests.get(url, verify=False)
        numerics.append(Image.open(io.BytesIO(response.content)).convert('RGB'))
    print()

    numerics[0].save('./downloads/%s/%s-jianpu.pdf' % (title.lower(), title.lower()), save_all=True,
                     append_images=numerics[1:])
    print('downloaded jianpu pdf succesfully')
    print()