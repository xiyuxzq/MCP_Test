#!/usr/bin/env python
"""
测试真实日期和标签获取功能
验证API返回的真实日期是否正确使用，以及标签获取是否有效
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_real_date_and_tags():
    """测试真实日期和标签获取"""
    print("🎨 测试ColorHunt真实日期和标签获取")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 测试不同标签
    test_tags = ['popular', 'vintage', 'nature']
    
    for tag in test_tags:
        print(f"\n📋 测试标签: {tag}")
        print("-" * 40)
        
        # 直接调用API方法
        api_palettes = scraper.get_palettes_from_api(tag, 2)
        
        if not api_palettes:
            print(f"❌ API无法获取标签 '{tag}' 的数据")
            continue
        
        print(f"✅ API成功获取 {len(api_palettes)} 个配色方案")
        
        for i, palette in enumerate(api_palettes):
            print(f"\n🎨 配色方案 {i+1}:")
            print(f"   ID: {palette['id']}")
            print(f"   名称: {palette['name']}")
            print(f"   颜色: {palette['colors']}")
            print(f"   ❤️ 点赞数: {palette['likes']} {'✅ (API真实数据)' if palette['likes'] > 0 else '⚠️ (无点赞数据)'}")
            print(f"   📅 日期: {palette['date']} {'✅ (API真实相对时间)' if palette['date'] and 'weeks' in palette['date'] or 'days' in palette['date'] or 'months' in palette['date'] or 'years' in palette['date'] or 'hour' in palette['date'] else '⚠️ (非相对时间格式)'}")
            print(f"   🏷️ 标签: {palette['tags']} {'✅ (已获取标签)' if palette['tags'] else '⚠️ (无标签数据)'}")
            print(f"   🔗 网址: {palette['source_url']}")
            print(f"   📊 数据来源: {'API+网页' if palette.get('api_source') else '网页抓取'}")
            
            # 保存示例数据
            filename = f"real_date_tags_{tag}_{i+1}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(palette, f, indent=2, ensure_ascii=False)
            print(f"   📁 已保存: {filename}")

def analyze_date_formats():
    """分析日期格式的正确性"""
    print("\n" + "=" * 60)
    print("📅 分析日期格式正确性")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 获取一些配色方案数据
    api_palettes = scraper.get_palettes_from_api('popular', 5)
    
    if api_palettes:
        print("✅ 日期格式分析:")
        for i, palette in enumerate(api_palettes):
            date = palette['date']
            print(f"   配色方案{i+1}: {date}")
            
            # 验证日期格式
            if any(unit in date for unit in ['hour', 'day', 'week', 'month', 'year']):
                print(f"     ✅ 正确的相对时间格式")
            else:
                print(f"     ⚠️ 非标准相对时间格式")
        
        print(f"\n💡 总结:")
        print(f"   - API返回的日期是相对时间格式（如 '4 weeks', '3 days'）")
        print(f"   - 这些是真实的发布时间，比绝对日期更有意义")
        print(f"   - 用户可以直观了解配色方案的新旧程度")

def test_specific_palette():
    """测试截图中的特定配色方案"""
    print("\n" + "=" * 60)
    print("🔍 测试截图中的特定配色方案")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 截图中的配色方案
    target_code = "626f47a4b465f5ecd5f0bb78"
    target_url = f"https://colorhunt.co/palette/{target_code}"
    
    print(f"🎯 目标配色方案: {target_code}")
    print(f"🔗 URL: {target_url}")
    
    # 从popular API中查找这个配色方案
    api_palettes = scraper.get_palettes_from_api('popular', 20)
    
    found_palette = None
    for palette in api_palettes:
        if palette['palette_id'] == target_code:
            found_palette = palette
            break
    
    if found_palette:
        print(f"\n✅ 在API数据中找到目标配色方案:")
        print(f"   颜色: {found_palette['colors']}")
        print(f"   点赞数: {found_palette['likes']} (截图显示: 2,347)")
        print(f"   日期: {found_palette['date']} (截图显示: 4 weeks)")
        print(f"   标签: {found_palette['tags']} (截图显示: Sage, Green, Beige, Nature, Earth, Summer, Food, Vintage)")
        
        # 验证数据一致性
        if str(found_palette['likes']) in ['2347', '2348']:  # API可能有轻微差异
            print(f"   ✅ 点赞数与截图基本一致")
        else:
            print(f"   ⚠️ 点赞数与截图不一致")
        
        if found_palette['date'] == '4 weeks':
            print(f"   ✅ 日期与截图完全一致")
        else:
            print(f"   ⚠️ 日期与截图不一致")
    else:
        print(f"❌ 未在API数据中找到目标配色方案")

def main():
    """主函数"""
    print("ColorHunt真实日期和标签测试")
    print("=" * 60)
    
    try:
        test_real_date_and_tags()
        analyze_date_formats()
        test_specific_palette()
        
        print("\n🎉 测试完成！")
        print("💡 说明: 现在使用API的真实相对时间格式，并尝试获取标签信息")
        print("🔍 检查生成的JSON文件查看详细数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 