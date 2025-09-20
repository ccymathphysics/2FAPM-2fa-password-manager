#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
密码管理对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt

from core.language import get_language_manager


class PasswordDialog(QDialog):
    """密码管理对话框类"""
    
    def __init__(self, parent=None, record=None):
        """初始化密码管理对话框"""
        super().__init__(parent)
        self.record = record
        self.data = {}
        self.lang_manager = get_language_manager()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        if self.record:
            self.setWindowTitle(self.lang_manager.get_text("edit_password_title"))
        else:
            self.setWindowTitle(self.lang_manager.get_text("add_password_title"))
        
        self.setModal(True)
        self.setFixedSize(400, 250)
        
        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建表单布局
        form_layout = QFormLayout()
        
        # 创建输入字段
        self.service_name_field = QLineEdit()
        self.username_field = QLineEdit()
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        
        # 如果是编辑模式，填充现有数据
        if self.record:
            self.service_name_field.setText(self.record.get('service_name', ''))
            self.username_field.setText(self.record.get('username', ''))
            # 注意：出于安全考虑，不显示现有密码
            # 用户需要重新输入密码
        
        # 添加字段到表单
        form_layout.addRow(self.lang_manager.get_text("service_label"), self.service_name_field)
        form_layout.addRow(self.lang_manager.get_text("username_label"), self.username_field)
        form_layout.addRow(self.lang_manager.get_text("password_label"), self.password_field)
        
        layout.addLayout(form_layout)
        
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
        self.service_name_field.setFocus()
    
    def accept(self):
        """接受输入"""
        service_name = self.service_name_field.text().strip()
        username = self.username_field.text().strip()
        password = self.password_field.text()
        
        # 验证输入
        if not service_name:
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("service_required"))
            return
        
        if not username:
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("username_required"))
            return
            
        if not password:
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("password_required"))
            return
        
        # 保存数据
        self.data = {
            'service_name': service_name,
            'username': username,
            'password': password
        }
        
        super().accept()
    
    def get_data(self):
        """获取输入数据"""
        return self.data
