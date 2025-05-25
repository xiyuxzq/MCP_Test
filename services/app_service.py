"""
应用程序服务类，负责启动应用程序
"""
import subprocess
from typing import Tuple, Optional

class AppService:
    """应用程序服务类，提供启动应用程序的功能"""
    
    @staticmethod
    def open_application(app_name: str) -> Tuple[bool, Optional[str]]:
        """
        打开指定的应用程序
        
        Args:
            app_name: 应用程序名称
            
        Returns:
            Tuple[bool, Optional[str]]: (是否成功, 错误信息)
        """
        try:
            subprocess.run(['open', '-a', app_name], check=True)
            return True, None
        except subprocess.CalledProcessError as e:
            return False, f"打开应用程序时出错：{str(e)}"
        except FileNotFoundError:
            return False, f"无法找到应用程序，请确保已安装 {app_name}" 