import aiohttp
import asyncio
from lxml import etree
import re
import os
from concurrent.futures import ThreadPoolExecutor

# 配置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

async def fetch_page_content(session, url):
    """获取指定URL的内容，返回标题和正文"""
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            if response.status != 200:
                print(f"页面 {url} 返回状态码 {response.status}，跳过此页")
                return None, []

            text = await response.text(encoding='utf-8')

            # 解析网页源码
            tree = etree.HTML(text)

            # 获取标题并清理文本
            title_element = tree.xpath('//div[@class="submenu"]/h1/text()')
            title = ''.join(re.findall(r'[\u4e00-\u9fa5]+', ''.join(title_element))) if title_element else '未知标题'

            # 获取正文内容并去除空段落
            content = [p.strip() for p in tree.xpath('//div[@class="con"]/p/text()') if p.strip()]
            
            return title, content
    except Exception as e:
        print(f"处理页面 {url} 时发生错误: {e}")
        return None, []

def save_novel(directory, chapter_data):
    """保存小说内容到指定目录的文件中"""
    for title, contents in chapter_data.items():
        file_path = os.path.join(directory, f"{title}.txt")
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n")  # 写入标题到文件的第一行
            for paragraph in contents:
                file.write(paragraph + '\n')  # 追加正文内容到文件

async def process_chapter(chapter, max_pages_per_chapter, directory, chapter_data):
    """处理单个章节的所有页面，并将其内容添加到chapter_data字典中"""
    all_contents = []  # 存储当前章节的所有内容
    current_title = None  # 初始化章节标题
    
    async with aiohttp.ClientSession() as session:
        for page in range(1, max_pages_per_chapter + 1):
            url = f'https://www.sudugu.com/318/{chapter}.html' if page == 1 else f'https://www.sudugu.com/318/{chapter}-{page}.html'
            
            print(f'正在处理页面: {url}')
            
            fetched_title, content = await fetch_page_content(session, url)
            
            if not fetched_title or not content:
                print(f"页面 {url} 没有有效内容，跳过此页")
                continue
            
            if not current_title:
                current_title = fetched_title  # 只在第一次获取标题时赋值
            
            all_contents.extend(content)
        
        if all_contents and current_title:
            chapter_data[current_title] = all_contents
            print('*' * 50)
            print(f'{current_title} 保存完成')
        else:
            print(f'章节 {chapter} 无有效内容，跳过该章节')

def setup_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)

async def main():
    # 文件路径
    directory = r'D:\VSCode\Python_Project\爬虫\小说爬取\Get_novel\完美世界\完美世界正文'
    
    base_chapter_number = 478053  # 初始章节编号
    total_chapters = 100  # 总共要爬取的章节数量
    max_pages_per_chapter = 5  # 每一章最多页数
    thread_pool_size = 5  # 设置线程池大小为5

    setup_directory(directory)  # 确保目录存在
    
    chapter_data = {}  # 存储章节标题和内容

    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=thread_pool_size) as executor:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for chapter in range(base_chapter_number, base_chapter_number + total_chapters):
                tasks.append(loop.run_in_executor(executor, lambda c=chapter: asyncio.run(process_chapter(c, max_pages_per_chapter, directory, chapter_data))))
            
            await asyncio.gather(*tasks)
        
        # 直接保存章节数据
        save_novel(directory, chapter_data)

if __name__ == "__main__":
    asyncio.run(main())