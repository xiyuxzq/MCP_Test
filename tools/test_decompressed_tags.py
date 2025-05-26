#!/usr/bin/env python
"""
正确处理压缩响应，分析ColorHunt配色方案页面的真实内容
"""
import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import gzip
import time

def test_decompressed_response():
    """测试正确解压响应内容"""
    print("🔍 测试正确解压ColorHunt响应内容")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    # 测试截图中的配色方案
    target_code = '626f47a4b465f5ecd5f0bb78'
    url = f'https://colorhunt.co/palette/{target_code}'
    
    print(f"🎯 目标URL: {url}")
    print("-" * 40)
    
    try:
        # 使用requests自动处理压缩
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应长度: {len(response.text)}")
        print(f"编码: {response.encoding}")
        
        if response.status_code == 200:
            # 保存解压后的内容
            with open('palette_decompressed.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("📁 已保存解压后的内容: palette_decompressed.html")
            
            # 分析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找标题
            title = soup.find('title')
            print(f"\n页面标题: {title.text if title else 'N/A'}")
            
            # 查找所有链接
            links = soup.find_all('a')
            print(f"找到 {len(links)} 个链接")
            
            # 查找标签相关的链接
            tag_links = []
            for link in links:
                href = link.get('href', '')
                text = link.text.strip()
                if '/palettes/' in href and text and len(text) < 20:
                    tag_links.append((text, href))
            
            print(f"标签链接: {tag_links}")
            
            # 查找可能包含标签的元素
            tag_elements = soup.find_all(['div', 'span', 'a'], class_=re.compile(r'tag|label|category', re.I))
            print(f"找到 {len(tag_elements)} 个可能的标签元素")
            
            for elem in tag_elements:
                print(f"  {elem.name}: {elem.get('class')} - {elem.text.strip()}")
            
            # 查找包含特定关键词的元素
            keywords = ['sage', 'green', 'beige', 'nature', 'earth', 'summer', 'food', 'vintage']
            found_keywords = []
            
            page_text = soup.get_text().lower()
            for keyword in keywords:
                if keyword in page_text:
                    found_keywords.append(keyword)
            
            print(f"在页面中找到的关键词: {found_keywords}")
            
            # 查找script标签中的数据
            scripts = soup.find_all('script')
            print(f"找到 {len(scripts)} 个script标签")
            
            for i, script in enumerate(scripts):
                if script.string and len(script.string) > 50:
                    script_content = script.string
                    if any(keyword in script_content.lower() for keyword in ['tag', 'palette', 'color']):
                        print(f"\nScript {i+1} 包含相关内容:")
                        print(script_content[:300] + "..." if len(script_content) > 300 else script_content)
            
            # 查找meta标签
            meta_tags = soup.find_all('meta')
            print(f"\n找到 {len(meta_tags)} 个meta标签")
            
            for meta in meta_tags:
                name = meta.get('name', meta.get('property', ''))
                content = meta.get('content', '')
                if name and content and any(keyword in content.lower() for keyword in keywords):
                    print(f"  {name}: {content}")
            
            # 查找所有包含颜色代码的元素
            color_elements = soup.find_all(text=re.compile(r'#[0-9a-fA-F]{6}'))
            print(f"\n找到 {len(color_elements)} 个包含颜色代码的元素")
            
            # 查找data属性
            data_elements = soup.find_all(attrs={'data-tag': True})
            if data_elements:
                print(f"找到 {len(data_elements)} 个带有data-tag属性的元素")
                for elem in data_elements:
                    print(f"  {elem.name}: data-tag='{elem.get('data-tag')}'")
            
        else:
            print(f"❌ 请求失败")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()

def test_javascript_rendering():
    """测试是否需要JavaScript渲染"""
    print("\n" + "=" * 60)
    print("🔍 测试JavaScript渲染需求")
    print("=" * 60)
    
    # 尝试使用selenium获取完整渲染的页面
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        print("✅ Selenium可用，尝试JavaScript渲染")
        
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        target_code = '626f47a4b465f5ecd5f0bb78'
        url = f'https://colorhunt.co/palette/{target_code}'
        
        print(f"访问: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        # 获取页面源码
        page_source = driver.page_source
        
        # 保存渲染后的页面
        with open('palette_rendered.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        print("📁 已保存渲染后的页面: palette_rendered.html")
        
        # 分析渲染后的页面
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # 查找标签
        tag_links = soup.find_all('a', href=re.compile(r'/palettes/[a-zA-Z]+$'))
        tags = [link.text.strip() for link in tag_links if link.text.strip()]
        print(f"渲染后找到的标签: {list(set(tags))}")
        
        driver.quit()
        
    except ImportError:
        print("⚠️ Selenium未安装，跳过JavaScript渲染测试")
        print("如需安装: pip install selenium")
    except Exception as e:
        print(f"❌ Selenium测试异常: {e}")

def analyze_api_structure():
    """分析API结构，看看是否有其他端点"""
    print("\n" + "=" * 60)
    print("🔍 分析API结构")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://colorhunt.co/'
    }
    
    # 测试不同的API参数组合
    test_cases = [
        # 尝试获取特定配色方案的详细信息
        {'step': 0, 'sort': 'new', 'tags': '', 'timeframe': '', 'palette_id': '626f47a4b465f5ecd5f0bb78'},
        {'step': 0, 'sort': 'new', 'tags': '', 'timeframe': '', 'id': '626f47a4b465f5ecd5f0bb78'},
        {'step': 0, 'sort': 'new', 'tags': '', 'timeframe': '', 'code': '626f47a4b465f5ecd5f0bb78'},
        # 尝试获取标签信息
        {'action': 'get_tags', 'palette_id': '626f47a4b465f5ecd5f0bb78'},
        {'action': 'palette_details', 'id': '626f47a4b465f5ecd5f0bb78'},
    ]
    
    for i, post_data in enumerate(test_cases):
        print(f"\n📋 测试API参数 {i+1}: {post_data}")
        
        try:
            response = requests.post(
                'https://colorhunt.co/php/feed.php', 
                headers=headers, 
                data=post_data,
                timeout=10
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应长度: {len(response.text)}")
            
            if response.text.strip():
                print(f"响应内容: {response.text[:200]}...")
                
                # 尝试解析JSON
                try:
                    json_data = json.loads(response.text)
                    print(f"JSON数据: {json_data}")
                except:
                    pass
            else:
                print("空响应")
                
        except Exception as e:
            print(f"❌ 异常: {e}")

def main():
    """主函数"""
    print("ColorHunt解压响应和标签分析")
    print("=" * 60)
    
    try:
        test_decompressed_response()
        test_javascript_rendering()
        analyze_api_structure()
        
        print("\n🎉 测试完成！")
        print("💡 说明: 通过正确解压响应和JavaScript渲染尝试获取真实标签")
        print("🔍 检查生成的HTML文件查看详细内容。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 