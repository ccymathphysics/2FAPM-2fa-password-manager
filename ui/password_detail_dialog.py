#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
密码详情对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt
import pyperclip  # 用于复制到剪贴板

from core.language import get_language_manager


class PasswordDetailDialog(QDialog):
    """密码详情对话框"""
    
    def __init__(self, record, parent=None):
        """初始化密码详情对话框"""
        super().__init__(parent)
        self.record = record
        self.real_password = record['password']
        self.lang_manager = get_language_manager()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(self.lang_manager.get_text("password_detail"))
        self.setFixedSize(400, 300)
        self.setModal(True)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 服务名称
        service_label = QLabel(f"{self.lang_manager.get_text('service')} {self.record['service_name']}")
        service_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(service_label)
        
        # 用户名
        username_label = QLabel(f"{self.lang_manager.get_text('user')} {self.record['username']}")
        username_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(username_label)
        
        # 密码显示区域
        password_layout = QHBoxLayout()
        
        # 密码标签
        self.password_label = QLabel(self.lang_manager.get_text("password"))
        password_layout.addWidget(self.password_label)
        
        # 密码显示框
        self.password_display = QTextEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setMaximumHeight(30)
        self.password_display.setText("······")  # 默认显示掩码
        password_layout.addWidget(self.password_display)
        
        # 显示密码按钮
        self.show_password_button = QPushButton(self.lang_manager.get_text("show"))
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_button)
        
        # 复制密码按钮
        self.copy_button = QPushButton(self.lang_manager.get_text("copy"))
        self.copy_button.clicked.connect(self.copy_password)
        password_layout.addWidget(self.copy_button)
        
        layout.addLayout(password_layout)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # 关闭按钮
        close_button = QPushButton(self.lang_manager.get_text("close"))
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 设置焦点到关闭按钮
        close_button.setFocus()
    
    def toggle_password_visibility(self):
        """切换密码可见性"""
        if self.password_display.toPlainText() == "······":
            # 显示真实密码
            self.password_display.setText(self.real_password)
            self.show_password_button.setText(self.lang_manager.get_text("hide"))
        else:
            # 隐藏密码，显示掩码
            self.password_display.setText("······")
            self.show_password_button.setText(self.lang_manager.get_text("show"))
    
    def copy_password(self):
        """复制密码到剪贴板"""
        try:
            pyperclip.copy(self.real_password)
            QMessageBox.information(
                self, 
                self.lang_manager.get_text("copy_success"), 
                self.lang_manager.get_text("copy_success_message")
            )
        except Exception as e:
            QMessageBox.critical(
                self, 
                self.lang_manager.get_text("error"), 
                self.lang_manager.get_text_with_args("copy_failed", error=str(e))
            )
