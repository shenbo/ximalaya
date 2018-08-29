import requests
import sys
from bs4 import BeautifulSoup
import os


# 冬吴同学会 @ 喜马拉雅 API_url
album_url = 'http://www.ximalaya.com/2452186/album/8475135'
json_url = 'http://www.ximalaya.com/tracks/{}.json'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/57.0.2987.133'}


# 获得专辑中的节目列表
def get_mp3_list():
    # 获得专辑名称
    res = requests.get(album_url, headers=headers)
    # soup = BeautifulSoup(res.content, 'lxml')
    soup = BeautifulSoup(res.content, 'html.parser')
    print(soup.title.string)

    # 网页中关于节目描述的div格式
    # <div class="dOi2 text">
    #     <a title="No.0 xxxxxxxxxxx" href="/shangye/8475135/idxxxxxxxx">No.0 xxxxxxxxxx</a>
    # </div>

    # 获得节目列表
    mp3_div = soup.find_all('div',{'class': 'e-2304105070 text'})
    mp3_list = []
    for div in mp3_div:
        # 获得节目名称、ID、JSON
        title = div.a.get('title')
        id = div.a.get('href').split('/')[-1]

        mp3_info = {'title': title, 'id': id}
        mp3_list.append(mp3_info)
    # print('--节目清单--\n',mp3_list)
    return mp3_list

# get_mp3_list()


# 下载单个节目
def download_mp3(id):
    mp3_info = requests.get(json_url.format(id), headers=headers).json()
    # 替换文件名中的特殊字符
    filename = mp3_info['title'].replace('\"', '“').replace(':', '：') + '.m4a'
    path = mp3_info['play_path']

    os.chdir(os.getcwd())
    if os.path.exists(filename):
        return 'Already exists'

    # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    try:
        with open(filename, 'wb') as f:
            response = requests.get(path, stream=True)
            if not response.ok:
                print('response error with', filename)

            total_length = response.headers.get('content-length')
            print(filename, ', file size: ', int(total_length)/1000000.0, ' MB')

            chunk_size = 1024
            for block in response.iter_content(chunk_size):
                f.write(block)
            print('ok ---')

    except Exception as e:
        print('other error with', filename)
        os.remove(filename)

# download_mp3('90460149')


# 下载专辑
def download_ablum(num=1):
    mp3_list = get_mp3_list()
    if len(mp3_list) < num:
        num = len(mp3_list)

    for i in mp3_list[0:num]:
        # print(i['id'])
        download_mp3(i['id'])

# 下载近期节目
download_ablum(5)
