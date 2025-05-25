#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试ColorHunt网站的HTML结构
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_colorhunt_page(tag='summer'):
    """调试ColorHunt标签页面的HTML结构"""
    
    url = f"https://colorhunt.co/palettes/{tag}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://colorhunt.co/',
        'Cache-Control': 'no-cache'
    }
    
    print(f"🔍 调试页面: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📏 响应内容长度: {len(response.text)} 字符")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. 查找页面标题
            title = soup.find('title')
            if title:
                print(f"📄 页面标题: {title.text.strip()}")
            
            # 2. 查找所有可能的配色方案相关元素
            print("\n🔍 查找配色方案相关元素:")
            
            selectors_to_test = [
                '.palette',
                '.item',
                '.color-palette',
                '[data-id]',
                'a[href*="/palette/"]',
                '.palettes',
                '.palette-item',
                '.color-item',
                'div[class*="palette"]',
                'div[class*="color"]'
            ]
            
            for selector in selectors_to_test:
                elements = soup.select(selector)
                print(f"  {selector}: {len(elements)} 个元素")
                
                if elements and len(elements) > 0:
                    # 显示前2个元素的详细信息
                    for i, elem in enumerate(elements[:2]):
                        print(f"    元素 {i+1}:")
                        print(f"      标签: {elem.name}")
                        print(f"      类: {elem.get('class', [])}")
                        print(f"      ID: {elem.get('id', '')}")
                        print(f"      href: {elem.get('href', '')}")
                        print(f"      data-id: {elem.get('data-id', '')}")
                        print(f"      文本内容: {elem.text.strip()[:100]}...")
            
            # 3. 查找所有包含 /palette/ 的链接
            print("\n🔗 查找配色方案链接:")
            palette_links = soup.find_all('a', href=re.compile(r'/palette/'))
            print(f"找到 {len(palette_links)} 个配色方案链接")
            
            for i, link in enumerate(palette_links[:5]):  # 只显示前5个
                href = link.get('href', '')
                print(f"  链接 {i+1}: {href}")
                print(f"    类: {link.get('class', [])}")
                print(f"    文本: {link.text.strip()[:50]}...")
            
            # 4. 查找所有可能包含颜色代码的元素
            print("\n🌈 查找颜色代码:")
            color_pattern = re.compile(r'#[0-9a-fA-F]{6}')
            color_matches = color_pattern.findall(response.text)
            unique_colors = list(set(color_matches))
            print(f"找到 {len(unique_colors)} 个唯一颜色代码:")
            for color in unique_colors[:10]:  # 只显示前10个
                print(f"  {color}")
            
            # 5. 查找JavaScript中的数据
            print("\n📜 查找JavaScript数据:")
            scripts = soup.find_all('script')
            for i, script in enumerate(scripts):
                if script.string and ('palette' in script.string.lower() or 'color' in script.string.lower()):
                    content = script.string.strip()
                    if len(content) > 50:  # 只显示有意义的脚本
                        print(f"  脚本 {i+1} (前200字符): {content[:200]}...")
            
            # 6. 检查是否有"No results"信息
            no_results = soup.find(text=re.compile(r'No results|couldn\'t find'))
            if no_results:
                print(f"\n⚠️ 发现'无结果'信息: {no_results.strip()}")
            
            # 7. 保存HTML到文件以便进一步分析
            with open(f'debug_{tag}_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"\n💾 HTML内容已保存到: debug_{tag}_page.html")
            
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 调试时出错: {e}")

if __name__ == "__main__":
    # 调试不同的标签页面
    tags_to_debug = ['summer', 'retro', 'vintage']
    
    for tag in tags_to_debug:
        print(f"\n{'='*80}")
        debug_colorhunt_page(tag)
        print(f"{'='*80}") 