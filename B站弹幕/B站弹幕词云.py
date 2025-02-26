import requests
import xml.etree.ElementTree as ET
import jieba
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 获取视频CID
def get_cid(bvid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['data']['cid']

# 获取弹幕数据
def get_danmaku(cid):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f'https://comment.bilibili.com/{cid}.xml'
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    return [d.text for d in root.findall('.//d')]

# 文本处理（分词+清洗）
def process_text(texts, stopwords):
    words = []
    for text in texts:
        # 去除特殊符号和空白
        text = re.sub(r'[^\w\s]', '', text.strip())
        # 中文分词
        seg_list = jieba.cut(text)
        # 过滤停用词和单字
        words.extend([
            word for word in seg_list
            if word not in stopwords and len(word) > 1
        ])
    return words

# 生成词云
def generate_wordcloud(words, font_path, bvid):
    word_count = Counter(words)
    
    wc = WordCloud(
        font_path=font_path,
        background_color='white',
        width=1600,
        height=1200,
        max_words=200,
        collocations=False
    )
    
    wc.generate_from_frequencies(word_count)
    
    plt.figure(figsize=(14, 10), dpi=500)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(f'{bvid}.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    # 用户输入BVID（示例：BV1ix411h7xm）
    bvid = input("请输入B站视频BV号：")
    
    try:
        # 获取CID
        cid = get_cid(bvid)
        print(f"成功获取CID: {cid}")
        
        # 获取弹幕
        danmaku_list = get_danmaku(cid)
        print(f"共获取到{len(danmaku_list)}条弹幕")
        
        # 加载停用词表（需自行准备）
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stopwords = set(f.read().splitlines())
        
        # 处理文本
        words = process_text(danmaku_list, stopwords)
        
        # 生成词云（需中文字体文件）
        generate_wordcloud(words, r"E:\文件\SimHei(1).ttf", bvid)  # 替换为你的字体路径
        
    except Exception as e:
        print(f"程序出错：{str(e)}")

if __name__ == "__main__":
    main()