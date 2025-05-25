#!/usr/bin/env python
"""
配色方案图片生成工具
用于将抓取的配色方案转换为图片格式
"""
import os
import json
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Optional
import logging
import math
import argparse
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PaletteImageGenerator:
    """配色方案图片生成器"""
    
    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple:
        """将十六进制颜色代码转换为RGB元组"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def create_palette_image(colors: List[str], palette_id: str, output_dir: str, 
                            width: int = 800, height: int = 400) -> Optional[str]:
        """
        从颜色列表创建配色方案图片
        
        Args:
            colors: 颜色代码列表，如 ["#FF5733", "#33FF57", "#3357FF"]
            palette_id: 配色方案ID
            output_dir: 输出目录路径
            width: 图片宽度，默认800像素
            height: 图片高度，默认400像素
            
        Returns:
            str: 保存的图片路径，如果失败则为None
        """
        try:
            # 确保颜色列表不为空
            if not colors:
                logger.error("颜色列表为空，无法生成配色方案图片")
                return None
                
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)
            
            # 创建一个新图片
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # 计算每个颜色块的高度
            color_height = height // len(colors)
            
            # 绘制颜色块
            for i, color in enumerate(colors):
                try:
                    # 转换颜色格式并验证
                    if not color.startswith('#'):
                        color = f"#{color}"
                    if len(color) != 7:  # #RRGGBB 格式应为7个字符
                        logger.warning(f"跳过无效的颜色代码: {color}")
                        continue
                        
                    # 计算当前颜色块的位置
                    y0 = i * color_height
                    y1 = (i + 1) * color_height
                    
                    # 绘制矩形
                    draw.rectangle([(0, y0), (width, y1)], fill=color)
                    
                    # 尝试添加颜色代码文本
                    try:
                        # 计算文本颜色（深色背景用白色文本，浅色背景用黑色文本）
                        r, g, b = PaletteImageGenerator.hex_to_rgb(color)
                        text_color = "white" if (r + g + b) < 382 else "black"
                        
                        # 绘制颜色代码文本
                        font_size = 24
                        try:
                            font = ImageFont.truetype("Arial", font_size)
                        except IOError:
                            font = ImageFont.load_default()
                            
                        text_pos = (20, y0 + (color_height - font_size) // 2)
                        draw.text(text_pos, color, fill=text_color, font=font)
                    except Exception as e:
                        logger.warning(f"绘制文本时出错: {e}")
                        
                except Exception as e:
                    logger.warning(f"处理颜色 {color} 时出错: {e}")
            
            # 保存图片
            file_name = f"colorhunt_{palette_id}.png"
            file_path = os.path.join(output_dir, file_name)
            img.save(file_path)
            logger.info(f"配色方案图片已保存: {file_path}")
            
            return file_path
            
        except Exception as e:
            logger.exception(f"生成配色方案图片时出错: {str(e)}")
            return None
    
    @staticmethod
    def generate_from_json(json_file_path: str, output_dir: Optional[str] = None) -> Optional[str]:
        """
        从JSON文件生成配色方案图片
        
        Args:
            json_file_path: JSON文件路径
            output_dir: 输出目录，如果为None则与JSON文件保存在同一目录
            
        Returns:
            str: 生成的图片路径，如果失败则为None
        """
        try:
            # 加载JSON文件
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 提取颜色和ID
            colors = data.get('colors', [])
            palette_id = data.get('id', 'unknown')
            
            # 确定输出目录
            if output_dir is None:
                output_dir = os.path.dirname(json_file_path)
            
            # 生成图片
            return PaletteImageGenerator.create_palette_image(colors, palette_id, output_dir)
            
        except Exception as e:
            logger.exception(f"从JSON生成配色方案图片时出错: {str(e)}")
            return None

    @staticmethod
    def extract_colors_from_image(image_path: str, num_colors: int = 4) -> List[str]:
        """
        从图片中提取主要颜色
        
        Args:
            image_path: 图片路径
            num_colors: 要提取的颜色数量
            
        Returns:
            List[str]: 颜色代码列表，如 ["#FF5733", "#33FF57"]
        """
        try:
            # 打开图片
            img = Image.open(image_path)
            
            # 调整图片大小以加快处理速度
            img.thumbnail((200, 200))
            
            # 如果是有透明通道的图片，转换为RGB
            if img.mode == 'RGBA':
                img = img.convert('RGB')
                
            # 获取所有像素
            pixels = list(img.getdata())
            
            # 像素颜色计数
            color_count = {}
            for pixel in pixels:
                if pixel in color_count:
                    color_count[pixel] += 1
                else:
                    color_count[pixel] = 1
            
            # 按出现频率排序
            sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
            
            # 选择最常见的颜色，但忽略太接近的颜色
            result = []
            threshold = 60  # 颜色差异阈值
            
            for color, _ in sorted_colors:
                # 跳过接近白色和黑色的颜色
                r, g, b = color
                # 跳过接近白色的颜色
                if r > 240 and g > 240 and b > 240:
                    continue
                # 跳过接近黑色的颜色
                if r < 15 and g < 15 and b < 15:
                    continue
                
                # 检查是否与已选颜色太接近
                too_close = False
                for selected_color in result:
                    sr, sg, sb = PaletteImageGenerator.hex_to_rgb(selected_color)
                    # 计算颜色距离
                    distance = math.sqrt((r - sr) ** 2 + (g - sg) ** 2 + (b - sb) ** 2)
                    if distance < threshold:
                        too_close = True
                        break
                
                if not too_close:
                    # 转换为十六进制
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    result.append(hex_color)
                    
                    # 如果已经选择了足够的颜色，就退出
                    if len(result) >= num_colors:
                        break
            
            # 如果没有足够的颜色，添加一些默认颜色
            default_colors = ["#3a3845", "#f7ccac", "#c69b7b", "#826f66"]
            while len(result) < num_colors:
                for color in default_colors:
                    if color not in result:
                        result.append(color)
                        break
                if len(result) >= num_colors:
                    break
            
            return result[:num_colors]
            
        except Exception as e:
            logger.exception(f"从图片提取颜色时出错: {str(e)}")
            # 返回默认颜色
            return ["#3a3845", "#f7ccac", "#c69b7b", "#826f66"][:num_colors]

def process_all_json_files(json_dir: str, output_dir: Optional[str] = None) -> int:
    """
    批量处理目录中所有的JSON配色方案文件
    
    Args:
        json_dir: JSON文件目录
        output_dir: 输出目录，如果为None则与JSON文件保存在同一目录
        
    Returns:
        int: 成功处理的文件数量
    """
    try:
        count = 0
        for file_name in os.listdir(json_dir):
            if file_name.endswith('.json') and 'colorhunt' in file_name:
                json_path = os.path.join(json_dir, file_name)
                if PaletteImageGenerator.generate_from_json(json_path, output_dir):
                    count += 1
        return count
    except Exception as e:
        logger.exception(f"批量处理JSON文件时出错: {str(e)}")
        return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='配色方案工具')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # 从JSON创建图片的命令
    create_parser = subparsers.add_parser('create', help='从JSON创建配色方案图片')
    create_parser.add_argument('json_path', help='JSON文件路径或目录')
    create_parser.add_argument('--output', '-o', help='输出目录')
    
    # 从图片提取颜色的命令
    extract_parser = subparsers.add_parser('extract', help='从图片提取配色方案')
    extract_parser.add_argument('image_path', help='图片文件路径')
    extract_parser.add_argument('--colors', '-c', type=int, default=4, help='要提取的颜色数量')
    extract_parser.add_argument('--output', '-o', help='输出目录')
    extract_parser.add_argument('--save', '-s', action='store_true', help='保存提取的配色方案')
    
    # 测试命令
    test_parser = subparsers.add_parser('test', help='测试生成配色方案图片')
    
    args = parser.parse_args()
    
    # 根据命令执行相应的操作
    if args.command == 'create':
        if os.path.isdir(args.json_path):
            count = process_all_json_files(args.json_path, args.output)
            print(f"成功处理 {count} 个配色方案文件")
        else:
            result = PaletteImageGenerator.generate_from_json(args.json_path, args.output)
            if result:
                print(f"配色方案图片已保存到: {result}")
            else:
                print("生成配色方案图片失败")
    
    elif args.command == 'extract':
        colors = PaletteImageGenerator.extract_colors_from_image(args.image_path, args.colors)
        print(f"从图片提取的颜色: {', '.join(colors)}")
        
        if args.save:
            # 生成ID
            import hashlib
            image_hash = hashlib.md5(open(args.image_path, 'rb').read()).hexdigest()[:8]
            palette_id = f"image-{image_hash}"
            
            # 确定输出目录
            output_dir = args.output or os.path.expanduser("~/Downloads/colorhunt_palettes")
            os.makedirs(output_dir, exist_ok=True)
            
            # 保存为JSON
            palette_data = {
                "id": palette_id,
                "name": f"Image Palette {palette_id}",
                "colors": colors,
                "source": "image_extract",
                "source_image": args.image_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            json_path = os.path.join(output_dir, f"image_palette_{palette_id}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(palette_data, f, indent=2)
            print(f"配色方案JSON已保存: {json_path}")
            
            # 生成图片
            img_dir = os.path.join(output_dir, "images")
            os.makedirs(img_dir, exist_ok=True)
            
            img_path = PaletteImageGenerator.create_palette_image(colors, palette_id, img_dir)
            if img_path:
                print(f"配色方案图片已保存: {img_path}")
    
    elif args.command == 'test' or not args.command:
        # 测试生成配色方案图片
        colors = ["#503a65", "#574f7d", "#95b8d1", "#b8e0d4"]
        output_dir = "./outputs"
        os.makedirs(output_dir, exist_ok=True)
        
        img_path = PaletteImageGenerator.create_palette_image(colors, "test", output_dir)
        if img_path:
            print(f"测试配色方案图片已保存: {img_path}")
        
        # 处理下载目录中的所有JSON文件
        download_dir = os.path.expanduser("~/Downloads/colorhunt_palettes")
        if os.path.exists(download_dir):
            count = process_all_json_files(download_dir)
            print(f"成功处理 {count} 个配色方案文件") 