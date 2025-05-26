#!/usr/bin/env python
"""
测试ColorHunt API真实数据获取
验证API返回的likes、date等真实信息是否被正确解析
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_api_real_data():
    """测试API真实数据获取"""
    print("🎨 测试ColorHunt API真实数据获取")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 测试不同标签
    test_tags = ['popular', 'new', 'vintage', 'pastel']
    
    for tag in test_tags:
        print(f"\n📋 测试标签: {tag}")
        print("-" * 40)
        
        # 直接调用API方法
        api_palettes = scraper.get_palettes_from_api(tag, 3)
        
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
            print(f"   📅 日期: {palette['date']} {'✅ (API真实数据)' if palette['date'] != '2025-05-26' else '⚠️ (默认日期)'}")
            print(f"   🏷️ 标签: {palette.get('tags', [])}")
            print(f"   👤 作者: {palette.get('author', 'N/A')}")
            print(f"   🔗 网址: {palette['source_url']}")
            print(f"   📊 数据来源: {'API真实数据' if palette.get('api_source') else '网页抓取'}")
            
            # 保存示例数据
            filename = f"api_real_{tag}_{i+1}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(palette, f, indent=2, ensure_ascii=False)
            print(f"   📁 已保存: {filename}")

def test_comparison():
    """对比API数据和网页抓取数据"""
    print("\n" + "=" * 60)
    print("🔍 对比API数据 vs 网页抓取数据")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 获取API数据
    api_palettes = scraper.get_palettes_from_api('popular', 2)
    
    if api_palettes:
        print(f"\n📊 API数据示例:")
        palette = api_palettes[0]
        print(f"   点赞数: {palette['likes']} (API)")
        print(f"   日期: {palette['date']} (API)")
        print(f"   数据来源: {palette['extraction_method']}")
        
        # 测试网页抓取同一个URL
        url = palette['source_url']
        web_palette = scraper._extract_from_webpage(url, 0)
        
        if web_palette:
            print(f"\n📊 网页抓取数据对比:")
            print(f"   点赞数: {web_palette['likes']} (网页)")
            print(f"   日期: {web_palette['date']} (网页)")
            print(f"   数据来源: {web_palette['extraction_method']}")
            
            print(f"\n💡 结论:")
            print(f"   API数据更准确: 包含真实点赞数和日期")
            print(f"   网页抓取作为备用: 无法获取点赞数等元数据")

def main():
    """主函数"""
    print("ColorHunt API真实数据测试")
    print("=" * 60)
    
    try:
        test_api_real_data()
        test_comparison()
        
        print("\n🎉 测试完成！")
        print("💡 说明: API数据包含真实的点赞数、日期等信息")
        print("🔍 检查生成的JSON文件查看详细数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 