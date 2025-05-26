#!/usr/bin/env python
"""
测试纯真实ColorHunt数据获取
验证改进后的爬虫只获取真实数据，无法获取时返回失败
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_real_only_data():
    """测试只获取真实数据"""
    print("🎨 测试纯真实ColorHunt数据获取")
    print("=" * 50)
    print("⚠️  注意：此版本只获取真实数据，无法获取时会返回失败")
    print()
    
    scraper = ColorHuntScraper()
    
    # 测试不同标签
    test_tags = ['popular', 'vintage', 'pastel', 'dark', 'nonexistent']
    
    total_success = 0
    total_failed = 0
    
    for tag in test_tags:
        print(f"\n📋 测试标签: {tag}")
        print("-" * 30)
        
        # 获取URL列表
        urls = scraper.get_palette_urls_by_tag(tag, 5)
        
        if not urls:
            print(f"❌ 标签 '{tag}' 无法获取到真实数据")
            total_failed += 1
            continue
        
        print(f"✅ 获取到 {len(urls)} 个真实URL")
        
        # 测试提取数据
        success_count = 0
        for i, url in enumerate(urls[:3]):  # 只测试前3个
            print(f"\n🔍 测试URL {i+1}: {url}")
            
            palette = scraper.extract_palette_data_from_url(url, i)
            
            if palette:
                print(f"✅ 成功提取真实配色方案:")
                print(f"   ID: {palette['id']}")
                print(f"   名称: {palette['name']}")
                print(f"   颜色: {palette['colors']}")
                print(f"   点赞数: {palette['likes']} {'(真实数据)' if palette['likes'] > 0 else '(未获取到)'}")
                print(f"   日期: {palette['date']}")
                print(f"   网址: {palette['source_url']}")
                
                # 验证数据完整性
                if len(palette['colors']) == 4:
                    print(f"   ✅ 颜色数据完整 (4种颜色)")
                else:
                    print(f"   ⚠️ 颜色数据不完整 ({len(palette['colors'])}种颜色)")
                
                # 保存为JSON文件
                filename = f"real_palette_{tag}_{i+1}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(palette, f, indent=2, ensure_ascii=False)
                print(f"   📁 已保存到: {filename}")
                
                success_count += 1
                
            else:
                print(f"❌ 提取失败 - 数据不完整或无法获取真实数据")
        
        if success_count > 0:
            print(f"\n✅ 标签 '{tag}' 成功获取 {success_count} 个真实配色方案")
            total_success += 1
        else:
            print(f"\n❌ 标签 '{tag}' 未能获取到任何有效的真实数据")
            total_failed += 1

    # 总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"✅ 成功标签: {total_success}")
    print(f"❌ 失败标签: {total_failed}")
    print(f"📈 成功率: {total_success/(total_success+total_failed)*100:.1f}%")
    
    if total_success > 0:
        print("\n🎉 成功获取到真实数据！")
        print("💡 说明：所有数据均来自ColorHunt网站，无任何模拟或备用数据")
    else:
        print("\n⚠️ 未能获取到任何真实数据")
        print("💡 可能原因：网络连接问题、网站结构变化或API限制")

def main():
    """主函数"""
    print("ColorHunt 纯真实数据测试")
    print("=" * 50)
    
    try:
        test_real_only_data()
        print("\n🔍 检查生成的JSON文件查看真实数据详情。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 