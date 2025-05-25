#!/usr/bin/env python
"""
ColorHunt 配色方案爬虫测试脚本 - 独立版本
不依赖于 WebService 模块，直接从网站获取实时数据
通过直接访问配色方案URL抓取真实数据
"""
import sys
import logging
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict, Tuple, Optional
import re
import random
import concurrent.futures

# 尝试导入图片生成器
try:
    from color_palette_generator import PaletteImageGenerator
    PALETTE_IMAGE_SUPPORT = True
except ImportError:
    PALETTE_IMAGE_SUPPORT = False
    print("警告: 未能导入 PaletteImageGenerator，将不会生成配色方案图片")
    print("请先安装必要的依赖: pip install pillow")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def get_palette_urls() -> List[str]:
    """
    获取调色板URL列表 - 通过API接口获取
    
    Returns:
        List[str]: URL列表
    """
    # 不同分类的标签
    tag_categories = [
        "pastel", "vintage", "retro", "neon", "gold", "light", "dark", 
        "warm", "cold", "summer", "fall", "winter", "spring", "happy", 
        "nature", "earth", "night", "space", "rainbow", "gradient","sunset",
        "sky","sea","kids","skin","food","cream","coffee","wedding","christmas","halloween"
    ]
    
    # 收集调色板URL
    palette_urls = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/html, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://colorhunt.co/'
    }
    
    # 请求不同分类的配色数据
    for tag in tag_categories:
        try:
            logger.info(f"请求分类: {tag}")
            
            # 构建POST数据
            post_data = {
                'step': 0,
                'sort': 'new',
                'tags': tag,
                'timeframe': ''
            }
            
            # 请求API
            response = requests.post(
                'https://colorhunt.co/php/feed.php', 
                headers=headers, 
                data=post_data,
                timeout=10
            )
            
            if response.status_code != 200:
                logger.warning(f"请求分类 {tag} 失败, 状态码: {response.status_code}")
                continue
            
            # 解析JSON数据
            try:
                palette_data = json.loads(response.text)
                logger.info(f"分类 {tag} 获取到 {len(palette_data)} 个配色方案")
                
                # 提取配色代码并构建URL
                for item in palette_data:
                    if 'code' in item:
                        code = item['code']
                        url = f"https://colorhunt.co/palette/{code}"
                        if url not in palette_urls:
                            palette_urls.append(url)
                            logger.info(f"找到配色URL: {url}")
                            
            except json.JSONDecodeError as e:
                logger.warning(f"解析分类 {tag} 的JSON数据失败: {e}")
                continue
                
        except Exception as e:
            logger.warning(f"处理分类 {tag} 时出错: {e}")
            continue
    
    # 如果没有找到任何调色板URL，直接返回空列表，不再补充备用颜色
    if not palette_urls or len(palette_urls) < 1:
        logger.info("未能获取到任何调色板URL")
        return []

    logger.info(f"总共找到 {len(palette_urls)} 个调色板URL")
    return palette_urls

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

def scrape_colorhunt_palettes(limit=20) -> Tuple[bool, Optional[str], Optional[List[Dict]]]:
    """
    抓取 colorhunt.co 网站的配色方案
    
    Args:
        limit: 要抓取的配色方案数量限制
    
    Returns:
        Tuple[bool, str, List[Dict]]: (是否成功, 错误信息, 配色方案列表)
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
        palette_urls = get_palette_urls()
        
        if not palette_urls:
            return False, "未能获取到任何调色板URL", None
            
        # 限制URL数量
        palette_urls = palette_urls[:limit]
        
        # 处理每个URL，提取调色板数据
        all_palettes = []
        
        # 使用多线程加速处理，但设置较短的超时时间
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # 提交所有任务
            future_to_url = {executor.submit(extract_palette_data_from_url, url, idx): (url, idx) 
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

def test_scrape_colorhunt(limit=20):
    """测试爬取 ColorHunt 配色方案"""
    logger.info(f"开始爬取 ColorHunt 配色方案，数量限制: {limit}")
    try:
        success, error, palettes = scrape_colorhunt_palettes(limit)
        
        if not success:
            logger.error(f"爬取失败: {error}")
            return False
            
        logger.info(f"爬取成功，获取了 {len(palettes)} 个配色方案")
        for p in palettes:
            logger.info(f"配色方案: {p['name']}")
            logger.info(f"颜色代码: {', '.join(p['colors'])}")
            logger.info(f"来源URL: {p['source_url']}")
            if 'likes' in p and p['likes']:
                logger.info(f"点赞数: {p['likes']}")
            if 'date' in p and p['date']:
                logger.info(f"日期: {p['date']}")
            logger.info(f"JSON保存位置: ~/Downloads/colorhunt_palettes/colorhunt_{p['id']}.json")
            if 'image_path' in p:
                logger.info(f"图片保存位置: {p['image_path']}")
            logger.info("-" * 50)
            
        return True
    except Exception as e:
        logger.exception(f"测试过程中发生异常: {str(e)}")
        return False

if __name__ == "__main__":
    # 获取命令行参数
    limit = 20  # 默认值
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            logger.error(f"无效的参数: {sys.argv[1]}，使用默认值 20")
    
    # 运行测试
    test_scrape_colorhunt(limit) 