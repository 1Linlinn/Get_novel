import os
import requests
from lxml import etree

# 定义需要抓取的URL列表
url_list = [
    'https://www.sudugu.com/318/#dir',
    'https://www.sudugu.com/318/p-2.html#dir'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

def fetch_and_parse(url):
    """
    发送请求并解析网页内容
    :param url: 目标网页的URL
    :return: 解析后的XPath结果列表
    """
    try:
        # 使用requests发送请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        return etree.HTML(response.text)
    except requests.RequestException as e:
        print(f"请求 {url} 失败: {e}")
        return None

def extract_data(tree):
    """
    从解析后的HTML树中提取所需数据
    :param tree: 解析后的HTML树
    :return: 提取的数据列表
    """
    if tree is None:
        return []
    
    # 使用XPath表达式提取数据
    result = tree.xpath('//div[@id="list"]/ul/li/a/text()')
    return result if result else []

def main():
    """
    主函数，负责遍历URL列表并处理每个URL的数据
    """
    for url in url_list:
        print(f"正在处理: {url}")
        
        # 获取并解析网页内容
        tree = fetch_and_parse(url)
        
        # 提取所需数据
        result = extract_data(tree)
        
        # 打印结果
        for res in result:
            print(res)

if __name__ == "__main__":
    main()