#!/usr/bin/env python
"""
测试ColorHunt Popular时间范围子分类功能
验证popular-month、popular-year、popular-alltime是否能正常工作
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_popular_timeframes():
    """测试Popular时间范围子分类"""
    print("🎨 测试ColorHunt Popular时间范围子分类")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 测试Popular的不同时间范围
    popular_tags = [
        ('popular', '默认Popular (30天)'),
        ('popular-month', 'Popular - Month (30天)'),
        ('popular-year', 'Popular - Year (365天)'),
        ('popular-alltime', 'Popular - All Time (所有时间)')
    ]
    
    success_count = 0
    total_count = len(popular_tags)
    
    for tag, description in popular_tags:
        print(f"\n📋 测试标签: {tag}")
        print(f"📝 描述: {description}")
        print("-" * 40)
        
        # 直接调用API方法
        api_palettes = scraper.get_palettes_from_api(tag, 3)
        
        if not api_palettes:
            print(f"❌ API无法获取标签 '{tag}' 的数据")
            continue
        
        print(f"✅ API成功获取 {len(api_palettes)} 个配色方案")
        success_count += 1
        
        # 显示前3个配色方案的统计信息
        likes_list = [p['likes'] for p in api_palettes]
        dates_list = [p['date'] for p in api_palettes]
        
        print(f"📊 点赞数范围: {min(likes_list)} - {max(likes_list)}")
        print(f"📅 时间范围: {dates_list}")
        
        # 保存第一个配色方案作为示例
        if api_palettes:
            palette = api_palettes[0]
            print(f"\n🎨 示例配色方案:")
            print(f"   名称: {palette['name']}")
            print(f"   颜色: {palette['colors']}")
            print(f"   ❤️ 点赞数: {palette['likes']}")
            print(f"   📅 日期: {palette['date']}")
            print(f"   🔗 网址: {palette['source_url']}")
            
            # 保存示例数据
            filename = f"popular_timeframe_{tag.replace('-', '_')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(palette, f, indent=2, ensure_ascii=False)
            print(f"   📁 已保存: {filename}")

def compare_timeframes():
    """对比不同时间范围的数据差异"""
    print("\n" + "=" * 60)
    print("🔍 对比不同时间范围的Popular数据")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    timeframes = ['popular-month', 'popular-year', 'popular-alltime']
    results = {}
    
    for tag in timeframes:
        api_palettes = scraper.get_palettes_from_api(tag, 5)
        if api_palettes:
            likes_list = [p['likes'] for p in api_palettes]
            results[tag] = {
                'count': len(api_palettes),
                'max_likes': max(likes_list),
                'min_likes': min(likes_list),
                'avg_likes': sum(likes_list) / len(likes_list)
            }
    
    print(f"\n📊 数据对比:")
    for tag, data in results.items():
        timeframe_name = tag.replace('popular-', '').title()
        print(f"\n🏷️ {timeframe_name}:")
        print(f"   配色方案数: {data['count']}")
        print(f"   最高点赞数: {data['max_likes']}")
        print(f"   最低点赞数: {data['min_likes']}")
        print(f"   平均点赞数: {data['avg_likes']:.1f}")
    
    print(f"\n💡 分析:")
    if 'popular-alltime' in results and 'popular-month' in results:
        alltime_max = results['popular-alltime']['max_likes']
        month_max = results['popular-month']['max_likes']
        print(f"   All Time vs Month 最高点赞数比较: {alltime_max} vs {month_max}")
        if alltime_max > month_max:
            print(f"   ✅ All Time 数据包含更高点赞数的历史热门配色方案")
        else:
            print(f"   ⚠️ 当前月度热门可能超过历史记录")

def main():
    """主函数"""
    print("ColorHunt Popular时间范围测试")
    print("=" * 60)
    
    try:
        test_popular_timeframes()
        compare_timeframes()
        
        print("\n🎉 测试完成！")
        print("💡 说明: Popular标签现在支持Month、Year、All Time时间范围")
        print("🔍 检查生成的JSON文件查看详细数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 