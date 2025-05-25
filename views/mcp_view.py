"""
MCP视图接口，定义视图层的接口
"""
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Optional

class IMcpView(ABC):
    """MCP视图接口"""
    
    @abstractmethod
    def show_file_list(self, files: List[str]) -> None:
        """显示文件列表"""
        pass
    
    @abstractmethod
    def show_organize_result(self, moved_count: int, errors: List[str]) -> str:
        """显示整理结果"""
        pass
    
    @abstractmethod
    def show_app_open_result(self, success: bool, error_message: str = None) -> str:
        """显示应用程序打开结果"""
        pass
    
    @abstractmethod
    def show_greeting(self, name: str) -> str:
        """显示问候语"""
        pass

class McpView(IMcpView):
    """MCP视图实现类"""
    
    def show_file_list(self, files: List[str]) -> List[str]:
        """显示文件列表"""
        return files
    
    def show_organize_result(self, moved_count: int, errors: List[str]) -> str:
        """显示整理结果"""
        if not errors:
            return f"整理完成! 共移动了 {moved_count} 个文件到对应分类文件夹。"
        else:
            error_files = ", ".join(errors)
            return f"整理完成! 共移动了 {moved_count} 个文件，但有 {len(errors)} 个文件失败: {error_files}"
    
    def show_app_open_result(self, success: bool, error_message: str = None) -> str:
        """显示应用程序打开结果"""
        if success:
            return "应用程序已成功打开。"
        else:
            return error_message or "打开应用程序失败，未知错误。"
    
    def show_greeting(self, name: str) -> str:
        """显示问候语"""
        return f"你好 {name}! (Hello {name}!)" 