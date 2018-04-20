import requests
import sys
from bs4 import BeautifulSoup
import os


# 冬吴同学会
album_url = 'http://www.ximalaya.com/2452186/album/8475135'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/57.0.2987.133'}
res = requests.get(album_url, headers=headers)

# 获得专辑名称
# soup = BeautifulSoup(res.content, 'lxml')
soup = BeautifulSoup(res.content, 'html.parser')
print(soup.title.string)

# 获得各期节目ID，生成json链接 
mp3_ids = soup.select_one('.personal_body').attrs['sound_ids']
print('共有{}期节目'.format(len(mp3_ids)))

json_url = 'http://www.ximalaya.com/tracks/{id}.json'
json_urls = [json_url.format(id=i) for i in mp3_ids.split(',')]
# print(json_urls)


def albums_list(num = 10):
    mp3_titles = soup.find_all('a',{'class': 'title'})
    if num > len(mp3_titles):
        num = len(mp3_titles)

    print('--节目清单--')
    for link in mp3_titles[0:num]:
        print(link.get('title'))



def get_mp3_info(js_url):
    mp3_info = requests.get(js_url, headers=headers).json()
    filename = mp3_info['title'].replace('\"', '“').replace(':', '：') + '.m4a'
    path = mp3_info['play_path']
     
    return filename, path


def download(file_name, mp3_path):
    os.chdir(os.getcwd())
    if os.path.exists(file_name):
        return 'Already exists'

    # http://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    try:
        with open(file_name, 'wb') as f:
            response = requests.get(mp3_path, stream=True)
            if not response.ok:
                print('response error with', file_name)

            total_length = response.headers.get('content-length')
            print(file_name, ', file size: ', int(total_length)/1000000.0, ' MB')

            chunk_size = 1024
            for block in response.iter_content(chunk_size):
                f.write(block)
            print('ok ---')

    except Exception as e:
        print('other error with', file_name)
        os.remove(file_name)


def download_ablum(num=3):
    if len(json_urls) < num:
        num = len(json_urls)
    for i in json_urls[0:num]:
        f, p = get_mp3_info(i)
        download(f, p)


hint = '\n >> 请输入命令...\n'\
    '    --d        下载近期节目...\n'\
    '    --l        列出所有节目...\n'\
    ' >> '


cmd = input(hint)
if cmd == 'q':
    sys.exit(1)
elif cmd == 'l':
    albums_list(10)
elif cmd == 'd':
    download_ablum(5)
else :
    pass
