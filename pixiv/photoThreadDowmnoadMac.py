# 导入
from DrissionPage import ChromiumPage
# 创建页面对象
page = ChromiumPage()
import os
import threading
from concurrent.futures import ThreadPoolExecutor

def download(url, author):
    save_path = f'/Users/jbos/Downloads/pixiv/{author}'
    try:
        res = page.download(url, save_path)
        if res[0]:
            print(f"Downloaded {url}: {res[1]}")
        else:
            print(f"Failed to download {url}: {res[1]}")
            # 如果下载失败，尝试将文件类型从 jpg 改为 png 再次下载
            if url.endswith(".jpg"):
                new_url = url.replace(".jpg", ".png")
                print(f"Retrying with {new_url}")
                res = page.download(new_url, save_path)
                if res[0]:
                    print(f"Downloaded {new_url}: {res[1]}")
                else:
                    print(f"Failed to download {new_url}: {res[1]}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def multi_thread_download(urls, author, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        threads = [executor.submit(download, url, author) for url in urls]
        for thread in threads:
            thread.result()
    print("All downloads completed.")

def convert_url(original_url):
    # 替换部分内容
    converted_url = original_url.replace("/c/250x250_80_a2/img-master/", "/img-original/")
    converted_url = converted_url.replace("_square1200", "")
    return converted_url

# 创建一个空列表
my_array = []
# 访问网页

# 在这里填入作者编号
author="5375417"

# 创建保存文件的文件夹
save_folder = f'/Users/jbos/Downloads/pixiv/{author}'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 开始网页
a = 1
# 总页数
while a <= 14:
    page.get(f'https://www.pixiv.net/users/{author}/artworks?p={a}')
    # 在页面中查找元素
    items = page.eles('.sc-rp5asc-9 itpOYX')
    # 遍历元素
    for item in items:
        # 打印<a>元素文本和href属性
        # my_array.append(item.child().attr('src'))
        my_array.append(convert_url(item.child().attr('src')))
    a += 1

my_array = list(set(my_array))  
multi_thread_download(my_array, author)
