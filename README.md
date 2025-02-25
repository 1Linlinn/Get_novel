# Get_novel
在[https://www.sudugu.com/] 以完美世界为例进行了爬取操作
## 目录
目录一共两页，url没有什么太多共同之处，所以采取以下思路进行爬取测试
- 爬取第一页目录
- 爬取第二页目录
- 使用列表和循环处理两页目录
- 测试爬取内容并保存
- 修改最终版本的代码

------
## 小说正文
发现小说少了挺多章节，但是每一章节的url倒是连续的
- 第一章：https://www.sudugu.com/318/478053.html
- 第二章：https://www.sudugu.com/318/478054.html
- 第三章：https://www.sudugu.com/318/478055.html
- 第四章：缺失
- 第五章：https://www.sudugu.com/318/478056.html

### 章节爬取
每一章的内容原来不只有一页，有点难搞，要翻页，但是不确定每一个章节有多少页，以前两章分析一下
#### 第一章
- 第一页：https://www.sudugu.com/318/478053.html
- 第二页：https://www.sudugu.com/318/478053-2.html
- 第三页：https://www.sudugu.com/318/478053-3.html
- 第四页：https://www.sudugu.com/318/478053-4.html
#### 第二章
- 第一页：https://www.sudugu.com/318/478054.html
- 第二页：https://www.sudugu.com/318/478054-2.html
- 第三页：https://www.sudugu.com/318/478054-3.html
- 第四页：https://www.sudugu.com/318/478054-4.html

-----
  大致看来，每一章节应该在5页左右，但是每一章节的首页url比较特殊，应该要特殊处理
  #### 思路分析
  - 先爬取第一章的四页试一下效果如何
  
