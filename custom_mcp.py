# custom_mcp.py
from mcp.server.fastmcp import FastMCP
import os
import shutil
import pathlib
import subprocess
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入MCP组件
from views.mcp_view import McpView
from presenters.mcp_presenter import McpPresenter

mcp = FastMCP()

# 创建MVP架构组件
view = McpView()
presenter = McpPresenter(view)

@mcp.tool()
def list_desktop_files() -> list:
    """获取当前用户桌面上的所有文件列表（macOS专属实现）"""
    desktop_path = os.path.expanduser("~/Desktop")
    return os.listdir(desktop_path)

@mcp.tool()
def create_folder_and_move_files() -> str:
    """创建文件夹将文件分类整理，图片类型放到对应的文件夹，文档类型放到自己的文件夹等等，自动识别文件后缀看把文件放到哪一个文件夹内"""
    desktop_path = os.path.expanduser("~/Desktop")
    
    # 定义文件类型和对应的文件夹名称
    file_categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.xls', '.ppt', '.pptx'],
        'archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
        'applications': ['.app', '.exe', '.dmg', '.pkg'],
        'videos': ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
        'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.rb', '.php', '.go', '.ts']
    }
    
    # 创建分类文件夹
    for folder_name in file_categories.keys():
        folder_path = os.path.join(desktop_path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    
    # 创建其他文件夹用于未分类文件
    others_folder = os.path.join(desktop_path, 'others')
    if not os.path.exists(others_folder):
        os.makedirs(others_folder)
    
    # 获取桌面上的所有文件
    desktop_files = [f for f in os.listdir(desktop_path) if os.path.isfile(os.path.join(desktop_path, f))]
    
    # 移动的文件数量计数
    moved_files_count = 0
    
    # 分类文件并移动到对应文件夹
    for file_name in desktop_files:
        # 跳过系统文件和隐藏文件
        if file_name.startswith('.'):
            continue
        
        file_path = os.path.join(desktop_path, file_name)
        file_ext = pathlib.Path(file_name).suffix.lower()
        
        # 确定文件类型
        destination_folder = None
        for category, extensions in file_categories.items():
            if file_ext in extensions:
                destination_folder = category
                break
        
        # 如果没有匹配的类别，放入others文件夹
        if destination_folder is None:
            destination_folder = 'others'
        
        # 移动文件
        destination_path = os.path.join(desktop_path, destination_folder, file_name)
        try:
            shutil.move(file_path, destination_path)
            moved_files_count += 1
        except Exception as e:
            print(f"移动文件 {file_name} 时出错: {str(e)}")
    
    # 跳过文件夹，不要移动
    result = f"整理完成! 共移动了 {moved_files_count} 个文件到对应分类文件夹。"
    return result

@mcp.tool()
def open_chrome() -> str:
    """打开谷歌浏览器（macOS专属实现）"""
    try:
        subprocess.run(['open', '-a', 'Google Chrome'], check=True)
        return "谷歌浏览器已成功打开。"
    except subprocess.CalledProcessError as e:
        return f"打开谷歌浏览器时出错：{str(e)}"
    except FileNotFoundError:
        return "无法找到谷歌浏览器，请确保已安装。"

@mcp.tool()
def say_hello(name: str) -> str:
    """生成个性化问候语（中英双语版）"""
    return f"  你好 {name}! (Hello {name}!)"

@mcp.tool()
def scrape_colorhunt_palettes(limit: int = 5) -> str:
    """抓取ColorHunt网站的配色方案"""
    return presenter.scrape_colorhunt_palettes(limit)

@mcp.tool()
def test_simple_colorhunt(limit: int = 5) -> str:
    """测试简化的配色方案抓取"""
    return presenter.test_simple_colorhunt(limit)

@mcp.resource("config://app_settings")
def get_app_config() -> dict:
    return {"theme": "dark", "language": "zh-CN"}

@mcp.prompt()
def code_review_prompt(code: str) -> str:
    return f"请审查以下代码并指出问题：\n\n{code}"


if __name__ == "__main__":
    mcp.run(transport='stdio')