#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
认证对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

from core.language import get_language_manager


class AuthDialog(QDialog):
    """认证对话框类"""
    
    def __init__(self, parent=None, title="认证", label_text="请输入密码:"):
        """初始化认证对话框"""
        super().__init__(parent)
        self.input_text = ""
        self.lang_manager = get_language_manager()
        self.init_ui(title, label_text)
    
    def init_ui(self, title, label_text):
        """初始化用户界面"""
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建标签
        label = QLabel(label_text)
        layout.addWidget(label)
        
        # 创建输入框
        self.input_field = QLineEdit()
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.returnPressed.connect(self.accept)
        layout.addWidget(self.input_field)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        ok_button = QPushButton(self.lang_manager.get_text("save"))
        ok_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton(self.lang_manager.get_text("cancel"))
        cancel_button.clicked.connect(self.reject)
        
        # 添加按钮到布局
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # 设置默认焦点
        self.input_field.setFocus()
    
    def accept(self):
        """接受输入"""
        self.input_text = self.input_field.text()
        if not self.input_text:
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("password_required"))
            return
        super().accept()
    
    def get_input(self):
        """获取输入文本"""
        return self.input_text
