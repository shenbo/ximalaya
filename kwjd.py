import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re
import json

# 坑王驾到 @ pengdouw.com
# http://www.pengdouw.com/kengwangjiadao/
album_url = 'http://www.pengdouw.com/kengwangjiadao/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3702.0'}
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
    # print({'title': title, 'href': href})
    mp3_list.append({'title': title, 'href': href})

desp = '\n'
# 获取下载链接
for mp3 in mp3_list[:3]:
    url = 'http://www.pengdouw.com' + mp3['href']
    res = requests.get(url, headers=headers)

    """
    <div class="v_txt">
        <p id="bofang1"><script type="text/javascript">bofang1('m3u8','https://youku.xlabzjx.com/20190223/L7Drbxc3/index.m3u8');</script></p>
        <p id="bofang2"><script type="text/javascript">bofang2('腾讯音频','u0841et002m');</script></p>
        <p id="bofang3"><script type="text/javascript">bofang3('bilibili音频','44487404');</script></p>
    </div>
    <div class="v_right">
        <p id="bofang4"><script type="text/javascript">bofang4('m3u8','https://youku.xlabzjx.com/20190223/L7Drbxc3/index.m3u8');</script></p>
        <p id="bofang5"><script type="text/javascript">bofang5('迅雷','thunder://QUFodHRwOi8veHVubGVpLnp1aWRheHVubGVpLmNvbS8xOTAyL+WdkeeOi+mpvuWIsOesrOS4ieWtozIwMTkwMjIzLm1wNFpa');</script></p>
        <br /><span style="color:#666;">m3u8资源高峰时加载较慢,请耐心等待</span>
        <br /><span style="color:#ff0000;"><strong>本站视频默认播放密码均为pengdouwcom</strong></span>
    </div>
    """
    # soup = BeautifulSoup(res.content, 'html.parser')    # 解析器：'lxml'
    # mp3_p = soup.find('p', {'id': ['bofang3']})         # bilibili
    # mp3_s = mp3_p.script

    # bili_id = mp3_s.get_text().split('\'')[-2]
    # video_url = 'https://www.bilibili.com/video/av' + bili_id
    # print(video_url)

    """
    <div class="v_txt">
        <p id="bofang1"><script type="text/javascript">bofang1('m3u8','https://v2.juhui600.com/20190316/5bsyFpvx/index.m3u8');</script></p>
        <p id="bofang2"><script type="text/javascript">bofang2('优酷音频','XNDEwMDMyMjkyMA==');</script></p>
        <p id="bofang3"><script type="text/javascript">bofang3('m3u8','http://iqiyi.qq-zuidazy.com/20190316/7355_e891b7a4/index.m3u8');</script></p>
    </div>
    <div class="v_right">
        <p id="bofang4"><script type="text/javascript">bofang4('m3u8','https://v2.juhui600.com/20190316/5bsyFpvx/index.m3u8');</script></p>
        <p id="bofang5"><script type="text/javascript">bofang5('迅雷','thunder://QUFodHRwOi8vZG93bmxvYWQueHVubGVpenVpZGEuY29tLzE5MDMv5Z2R546L6am+5Yiw56ys5LiJ5a2jMjAxOTAzMTYubXA0Wlo=');</script></p>
        <br /><span style="color:#666;">m3u8资源高峰时加载较慢,请耐心等待</span>
        <br /><span style="color:#ff0000;"><strong>本站视频默认播放密码均为pengdouwcom</strong></span>
    </div>
    """
    html = res.content.decode('gbk')    
    pattern = re.compile(r'https:\S*.m3u8')
    res = pattern.findall(html)
    video_url = res[0]

    # 系统配置文件 `/etc/youtube-dl.conf`： -o ~/Sync/ytb/%(title)s.%(ext)s
    #
    # -F                    获得所有视频格式
    # -v                    调试模式
    # --get-filename        获得视频名称
    # -x -k                 下载结束后转为音频格式；保留原始视频；
    # --no-post-overwrites  不覆盖已有文件
    #
    # youtube-dl -v -F https://www.bilibili.com/video/av45133914

    cmd = 'youtube-dl -x -k --no-post-overwrites ' + video_url
    print(cmd)
    p = subprocess.Popen(cmd, shell=True)
    print(p)

    desp += '- {}    已下载\n'.format(mp3['title'])

with open('web_monitor/config.json', encoding='utf-8') as f:
        config = json.load(f)
        key = config['ftqq']
        print(key)

        api = 'https://sc.ftqq.com/{}.send'.format(key)
        send_data = {'text': '坑王', 'desp': desp}
        requests.post(api, headers=headers, data=send_data)