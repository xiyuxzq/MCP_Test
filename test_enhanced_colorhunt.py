#!/usr/bin/env python3
"""
测试增强版ColorHunt配色方案抓取功能
Test enhanced ColorHunt palette scraping functionality
"""

from services.web_service import WebService
import json

def test_enhanced_colorhunt():
    """测试增强版配色方案获取功能"""
    print("=== 测试增强版ColorHunt配色方案抓取 ===")
    
    # 获取3个配色方案
    success, error, palettes = WebService.get_enhanced_colorhunt_palettes(3)
    
    if success and palettes:
        print(f"✅ 成功获取到 {len(palettes)} 个配色方案")
        print("\n" + "="*60)
        
        for i, palette in enumerate(palettes, 1):
            print(f"\n📋 配色方案 {i}")
            print("="*40)
            
            # 使用格式化方法输出详细信息
            formatted_info = WebService.format_palette_info(palette)
            print(formatted_info)
            
            print("\n" + "-"*40)
            
        # 输出JSON格式的原始数据（用于调试）
        print("\n🔍 原始JSON数据预览:")
        for i, palette in enumerate(palettes[:1], 1):  # 只显示第一个的JSON
            print(f"\n配色方案 {i} JSON:")
            print(json.dumps(palette, ensure_ascii=False, indent=2))
            
    else:
        print(f"❌ 获取失败: {error}")
        
    print("\n" + "="*60)
    print("测试完成")

if __name__ == "__main__":
    test_enhanced_colorhunt() 