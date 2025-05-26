#!/usr/bin/env python
"""
ColorHunt 配色方案下载器 - PyQt GUI版本
独立工具，提供图形界面让用户选择标签、数量等参数下载配色方案
"""
import sys
import os
import json
import time
import logging
import requests
from bs4 import BeautifulSoup
import re
import random
import concurrent.futures
from typing import List, Dict, Tuple, Optional
from pathlib import Path

# PyQt imports
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                QWidget, QPushButton, QLabel, QComboBox, QSpinBox, 
                                QTextEdit, QProgressBar, QFileDialog, QGroupBox,
                                QCheckBox, QMessageBox, QGridLayout, QScrollArea)
    from PyQt5.QtCore import QThread, pyqtSignal, Qt
    from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QBrush
except ImportError:
    print("错误: 未安装PyQt5，请运行: pip install PyQt5")
    sys.exit(1)

# 尝试导入图片生成器
try:
    from PIL import Image, ImageDraw, ImageFont
    PALETTE_IMAGE_SUPPORT = True
except ImportError:
    PALETTE_IMAGE_SUPPORT = False
    print("警告: 未安装Pillow，将无法生成配色方案图片")
    print("请运行: pip install Pillow")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PaletteImageGenerator:
    """配色方案图片生成器"""
    
    @staticmethod
    def create_palette_image(colors: List[str], palette_id: str, output_dir: str) -> str:
        """
        创建配色方案图片
        
        Args:
            colors: 颜色列表
            palette_id: 配色方案ID
            output_dir: 输出目录
            
        Returns:
            str: 图片文件路径
        """
        if not PALETTE_IMAGE_SUPPORT:
            raise ImportError("Pillow未安装，无法生成图片")
            
        # 创建图片 (400x100)
        width, height = 400, 100
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # 每个颜色块的宽度
        color_width = width // len(colors)
        
        # 绘制颜色块
        for i, color in enumerate(colors):
            x1 = i * color_width
            x2 = (i + 1) * color_width
            try:
                draw.rectangle([x1, 0, x2, height], fill=color)
            except Exception as e:
                logger.warning(f"绘制颜色 {color} 失败: {e}")
                draw.rectangle([x1, 0, x2, height], fill='#CCCCCC')
        
        # 保存图片
        img_path = os.path.join(output_dir, f"palette_{palette_id}.png")
        img.save(img_path)
        return img_path

class ColorHuntScraper:
    """ColorHunt网站爬虫类"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://colorhunt.co/'
        }
        
        self.available_tags = [
            "popular", "new", "random", "pastel", "vintage", "retro", "neon", 
            "gold", "light", "dark", "warm", "cold", "summer", "fall", "winter", 
            "spring", "happy", "nature", "earth", "night", "space", "rainbow", 
            "gradient", "sunset", "sky", "sea", "kids", "skin", "food", "cream", 
            "coffee", "wedding", "christmas", "halloween"
        ]
        
        # API数据缓存
        self._api_cache = {}
    
    def get_palette_urls_by_tag(self, tag: str, limit: int = 20) -> List[str]:
        """
        根据标签获取配色方案URL列表 - 仅获取真实数据
        
        Args:
            tag: 标签名称
            limit: 数量限制
            
        Returns:
            List[str]: URL列表，如果无法获取真实数据则返回空列表
        """
        palette_urls = []
        
        # 方法1: 尝试原始API - 直接返回完整数据
        api_palettes = self.get_palettes_from_api(tag, limit)
        if api_palettes:
            # 将API数据缓存起来，避免重复请求
            self._api_cache = {palette['source_url']: palette for palette in api_palettes}
            return [palette['source_url'] for palette in api_palettes]
        
        # 方法2: 直接从主页抓取配色方案
        try:
            logger.info(f"方法2: 从网页抓取配色方案")
            
            # 构建标签页面URL - 修复new、popular、random的路径
            if tag == 'new':
                url = 'https://colorhunt.co/'  # 主页默认显示new
            elif tag == 'popular':
                url = 'https://colorhunt.co/popular'
            elif tag == 'random':
                url = 'https://colorhunt.co/random'
            else:
                url = f'https://colorhunt.co/palettes/{tag}'
            
            logger.info(f"访问URL: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                # 使用正则表达式查找配色方案URL
                palette_pattern = r'href="/palette/([a-fA-F0-9]{24})"'
                matches = re.findall(palette_pattern, response.text)
                
                if matches:
                    logger.info(f"网页抓取成功: 找到 {len(matches)} 个配色方案")
                    for match in matches[:limit]:
                        palette_url = f"https://colorhunt.co/palette/{match}"
                        palette_urls.append(palette_url)
                    
                    if palette_urls:
                        logger.info(f"网页抓取方法成功获取到 {len(palette_urls)} 个真实URL")
                        return palette_urls
                else:
                    logger.warning("网页抓取: 未找到配色方案链接")
            else:
                logger.warning(f"网页请求失败, 状态码: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"网页抓取异常: {e}")
        
        # 如果所有方法都失败，返回空列表
        logger.error(f"无法获取标签 {tag} 的真实配色方案数据")
        return []
    
    def get_palettes_from_api(self, tag: str, limit: int = 20) -> List[Dict]:
        """
        直接从API获取完整的配色方案数据，包括真实的likes、date等信息
        
        Args:
            tag: 标签名称
            limit: 数量限制
            
        Returns:
            List[Dict]: 配色方案数据列表
        """
        try:
            logger.info(f"方法1: 尝试API请求标签: {tag}")
            
            # 为不同类型的标签构建不同的API参数
            if tag == 'new':
                post_data = {
                    'step': 0,
                    'sort': 'new',
                    'tags': '',
                    'timeframe': ''
                }
            elif tag == 'popular':
                post_data = {
                    'step': 0,
                    'sort': 'popular',
                    'tags': '',
                    'timeframe': '30'  # 30天内的热门
                }
            elif tag == 'random':
                post_data = {
                    'step': 0,
                    'sort': 'random',
                    'tags': '',
                    'timeframe': ''
                }
            else:
                # 具体标签使用原来的方式
                post_data = {
                    'step': 0,
                    'sort': 'new',
                    'tags': tag,
                    'timeframe': ''
                }
            
            logger.info(f"API参数: {post_data}")
            response = requests.post(
                'https://colorhunt.co/php/feed.php', 
                headers=self.headers, 
                data=post_data,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    api_data = json.loads(response.text)
                    if api_data and len(api_data) > 0:
                        logger.info(f"API成功: 标签 {tag} 获取到 {len(api_data)} 个配色方案")
                        
                        palettes = []
                        for i, item in enumerate(api_data[:limit]):
                            if 'code' in item:
                                palette = self.create_palette_from_api_data(item, i, tag)
                                if palette:
                                    palettes.append(palette)
                        
                        if palettes:
                            logger.info(f"API方法成功创建 {len(palettes)} 个配色方案数据")
                            return palettes
                            
                except json.JSONDecodeError as e:
                    logger.warning(f"API JSON解析失败: {e}")
            else:
                logger.warning(f"API请求失败, 状态码: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"API请求异常: {e}")
        
        return []
    
    def create_palette_from_api_data(self, api_item: Dict, idx: int, tag: str) -> Optional[Dict]:
        """
        从API数据直接创建配色方案数据，使用真实的likes、date等信息
        
        Args:
            api_item: API返回的单个配色方案数据
            idx: 索引
            tag: 标签名称
            
        Returns:
            Optional[Dict]: 配色方案数据
        """
        try:
            code = api_item.get('code', '')
            if not code or len(code) != 24:
                logger.warning(f"无效的配色代码: {code}")
                return None
            
            # 从code提取颜色
            colors = []
            for i in range(4):
                hex_color = f"#{code[i*6:(i+1)*6].upper()}"
                colors.append(hex_color)
            
            # 获取真实的点赞数
            likes = api_item.get('likes', 0)
            if isinstance(likes, str):
                # 处理可能的字符串格式点赞数
                likes_match = re.search(r'\d+', likes)
                likes = int(likes_match.group()) if likes_match else 0
            elif not isinstance(likes, int):
                likes = 0
            
            # 获取真实的日期
            date = api_item.get('date', time.strftime("%Y-%m-%d"))
            if not date:
                date = time.strftime("%Y-%m-%d")
            
            # 获取其他可能的API数据
            title = api_item.get('title', '')
            author = api_item.get('author', '')
            tags_list = api_item.get('tags', [])
            if isinstance(tags_list, str):
                tags_list = [tags_list] if tags_list else []
            
            # 构建配色方案名称
            if title:
                name = title
            else:
                name = f"ColorHunt {tag.title()} Palette"
            
            # 构建URL
            source_url = f"https://colorhunt.co/palette/{code}"
            
            # 创建配色方案数据
            palette_data = {
                "id": f"colorhunt-api-{idx+1}-{code}",
                "name": name,
                "colors": colors,
                "source": "colorhunt.co",
                "source_url": source_url,
                "palette_id": code,
                "likes": likes,  # 真实的点赞数
                "date": date,    # 真实的日期
                "tags": tags_list,
                "author": author,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "extraction_method": "Direct API data",
                "api_source": True  # 标记这是来自API的真实数据
            }
            
            logger.info(f"从API创建配色方案: {name}, 点赞数: {likes}, 日期: {date}")
            return palette_data
            
        except Exception as e:
            logger.warning(f"从API数据创建配色方案失败: {e}")
            return None

    def extract_palette_data_from_url(self, url: str, idx: int = 0) -> Optional[Dict]:
        """
        从URL中提取调色板数据 - 优先使用API缓存数据
        
        Args:
            url: 调色板URL
            idx: 索引，用于生成ID
            
        Returns:
            Optional[Dict]: 调色板数据
        """
        # 首先检查是否有缓存的API数据
        if hasattr(self, '_api_cache') and url in self._api_cache:
            logger.info(f"使用缓存的API数据: {url}")
            return self._api_cache[url]
        
        # 如果没有缓存，进行网页抓取
        return self._extract_from_webpage(url, idx)
    
    def _extract_from_webpage(self, url: str, idx: int = 0) -> Optional[Dict]:
        """
        从网页中提取调色板数据 - 备用方法
        
        Args:
            url: 调色板URL
            idx: 索引，用于生成ID
            
        Returns:
            Optional[Dict]: 调色板数据
        """
        try:
            logger.info(f"请求调色板页面: {url}")
            
            response = requests.get(url, headers=self.headers, timeout=8)
            if response.status_code != 200:
                logger.warning(f"请求 {url} 失败, 状态码: {response.status_code}")
                return None
                
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
                
            # 从URL中提取颜色代码
            colors = []
            palette_id = url.split('/')[-1]
            
            # 从URL直接提取颜色代码（ColorHunt的标准格式：24个字符，每6个字符一种颜色）
            if len(palette_id) == 24 and all(c in '0123456789abcdefABCDEF' for c in palette_id):
                for i in range(4):
                    hex_color = f"#{palette_id[i*6:(i+1)*6].upper()}"
                    colors.append(hex_color)
                logger.info(f"从URL直接提取到颜色: {colors}")
            
            # 如果URL格式不标准，尝试其他方法
            if not colors or len(colors) < 4:
                # 方法1: 查找页面中的颜色div元素
                color_divs = soup.find_all('div', {'class': re.compile(r'color|palette')})
                for div in color_divs:
                    style = div.get('style', '')
                    color_match = re.search(r'background-color:\s*#([0-9a-fA-F]{6})', style)
                    if color_match:
                        color = f"#{color_match.group(1).upper()}"
                        if color not in colors:
                            colors.append(color)
                            logger.info(f"从div样式提取到颜色: {color}")
                
                # 方法2: 查找页面中的所有十六进制颜色代码
                if len(colors) < 4:
                    color_matches = re.findall(r'#([0-9a-fA-F]{6})', response.text)
                    for color_code in color_matches:
                        color = f"#{color_code.upper()}"
                        if color not in colors and color != '#FFFFFF' and color != '#000000':
                            colors.append(color)
                            if len(colors) >= 4:
                                break
                    logger.info(f"从页面内容提取到颜色: {colors}")
            
            # 检查是否获取到足够的颜色
            if len(colors) < 4:
                logger.warning(f"只获取到 {len(colors)} 种颜色，需要4种颜色，数据不完整")
                return None
            colors = colors[:4]
            
            # 提取配色方案名称
            name = f"ColorHunt Palette {palette_id[:6]}"
            
            # 尝试从title标签提取名称
            title_elem = soup.find('title')
            if title_elem:
                title_text = title_elem.text.strip()
                if title_text and 'Color Hunt' in title_text:
                    name = title_text
                    logger.info(f"提取到配色方案名称: {name}")
            
            # 尝试从meta描述提取名称
            if name == f"ColorHunt Palette {palette_id[:6]}":
                meta_desc = soup.find('meta', {'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    desc = meta_desc.get('content')
                    if 'palette' in desc.lower():
                        name = desc[:50] + "..." if len(desc) > 50 else desc
                        logger.info(f"从meta描述提取到名称: {name}")
            
            # 创建调色板数据（网页抓取版本，点赞数为0）
            palette_data = {
                "id": f"colorhunt-web-{idx+1}-{palette_id}",
                "name": name,
                "colors": colors,
                "source": "colorhunt.co",
                "source_url": url,
                "palette_id": palette_id,
                "likes": 0,  # 网页抓取无法获取真实点赞数
                "date": time.strftime("%Y-%m-%d"),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "extraction_method": "Webpage scraping (fallback)",
                "api_source": False  # 标记这不是来自API的数据
            }
            
            logger.info(f"从网页创建配色方案: {name} (无真实点赞数)")
            return palette_data
            
        except Exception as e:
            logger.warning(f"处理URL {url} 时出错: {e}")
            return None

class DownloadThread(QThread):
    """下载线程"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    palette_downloaded = pyqtSignal(dict)
    finished_signal = pyqtSignal(bool, str, list)
    
    def __init__(self, tag, count, save_dir, save_images, save_json):
        super().__init__()
        self.tag = tag
        self.count = count
        self.save_dir = save_dir
        self.save_images = save_images
        self.save_json = save_json
        self.scraper = ColorHuntScraper()
        
    def run(self):
        """运行下载任务"""
        try:
            self.status_updated.emit(f"开始获取 {self.tag} 标签的配色方案...")
            
            # 获取URL列表
            urls = self.scraper.get_palette_urls_by_tag(self.tag, self.count)
            
            if not urls:
                self.finished_signal.emit(False, f"无法从ColorHunt网站获取标签'{self.tag}'的真实配色方案数据。请检查网络连接或尝试其他标签。", [])
                return
            
            self.status_updated.emit(f"找到 {len(urls)} 个配色方案，开始下载...")
            
            # 创建保存目录
            os.makedirs(self.save_dir, exist_ok=True)
            if self.save_images:
                images_dir = os.path.join(self.save_dir, "images")
                os.makedirs(images_dir, exist_ok=True)
            
            # 下载配色方案
            palettes = []
            for i, url in enumerate(urls):
                try:
                    self.status_updated.emit(f"下载配色方案 {i+1}/{len(urls)}")
                    
                    palette_data = self.scraper.extract_palette_data_from_url(url, i)
                    if palette_data:
                        palettes.append(palette_data)
                        
                        # 保存JSON
                        if self.save_json:
                            json_path = os.path.join(self.save_dir, f"palette_{palette_data['palette_id']}.json")
                            with open(json_path, 'w', encoding='utf-8') as f:
                                json.dump(palette_data, f, indent=2, ensure_ascii=False)
                        
                        # 保存图片
                        if self.save_images and PALETTE_IMAGE_SUPPORT:
                            try:
                                img_path = PaletteImageGenerator.create_palette_image(
                                    palette_data['colors'], palette_data['palette_id'], images_dir
                                )
                                palette_data["image_path"] = img_path
                            except Exception as e:
                                logger.warning(f"生成图片失败: {e}")
                        
                        self.palette_downloaded.emit(palette_data)
                    
                    # 更新进度
                    progress = int((i + 1) / len(urls) * 100)
                    self.progress_updated.emit(progress)
                    
                except Exception as e:
                    logger.warning(f"下载 {url} 失败: {e}")
                    continue
            
            self.finished_signal.emit(True, f"成功下载 {len(palettes)} 个配色方案", palettes)
            
        except Exception as e:
            self.finished_signal.emit(False, f"下载过程中出错: {str(e)}", [])

class ColorHuntGUI(QMainWindow):
    """ColorHunt配色方案下载器主界面"""
    
    def __init__(self):
        super().__init__()
        self.scraper = ColorHuntScraper()
        self.download_thread = None
        self.palettes = []
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("ColorHunt 配色方案下载器")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("ColorHunt 配色方案下载器")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 设置区域
        settings_group = QGroupBox("下载设置")
        settings_layout = QGridLayout(settings_group)
        
        # 标签选择
        settings_layout.addWidget(QLabel("选择标签:"), 0, 0)
        self.tag_combo = QComboBox()
        self.tag_combo.addItems(self.scraper.available_tags)
        self.tag_combo.setCurrentText("popular")
        settings_layout.addWidget(self.tag_combo, 0, 1)
        
        # 数量选择
        settings_layout.addWidget(QLabel("下载数量:"), 1, 0)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 100)
        self.count_spin.setValue(10)
        settings_layout.addWidget(self.count_spin, 1, 1)
        
        # 保存目录选择
        settings_layout.addWidget(QLabel("保存目录:"), 2, 0)
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel(str(Path.home() / "Downloads" / "colorhunt_palettes"))
        self.dir_button = QPushButton("选择目录")
        self.dir_button.clicked.connect(self.select_directory)
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_button)
        settings_layout.addLayout(dir_layout, 2, 1)
        
        # 保存选项
        options_layout = QHBoxLayout()
        self.save_json_check = QCheckBox("保存JSON文件")
        self.save_json_check.setChecked(True)
        self.save_images_check = QCheckBox("保存配色图片")
        self.save_images_check.setChecked(PALETTE_IMAGE_SUPPORT)
        self.save_images_check.setEnabled(PALETTE_IMAGE_SUPPORT)
        options_layout.addWidget(self.save_json_check)
        options_layout.addWidget(self.save_images_check)
        settings_layout.addLayout(options_layout, 3, 0, 1, 2)
        
        main_layout.addWidget(settings_group)
        
        # 控制按钮
        button_layout = QHBoxLayout()
        self.download_button = QPushButton("开始下载")
        self.download_button.clicked.connect(self.start_download)
        self.stop_button = QPushButton("停止下载")
        self.stop_button.clicked.connect(self.stop_download)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)
        
        # 状态显示
        self.status_label = QLabel("准备就绪")
        main_layout.addWidget(self.status_label)
        
        # 结果显示区域
        results_group = QGroupBox("下载结果")
        results_layout = QVBoxLayout(results_group)
        
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(200)
        results_layout.addWidget(self.results_text)
        
        main_layout.addWidget(results_group)
        
        # 配色方案预览区域
        preview_group = QGroupBox("配色方案预览")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_scroll = QScrollArea()
        self.preview_widget = QWidget()
        self.preview_layout = QVBoxLayout(self.preview_widget)
        self.preview_scroll.setWidget(self.preview_widget)
        self.preview_scroll.setWidgetResizable(True)
        preview_layout.addWidget(self.preview_scroll)
        
        main_layout.addWidget(preview_group)
        
    def select_directory(self):
        """选择保存目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择保存目录")
        if directory:
            self.dir_label.setText(directory)
    
    def start_download(self):
        """开始下载"""
        tag = self.tag_combo.currentText()
        count = self.count_spin.value()
        save_dir = self.dir_label.text()
        save_images = self.save_images_check.isChecked()
        save_json = self.save_json_check.isChecked()
        
        # 清空之前的结果
        self.palettes.clear()
        self.results_text.clear()
        self.clear_preview()
        
        # 创建并启动下载线程
        self.download_thread = DownloadThread(tag, count, save_dir, save_images, save_json)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.status_updated.connect(self.update_status)
        self.download_thread.palette_downloaded.connect(self.add_palette_preview)
        self.download_thread.finished_signal.connect(self.download_finished)
        
        self.download_thread.start()
        
        # 更新UI状态
        self.download_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress_bar.setValue(0)
        
    def stop_download(self):
        """停止下载"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.terminate()
            self.download_thread.wait()
        
        self.download_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("下载已停止")
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        
    def update_status(self, message):
        """更新状态信息"""
        self.status_label.setText(message)
        
    def add_palette_preview(self, palette_data):
        """添加配色方案预览"""
        self.palettes.append(palette_data)
        
        # 创建预览widget
        preview_item = QWidget()
        item_layout = QHBoxLayout(preview_item)
        
        # 颜色预览
        colors_widget = QWidget()
        colors_widget.setFixedSize(200, 50)
        colors_layout = QHBoxLayout(colors_widget)
        colors_layout.setContentsMargins(0, 0, 0, 0)
        colors_layout.setSpacing(0)
        
        for color in palette_data['colors']:
            color_label = QLabel()
            color_label.setFixedSize(50, 50)
            color_label.setStyleSheet(f"background-color: {color}; border: 1px solid #ccc;")
            colors_layout.addWidget(color_label)
        
        item_layout.addWidget(colors_widget)
        
        # 信息显示
        info_text = f"""
        <b>名称:</b> {palette_data['name']}<br>
        <b>颜色:</b> {', '.join(palette_data['colors'])}<br>
        <b>点赞数:</b> {palette_data['likes']}<br>
        <b>网址:</b> <a href="{palette_data['source_url']}">{palette_data['source_url']}</a>
        """
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setOpenExternalLinks(True)
        item_layout.addWidget(info_label)
        
        self.preview_layout.addWidget(preview_item)
        
        # 添加到结果文本
        result_text = f"✅ {palette_data['name']} - {', '.join(palette_data['colors'])} - 点赞数: {palette_data['likes']}\n"
        self.results_text.append(result_text)
        
    def clear_preview(self):
        """清空预览区域"""
        while self.preview_layout.count():
            child = self.preview_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def download_finished(self, success, message, palettes):
        """下载完成"""
        self.download_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        if success:
            self.status_label.setText(f"下载完成！{message}")
            QMessageBox.information(self, "下载完成", message)
        else:
            self.status_label.setText(f"下载失败：{message}")
            QMessageBox.warning(self, "下载失败", message)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("ColorHunt 配色方案下载器")
    app.setApplicationVersion("1.0")
    
    # 创建并显示主窗口
    window = ColorHuntGUI()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 