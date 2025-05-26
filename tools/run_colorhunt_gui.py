#!/usr/bin/env python
"""
ColorHunt GUI 启动脚本
检查依赖并启动图形界面
"""
import sys
import subprocess
import importlib

def check_dependencies():
    """检查必要的依赖是否已安装"""
    required_packages = {
        'PyQt5': 'PyQt5',
        'requests': 'requests', 
        'bs4': 'beautifulsoup4',
        'PIL': 'Pillow'
    }
    
    missing_packages = []
    
    for module_name, package_name in required_packages.items():
        try:
            importlib.import_module(module_name)
            print(f"✅ {package_name} 已安装")
        except ImportError:
            print(f"❌ {package_name} 未安装")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("\n✅ 所有依赖已满足，启动GUI...")
    return True

def main():
    """主函数"""
    print("ColorHunt 配色方案下载器 - GUI版本")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 导入并启动GUI
    try:
        from colorhunt_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ 导入GUI模块失败: {e}")
        print("请确保 colorhunt_gui.py 文件在同一目录下")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动GUI失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 