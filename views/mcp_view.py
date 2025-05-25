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

    @abstractmethod
    def show_colorhunt_palettes(self, success: bool, error: str, palettes: list) -> str:
        """
        展示 colorhunt.co 配色方案抓取结果
        Args:
            success: 是否成功
            error: 错误信息
            palettes: 配色方案列表
        Returns:
            str: 展示字符串
        """
        pass

    @abstractmethod
    def show_extracted_palette(self, palette_data: Dict) -> str:
        """
        展示从图片提取的配色方案
        Args:
            palette_data: 配色方案数据
        Returns:
            str: 展示字符串
        """
        pass
    
    @abstractmethod
    def show_error(self, error_message: str) -> str:
        """
        展示错误信息
        Args:
            error_message: 错误信息
        Returns:
            str: 展示字符串
        """
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

    def show_colorhunt_palettes(self, success: bool, error: str, palettes: list) -> str:
        """
        展示 colorhunt.co 配色方案抓取结果
        """
        if not success:
            return f"抓取失败: {error}"
        if not palettes:
            return "未获取到配色方案。"
        result = [f"{p['name']}: {', '.join(p['colors'])}" for p in palettes]
        return "\n".join(result)

    def show_extracted_palette(self, palette_data: Dict) -> str:
        """
        展示从图片提取的配色方案
        """
        colors = palette_data.get("colors", [])
        name = palette_data.get("name", "未命名配色方案")
        source_image = palette_data.get("source_image", "未知来源")
        image_path = palette_data.get("image_path", "")
        
        result = [
            f"配色方案: {name}",
            f"来源图片: {source_image}",
            f"颜色代码: {', '.join(colors)}",
        ]
        
        if image_path:
            result.append(f"配色方案图片已保存: {image_path}")
            
        return "\n".join(result)
    
    def show_error(self, error_message: str) -> str:
        """
        展示错误信息
        """
        return f"错误: {error_message}" 