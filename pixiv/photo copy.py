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

download("https://i.pximg.net/img-original/img-master/img/2022/08/02/20/01/23/19386089_p0.jpg")