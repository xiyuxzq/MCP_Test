"""
文件服务类，负责文件操作
"""
import os
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from models.file_model import FileModel, FileType

class FileService:
    """文件服务类，提供文件操作相关的服务"""
    
    @staticmethod
    def list_desktop_files() -> List[str]:
        """获取桌面文件列表"""
        desktop_path = os.path.expanduser("~/Desktop")
        return os.listdir(desktop_path)
    
    @staticmethod
    def get_file_models(directory_path: str) -> List[FileModel]:
        """获取指定目录下的所有文件模型"""
        path = Path(directory_path)
        if not path.exists() or not path.is_dir():
            raise ValueError(f"无效的目录路径: {directory_path}")
        
        file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path)]
        return [FileModel(fp) for fp in file_paths if os.path.isfile(fp)]
    
    @staticmethod
    def create_directory(directory_path: str) -> None:
        """创建目录（如果不存在）"""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    @staticmethod
    def move_file(source_path: str, destination_path: str) -> bool:
        """移动文件"""
        try:
            shutil.move(source_path, destination_path)
            return True
        except Exception as e:
            print(f"移动文件时出错: {str(e)}")
            return False
    
    def organize_desktop_files(self) -> Tuple[int, List[str]]:
        """整理桌面文件，返回成功移动的文件数量和错误列表"""
        desktop_path = os.path.expanduser("~/Desktop")
        
        # 创建分类文件夹
        file_categories = FileType.get_extension_map()
        for category in list(file_categories.keys()) + [FileType.OTHERS]:
            category_path = os.path.join(desktop_path, category)
            self.create_directory(category_path)
        
        # 获取桌面文件
        file_models = self.get_file_models(desktop_path)
        
        # 过滤掉隐藏文件
        file_models = [fm for fm in file_models if not fm.is_hidden]
        
        # 移动文件
        moved_count = 0
        errors = []
        
        for file_model in file_models:
            source_path = str(file_model.path)
            destination_folder = os.path.join(desktop_path, file_model.type)
            destination_path = os.path.join(destination_folder, file_model.name)
            
            success = self.move_file(source_path, destination_path)
            if success:
                moved_count += 1
            else:
                errors.append(file_model.name)
        
        return moved_count, errors 