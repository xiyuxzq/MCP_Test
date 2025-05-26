#!/usr/bin/env python
"""
调试ColorHunt API响应，查看原始数据结构
分析哪些字段包含真实的日期和标签信息
"""
import sys
import os
import json
import requests

def debug_api_response():
    """调试API响应数据"""
    print("🔍 调试ColorHunt API响应数据")
    print("=" * 60)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://colorhunt.co/'
    }
    
    # 测试不同的API参数
    test_cases = [
        ('popular', {'step': 0, 'sort': 'popular', 'tags': '', 'timeframe': '30'}),
        ('vintage', {'step': 0, 'sort': 'new', 'tags': 'vintage', 'timeframe': ''}),
        ('new', {'step': 0, 'sort': 'new', 'tags': '', 'timeframe': ''})
    ]
    
    for tag, post_data in test_cases:
        print(f"\n📋 测试标签: {tag}")
        print(f"📝 API参数: {post_data}")
        print("-" * 40)
        
        try:
            response = requests.post(
                'https://colorhunt.co/php/feed.php', 
                headers=headers, 
                data=post_data,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    api_data = json.loads(response.text)
                    if api_data and len(api_data) > 0:
                        print(f"✅ API成功返回 {len(api_data)} 个配色方案")
                        
                        # 分析前3个配色方案的数据结构
                        for i, item in enumerate(api_data[:3]):
                            print(f"\n🎨 配色方案 {i+1} 原始数据:")
                            print(f"   所有字段: {list(item.keys())}")
                            
                            # 显示所有字段的值
                            for key, value in item.items():
                                print(f"   {key}: {repr(value)}")
                            
                            # 保存原始数据
                            filename = f"debug_api_{tag}_{i+1}.json"
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(item, f, indent=2, ensure_ascii=False)
                            print(f"   📁 已保存原始数据: {filename}")
                            
                            if i == 0:  # 只详细分析第一个
                                break
                    else:
                        print(f"❌ API返回空数据")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON解析失败: {e}")
                    print(f"原始响应: {response.text[:200]}...")
            else:
                print(f"❌ API请求失败, 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def analyze_date_formats():
    """分析不同的日期格式"""
    print("\n" + "=" * 60)
    print("📅 分析日期格式")
    print("=" * 60)
    
    # 从之前的测试数据中观察到的日期格式
    date_examples = [
        "4 weeks",
        "9 months", 
        "9 years",
        "1 hour",
        "2 days",
        "3 weeks"
    ]
    
    print("观察到的日期格式:")
    for date in date_examples:
        print(f"   - {date}")
    
    print("\n💡 分析:")
    print("   - API返回的是相对时间格式（如 '4 weeks', '9 months'）")
    print("   - 这些是真实的发布时间，不是绝对日期")
    print("   - 格式：数字 + 时间单位（hour/day/week/month/year）")

def main():
    """主函数"""
    print("ColorHunt API数据结构调试")
    print("=" * 60)
    
    try:
        debug_api_response()
        analyze_date_formats()
        
        print("\n🎉 调试完成！")
        print("🔍 检查生成的debug_api_*.json文件查看完整的API数据结构。")
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 