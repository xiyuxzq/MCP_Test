#!/usr/bin/env python
"""
测试ColorHunt主要导航标签的修复效果
验证new、popular、random标签是否能正常获取数据
"""
import sys
import os
import json
from colorhunt_gui import ColorHuntScraper

def test_navigation_tags():
    """测试主要导航标签"""
    print("🎨 测试ColorHunt主要导航标签修复效果")
    print("=" * 60)
    
    scraper = ColorHuntScraper()
    
    # 测试主要导航标签
    navigation_tags = ['new', 'popular', 'random']
    
    # 测试具体标签作为对比
    specific_tags = ['pastel', 'vintage', 'dark']
    
    all_tags = navigation_tags + specific_tags
    
    success_count = 0
    total_count = len(all_tags)
    
    for tag in all_tags:
        print(f"\n📋 测试标签: {tag}")
        print("-" * 40)
        
        tag_type = "主要导航" if tag in navigation_tags else "具体标签"
        print(f"🏷️ 标签类型: {tag_type}")
        
        # 获取URL列表
        urls = scraper.get_palette_urls_by_tag(tag, 5)
        
        if not urls:
            print(f"❌ 标签 '{tag}' 无法获取到数据")
            continue
        
        print(f"✅ 获取到 {len(urls)} 个URL")
        success_count += 1
        
        # 测试第一个URL的数据提取
        if urls:
            print(f"\n🔍 测试第一个配色方案:")
            first_url = urls[0]
            print(f"   URL: {first_url}")
            
            palette = scraper.extract_palette_data_from_url(first_url, 0)
            
            if palette:
                print(f"   ✅ 数据提取成功:")
                print(f"   🎨 颜色: {palette['colors']}")
                print(f"   ❤️ 点赞数: {palette['likes']}")
                print(f"   📅 日期: {palette['date']}")
                
                # 保存示例数据
                filename = f"test_{tag}_sample.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(palette, f, indent=2, ensure_ascii=False)
                print(f"   📁 示例已保存: {filename}")
                
            else:
                print(f"   ❌ 数据提取失败")

    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"✅ 成功标签: {success_count}/{total_count}")
    print(f"📈 成功率: {success_count/total_count*100:.1f}%")
    
    # 分类统计
    nav_success = sum(1 for tag in navigation_tags if tag in [t for t in all_tags[:success_count]])
    spec_success = sum(1 for tag in specific_tags if tag in [t for t in all_tags[:success_count]])
    
    print(f"\n📊 分类统计:")
    print(f"🧭 主要导航标签: {nav_success}/{len(navigation_tags)} 成功")
    print(f"🏷️ 具体标签: {spec_success}/{len(specific_tags)} 成功")
    
    if nav_success == len(navigation_tags):
        print("\n🎉 主要导航标签修复成功！")
    else:
        print("\n⚠️ 主要导航标签仍有问题，需要进一步调试")

def main():
    """主函数"""
    print("ColorHunt 主要导航标签测试")
    print("=" * 60)
    
    try:
        test_navigation_tags()
        print("\n🔍 检查生成的JSON文件查看详细数据。")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 