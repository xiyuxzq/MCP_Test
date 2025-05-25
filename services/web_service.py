"""
网络服务类，负责处理网络请求和网站抓取
"""
import os
import requests
import logging
from typing import Tuple, Optional, List, Dict
from bs4 import BeautifulSoup
import json
import time
import re
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入图片生成器
try:
    from color_palette_generator import PaletteImageGenerator
    PALETTE_IMAGE_SUPPORT = True
except ImportError:
    PALETTE_IMAGE_SUPPORT = False
    logging.warning("无法导入 PaletteImageGenerator，将不会生成配色方案图片")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebService:
    """网络服务类，提供网站抓取和数据下载功能"""
    
    @staticmethod
    def scrape_colorhunt_palettes(limit: int = 5) -> Tuple[bool, Optional[str], Optional[List[Dict]]]:
        """
        抓取colorhunt.co网站的配色方案
        
        Args:
            limit: 要抓取的配色方案数量限制
            
        Returns:
            Tuple[bool, Optional[str], Optional[List[Dict]]]: (是否成功, 错误信息, 配色方案列表)
        """
        try:
            # 创建下载目录
            download_dir = os.path.expanduser("~/Downloads/colorhunt_palettes")
            os.makedirs(download_dir, exist_ok=True)
            logger.info(f"创建或确认下载目录: {download_dir}")
            
            # 创建图片目录
            images_dir = os.path.join(download_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            logger.info(f"创建或确认图片目录: {images_dir}")
            
            # 抓取colorhunt.co网站
            logger.info("开始请求 colorhunt.co 网站...")
            response = requests.get("https://colorhunt.co/", timeout=15)
            if response.status_code != 200:
                error_msg = f"抓取网站失败，状态码: {response.status_code}"
                logger.error(error_msg)
                return False, error_msg, None
                
            # 解析HTML
            logger.info("开始解析HTML内容...")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找配色方案元素
            logger.info(f"查找配色方案元素，限制数量: {limit}")
            palette_elements = soup.select('.palette')[:limit]
            
            if not palette_elements:
                error_msg = "未找到配色方案元素，网站结构可能已变更"
                logger.error(error_msg)
                return False, error_msg, None
            
            logger.info(f"找到 {len(palette_elements)} 个配色方案元素")
            
            # 默认颜色值（当无法提取时使用）
            default_colors = ["#3a3845", "#f7ccac", "#c69b7b", "#826f66"]
            
            # 提取配色方案数据
            palettes = []
            for idx, elem in enumerate(palette_elements):
                try:
                    logger.info(f"处理第 {idx+1} 个配色方案...")
                    
                    # 生成ID
                    palette_id = f"palette-{idx+1}"
                    
                    # 尝试从 .place 元素提取颜色
                    colors = []
                    place_elements = elem.select('.place')
                    
                    if place_elements:
                        logger.info(f"找到 {len(place_elements)} 个 .place 元素")
                        for place_elem in place_elements:
                            style = place_elem.get('style', '')
                            if style and 'background' in style:
                                try:
                                    bg_parts = style.split('background')
                                    if len(bg_parts) > 1:
                                        color_parts = bg_parts[1].split(';')
                                        color_code = color_parts[0].strip().lstrip(':').strip()
                                        if color_code.startswith('#'):
                                            colors.append(color_code)
                                            logger.info(f"提取到颜色代码: {color_code}")
                                except Exception as e:
                                    logger.warning(f"提取颜色时出错: {e}")
                    
                    # 如果未提取到颜色，尝试正则表达式
                    if not colors:
                        html_fragment = str(elem)
                        color_matches = re.findall(r'style="background:(#[0-9a-fA-F]{6})"', html_fragment)
                        if color_matches:
                            for color in color_matches:
                                colors.append(color)
                                logger.info(f"通过正则提取到颜色代码: {color}")
                    
                    # 如果仍未提取到颜色，使用默认颜色
                    if not colors:
                        colors = default_colors.copy()
                        logger.warning(f"未能提取到颜色，使用默认颜色")
                    
                    # 将方案保存为JSON文件
                    palette_data = {
                        "id": palette_id,
                        "name": f"ColorHunt Palette {palette_id}",
                        "colors": colors,
                        "source": "colorhunt.co",
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # 保存JSON文件
                    json_path = os.path.join(download_dir, f"colorhunt_{palette_id}.json")
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(palette_data, f, indent=2)
                    logger.info(f"配色方案JSON已保存: {json_path}")
                    
                    # 保存图片
                    if PALETTE_IMAGE_SUPPORT:
                        try:
                            img_path = PaletteImageGenerator.create_palette_image(
                                colors, palette_id, images_dir
                            )
                            palette_data["image_path"] = img_path
                            logger.info(f"配色方案图片已保存: {img_path}")
                        except Exception as e:
                            logger.warning(f"生成配色方案图片时出错: {e}")
                    
                    palettes.append(palette_data)
                    
                except Exception as e:
                    logger.exception(f"处理配色方案时出错: {str(e)}")
            
            if not palettes:
                return False, "未能成功提取任何配色方案", None
                
            logger.info(f"成功抓取并处理了 {len(palettes)} 个配色方案")
            return True, None, palettes
            
        except requests.RequestException as e:
            error_msg = f"网络请求错误: {str(e)}"
            logger.exception(error_msg)
            return False, error_msg, None
        except Exception as e:
            error_msg = f"抓取配色方案时出错: {str(e)}"
            logger.exception(error_msg)
            return False, error_msg, None
            
    @staticmethod
    def debug_html_structure(html_content: str) -> str:
        """
        调试用方法：分析HTML结构，查找可能的配色方案元素
        
        Args:
            html_content: HTML内容
            
        Returns:
            str: 分析结果
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 尝试不同的选择器
            selectors = ['.palette', '.palettes', '.color-palette', '.colors', '[data-id]']
            results = []
            
            for selector in selectors:
                elements = soup.select(selector)
                results.append(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
                
                # 输出前2个元素的信息
                if elements and len(elements) > 0:
                    for i, elem in enumerate(elements[:2]):
                        results.append(f"  - 元素 {i+1}: {elem.name}, 类: {elem.get('class')}, ID: {elem.get('id')}")
                        results.append(f"    属性: {elem.attrs}")
            
            return "\n".join(results)
            
        except Exception as e:
            return f"分析HTML结构时出错: {str(e)}" 