"""
配置工具类
"""

class Config:
    """配置工具类，提供应用程序配置"""
    
    @staticmethod
    def get_app_config() -> dict:
        """获取应用程序配置"""
        return {
            "theme": "dark",
            "language": "zh-CN"
        } 