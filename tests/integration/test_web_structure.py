#!/usr/bin/env python
"""
网站结构分析工具
用于分析 colorhunt.co 的 DOM 结构，辅助调试 CSS 选择器
"""
import sys
import logging
import requests
from bs4 import BeautifulSoup

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def analyze_website_structure(url="https://colorhunt.co/"):
    """分析网站结构，辅助找到正确的选择器"""
    logger.info(f"开始分析网站: {url}")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            logger.error(f"请求失败，状态码: {response.status_code}")
            return
            
        logger.info("开始分析HTML结构...")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尝试可能的选择器
        selectors = [
            '.palette', 
            '.palettes', 
            '.color-palette', 
            '.colors', 
            '[data-id]',
            'div[style*="background"]',
            '.palette-color'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            logger.info(f"选择器 '{selector}' 找到 {len(elements)} 个元素")
            
            # 分析前2个元素
            if elements and len(elements) > 0:
                for i, elem in enumerate(elements[:2]):
                    logger.info(f"  - 元素 {i+1}: 标签={elem.name}, 类={elem.get('class')}, ID={elem.get('id')}")
                    logger.info(f"    属性: {elem.attrs}")
                    
                    # 查看子元素
                    children = list(elem.children)
                    logger.info(f"    子元素数量: {len(children)}")
                    for j, child in enumerate(children[:3]):
                        if hasattr(child, 'name') and child.name is not None:
                            logger.info(f"      子元素 {j+1}: {child.name}, 类={child.get('class')}")
        
        # 保存HTML内容以供手动分析
        with open('colorhunt_structure.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        logger.info("已保存HTML内容到 colorhunt_structure.html")
        
    except Exception as e:
        logger.exception(f"分析过程中出错: {str(e)}")

if __name__ == "__main__":
    url = "https://colorhunt.co/"
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    analyze_website_structure(url) 