#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
初始化脚本
用于安装依赖和初始化程序
"""

import subprocess
import sys
import os
from pathlib import Path


def install_dependencies():
    """安装项目依赖"""
    print("正在安装项目依赖...")
    
    # 获取requirements.txt路径
    project_root = Path(__file__).resolve().parent
    requirements_file = project_root / "requirements.txt"
    
    if not requirements_file.exists():
        print("错误: 找不到requirements.txt文件")
        return False
    
    try:
        # 使用pip安装依赖
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("依赖安装成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False
    except Exception as e:
        print(f"安装过程中发生错误: {e}")
        return False


def main():
    """主函数"""
    print("2FA Password Manager 初始化脚本")
    print("=" * 40)
    
    # 检查是否需要安装依赖
    install_deps = input("是否需要安装项目依赖? (y/n): ").strip().lower()
    
    if install_deps == 'y':
        if not install_dependencies():
            print("依赖安装失败，程序无法继续运行。")
            return
    
    print("\n初始化完成!")
    print("可以通过以下命令启动程序:")
    print("  python main.py")
    
    # 询问是否立即启动程序
    start_now = input("\n是否立即启动程序? (y/n): ").strip().lower()
    
    if start_now == 'y':
        try:
            # 启动主程序
            project_root = Path(__file__).resolve().parent
            main_script = project_root / "main.py"
            subprocess.call([sys.executable, str(main_script)])
        except Exception as e:
            print(f"启动程序时发生错误: {e}")


if __name__ == "__main__":
    main()
