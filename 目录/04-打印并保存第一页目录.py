import os
import requests
from lxml import etree

# 获取小说文章
url = 'https://www.sudugu.com/318/#dir'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# 使用requests发送请求
response = requests.get(url, headers=headers)

# 解析网页源码 来获取我们想要的数据
tree = etree.HTML(response.text)

# 获取想要的数据  xpath的返回值是一个列表类型的数据
# 获取页面中的标题或特定元素
result = tree.xpath('//div[@id="list"]/ul/li/a/text()')

# 自定义小说索引名称
novel_index = input("请输入小说索引名称: ")

# 创建“小说目录”文件夹
directory = "小说目录"
if not os.path.exists(directory):
    os.makedirs(directory)

# 文件路径
file_path = os.path.join(directory, f"{novel_index}.txt")

# 打印结果并保存到文件
with open(file_path, 'w', encoding='utf-8') as file:
    for res in result or []:
        print(res)
        file.write(res + '\n')

print(f"已将内容保存到 {file_path}")