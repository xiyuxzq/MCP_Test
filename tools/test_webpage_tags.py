#!/usr/bin/env python
"""
测试从ColorHunt配色方案页面提取标签信息
分析网页HTML结构，获取真实的标签数据
"""
import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import re

def test_webpage_tags():
    """测试从网页提取标签"""
    print("🔍 测试从ColorHunt配色方案页面提取标签")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # 测试几个不同的配色方案URL
    test_urls = [
        'https://colorhunt.co/palette/626f47a4b465f5ecd5f0bb78',  # 从截图推测的URL
        'https://colorhunt.co/palette/222831393e46948979dfd0b8',  # 之前测试的popular配色
        'https://colorhunt.co/palette/ffe99affd586ffaaaaff9898'   # vintage配色
    ]
    
    for url in test_urls:
        print(f"\n📋 测试URL: {url}")
        print("-" * 40)
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取配色方案信息
                palette_info = extract_palette_info(soup, url)
                
                if palette_info:
                    print("✅ 成功提取配色方案信息:")
                    for key, value in palette_info.items():
                        print(f"   {key}: {value}")
                    
                    # 保存提取的数据
                    palette_id = url.split('/')[-1]
                    filename = f"webpage_tags_{palette_id}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(palette_info, f, indent=2, ensure_ascii=False)
                    print(f"   📁 已保存: {filename}")
                else:
                    print("❌ 未能提取到配色方案信息")
                    
            else:
                print(f"❌ 请求失败, 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def extract_palette_info(soup, url):
    """从网页HTML中提取配色方案信息"""
    info = {
        'url': url,
        'palette_id': url.split('/')[-1],
        'colors': [],
        'tags': [],
        'likes': 0,
        'date': '',
        'title': '',
        'author': ''
    }
    
    try:
        # 提取标题
        title_elem = soup.find('title')
        if title_elem:
            info['title'] = title_elem.text.strip()
        
        # 提取颜色（从URL解析）
        palette_id = info['palette_id']
        if len(palette_id) == 24:
            for i in range(4):
                hex_color = f"#{palette_id[i*6:(i+1)*6].upper()}"
                info['colors'].append(hex_color)
        
        # 方法1: 查找标签链接
        tag_links = soup.find_all('a', href=re.compile(r'/palettes/'))
        for link in tag_links:
            tag_text = link.text.strip()
            if tag_text and tag_text not in info['tags']:
                # 过滤掉一些非标签的链接
                if not any(x in tag_text.lower() for x in ['palette', 'color', 'hunt', 'home']):
                    info['tags'].append(tag_text)
        
        # 方法2: 查找包含标签的div或span元素
        tag_elements = soup.find_all(['div', 'span', 'a'], class_=re.compile(r'tag|label|category'))
        for elem in tag_elements:
            tag_text = elem.text.strip()
            if tag_text and tag_text not in info['tags']:
                if len(tag_text) < 20 and tag_text.isalpha():  # 标签通常是短的单词
                    info['tags'].append(tag_text)
        
        # 方法3: 查找页面中的所有链接，筛选可能的标签
        all_links = soup.find_all('a')
        for link in all_links:
            href = link.get('href', '')
            text = link.text.strip()
            
            # 如果链接指向标签页面，且文本是单个词
            if '/palettes/' in href and text and len(text.split()) == 1:
                if text.lower() not in ['home', 'new', 'popular', 'random'] and text not in info['tags']:
                    info['tags'].append(text)
        
        # 提取点赞数
        like_patterns = [
            r'(\d+)\s*likes?',
            r'likes?\s*(\d+)',
            r'❤️\s*(\d+)',
            r'♥\s*(\d+)'
        ]
        
        page_text = soup.get_text()
        for pattern in like_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                info['likes'] = int(match.group(1))
                break
        
        # 提取日期/时间
        time_patterns = [
            r'(\d+)\s+(hour|day|week|month|year)s?\s+ago',
            r'(\d+)\s+(hour|day|week|month|year)s?',
            r'(yesterday|today)',
            r'(\d{4}-\d{2}-\d{2})'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, page_text, re.IGNORECASE)
            if match:
                info['date'] = match.group(0)
                break
        
        # 查找meta标签中的信息
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            desc = meta_desc.get('content', '')
            # 从描述中提取可能的标签
            desc_words = re.findall(r'\b[a-zA-Z]+\b', desc)
            for word in desc_words:
                if len(word) > 2 and word.lower() not in ['color', 'palette', 'hunt', 'the', 'and', 'for']:
                    if word not in info['tags']:
                        info['tags'].append(word)
        
        # 清理标签列表
        info['tags'] = [tag for tag in info['tags'] if len(tag) > 1 and len(tag) < 15]
        info['tags'] = list(set(info['tags']))  # 去重
        
        return info
        
    except Exception as e:
        print(f"❌ 提取信息时出错: {e}")
        return None

def main():
    """主函数"""
    print("ColorHunt网页标签提取测试")
    print("=" * 60)
    
    try:
        test_webpage_tags()
        
        print("\n🎉 测试完成！")
        print("🔍 检查生成的webpage_tags_*.json文件查看提取的标签数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 