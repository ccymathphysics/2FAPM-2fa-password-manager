#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
二维码显示对话框
"""

import tempfile
import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout,
    QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from core.language import get_language_manager


class QRDialog(QDialog):
    """二维码显示对话框类"""
    
    def __init__(self, auth, parent=None):
        """初始化二维码显示对话框"""
        super().__init__(parent)
        self.auth = auth
        self.lang_manager = get_language_manager()
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(self.lang_manager.get_text("qr_title"))
        self.setModal(True)
        self.setFixedSize(400, 500)
        
        # 创建布局
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建说明标签
        instruction_label = QLabel(
            f"{self.lang_manager.get_text('scan_qr')}\n"
            f"{self.lang_manager.get_text('enter_code_prompt')}"
        )
        instruction_label.setWordWrap(True)
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)
        
        # 生成二维码
        qr_image = self.auth.generate_qr_code("User")
        
        # 保存二维码到临时文件
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            qr_image.save(tmp_file.name)
            temp_filename = tmp_file.name
        
        # 创建二维码标签
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        
        # 加载二维码图像
        pixmap = QPixmap(temp_filename)
        # 缩放图像以适应标签
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.qr_label.setPixmap(pixmap)
        
        layout.addWidget(self.qr_label)
        
        # 创建验证码输入框
        self.token_input = QLineEdit()
        self.token_input.setMaxLength(6)
        self.token_input.setPlaceholderText(self.lang_manager.get_text("enter_code"))
        layout.addWidget(self.token_input)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建验证按钮
        verify_button = QPushButton(self.lang_manager.get_text("verify_2fa"))
        verify_button.clicked.connect(self.verify_pairing)
        
        # 创建关闭按钮
        close_button = QPushButton(self.lang_manager.get_text("close"))
        close_button.clicked.connect(self.accept)
        
        # 添加按钮到布局
        button_layout.addWidget(verify_button)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # 删除临时文件
        os.unlink(temp_filename)
    
    def verify_pairing(self):
        """验证配对"""
        token = self.token_input.text().strip()
        
        if not token:
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("enter_code"))
            return
        
        if len(token) != 6 or not token.isdigit():
            QMessageBox.warning(self, self.lang_manager.get_text("error"), 
                              self.lang_manager.get_text("enter_code"))
            return
        
        # 验证令牌
        if self.auth.verify_token(token):
            QMessageBox.information(self, self.lang_manager.get_text("auth_success"), 
                                  self.lang_manager.get_text("pair_success"))
            self.accept()
        else:
            QMessageBox.warning(self, self.lang_manager.get_text("auth_failed"), 
                              self.lang_manager.get_text("pair_failed"))
            self.token_input.clear()
            self.token_input.setFocus()
