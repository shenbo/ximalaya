import os
import subprocess
import requests
from bs4 import BeautifulSoup


# 坑王驾到 @ pengdouw.com
# http://www.pengdouw.com/kengwangjiadao/
album_url = 'http://www.pengdouw.com/kengwangjiadao/' 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3702.0'}
res = requests.get(album_url, headers=headers)
# print(res.content.decode('gbk'))

soup = BeautifulSoup(res.content, 'html.parser')    # 解析器：'lxml'
print(soup.title.string)                            # 获得专辑名称

# 获得节目列表
mp3_list = []
mp3_div = soup.find('div', {'class': ['index_middle_c']})
mp3_a = mp3_div.ul.find_all('a')

for a in mp3_a[1::2]:
    title = a.get('title')
    href = a.get('href')
    print({'title': title, 'href': href})
    mp3_list.append({'title': title, 'href': href})

# 获取下载链接
for mp3 in mp3_list[:2]:
    url = 'http://www.pengdouw.com' + mp3['href']
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')    # 解析器：'lxml'
    mp3_p = soup.find('p', {'id': ['bofang3']})         # bilibili
    mp3_s = mp3_p.script

    bili_id = mp3_s.get_text().split('\'')[-2]
    bili_url = 'https://www.bilibili.com/video/av' + bili_id
    print(bili_url)

    # 系统配置文件 `/etc/youtube-dl.conf`： -o ~/Sync/ytb/%(title)s.%(ext)s
    # 
    # -F                    获得所有视频格式
    # -v                    调试模式
    # --get-filename        获得视频名称
    # -x -k                 下载结束后转为音频格式；保留原始视频；
    # --no-post-overwrites  不覆盖已有文件
    #
    # youtube-dl -v -F https://www.bilibili.com/video/av45133914
    
    cmd = 'youtube-dl -x -k --no-post-overwrites ' + bili_url
    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    print(p)
