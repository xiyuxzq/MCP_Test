#!/usr/bin/env python
"""
测试真实ColorHunt数据获取
验证改进后的爬虫能否获取到真实的配色方案数据
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_real_colorhunt_data():
    """测试获取真实ColorHunt数据"""
    print("🎨 测试获取真实ColorHunt数据")
    print("=" * 50)
    
    scraper = ColorHuntScraper()
    
    # 测试不同标签
    test_tags = ['popular', 'vintage', 'pastel', 'dark']
    
    for tag in test_tags:
        print(f"\n📋 测试标签: {tag}")
        print("-" * 30)
        
        # 获取URL列表
        urls = scraper.get_palette_urls_by_tag(tag, 3)
        print(f"获取到 {len(urls)} 个URL")
        
        if not urls:
            print("❌ 未获取到任何URL")
            continue
        
        # 测试提取数据
        for i, url in enumerate(urls[:2]):  # 只测试前2个
            print(f"\n🔍 测试URL {i+1}: {url}")
            
            palette = scraper.extract_palette_data_from_url(url, i)
            
            if palette:
                print(f"✅ 成功提取配色方案:")
                print(f"   ID: {palette['id']}")
                print(f"   名称: {palette['name']}")
                print(f"   颜色: {palette['colors']}")
                print(f"   点赞数: {palette['likes']}")
                print(f"   日期: {palette['date']}")
                print(f"   网址: {palette['source_url']}")
                
                # 保存为JSON文件
                filename = f"test_palette_{tag}_{i+1}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(palette, f, indent=2, ensure_ascii=False)
                print(f"   已保存到: {filename}")
                
            else:
                print(f"❌ 提取失败")

def main():
    """主函数"""
    print("ColorHunt 真实数据测试")
    print("=" * 50)
    
    try:
        test_real_colorhunt_data()
        print("\n🎉 测试完成！")
        print("检查生成的JSON文件查看详细数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 