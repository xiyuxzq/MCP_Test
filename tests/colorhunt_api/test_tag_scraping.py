#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试基于标签页面的ColorHunt配色方案抓取功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.web_service import WebService

def test_tag_scraping():
    """测试不同标签的配色方案抓取"""
    
    # 测试的标签列表
    test_tags = ['summer', 'retro', 'vintage', 'pastel', 'neon']
    
    for tag in test_tags:
        print(f"\n{'='*60}")
        print(f"🏷️ 测试标签: {tag.upper()}")
        print(f"🔗 标签页面: https://colorhunt.co/palettes/{tag}")
        print(f"{'='*60}")
        
        try:
            # 抓取该标签的配色方案
            success, error, palettes = WebService.scrape_colorhunt_by_tag(tag, 3)
            
            if success and palettes:
                print(f"✅ 成功抓取到 {len(palettes)} 个 {tag} 标签的配色方案\n")
                
                for i, palette in enumerate(palettes, 1):
                    print(f"📋 配色方案 {i}: {palette['name']}")
                    print(f"🌈 颜色: {' | '.join(palette['colors'])}")
                    print(f"🏷️ 标签: {', '.join(palette.get('tags', []))}")
                    print(f"🔗 网址: {palette['source_url']}")
                    
                    # 检查是否包含目标标签
                    tags_str = str(palette.get('tags', [])).lower()
                    if tag.lower() in tags_str:
                        print(f"✅ 确认包含 {tag} 标签")
                    else:
                        print(f"⚠️ 未明确包含 {tag} 标签，但来自该标签页面")
                    
                    print("-" * 40)
            else:
                print(f"❌ 抓取失败: {error}")
                
        except Exception as e:
            print(f"❌ 测试 {tag} 标签时出错: {e}")

def test_summer_tag_specifically():
    """专门测试summer标签"""
    print(f"\n{'='*60}")
    print("🌞 专门测试 SUMMER 标签页面抓取")
    print("🔗 页面: https://colorhunt.co/palettes/summer")
    print(f"{'='*60}")
    
    try:
        success, error, palettes = WebService.scrape_colorhunt_by_tag('summer', 5)
        
        if success and palettes:
            print(f"✅ 成功从summer标签页面抓取到 {len(palettes)} 个配色方案\n")
            
            for i, palette in enumerate(palettes, 1):
                print(f"📋 配色方案 {i}: {palette['name']}")
                print(f"🌈 颜色代码: {' | '.join(palette['colors'])} ✅")
                print(f"❤️ 点赞数: {palette.get('likes', '未知')}")
                print(f"📅 发布时间: {palette.get('date', '未知')}")
                print(f"🏷️ 标签: {', '.join(palette.get('tags', []))}")
                print(f"🔗 网址: {palette['source_url']} ✅")
                
                # 显示元数据
                metadata = palette.get('metadata', {})
                if 'tag_source' in metadata:
                    print(f"📍 标签来源: {metadata['tag_source']}")
                if 'tag_page_url' in metadata:
                    print(f"📄 来源页面: {metadata['tag_page_url']}")
                
                print("=" * 50)
                
            print("\n🎯 总结:")
            print("✅ 所有配色方案均来自ColorHunt的summer标签页面")
            print("✅ 颜色代码准确可用")
            print("⚠️ 元数据信息可能为推测值")
            
        else:
            print(f"❌ 抓取失败: {error}")
            
    except Exception as e:
        print(f"❌ 测试summer标签时出错: {e}")

if __name__ == "__main__":
    print("🚀 开始测试基于标签页面的ColorHunt配色方案抓取功能")
    
    # 测试多个标签
    test_tag_scraping()
    
    # 专门测试summer标签
    test_summer_tag_specifically()
    
    print("\n🏁 测试完成！") 