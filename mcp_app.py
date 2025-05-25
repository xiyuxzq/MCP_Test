"""
MCP应用程序主文件
"""
from mcp.server.fastmcp import FastMCP

from views.mcp_view import McpView
from presenters.mcp_presenter import McpPresenter
from utils.config import Config

# 创建MCP实例
mcp = FastMCP()

# 创建MVP架构组件
view = McpView()
presenter = McpPresenter(view)

# 注册MCP工具
@mcp.tool()
def list_desktop_files() -> list:
    """获取当前用户桌面上的所有文件列表（macOS专属实现）"""
    return presenter.list_desktop_files()

@mcp.tool()
def create_folder_and_move_files() -> str:
    """创建文件夹将文件分类整理，图片类型放到对应的文件夹，文档类型放到自己的文件夹等等，自动识别文件后缀看把文件放到哪一个文件夹内"""
    return presenter.organize_desktop_files()

@mcp.tool()
def open_chrome() -> str:
    """打开谷歌浏览器（macOS专属实现）"""
    return presenter.open_chrome()

@mcp.tool()
def say_hello(name: str) -> str:
    """生成个性化问候语（中英双语版）"""
    return presenter.say_hello(name)

@mcp.tool()
def scrape_colorhunt_palettes(limit: int = 5) -> str:
    """抓取 colorhunt.co 配色方案"""
    return presenter.scrape_colorhunt_palettes(limit)

@mcp.tool()
def extract_palette_from_image(image_path: str, num_colors: int = 4) -> str:
    """从图片提取配色方案"""
    return presenter.extract_palette_from_image(image_path, num_colors)

# 注册MCP资源
@mcp.resource("config://app_settings")
def get_app_config() -> dict:
    return Config.get_app_config()

# 注册MCP提示
@mcp.prompt()
def code_review_prompt(code: str) -> str:
    return f"请审查以下代码并指出问题：\n\n{code}"

# 运行MCP服务
if __name__ == "__main__":
    mcp.run(transport='stdio') 