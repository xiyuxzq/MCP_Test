"""
MCP表示层，连接模型层和视图层
"""
from typing import List, Dict, Any, Tuple, Optional

from views.mcp_view import IMcpView
from services.file_service import FileService
from services.app_service import AppService
from services.web_service import WebService

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
        抓取ColorHunt配色方案
        
        Args:
            limit: 配色方案数量限制
            
        Returns:
            str: 处理结果
        """
        try:
            success, error, palettes = WebService.scrape_colorhunt_palettes(limit)
            return self.view.show_colorhunt_palettes(success, error, palettes)
        except Exception as e:
            return f"抓取配色方案时出错: {str(e)}"
    
    def test_simple_colorhunt(self, limit: int = 5) -> str:
        """
        测试简化的配色方案抓取
        
        Args:
            limit: 配色方案数量限制
            
        Returns:
            str: 处理结果
        """
        try:
            success, error, palettes = WebService.test_simple_scrape(limit)
            return self.view.show_colorhunt_palettes(success, error, palettes)
        except Exception as e:
            return f"测试配色方案抓取时出错: {str(e)}"
