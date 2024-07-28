from DrissionPage import ChromiumPage
import os
from concurrent.futures import ThreadPoolExecutor

# 创建页面对象
page = ChromiumPage()

def download(url, file_name, author):
    save_path = f'/Users/jbos/Downloads/pixiv/{author}'
    try:
        res = page.download(url, save_path,file_name)
        if res[0]:
            print(f"Downloaded {url} as {file_name}: {res[1]}")
        else:
            print(f"Failed to download {url} as {file_name}: {res[1]}")
            # 如果下载失败，尝试将文件类型从 jpg 改为 png 再次下载
            if url.endswith(".jpg"):
                new_url = url.replace(".jpg", ".png")
                print(f"Retrying with {new_url}")
                res = page.download(new_url, save_path,file_name)
                if res[0]:
                    print(f"Downloaded {new_url} as {file_name}: {res[1]}")
                else:
                    print(f"Failed to download {new_url} as {file_name}: {res[1]}")
    except Exception as e:
        print(f"Failed to download {url} as {file_name}: {e}")

def multi_thread_download(items, author, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        threads = [executor.submit(download, item['src'], item['fileName'], author) for item in items]
        for thread in threads:
            thread.result()
    print("All downloads completed.")
def convert_url(original_url):
    if original_url is None:
        raise ValueError("URL is None")
    # 判断并替换不同的部分内容
    if "/img-master/" in original_url:
        converted_url = original_url.replace("/c/250x250_80_a2/img-master/", "/img-original/")
        converted_url = converted_url.replace("_square1200", "")
    elif "/custom-thumb/" in original_url:
        converted_url = original_url.replace("/c/250x250_80_a2/custom-thumb/", "/img-original/")
        converted_url = converted_url.replace("_custom1200", "")
    else:
        # 如果不匹配任何已知模式，返回原始URL
        converted_url = original_url
    return converted_url

def make_unique_file_name(file_name, existing_names):
    base_name, ext = os.path.splitext(file_name)
    count = 1
    new_file_name = file_name
    while new_file_name in existing_names:
        new_file_name = f"{base_name}_{count}{ext}"
        count += 1
    existing_names.add(new_file_name)
    return new_file_name

def process_file_name(file_name):
    first_space_index = file_name.find(' ')
    all_spaces = [i for i, char in enumerate(file_name) if char == ' ']
    if len(all_spaces) < 2:
        raise ValueError("File name does not contain enough spaces for the desired processing.")
    second_last_space_index = all_spaces[-2]
    
    if first_space_index != -1 and second_last_space_index != -1:
        file_name = file_name[first_space_index + 1:second_last_space_index]
    return file_name.strip()

# 创建一个空列表
my_array = []
existing_names = set()

# 在这里填入作者编号
author = "91270513"

# 创建保存文件的文件夹
save_folder = f'/Users/jbos/Downloads/pixiv/{author}'
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# 开始网页
a = 1
# 总页数
while a <= 1:
    page.get(f'https://www.pixiv.net/users/{author}/artworks?p={a}')
    # 在页面中查找元素
    items = page.eles('.sc-rp5asc-9 cYUezH')
    # 遍历元素
    for item in items:
        # 检查子元素是否存在，并获取src属性
        child = item.child()
        if child is None:
            raise ValueError("Child element is None")
        src = child.attr('src')
        file_name=child.attr('alt')
        if src is None:
            raise ValueError("src attribute is None")
        file_name = process_file_name(file_name)
        converted_url = convert_url(src)
        if converted_url:
            unique_file_name = make_unique_file_name(file_name, existing_names)
            my_array.append({"src": converted_url, "fileName": unique_file_name})
    a += 1

multi_thread_download(my_array, author)
