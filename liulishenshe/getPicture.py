# 导入
import os
from DrissionPage import ChromiumPage
# 创建页面对象
page = ChromiumPage()
def getPictureByUrl(name,url):
    page.new_tab(url)
    items2=page.eles('.alignnone size-full')
    for item in items2:
        b=1
        # print(item.link)
        # 点击按钮触发下载，并设置下载路径和文件名
        # page.download(item.link, f'D:\code\liulishenshe\{name}')
        print(item)
        b+=1
# 访问网页
a = 1
while a<=1:
    page.get(f'https://hacg.zip/wp/category/all/anime/page/{a}')
    # 在页面中查找元素
    items = page.eles('.entry-title')
    # 遍历元素
    for index,item in enumerate(items):
        if index == 0:
            continue  # 跳过第一个元素
        # 获取当前<h3>元素下的<a>元素
        lnk = item('tag:a')
        # 打印<a>元素文本和href属性
        getPictureByUrl(lnk.text, lnk.link)
        # 打印<a>元素文本和href属性
        # print(lnk.text, lnk.link
    a+=1