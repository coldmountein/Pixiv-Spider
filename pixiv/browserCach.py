# 导入
from DrissionPage import ChromiumPage
# 创建页面对象
page = ChromiumPage()
from concurrent.futures import ThreadPoolExecutor

page.get('https://www.pixiv.net/users/25215933')