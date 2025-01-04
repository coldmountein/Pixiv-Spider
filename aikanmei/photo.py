from DrissionPage import ChromiumPage
import os
from concurrent.futures import ThreadPoolExecutor

# 创建页面对象
page = ChromiumPage()

# 创建一个空列表
my_array = []
existing_names = set()

# 在这里填入作者编号
authorNumber = "91270513"
authorID=""

# 开始网页
a = 1
# 总页数
page.get(f'https://aikanmei.com/fuli-content/2MdTdQ/index.html')
items = page.eles('.owl-lazy')
save_path = f'/Users/jbos/Downloads/aikanmei'

def remove_w400(url: str) -> str:
    """
    从给定的 URL 中删除 '/w400/'。

    参数:
        url (str): 包含 '/w400/' 的 URL 字符串。

    返回:
        str: 删除 '/w400/' 后的 URL。
    """
    return url.replace("/w400/", "/")

for index, item in enumerate(items):
    # if index >= 10:  # 只循环前10个
    #     break
    # print(item)  # 打印 item 的基本信息
    # print(item.attr('alt'))
    # print(item.attr('data-src'))
    page.download(remove_w400(item.attr('data-src')), save_path, item.attr('alt'))
a += 1