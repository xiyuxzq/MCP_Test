"""
MCP表示层，连接模型层和视图层
"""
from typing import List, Dict, Any, Tuple, Optional

from views.mcp_view import IMcpView
from services.file_service import FileService
from services.app_service import AppService

class McpPresenter:
    """MCP表示层类，处理业务逻辑并更新视图"""
    
    def __init__(self, view: IMcpView):
        """
        初始化表示层
        
        Args:
            view: 视图接口实现
        """
        self.view = view
        self.file_service = FileService()
        self.app_service = AppService()
    
    def list_desktop_files(self) -> List[str]:
        """获取桌面文件列表并显示"""
        files = self.file_service.list_desktop_files()
        return self.view.show_file_list(files)
    
    def organize_desktop_files(self) -> str:
        """整理桌面文件并显示结果"""
        moved_count, errors = self.file_service.organize_desktop_files()
        return self.view.show_organize_result(moved_count, errors)
    
    def open_chrome(self) -> str:
        """打开谷歌浏览器并显示结果"""
        success, error_message = self.app_service.open_application("Google Chrome")
        return self.view.show_app_open_result(success, error_message)
    
    def say_hello(self, name: str) -> str:
        """生成问候语并显示"""
        return self.view.show_greeting(name)
    
    def scrape_colorhunt_palettes(self, limit: int = 5) -> str:
        """
        抓取 colorhunt.co 配色方案并展示结果
        Args:
            limit: 要抓取的配色方案数量
        Returns:
            str: 展示结果字符串
        """
        from services.web_service import WebService
        success, error, palettes = WebService.scrape_colorhunt_palettes(limit)
        return self.view.show_colorhunt_palettes(success, error, palettes)
    
    def extract_palette_from_image(self, image_path: str, num_colors: int = 4) -> str:
        """
        从图片提取配色方案并展示结果
        Args:
            image_path: 图片路径
            num_colors: 要提取的颜色数量
        Returns:
            str: 展示结果字符串
        """
        try:
            # 尝试导入图片生成器
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from color_palette_generator import PaletteImageGenerator
            
            # 确保图片存在
            if not os.path.exists(image_path):
                return self.view.show_error(f"图片不存在: {image_path}")
            
            # 提取颜色
            colors = PaletteImageGenerator.extract_colors_from_image(image_path, num_colors)
            if not colors:
                return self.view.show_error("无法从图片提取颜色")
            
            # 生成ID
            import hashlib
            import time
            image_hash = hashlib.md5(open(image_path, 'rb').read()).hexdigest()[:8]
            palette_id = f"image-{image_hash}"
            
            # 确定输出目录
            download_dir = os.path.expanduser("~/Downloads/colorhunt_palettes")
            os.makedirs(download_dir, exist_ok=True)
            
            # 保存为JSON
            import json
            palette_data = {
                "id": palette_id,
                "name": f"Image Palette {palette_id}",
                "colors": colors,
                "source": "image_extract",
                "source_image": image_path,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            json_path = os.path.join(download_dir, f"image_palette_{palette_id}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(palette_data, f, indent=2)
            
            # 生成图片
            images_dir = os.path.join(download_dir, "images")
            os.makedirs(images_dir, exist_ok=True)
            
            img_path = PaletteImageGenerator.create_palette_image(colors, palette_id, images_dir)
            if img_path:
                palette_data["image_path"] = img_path
            
            # 显示结果
            return self.view.show_extracted_palette(palette_data)
            
        except Exception as e:
            import traceback
            error_message = f"从图片提取配色方案时出错: {str(e)}\n{traceback.format_exc()}"
            return self.view.show_error(error_message) 