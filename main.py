#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2FA Password Manager 主程序入口
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from config.settings import APP_TITLE

def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
