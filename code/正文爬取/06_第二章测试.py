import requests
from lxml import etree
import re
import os

# 配置请求头和目标URL的基础部分
base_url = 'https://www.sudugu.com/318/478054'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

def fetch_page_content(url):
    """获取指定URL的内容，返回标题和正文"""
    try:
        # 发送HTTP请求并获取响应
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'  # 确保正确解码网页内容

        if response.status_code != 200:
            print(f"页面 {url} 返回状态码 {response.status_code}，跳过此页")
            return None, []

        # 解析网页源码
        tree = etree.HTML(response.text)

        # 获取标题并清理文本
        title_element = tree.xpath('//div[@class="submenu"]/h1/text()')
        title = ''.join(re.findall(r'[\u4e00-\u9fa5]+', ''.join(title_element))) if title_element else '未知标题'

        # 获取正文内容并去除空段落
        content = [p.strip() for p in tree.xpath('//div[@class="con"]/p/text()') if p.strip()]
        
        return title, content
    except Exception as e:
        print(f"处理页面 {url} 时发生错误: {e}")
        return None, []

def save_novel(directory, title, contents):
    """保存小说内容到指定目录的文件中"""
    file_path = os.path.join(directory, f"{title}.txt")
    mode = 'w' if not os.path.exists(file_path) else 'a'  # 如果文件不存在，则以写模式打开；否则以追加模式打开
    
    with open(file_path, mode, encoding='utf-8') as file:
        if mode == 'w':
            file.write(f"{title}\n")  # 写入标题到文件的第一行
        for paragraph in contents:
            file.write(paragraph + '\n')  # 追加正文内容到文件

def main():
    # 文件路径
    directory = r'D:\VSCode\Python_Project\爬虫\小说爬取\Get_novel\完美世界\完美世界正文'
    os.makedirs(directory, exist_ok=True)  # 确保目录存在
    
    title = None
    for page in range(1, 7):  # 遍历第1到第6页
        url = f'{base_url}-{page}.html' if page > 1 else f'{base_url}.html'  # 构建URL
        
        print(f'正在处理页面: {url}')
        
        current_title, content = fetch_page_content(url)
        
        if not current_title or not content:
            print(f"页面 {url} 没有有效内容，跳过此页")
            continue
        
        # 如果是第一次获取标题，则打印一次，并更新文件路径
        if page == 1:
            title = current_title
            print(title)
        
        save_novel(directory, title, content)
        print('*' * 50)
        print(f'{current_title} 第{page}页 保存完成')

    if title:
        print(f'{title} 完整内容保存完成')

if __name__ == "__main__":
    main()