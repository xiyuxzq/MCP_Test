"""
文件模型类，用于表示文件和文件类型
"""
from pathlib import Path
from typing import Optional, List, Dict

class FileType:
    """文件类型类，定义不同的文件类型及其对应的扩展名"""
    
    IMAGES = 'images'
    DOCUMENTS = 'documents'
    ARCHIVES = 'archives'
    APPLICATIONS = 'applications'
    VIDEOS = 'videos'
    AUDIO = 'audio'
    CODE = 'code'
    OTHERS = 'others'
    
    @classmethod
    def get_extension_map(cls) -> Dict[str, List[str]]:
        """获取文件类型与扩展名的映射关系"""
        return {
            cls.IMAGES: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            cls.DOCUMENTS: ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xlsx', '.xls', '.ppt', '.pptx'],
            cls.ARCHIVES: ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
            cls.APPLICATIONS: ['.app', '.exe', '.dmg', '.pkg'],
            cls.VIDEOS: ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv'],
            cls.AUDIO: ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
            cls.CODE: ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.rb', '.php', '.go', '.ts']
        }
    
    @classmethod
    def get_type_by_extension(cls, extension: str) -> str:
        """根据文件扩展名判断文件类型"""
        extension = extension.lower()
        extension_map = cls.get_extension_map()
        
        for file_type, extensions in extension_map.items():
            if extension in extensions:
                return file_type
        
        return cls.OTHERS

class FileModel:
    """文件模型类，表示一个文件"""
    
    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self.name = self.path.name
        self.extension = self.path.suffix.lower()
        self.type = FileType.get_type_by_extension(self.extension)
    
    @property
    def is_hidden(self) -> bool:
        """判断是否为隐藏文件"""
        return self.name.startswith('.')
    
    @property
    def is_directory(self) -> bool:
        """判断是否为目录"""
        return self.path.is_dir()
    
    def __str__(self) -> str:
        return f"FileModel(name={self.name}, type={self.type})" 