#!/usr/bin/env python
"""
生成20个配色方案
"""
from color_palette_generator import PaletteImageGenerator
import os
import json
import time

# 创建目录
output_dir = os.path.expanduser('~/Downloads/colorhunt_palettes')
images_dir = os.path.join(output_dir, 'images')
os.makedirs(output_dir, exist_ok=True)
os.makedirs(images_dir, exist_ok=True)

# 20个配色方案
palettes = [
    ['#503a65', '#574f7d', '#95b8d1', '#b8e0d4'],  # 紫色渐变
    ['#ffd3d0', '#ffddd0', '#ffe6d0', '#ffefd0'],  # 粉色渐变
    ['#fff5b8', '#ffce81', '#ff9b82', '#ff5c84'],  # 黄橙红渐变
    ['#282f3c', '#4d6d9a', '#8dbbde', '#ffffff'],  # 蓝灰渐变
    ['#f8b195', '#f67280', '#c06c84', '#6c5b7b'],  # 粉紫渐变
    ['#a8e6cf', '#dcedc1', '#ffd3b6', '#ffaaa5'],  # 柔和色调
    ['#222831', '#393e46', '#00adb5', '#eeeeee'],  # 深蓝绿配色
    ['#fbf0f0', '#dfd3d3', '#b8b0b0', '#7c7575'],  # 灰色渐变
    ['#f4f9f9', '#ccf2f4', '#a4ebf3', '#aaaaaa'],  # 淡蓝灰配色
    ['#f38181', '#fce38a', '#eaffd0', '#95e1d3'],  # 红黄绿配色
    ['#f9ed69', '#f08a5d', '#b83b5e', '#6a2c70'],  # 黄橙紫配色
    ['#f9f7f7', '#dbe2ef', '#3f72af', '#112d4e'],  # 蓝白配色
    ['#364f6b', '#3fc1c9', '#f5f5f5', '#fc5185'],  # 蓝灰粉配色
    ['#084177', '#687466', '#cd8d7b', '#fbc490'],  # 深蓝棕配色
    ['#e4f9f5', '#30e3ca', '#11999e', '#40514e'],  # 青绿配色
    ['#f6f6f6', '#d6e4f0', '#1e56a0', '#163172'],  # 蓝白配色2
    ['#f7fbfc', '#d6e6f2', '#b9d7ea', '#769fcd'],  # 蓝色渐变
    ['#d3f8e2', '#e4c1f9', '#f694c1', '#ede7b1'],  # 柔和彩虹
    ['#fff8e1', '#ffcdd2', '#f8bbd0', '#e1bee7'],  # 柔和粉色
    ['#005c97', '#363795', '#7c3679', '#f96167']   # 蓝紫红配色
]

# 为每个配色方案生成图片和JSON
for i, colors in enumerate(palettes):
    palette_id = f'custom-{i+1}'
    
    # 生成JSON
    palette_data = {
        'id': palette_id,
        'name': f'Custom Palette {i+1}',
        'colors': colors,
        'source': 'custom',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # 保存JSON
    json_path = os.path.join(output_dir, f'colorhunt_{palette_id}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(palette_data, f, indent=2)
    print(f'保存JSON: {json_path}')
    
    # 生成图片
    img_path = PaletteImageGenerator.create_palette_image(
        colors, palette_id, images_dir
    )
    if img_path:
        print(f'生成图片: {img_path}')

print('完成生成20个配色方案') 