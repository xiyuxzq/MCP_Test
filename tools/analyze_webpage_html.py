#!/usr/bin/env python
"""
分析ColorHunt配色方案页面的HTML结构
找到标签、点赞数、日期等元素的具体位置
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
import re

def analyze_html_structure():
    """分析HTML结构"""
    print("🔍 分析ColorHunt配色方案页面HTML结构")
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
    url = 'https://colorhunt.co/palette/626f47a4b465f5ecd5f0bb78'
    
    print(f"📋 分析URL: {url}")
    print("-" * 40)
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            print("✅ 页面加载成功")
            print(f"页面标题: {soup.title.text if soup.title else 'N/A'}")
            
            # 保存完整HTML用于分析
            with open('palette_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("📁 已保存完整HTML: palette_page.html")
            
            # 分析页面结构
            print("\n🔍 页面结构分析:")
            
            # 查找所有可能包含标签的元素
            print("\n1. 查找所有链接:")
            links = soup.find_all('a')
            for i, link in enumerate(links[:20]):  # 只显示前20个
                href = link.get('href', '')
                text = link.text.strip()
                if text:
                    print(f"   链接{i+1}: {text} -> {href}")
            
            print("\n2. 查找所有class属性:")
            all_elements = soup.find_all(True)
            classes = set()
            for elem in all_elements:
                if elem.get('class'):
                    classes.update(elem.get('class'))
            
            for cls in sorted(classes):
                print(f"   class: {cls}")
            
            print("\n3. 查找包含数字的文本（可能是点赞数）:")
            page_text = soup.get_text()
            number_matches = re.findall(r'\b\d+\b', page_text)
            for num in number_matches[:10]:  # 只显示前10个
                print(f"   数字: {num}")
            
            print("\n4. 查找时间相关的文本:")
            time_matches = re.findall(r'\b\d+\s+(hour|day|week|month|year)s?\b', page_text, re.IGNORECASE)
            for match in time_matches:
                print(f"   时间: {match}")
            
            print("\n5. 查找meta标签:")
            meta_tags = soup.find_all('meta')
            for meta in meta_tags:
                name = meta.get('name', meta.get('property', ''))
                content = meta.get('content', '')
                if name and content:
                    print(f"   {name}: {content[:100]}...")
            
            print("\n6. 查找script标签中的数据:")
            scripts = soup.find_all('script')
            for i, script in enumerate(scripts):
                if script.string and ('tag' in script.string.lower() or 'like' in script.string.lower()):
                    print(f"   Script {i+1}: {script.string[:200]}...")
            
        else:
            print(f"❌ 请求失败, 状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def check_feed_api():
    """检查feed.php API的响应"""
    print("\n" + "=" * 60)
    print("🔍 检查feed.php API响应")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://colorhunt.co/'
    }
    
    # 测试不同的API参数，看看是否有其他字段
    test_cases = [
        {'step': 0, 'sort': 'popular', 'tags': '', 'timeframe': '30'},
        {'step': 0, 'sort': 'new', 'tags': 'vintage', 'timeframe': ''},
        {'step': 0, 'sort': 'new', 'tags': 'nature', 'timeframe': ''}
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
            print(f"响应内容: {response.text[:500]}...")
            
            if response.text.strip() == '[]':
                print("⚠️ API返回空数组")
            elif response.text.strip() == '':
                print("⚠️ API返回空响应")
            
        except Exception as e:
            print(f"❌ API请求异常: {e}")

def main():
    """主函数"""
    print("ColorHunt页面结构分析")
    print("=" * 60)
    
    try:
        analyze_html_structure()
        check_feed_api()
        
        print("\n🎉 分析完成！")
        print("🔍 检查生成的palette_page.html文件查看完整页面结构。")
        
    except Exception as e:
        print(f"❌ 分析过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 