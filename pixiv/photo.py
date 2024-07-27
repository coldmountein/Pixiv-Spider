# 导入
from DrissionPage import ChromiumPage
# 创建页面对象
page = ChromiumPage()

def download(url):
    save_path = r'C:\Users\123\Desktop\code\code\pixiv\SMOKE'
    res = page.download(url, save_path)
    print(res)

def singlePageDownload(url):
    page.get(url)
    try:
        btn = page.ele('.sc-emr523-0 guczbC')
        btn.click()
    except:
        print("danzhang")
    item = page.ele('.sc-1qpw8k9-3 ilIMcK gtm-expand-full-size-illust')
    try:
        download(item.link)
    except:
        print("shibai")
# 创建一个空列表
my_array = []
# 访问网页
# 开始网页
a = 1
b=0
# 总页数
while a<=2:
    page.get(f'https://www.pixiv.net/users/2784396/artworks?p={a}')
    # 在页面中查找元素
    items = page.eles('.sc-d98f2c-0 sc-iasfms-6 bOcolJ')
    # 遍历元素
    for item in items:
        # 打印<a>元素文本和href属性
        my_array.append(item.link)
    a+=1
for items in my_array:
#     page.get(my_array[b])
    
    singlePageDownload(my_array[b])
    b+=1
