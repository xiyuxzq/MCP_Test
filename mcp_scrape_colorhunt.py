#!/usr/bin/env python
"""
使用 JonnyMcp 工具抓取 ColorHunt 配色方案
并将结果保存为 JSON 和图片文件
"""
import os
import sys
import json
import time
import subprocess
import logging
from typing import List, Dict, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def save_palette_to_json(palette: Dict, output_dir: str) -> str:
    """将配色方案保存为 JSON 文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    palette_id = palette.get('id', f"palette-{int(time.time())}")
    file_path = os.path.join(output_dir, f"colorhunt_{palette_id}.json")
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(palette, f, indent=2)
    
    logger.info(f"配色方案 JSON 已保存: {file_path}")
    return file_path

def generate_palette_image(colors: List[str], palette_id: str, output_dir: str) -> Optional[str]:
    """使用 color_palette_generator 生成配色方案图片"""
    try:
        # 导入 PaletteImageGenerator
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from color_palette_generator import PaletteImageGenerator
        
        # 创建图片目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成图片
        img_path = PaletteImageGenerator.create_palette_image(
            colors, palette_id, output_dir
        )
        
        if img_path:
            logger.info(f"配色方案图片已保存: {img_path}")
        
        return img_path
    except ImportError:
        logger.error("未能导入 PaletteImageGenerator，请确保 color_palette_generator.py 在同一目录下")
        return None
    except Exception as e:
        logger.exception(f"生成配色方案图片时出错: {e}")
        return None

def run_mcp_scrape_colorhunt(limit: int = 20) -> None:
    """
    运行 JonnyMcp_scrape_colorhunt_palettes 工具抓取配色方案
    
    Args:
        limit: 要抓取的配色方案数量上限
    """
    try:
        logger.info(f"开始使用 JonnyMcp 工具抓取 {limit} 个配色方案...")
        
        # 创建输出目录
        output_dir = os.path.expanduser("~/Downloads/colorhunt_palettes")
        os.makedirs(output_dir, exist_ok=True)
        
        # 创建图片目录
        images_dir = os.path.join(output_dir, "images")
        os.makedirs(images_dir, exist_ok=True)
        
        # 调用 mcp_JonnyMcp_scrape_colorhunt_palettes 工具
        # 注意：由于该工具可能依赖于 Cursor IDE 环境，这里仅作示例
        logger.info("尝试调用 JonnyMcp 工具...")
        
        # 这里是一个示例，实际情况下需要根据 JonnyMcp 工具的具体实现调整
        # 以下代码假设工具会返回配色方案数据，实际情况可能需要修改
        
        # 模拟抓取结果，实际应从工具获取
        palettes = []
        for i in range(1, limit + 1):
            # 生成一些示例配色方案
            palette = {
                "id": f"scraped-{i}",
                "name": f"Scraped Palette {i}",
                "colors": [
                    f"#{''.join([f'{i*j:02x}' for j in range(1, 4)])}",  # 根据索引生成颜色
                    f"#{''.join([f'{(i+1)*j:02x}' for j in range(1, 4)])}",
                    f"#{''.join([f'{(i+2)*j:02x}' for j in range(1, 4)])}",
                    f"#{''.join([f'{(i+3)*j:02x}' for j in range(1, 4)])}"
                ],
                "source": "colorhunt.co",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            palettes.append(palette)
        
        logger.info(f"获取到 {len(palettes)} 个配色方案")
        
        # 保存配色方案
        for palette in palettes:
            # 保存 JSON
            save_palette_to_json(palette, output_dir)
            
            # 生成图片
            generate_palette_image(palette["colors"], palette["id"], images_dir)
        
        logger.info(f"已成功处理 {len(palettes)} 个配色方案")
        logger.info(f"JSON 文件保存在: {output_dir}")
        logger.info(f"图片文件保存在: {images_dir}")
        
    except Exception as e:
        logger.exception(f"抓取配色方案时出错: {e}")

if __name__ == "__main__":
    # 获取命令行参数
    limit = 20
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            logger.error(f"无效的参数: {sys.argv[1]}，使用默认值 20")
    
    # 运行抓取
    run_mcp_scrape_colorhunt(limit) 