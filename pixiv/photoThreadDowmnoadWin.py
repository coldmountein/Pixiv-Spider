import os
from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage

# 下载函数
def download(url, file_name, author):
    save_path = os.path.join('.', 'pixiv', author)
    os.makedirs(save_path, exist_ok=True)
    try:
        page = ChromiumPage()  # 为每个线程创建一个独立页面对象
        res = page.download(url, save_path, file_name)
        if res[0]:
            print(f"Downloaded {url} as {file_name}: {res[1]}")
        else:
            print(f"Failed to download {url} as {file_name}: {res[1]}")
            # 重试下载 PNG 格式
            if url.endswith(".jpg"):
                new_url = url.replace(".jpg", ".png")
                print(f"Retrying with {new_url}")
                res = page.download(new_url, save_path, file_name)
                if res[0]:
                    print(f"Downloaded {new_url} as {file_name}: {res[1]}")
                else:
                    print(f"Failed to download {new_url} as {file_name}: {res[1]}")
    except Exception as e:
        print(f"Failed to download {url} as {file_name}: {e}")

# 多线程下载
def multi_thread_download(items, author, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        threads = [executor.submit(download, item['src'], item['fileName'], author) for item in items]
        for thread in threads:
            thread.result()
    print("All downloads completed.")

# 转换 URL 函数
def convert_url(original_url):
    if original_url is None:
        raise ValueError("URL is None")
    if "/img-master/" in original_url:
        converted_url = original_url.replace("/c/250x250_80_a2/img-master/", "/img-original/").replace("_square1200", "")
    elif "/custom-thumb/" in original_url:
        converted_url = original_url.replace("/c/250x250_80_a2/custom-thumb/", "/img-original/").replace("_custom1200", "")
    else:
        converted_url = original_url
    return converted_url

# 文件名去重
def make_unique_file_name(file_name, existing_names):
    base_name, ext = os.path.splitext(file_name)
    count = 1
    new_file_name = file_name
    while new_file_name in existing_names:
        new_file_name = f"{base_name}_{count}{ext}"
        count += 1
    existing_names.add(new_file_name)
    return new_file_name

# 文件名处理
def process_file_name(file_name):
    all_spaces = [i for i, char in enumerate(file_name) if char == ' ']
    if len(all_spaces) < 2:
        return file_name
    return file_name[all_spaces[0] + 1:all_spaces[-2]].strip()

# 下载流程
my_array = []
existing_names = set()
authorNumber = "110371277"
authorID = ""
a = 1
page = ChromiumPage()  # 创建页面对象

while a <= 1:
    page.get(f'https://www.pixiv.net/users/{authorNumber}/artworks?p={a}')
    authorID = page.ele('xpath://*[@id="root"]/div[2]/div/div[3]/div/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/h1').attr('innerHTML')
    items = page.eles('.sc-rp5asc-9 itpOYX')
    for item in items:
        child = item.child()
        if not child:
            continue
        src = child.attr('src')
        file_name = child.attr('alt')
        if src:
            processed_name = process_file_name(file_name)
            unique_file_name = make_unique_file_name(processed_name, existing_names)
            my_array.append({"src": convert_url(src), "fileName": unique_file_name})
    a += 1

multi_thread_download(my_array, authorID)
