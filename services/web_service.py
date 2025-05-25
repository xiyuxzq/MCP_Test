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
import random
import concurrent.futures

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
    def get_palette_urls() -> List[str]:
        """
        获取调色板URL列表
        
        Returns:
            List[str]: URL列表
        """
        # 探索不同类型的调色板页面
        explore_urls = [
            "https://colorhunt.co/",
            "https://colorhunt.co/palettes/popular",
            "https://colorhunt.co/palettes/new",
            "https://colorhunt.co/palettes/random",
            "https://colorhunt.co/palettes/pastel",
            "https://colorhunt.co/palettes/dark"
        ]
        
        # 收集调色板URL
        palette_urls = []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }
        
        for url in explore_urls:
            try:
                logger.info(f"探索页面: {url}")
                response = requests.get(url, headers=headers, timeout=15)
                if response.status_code != 200:
                    logger.warning(f"请求 {url} 失败, 状态码: {response.status_code}")
                    continue
                    
                # 解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找所有调色板链接
                for link in soup.find_all('a', href=True):
                    href = link.get('href', '')
                    if '/palette/' in href and href.count('/') == 2:
                        # 构建完整URL
                        full_url = href if href.startswith('http') else f"https://colorhunt.co{href}"
                        if full_url not in palette_urls:
                            palette_urls.append(full_url)
                            logger.info(f"找到调色板URL: {full_url}")
                            
                # 查找所有以六位十六进制数字组成的链接
                pattern = r'/palette/([0-9a-fA-F]{6}-[0-9a-fA-F]{6}-[0-9a-fA-F]{6}-[0-9a-fA-F]{6})'
                matches = re.findall(pattern, response.text)
                for match in matches:
                    full_url = f"https://colorhunt.co/palette/{match}"
                    if full_url not in palette_urls:
                        palette_urls.append(full_url)
                        logger.info(f"找到颜色代码URL: {full_url}")
                
            except Exception as e:
                logger.warning(f"处理 {url} 时出错: {e}")
                
        # 如果没有找到任何调色板URL，使用一些直接的颜色代码URL作为备用
        if not palette_urls or len(palette_urls) < 20:
            logger.info("使用备用颜色代码URL补充结果")
            backup_color_codes = [
                # 明亮色调系列
                "f9f7f7-3f72af-112d4e-dbe2ef",  # 蓝白配色
                "f38181-fce38a-eaffd0-95e1d3",  # 红黄绿配色
                "f9ed69-f08a5d-b83b5e-6a2c70",  # 黄橙紫配色
                "222831-393e46-00adb5-eeeeee",  # 深蓝绿配色
                "fbf0f0-dfd3d3-b8b0b0-7c7575",  # 灰色渐变
                # 柔和色调系列
                "f4f9f9-ccf2f4-a4ebf3-aaaaaa",  # 淡蓝灰配色
                "a8e6cf-dcedc1-ffd3b6-ffaaa5",  # 柔和色调
                "364f6b-3fc1c9-f5f5f5-fc5185",  # 蓝灰粉配色
                "084177-687466-cd8d7b-fbc490",  # 深蓝棕配色
                "e4f9f5-30e3ca-11999e-40514e"   # 青绿配色
            ]
            
            # 将备用颜色代码添加到URL列表中
            for code in backup_color_codes:
                url = f"https://colorhunt.co/palette/{code}"
                if url not in palette_urls:
                    palette_urls.append(url)
                
        logger.info(f"总共找到 {len(palette_urls)} 个调色板URL")
        return palette_urls
    
    @staticmethod
    def extract_palette_data_from_url(url: str, idx: int = 0) -> Optional[Dict]:
        """
        从URL中提取调色板数据
        
        Args:
            url: 调色板URL
            idx: 索引，用于生成ID
            
        Returns:
            Optional[Dict]: 调色板数据
        """
        try:
            logger.info(f"请求调色板页面: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
            }
            
            # 使用更短的超时时间
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code != 200:
                logger.warning(f"请求 {url} 失败, 状态码: {response.status_code}")
                return None
                
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
                
            # 从URL中提取颜色代码
            colors = []
            palette_id = url.split('/')[-1]
            
            # 方法1: 从URL中直接提取颜色代码（如果是颜色代码格式）
            if '-' in palette_id and all(len(part) == 6 and all(c in '0123456789abcdefABCDEF' for c in part) for part in palette_id.split('-')):
                parts = palette_id.split('-')
                colors = [f"#{part}" for part in parts]
                logger.info(f"从URL直接提取到颜色: {colors}")
            
            # 方法2: 从HTML内容中提取颜色
            if not colors or len(colors) < 4:
                # 查找所有可能的颜色元素
                color_elements = soup.select('[style*="background"]')
                for elem in color_elements:
                    style = elem.get('style', '')
                    color_match = re.search(r'background(?:-color)?:\s*(#[0-9a-fA-F]{6})', style)
                    if color_match:
                        color = color_match.group(1)
                        if color not in colors:
                            colors.append(color)
                            logger.info(f"从style提取到颜色: {color}")
            
            # 方法3: 从HTML内容中查找所有十六进制颜色代码
            if not colors or len(colors) < 4:
                # 查找所有可能的颜色代码
                color_matches = re.findall(r'#[0-9a-fA-F]{6}', response.text)
                for color in color_matches:
                    if color not in colors:
                        colors.append(color)
                        logger.info(f"从页面内容提取到颜色: {color}")
            
            # 方法4: 如果URL是颜色代码格式但解析失败，重新尝试
            if not colors and '-' in palette_id:
                parts = palette_id.split('-')
                for part in parts:
                    if len(part) == 6 and all(c in '0123456789abcdefABCDEF' for c in part):
                        colors.append(f"#{part}")
                        logger.info(f"重新从URL提取到颜色: #{part}")
            
            # 如果仍未找到足够的颜色，生成随机颜色补充
            while len(colors) < 4:
                random_color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
                if random_color not in colors:
                    colors.append(random_color)
                    logger.info(f"生成随机颜色补充: {random_color}")
            
            # 限制为4种颜色
            colors = colors[:4]
            
            # 提取其他信息
            name = f"ColorHunt Palette {palette_id}"
            likes = 0
            date = ""
            
            # 尝试提取名称
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.text.strip()
                if 'Color Palette' in title_text:
                    name = title_text
            
            # 尝试提取点赞数
            for like_selector in ['.likecount', '.likes', '.like-count', '.count']:
                like_elem = soup.select_one(like_selector)
                if like_elem:
                    try:
                        like_text = like_elem.text.strip()
                        likes = int(re.sub(r'\D', '', like_text))
                        logger.info(f"提取到点赞数: {likes}")
                        break
                    except Exception:
                        pass
            
            # 尝试提取日期
            for date_selector in ['.date', '.time', '.timestamp', '.info']:
                date_elem = soup.select_one(date_selector)
                if date_elem:
                    date = date_elem.text.strip()
                    logger.info(f"提取到日期: {date}")
                    break
            
            # 创建调色板数据
            palette_data = {
                "id": f"realtime-{idx+1}-{palette_id}",
                "name": name,
                "colors": colors,
                "source": "colorhunt.co",
                "source_url": url,
                "palette_id": palette_id,
                "likes": likes,
                "date": date,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return palette_data
            
        except requests.Timeout:
            logger.warning(f"请求 {url} 超时")
            return None
        except Exception as e:
            logger.warning(f"处理URL {url} 时出错: {e}")
            return None
    
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
            
            # 获取调色板URL列表
            palette_urls = WebService.get_palette_urls()
            
            if not palette_urls:
                return False, "未能获取到任何调色板URL", None
                
            # 限制URL数量
            palette_urls = palette_urls[:limit]
            
            # 处理每个URL，提取调色板数据
            all_palettes = []
            
            # 使用多线程加速处理，但设置较短的超时时间
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                # 提交所有任务
                future_to_url = {executor.submit(WebService.extract_palette_data_from_url, url, idx): (url, idx) 
                                for idx, url in enumerate(palette_urls)}
                
                # 处理结果
                for future in concurrent.futures.as_completed(future_to_url):
                    url, idx = future_to_url[future]
                    try:
                        palette_data = future.result(timeout=8)  # 8秒超时
                        if palette_data:
                            all_palettes.append(palette_data)
                            logger.info(f"成功提取调色板数据: {palette_data['id']}")
                    except concurrent.futures.TimeoutError:
                        logger.warning(f"处理 {url} 的任务超时")
                    except Exception as e:
                        logger.warning(f"处理 {url} 的任务时出错: {e}")
            
            # 如果没有获取到任何调色板，返回错误
            if not all_palettes:
                return False, "未能提取到任何调色板数据", None
                
            logger.info(f"成功提取 {len(all_palettes)} 个调色板数据")
            
            # 保存调色板数据
            for palette in all_palettes:
                try:
                    # 保存JSON文件
                    json_path = os.path.join(download_dir, f"colorhunt_{palette['id']}.json")
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(palette, f, indent=2, ensure_ascii=False)
                    logger.info(f"配色方案JSON已保存: {json_path}")
                    
                    # 生成并保存图片
                    if PALETTE_IMAGE_SUPPORT:
                        try:
                            img_path = PaletteImageGenerator.create_palette_image(
                                palette['colors'], palette['id'], images_dir
                            )
                            palette["image_path"] = img_path
                            logger.info(f"配色方案图片已保存: {img_path}")
                        except Exception as e:
                            logger.warning(f"生成配色方案图片时出错: {e}")
                except Exception as e:
                    logger.warning(f"保存配色方案 {palette['id']} 时出错: {e}")
            
            return True, None, all_palettes
            
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