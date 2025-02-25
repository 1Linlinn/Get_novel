import requests
from lxml import etree
import re
import os

# 配置请求头和目标URL
url = 'https://www.sudugu.com/318/478053-4.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

# 发送HTTP请求并获取响应
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 确保正确解码网页内容

# 解析网页源码
tree = etree.HTML(response.text)

# 获取标题并清理文本
title_element = tree.xpath('//div[@class="submenu"]/h1/text()')
if title_element:  # 确保有标题元素
    index = ''.join(re.findall(r'[\u4e00-\u9fa5]+', title_element[0]))  # 提取汉字字符
else:
    index = '未知标题'

# 获取正文内容
result = tree.xpath('//div[@class="con"]/p/text()')

# 文件路径
directory = r'D:\VSCode\Python_Project\爬虫\小说爬取\Get_novel\完美世界\完美世界正文'
file_path = os.path.join(directory, f"{index}第四页.txt")

# 打印结果并保存到文件
print(index)
with open(file_path, 'w', encoding='utf-8') as file:
    for paragraph in result:
        cleaned_paragraph = paragraph.strip()  # 去除段落两端的空白字符
        if cleaned_paragraph:  # 只写入非空段落
            print(cleaned_paragraph)
            file.write(cleaned_paragraph + '\n')
print('*' * 50)
print(f'{index}第四页 保存完成')