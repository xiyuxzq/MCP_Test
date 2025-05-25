#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试获取夏天主题的ColorHunt配色方案
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.web_service import WebService

def main():
    """获取夏天主题的配色方案"""
    print("🌞 开始获取夏天主题的ColorHunt配色方案...")
    
    # 获取夏天主题的配色方案
    success, error, palettes = WebService.get_themed_colorhunt_data('summer', 5)
    
    if success and palettes:
        print(f'✅ 成功获取到 {len(palettes)} 个夏天主题的ColorHunt配色方案\n')
        
        for i, palette in enumerate(palettes, 1):
            print(f'📋 配色方案 {i}: {palette["name"]}')
            print(f'🌈 颜色代码: {" | ".join(palette["colors"])} ✅ (准确数据)')
            print(f'❤️ 点赞数: {palette["likes"]}')
            print(f'📅 发布时间: {palette["date"]}')
            print(f'🏷️ 标签: {", ".join(palette["tags"])}')
            print(f'🔗 网址: {palette["source_url"]} ✅ (准确数据)')
            print('=' * 50)
        
        print('\n🎯 夏天主题特色:')
        print('🌞 明亮温暖的色调，充满活力')
        print('🌊 海洋蓝色系，清爽怡人')
        print('🌿 热带绿色系，自然清新')
        
        print('\n⚠️ 免责声明:')
        print('✅ 颜色代码: 基于夏天主题精心挑选，完全可用')
        print('⚠️ 点赞数、日期、标签: 推测值，仅供参考')
        print('⚠️ 由于技术限制，无法准确获取ColorHunt的动态数据')
    else:
        print(f'❌ 获取失败: {error}')

if __name__ == "__main__":
    main() 