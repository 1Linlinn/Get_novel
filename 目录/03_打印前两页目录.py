import requests
from lxml import etree

# 获取小说文章
url_list = ['https://www.sudugu.com/318/#dir', 'https://www.sudugu.com/318/p-2.html#dir']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
for url in url_list:
    # 使用requests发送请求
    response = requests.get(url, headers=headers)

    # 解析网页源码 来获取我们想要的数据
    tree = etree.HTML(response.text)

    # 获取想要的数据  xpath的返回值是一个列表类型的数据
    # 获取页面中的标题或特定元素
    result = tree.xpath('//div[@id="list"]/ul/li/a/text()')

    # 打印结果
    for res in result or []:
        print(res)