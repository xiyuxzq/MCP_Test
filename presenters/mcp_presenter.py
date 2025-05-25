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