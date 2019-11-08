import json
import os
import subprocess

import requests
from bs4 import BeautifulSoup

# 冬吴同学会 @ 喜马拉雅 API_url
album_url = 'https://www.ximalaya.com/shangye/8475135/'  # 第一季
album_url = 'https://www.ximalaya.com/shangye/16861863/'  # 第二季

json_url = 'http://www.ximalaya.com/tracks/{}.json'  # API_url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
}


# 获得专辑中的节目列表
def get_mp3_list(album=album_url):
    res = requests.get(album, headers=headers)
    # 指定解析器： 'html.parser', 或 'lxml' 等
    soup = BeautifulSoup(res.content, 'html.parser')
    print(soup.title.string)  # 获得专辑名称

    # 获得节目列表
    mp3_list = []
    # outer div
    DIV = soup.find(
        'div', {'class': ['sound-list-wrapper', ' '], 'id': ['anchor_sound_list']}
    )
    #
    divs = DIV.find_all_next('div', {'class': ['text', ' ']})

    for div in divs:
        title = div.a.get('title')  # 获得节目名称
        pid = div.a.get('href').split('/')[-1]  # 获得节目ID
        mp3_list.append({'title': title, 'pid': pid})

    if mp3_list:
        print('--节目清单--\n', mp3_list[0:5])
    else:
        print('-没发现节目!-\n', '---------\n')
        print(DIV, '---------\n')
        print(divs, '---------\n')

    return mp3_list


# 下载单个节目 -- by aria2 --
def download_mp3(pid):
    mp3_info = requests.get(json_url.format(pid), headers=headers).json()

    # 替换文件名中的特殊字符
    title = mp3_info['title'].replace('"', '“').replace(':', '：')
    mp3_url = mp3_info['play_path']

    filepath = 'MP3/'
    filename = f'{title}.m4a'

    if os.path.exists(filepath + filename):
        return f'- {title}    已存在\n'

    # 用 aira2 下载
    cmd = f'aria2c {mp3_url} -d {filepath} -o "{filename}"'

    retcode = subprocess.call(cmd, shell=True)
    if not retcode:
        return f'- {title}  已下载\n'
    else:
        os.remove(filepath + filename)
        return f'- {title}  下载出错:\n- {retcode}\n'


# 下载专辑
def download_ablum(lst=[], num=1):
    # print(lst)
    num = min(len(lst), num)

    desp = '\n'
    for i in lst[0:num]:
        # print(i['pid'])
        desp += download_mp3(i['pid'])
    print(desp)
    return desp


# 推送下载信息到手机 -- by ftqq --
def ftqq_alert(text, desp):
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)
        key = config['ftqq']
        print(key)

        api = 'https://sc.ftqq.com/{}.send'.format(key)
        send_data = {'text': text, 'desp': desp}
        x = requests.post(api, headers=headers, data=send_data)
        print(x)


# 下载近期节目
mp3_list = get_mp3_list()

msg = download_ablum(lst=mp3_list, num=5)

# ftqq_alert(text='冬吴_喜马拉雅', desp=msg)
