#!/usr/bin/env python
"""
直接抓取单个配色方案的简单脚本
"""
import os
import requests
import json
import time
from PIL import Image, ImageDraw

def get_one_palette():
    """获取一个特定的配色方案"""
    # 特定的配色方案URL
    url = "https://colorhunt.co/palette/222831-393e46-00adb5-eeeeee"
    
    # 发送请求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None
            
        # 直接从URL提取颜色
        palette_id = url.split('/')[-1]
        colors = ["#" + part for part in palette_id.split('-')]
        
        # 创建配色方案数据
        palette_data = {
            "id": "realtime-4-222831-393e46-00adb5-eeeeee",
            "name": "Color Palette: #222831 #-393E4 #6-00AD #B5-EEE #EEE - Color Hunt",
            "colors": colors,
            "source": "colorhunt.co",
            "source_url": url,
            "palette_id": palette_id,
            "date": "Today",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 创建下载目录
        download_dir = os.path.expanduser("~/Downloads/colorhunt_palettes")
        os.makedirs(download_dir, exist_ok=True)
        
        # 创建图片目录
        images_dir = os.path.join(download_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # 保存JSON文件
        json_path = os.path.join(download_dir, f"colorhunt_{palette_data['id']}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(palette_data, f, indent=2, ensure_ascii=False)
        print(f"配色方案JSON已保存: {json_path}")
        
        # 生成并保存图片
        img_path = create_palette_image(palette_data['colors'], palette_data['id'], images_dir)
        print(f"配色方案图片已保存: {img_path}")
        
        return palette_data
        
    except Exception as e:
        print(f"抓取配色方案时出错: {e}")
        return None

def create_palette_image(colors, palette_id, output_dir):
    """创建配色方案图片"""
    width, height = 400, 100
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # 计算每个颜色块的宽度
    block_width = width // len(colors)
    
    # 绘制颜色块
    for i, color in enumerate(colors):
        x0 = i * block_width
        x1 = (i + 1) * block_width
        draw.rectangle([x0, 0, x1, height], fill=color)
    
    # 保存图片
    img_path = os.path.join(output_dir, f"colorhunt_{palette_id}.png")
    img.save(img_path)
    
    return img_path

if __name__ == "__main__":
    palette = get_one_palette()
    if palette:
        print("成功获取配色方案:")
        print(f"颜色代码: {', '.join(palette['colors'])}")
        print(f"网址来源: {palette['source_url']}") 