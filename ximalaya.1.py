import os

import requests
from bs4 import BeautifulSoup

# 冬吴同学会 @ 喜马拉雅 API_url
album_url = 'https://www.ximalaya.com/shangye/8475135/'  # 第一季
album_url = 'https://www.ximalaya.com/shangye/16861863/'  # 第二季
json_url = 'http://www.ximalaya.com/tracks/{}.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}


# 获得专辑中的节目列表
def get_mp3_list():
    res = requests.get(album_url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')  # 解析器：'lxml'
    print(soup.title.string)  # 获得专辑名称

    # 网页中关于节目描述的div格式
    # <div class="text xxxx">
    #     <a title="No.0 xxxxxxxxxxx" href="/shangye/xxxxx/xxxxx">No.0 xxxxxxxxxx</a>
    # </div>

    # 获得节目列表
    mp3_list = []

    mp3_div = soup.find_all('div', {'class': ['text', ' ']})
    for div in mp3_div:
        title = div.a.get('title')  # 获得节目名称
        id = div.a.get('href').split('/')[-1]  # 获得节目ID
        mp3_list.append({'title': title, 'id': id})

    if mp3_list:
        print('--节目清单--\n', mp3_list[0:5])
    else:
        print('-没发现节目!-\n', mp3_div[0:5], '-------\n')

    return mp3_list


# 下载单个节目
def download_mp3(id):
    mp3_info = requests.get(json_url.format(id), headers=headers).json()
    # 替换文件名中的特殊字符
    title = mp3_info['title'].replace('\"', '“').replace(':', '：')
    filename = '{}.m4a'.format(title)
    filename = 'Sync/mp3/{}.m4a'.format(title)
    path = mp3_info['play_path']

    if os.path.exists(filename):
        return '- {}    已存在\n'.format(title)

    # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    try:
        with open(filename, 'wb') as f:
            response = requests.get(path, stream=True)
            print(path)
            filesize = int(response.headers.get('content-length')) / 1000000.0
            print('--- 正在下载 {} : {.2f} MB'.format(filename, filesize))

            for block in response.iter_content(1024):       # chunk_size = 1024
                f.write(block)
            return '- {}    已下载\n'.format(title)

    except Exception as e:
        os.remove(filename)
        return '- {}    下载出错\n'.format(title)


# 下载专辑
def download_ablum(num=1):
    lst = get_mp3_list()
    # print(lst)
    num = min(len(lst), num)

    desp = '\n'
    for i in lst[0:num]:
        # print(i['id'])
        desp += download_mp3(i['id'])
    print(desp)
    
    with open('web_monitor/config.json', encoding='utf-8') as f:
        config = json.load(f)
        key = config['ftqq']
        print(key)

        api = 'https://sc.ftqq.com/{}.send'.format(key)
        send_data = {'text': '冬吴_喜马拉雅', 'desp': desp}
        requests.post(api, headers=headers, data=send_data)


# 下载近期节目
download_ablum(5)
