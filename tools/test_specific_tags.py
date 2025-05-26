#!/usr/bin/env python
"""
专门测试特定配色方案的标签获取
尝试多种方法获取真实的标签信息
"""
import sys
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import time

def test_specific_palette_tags():
    """测试特定配色方案的标签获取"""
    print("🏷️ 测试特定配色方案标签获取")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    # 测试截图中的配色方案
    test_palette = {
        'code': '626f47a4b465f5ecd5f0bb78',
        'url': 'https://colorhunt.co/palette/626f47a4b465f5ecd5f0bb78',
        'expected_tags': ['Sage', 'Green', 'Beige', 'Nature', 'Earth', 'Summer', 'Food', 'Vintage']
    }
    
    print(f"🎯 目标配色方案: {test_palette['code']}")
    print(f"🔗 URL: {test_palette['url']}")
    print(f"📋 期望标签: {test_palette['expected_tags']}")
    print("-" * 40)
    
    # 方法1: 直接访问配色方案页面
    print("\n🔍 方法1: 直接访问配色方案页面")
    try:
        response = requests.get(test_palette['url'], headers=headers, timeout=15)
        print(f"状态码: {response.status_code}")
        print(f"响应长度: {len(response.text)}")
        
        if response.status_code == 200:
            # 保存完整响应用于分析
            with open('palette_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print("📁 已保存响应: palette_response.html")
            
            # 分析页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找标题
            title = soup.find('title')
            print(f"页面标题: {title.text if title else 'N/A'}")
            
            # 查找所有链接
            links = soup.find_all('a')
            print(f"找到 {len(links)} 个链接")
            
            # 查找可能的标签链接
            tag_links = []
            for link in links:
                href = link.get('href', '')
                text = link.text.strip()
                if '/palettes/' in href and text:
                    tag_links.append((text, href))
            
            print(f"可能的标签链接: {tag_links}")
            
            # 查找页面中的所有文本
            page_text = soup.get_text()
            print(f"页面文本长度: {len(page_text)}")
            
            # 在页面文本中查找期望的标签
            found_tags = []
            for tag in test_palette['expected_tags']:
                if tag.lower() in page_text.lower():
                    found_tags.append(tag)
            
            print(f"在页面文本中找到的期望标签: {found_tags}")
            
        else:
            print(f"❌ 请求失败")
            
    except Exception as e:
        print(f"❌ 方法1异常: {e}")
    
    # 方法2: 尝试获取页面的JSON数据
    print("\n🔍 方法2: 查找页面中的JSON数据")
    try:
        response = requests.get(test_palette['url'], headers=headers, timeout=15)
        if response.status_code == 200:
            # 查找script标签中的JSON数据
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            
            for i, script in enumerate(scripts):
                if script.string:
                    script_content = script.string
                    # 查找可能包含标签信息的JSON
                    if 'tag' in script_content.lower() or 'palette' in script_content.lower():
                        print(f"Script {i+1} 包含相关内容:")
                        print(script_content[:500] + "..." if len(script_content) > 500 else script_content)
                        
                        # 尝试提取JSON
                        json_matches = re.findall(r'\{[^{}]*\}', script_content)
                        for j, json_str in enumerate(json_matches):
                            try:
                                json_data = json.loads(json_str)
                                print(f"  JSON {j+1}: {json_data}")
                            except:
                                pass
    except Exception as e:
        print(f"❌ 方法2异常: {e}")
    
    # 方法3: 尝试访问可能的API端点
    print("\n🔍 方法3: 尝试访问可能的API端点")
    api_endpoints = [
        f"https://colorhunt.co/api/palette/{test_palette['code']}",
        f"https://colorhunt.co/php/palette.php?id={test_palette['code']}",
        f"https://colorhunt.co/palette/{test_palette['code']}.json"
    ]
    
    for endpoint in api_endpoints:
        try:
            print(f"尝试: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"  响应: {response.text[:200]}...")
                try:
                    json_data = json.loads(response.text)
                    print(f"  JSON数据: {json_data}")
                except:
                    pass
        except Exception as e:
            print(f"  异常: {e}")
    
    # 方法4: 分析ColorHunt主页，看看标签是如何组织的
    print("\n🔍 方法4: 分析ColorHunt主页标签结构")
    try:
        response = requests.get('https://colorhunt.co/', headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找标签相关的元素
            tag_elements = soup.find_all(['a', 'div', 'span'], class_=re.compile(r'tag|label|category', re.I))
            print(f"找到 {len(tag_elements)} 个可能的标签元素")
            
            for elem in tag_elements[:10]:  # 只显示前10个
                print(f"  {elem.name}: {elem.get('class')} - {elem.text.strip()}")
                
    except Exception as e:
        print(f"❌ 方法4异常: {e}")

def analyze_colorhunt_structure():
    """分析ColorHunt网站的整体结构"""
    print("\n" + "=" * 60)
    print("🏗️ 分析ColorHunt网站结构")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    # 分析不同页面的结构
    pages_to_analyze = [
        ('主页', 'https://colorhunt.co/'),
        ('Popular页面', 'https://colorhunt.co/popular'),
        ('Vintage标签页', 'https://colorhunt.co/palettes/vintage'),
        ('Nature标签页', 'https://colorhunt.co/palettes/nature')
    ]
    
    for page_name, url in pages_to_analyze:
        print(f"\n📄 分析 {page_name}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找配色方案链接
                palette_links = soup.find_all('a', href=re.compile(r'/palette/[a-fA-F0-9]{24}'))
                print(f"  找到 {len(palette_links)} 个配色方案链接")
                
                # 查找标签链接
                tag_links = soup.find_all('a', href=re.compile(r'/palettes/[a-zA-Z]+'))
                tag_names = [link.text.strip() for link in tag_links if link.text.strip()]
                print(f"  找到标签: {list(set(tag_names))}")
                
            else:
                print(f"  ❌ 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")

def test_alternative_approach():
    """测试替代方法：通过标签页面反向查找"""
    print("\n" + "=" * 60)
    print("🔄 测试替代方法：通过标签页面反向查找")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    target_code = '626f47a4b465f5ecd5f0bb78'
    expected_tags = ['sage', 'green', 'beige', 'nature', 'earth', 'summer', 'food', 'vintage']
    
    found_in_tags = []
    
    for tag in expected_tags:
        print(f"\n🔍 在标签页面 '{tag}' 中查找配色方案 {target_code}")
        try:
            url = f'https://colorhunt.co/palettes/{tag}'
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                if target_code in response.text:
                    found_in_tags.append(tag)
                    print(f"  ✅ 在 {tag} 标签页面中找到该配色方案")
                else:
                    print(f"  ❌ 在 {tag} 标签页面中未找到该配色方案")
            else:
                print(f"  ⚠️ 标签页面 {tag} 访问失败: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")
        
        time.sleep(0.5)  # 避免请求过快
    
    print(f"\n📊 结果总结:")
    print(f"期望标签: {expected_tags}")
    print(f"实际找到的标签: {found_in_tags}")
    print(f"匹配率: {len(found_in_tags)}/{len(expected_tags)} = {len(found_in_tags)/len(expected_tags)*100:.1f}%")

def main():
    """主函数"""
    print("ColorHunt特定配色方案标签获取测试")
    print("=" * 60)
    
    try:
        test_specific_palette_tags()
        analyze_colorhunt_structure()
        test_alternative_approach()
        
        print("\n🎉 测试完成！")
        print("💡 说明: 通过多种方法尝试获取真实的标签信息")
        print("🔍 检查生成的文件查看详细分析结果。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 