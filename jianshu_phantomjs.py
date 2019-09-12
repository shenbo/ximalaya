"""
shenbo @ jianshu
2019-08-03
"""
import random
import time

from bs4 import BeautifulSoup
from selenium import webdriver

# jianshu url
user_url = 'https://www.jianshu.com/u/273123e8cd8a'
blog_url = 'https://www.jianshu.com/p/'

# phantomjs path
phantomjs_path = r"C:\Users\shenbo\scoop\apps\PhantomJS\current\bin\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=phantomjs_path)

driver.get(user_url)

# == get blogs number ==
soup = BeautifulSoup(driver.page_source, 'html.parser')
div_all = soup.find_all('div', {'class': ['meta-block']})
blogs_num = div_all[2].a.p.text
print(f' 一共有 {blogs_num} 篇博客！ \n')


# == loading all pages. ( 9 bolgs per page ) ==
for i in range(int(blogs_num)//9 + 1):
    driver.execute_script('window.scrollBy(0, document.body.scrollHeight)')
    time.sleep(3)

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
# print(soup.contents)

# == get all blogs url ==
blog_list = []
tag_list = soup.find_all('a', {'class': ['title']})
for tag in tag_list:
    title = tag.text                             # blog 名称
    id = tag.get('href').split('/')[-1]          # blog id
    blog_list.append({'title': title, 'id': id})

print('-' * 10)
print('\n'.join([b['title'] for b in blog_list]))
print('-' * 10)

# ====== 读取 blog 页面 ======
newlist = blog_list * 100
random.shuffle(newlist)
newlist = newlist[::7]

for i, blog in enumerate(newlist):
    url = blog_url + blog['id']
    driver.get(url)
    print(f'- {i+1}/{len(newlist)}  {url}  {driver.title}')

    time.sleep(random.random() + 0.2)
driver.close()
driver.quit()

