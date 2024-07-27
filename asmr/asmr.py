# 导入
from DrissionPage import ChromiumPage
import csv

# 创建页面对象
page = ChromiumPage()


def add_keyword_to_array(number, frontKeyword):
    return frontKeyword + number


def checkUrl(url, keyword):
    page.get(f"https://www.asmr.one/work/{url}")

    title = page.ele(".text-h6 text-weight-regular q-mb-none text-black").attr(
        "innerText"
    )

    # 在页面中查找元素
    items = page.eles(".q-item__section column q-item__section--main justify-center")
    for item in items:
        if keyword in item.attr("innerText"):
            saveData(url, title, item.attr("innerText"))


def saveData(url, title, subTitle, filename="C:\\Users\\123\\Desktop\\code\\code\\asmr\\data.csv"):
    # 将数据保存到CSV文件中
    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["URL", "Title", "Subtitle"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 如果文件是空的，写入表头
        if csvfile.tell() == 0:
            writer.writeheader()

        # 写入数据行
        writer.writerow({"URL": add_keyword_to_array(url,frontKeyword), "Title": title, "Subtitle": subTitle})


# 创建一个空列表
my_array = []
# 访问网页
# 开始网页
keyword = "シコ"
frontKeyword = "https://www.asmr.one/work/"
# 开始页数
a = 1
b = 0
# 结束页数
while a <= 5:
    page.get(f"https://www.asmr.one/works?page={a}")
    # 在页面中查找元素
    items = page.eles(".col-xs-12 col-sm-4 col-md-3 col-lg-2 col-xl-2")
    # 遍历元素
    for item in items:
        # 打印<a>元素文本和href属性
        my_array.append(item.attr("id"))
    a += 1
for item in my_array:
    checkUrl(item, keyword)
