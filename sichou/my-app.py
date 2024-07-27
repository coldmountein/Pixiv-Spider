# 导入
from DrissionPage import SessionPage
# 创建页面对象
page = SessionPage()
# 访问网页
a = 1
while a<=1:
    page.get(f'https://hacg.zip/wp/category/all/anime/page/{a}')
    # 在页面中查找元素
    items = page.eles('.entry-title')
    # 遍历元素
    for item in items:
        # 获取当前<h3>元素下的<a>元素
        lnk = item('tag:a')
        # 打印<a>元素文本和href属性
        print(lnk.text, lnk.link)
    a+=1