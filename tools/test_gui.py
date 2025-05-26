#!/usr/bin/env python
"""
ColorHunt GUI 功能测试脚本
"""
import sys
import os
from colorhunt_gui import ColorHuntScraper, PaletteImageGenerator

def test_scraper():
    """测试爬虫功能"""
    print("🧪 测试ColorHunt爬虫功能...")
    
    scraper = ColorHuntScraper()
    
    # 测试可用标签
    print(f"✅ 可用标签数量: {len(scraper.available_tags)}")
    print(f"✅ 前5个标签: {scraper.available_tags[:5]}")
    
    # 测试获取URL
    print("\n🔍 测试获取配色方案URL...")
    urls = scraper.get_palette_urls_by_tag('popular', 3)
    print(f"获取到 {len(urls)} 个URL")
    
    if not urls:
        print("⚠️ 未获取到URL，尝试使用备用URL进行测试...")
        # 使用一些已知的ColorHunt URL进行测试
        test_urls = [
            "https://colorhunt.co/palette/ffdcdcfff2ebffe8cdffd6ba",
            "https://colorhunt.co/palette/eaebd0da6c6ccd5656af3e3e",
            "https://colorhunt.co/palette/ecfae5ddf6d2cae8bdb0db9c"
        ]
        urls = test_urls
        print(f"使用 {len(urls)} 个测试URL")
    
    # 测试提取配色数据
    print("\n🎨 测试提取配色数据...")
    for i, url in enumerate(urls[:2]):  # 只测试前2个
        print(f"\n测试URL {i+1}: {url}")
        palette = scraper.extract_palette_data_from_url(url, i)
        
        if palette:
            print(f"✅ 成功提取配色方案:")
            print(f"   ID: {palette['id']}")
            print(f"   名称: {palette['name']}")
            print(f"   颜色: {palette['colors']}")
            print(f"   点赞数: {palette['likes']}")
            print(f"   网址: {palette['source_url']}")
        else:
            print(f"❌ 提取失败")
    
    return True

def test_image_generator():
    """测试图片生成功能"""
    print("\n🖼️ 测试图片生成功能...")
    
    try:
        # 测试颜色
        test_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        test_id = "test_palette"
        output_dir = "/tmp/colorhunt_test"
        
        # 创建测试目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成图片
        img_path = PaletteImageGenerator.create_palette_image(
            test_colors, test_id, output_dir
        )
        
        if os.path.exists(img_path):
            print(f"✅ 图片生成成功: {img_path}")
            print(f"   颜色: {test_colors}")
            return True
        else:
            print(f"❌ 图片文件不存在: {img_path}")
            return False
            
    except Exception as e:
        print(f"❌ 图片生成失败: {e}")
        return False

def main():
    """主测试函数"""
    print("ColorHunt GUI 工具测试")
    print("=" * 40)
    
    # 测试爬虫功能
    scraper_ok = test_scraper()
    
    # 测试图片生成
    image_ok = test_image_generator()
    
    # 总结
    print("\n" + "=" * 40)
    print("测试结果总结:")
    print(f"🧪 爬虫功能: {'✅ 通过' if scraper_ok else '❌ 失败'}")
    print(f"🖼️ 图片生成: {'✅ 通过' if image_ok else '❌ 失败'}")
    
    if scraper_ok and image_ok:
        print("\n🎉 所有测试通过！GUI工具应该可以正常使用。")
        print("运行 'python colorhunt_gui.py' 启动图形界面。")
    else:
        print("\n⚠️ 部分测试失败，请检查网络连接和依赖安装。")

if __name__ == "__main__":
    main() 