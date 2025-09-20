#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主窗口界面
"""

import sys
import os
import hashlib
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QStatusBar, QMessageBox, QHeaderView,
    QDialog, QLineEdit, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap

from core.auth import get_auth
from core.database import get_database
from core.language import get_language_manager
from ui.auth_dialog import AuthDialog
from ui.password_dialog import PasswordDialog
from ui.qr_dialog import QRDialog
from ui.password_detail_dialog import PasswordDetailDialog
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE


class SetMasterPasswordDialog(QDialog):
    """设置管理员密码对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lang_manager = get_language_manager()
        self.setWindowTitle(self.lang_manager.get_text("set_master_password_title"))
        self.setModal(True)
        self.setMinimumWidth(300)
        
        layout = QFormLayout(self)
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText(self.lang_manager.get_text("enter_master_password"))
        
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setPlaceholderText(self.lang_manager.get_text("confirm_master_password"))
        
        layout.addRow(self.lang_manager.get_text("master_password_label"), self.password_edit)
        layout.addRow(self.lang_manager.get_text("confirm_password_label"), self.confirm_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def get_password(self):
        """获取密码"""
        password = self.password_edit.text()
        confirm = self.confirm_edit.text()
        
        if not password:
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("master_password_required"))
            return None
            
        if password != confirm:
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("password_mismatch"))
            return None
            
        return password


class ChangeMasterPasswordDialog(QDialog):
    """更改管理员密码对话框"""
    
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.lang_manager = get_language_manager()
        self.setWindowTitle(self.lang_manager.get_text("change_master_password_title"))
        self.setModal(True)
        self.setMinimumWidth(300)
        
        layout = QFormLayout(self)
        
        self.old_password_edit = QLineEdit()
        self.old_password_edit.setEchoMode(QLineEdit.Password)
        self.old_password_edit.setPlaceholderText(self.lang_manager.get_text("enter_current_password"))
        
        self.new_password_edit = QLineEdit()
        self.new_password_edit.setEchoMode(QLineEdit.Password)
        self.new_password_edit.setPlaceholderText(self.lang_manager.get_text("enter_new_password"))
        
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setPlaceholderText(self.lang_manager.get_text("confirm_new_password"))
        
        layout.addRow(self.lang_manager.get_text("current_password_label"), self.old_password_edit)
        layout.addRow(self.lang_manager.get_text("new_password_label"), self.new_password_edit)
        layout.addRow(self.lang_manager.get_text("confirm_new_password_label"), self.confirm_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def accept(self):
        """确认更改密码"""
        old_password = self.old_password_edit.text()
        new_password = self.new_password_edit.text()
        confirm = self.confirm_edit.text()
        
        if not old_password:
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("current_password_required"))
            return
            
        if not new_password:
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("new_password_required"))
            return
            
        if new_password != confirm:
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("new_password_mismatch"))
            return
            
        # 验证当前密码
        if not self.db.verify_master_password(old_password):
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("current_password_incorrect"))
            return
            
        # 验证2FA
        from core.auth import get_auth
        auth = get_auth()
        from ui.totp_dialog import TOTPDialog
        totp_dialog = TOTPDialog(auth, self, self.lang_manager.get_text("2fa_verification"), 
                               self.lang_manager.get_text("enter_6_digit_code"))
        if not totp_dialog.exec_():
            QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                              self.lang_manager.get_text("2fa_required_to_change_password"))
            return
            
        self.new_password = new_password
        super().accept()


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.auth = get_auth()
        self.db = get_database()
        self.last_verification_time = 0
        self.verification_timeout = 10  # 10秒内不需要重复验证
        self.init_ui()
        self.check_first_time_setup()
        self.check_and_setup_master_password()
    
    def init_ui(self):
        """初始化用户界面"""
        # 获取语言管理器
        self.lang_manager = get_language_manager()
        self.lang_manager.language_changed.connect(self.on_language_changed)
        
        self.setWindowTitle(self.lang_manager.get_text("app_title"))
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建顶部布局（包含按钮和语言切换）
        top_layout = QHBoxLayout()
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建按钮
        self.qr_button = QPushButton(self.lang_manager.get_text("show_qr"))
        self.qr_button.clicked.connect(self.show_qr_code)
        
        self.add_button = QPushButton(self.lang_manager.get_text("add_password"))
        self.add_button.clicked.connect(self.add_password)
        
        self.import_button = QPushButton(self.lang_manager.get_text("import_csv"))
        self.import_button.clicked.connect(self.import_csv)
        
        self.edit_button = QPushButton(self.lang_manager.get_text("edit_password"))
        self.edit_button.clicked.connect(self.edit_password)
        self.edit_button.setEnabled(False)
        
        self.delete_button = QPushButton(self.lang_manager.get_text("delete_password"))
        self.delete_button.clicked.connect(self.delete_password)
        self.delete_button.setEnabled(False)
        
        self.refresh_button = QPushButton(self.lang_manager.get_text("refresh_list"))
        self.refresh_button.clicked.connect(self.refresh_password_list)
        
        self.reset_button = QPushButton(self.lang_manager.get_text("reset_data"))
        self.reset_button.clicked.connect(self.reset_data)
        
        self.change_password_button = QPushButton(self.lang_manager.get_text("change_master_password"))
        self.change_password_button.clicked.connect(self.change_master_password)
        
        # 添加按钮到按钮布局
        button_layout.addWidget(self.qr_button)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.change_password_button)
        button_layout.addStretch()
        
        # 创建语言切换按钮
        self.lang_button = QPushButton(self.lang_manager.get_text("switch_to_cn"))
        self.lang_button.clicked.connect(self.switch_language)
        self.lang_button.setFixedWidth(70)
        
        # 添加按钮布局和语言切换按钮到顶部布局
        top_layout.addLayout(button_layout)
        top_layout.addWidget(self.lang_button)
        
        # 创建密码列表
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(4)
        self.password_table.setHorizontalHeaderLabels([
            self.lang_manager.get_text("id"),
            self.lang_manager.get_text("service_name"),
            self.lang_manager.get_text("username"),
            self.lang_manager.get_text("created_at")
        ])
        self.password_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.password_table.setSelectionMode(QTableWidget.SingleSelection)
        self.password_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.password_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.password_table.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # 设置表格列宽
        header = self.password_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # 添加部件到主布局
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.password_table)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(self.lang_manager.get_text("ready"))
        
        # 初始刷新密码列表
        self.refresh_password_list()
    
    def check_first_time_setup(self):
        """检查是否首次使用"""
        # 首次使用提示
        if not hasattr(self, '_first_time_checked'):
            self._first_time_checked = True
            QMessageBox.information(
                self, 
                self.lang_manager.get_text("welcome"), 
                self.lang_manager.get_text("welcome_message")
            )
    
    def verify_2fa(self, title="2FA验证", message="请输入6位验证码:"):
        """验证2FA令牌"""
        import time
        
        # 检查是否在超时时间内
        current_time = time.time()
        if current_time - self.last_verification_time < self.verification_timeout:
            return True
        
        from ui.totp_dialog import TOTPDialog
        
        dialog = TOTPDialog(self.auth, self, title, message)
        result = dialog.exec_()
        
        # 如果验证成功，更新最后验证时间
        if result:
            self.last_verification_time = time.time()
        
        return result
    
    def show_qr_code(self):
        """显示配对二维码"""
        # 检查密码库是否为空
        records = self.db.get_all_passwords()
        if len(records) > 0:
            # 密码库不为空，必须验证当前2FA验证码
            if not self.verify_2fa("验证2FA", "密码库中有密码，必须验证当前2FA验证码才能重新配对:"):
                return
        
        dialog = QRDialog(self.auth, self)
        dialog.exec_()
    
    def add_password(self):
        """添加密码"""
        # 验证管理员密码
        if not self.verify_master_password():
            return
            
        dialog = PasswordDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            if data:
                self.db.add_password(
                    data['service_name'],
                    data['username'],
                    data['password']
                )
                self.refresh_password_list()
                self.status_bar.showMessage("密码添加成功")
    
    def edit_password(self):
        """编辑密码"""
        selected_row = self.password_table.currentRow()
        if selected_row >= 0:
            record_id = int(self.password_table.item(selected_row, 0).text())
            # 验证管理员密码
            if not self.verify_master_password():
                return
            if self.verify_2fa("编辑密码验证", "请验证2FA以编辑密码:"):
                # 获取完整记录
                record = self.db.get_password(record_id)
                if record:
                    dialog = PasswordDialog(self, record)
                    if dialog.exec_():
                        data = dialog.get_data()
                        if data:
                            self.db.update_password(
                                record_id,
                                data['service_name'],
                                data['username'],
                                data['password']
                            )
                            self.refresh_password_list()
                            self.status_bar.showMessage("密码更新成功")
    
    def delete_password(self):
        """删除密码"""
        selected_row = self.password_table.currentRow()
        if selected_row >= 0:
            reply = QMessageBox.question(
                self, 
                "确认删除", 
                "确定要删除选中的密码记录吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                record_id = int(self.password_table.item(selected_row, 0).text())
                if self.db.delete_password(record_id):
                    self.refresh_password_list()
                    self.status_bar.showMessage("密码删除成功")
                else:
                    self.status_bar.showMessage("删除失败")
    
    def refresh_password_list(self):
        """刷新密码列表"""
        # 获取所有密码记录
        records = self.db.get_all_passwords()
        
        # 检查是否已绑定2FA设备
        from config.settings import SECRET_KEY_FILE
        is_bound = SECRET_KEY_FILE.exists()
        
        # 如果没有绑定2FA设备且有密码记录，显示提示
        if not is_bound and len(records) > 0:
            self.status_bar.showMessage("请先绑定2FA设备，否则密码不可访问")
            # 清空表格
            self.password_table.setRowCount(0)
            return
        
        # 设置表格行数
        self.password_table.setRowCount(len(records))
        
        # 填充数据
        for row, record in enumerate(records):
            self.password_table.setItem(row, 0, QTableWidgetItem(str(record['id'])))
            self.password_table.setItem(row, 1, QTableWidgetItem(record['service_name']))
            self.password_table.setItem(row, 2, QTableWidgetItem(record['username']))
            self.password_table.setItem(row, 3, QTableWidgetItem(record['created_at']))
        
        # 调整列宽
        self.password_table.resizeColumnsToContents()
        
        self.status_bar.showMessage(f"共 {len(records)} 条记录")
    
    def on_selection_changed(self):
        """选择改变时的处理"""
        has_selection = len(self.password_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        reply = QMessageBox.question(
            self, 
            self.lang_manager.get_text("confirm_exit"), 
            self.lang_manager.get_text("exit_message"),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    
    def on_item_double_clicked(self, item):
        """双击项目时的处理"""
        # 获取行号
        row = item.row()
        # 获取记录ID
        record_id = int(self.password_table.item(row, 0).text())
        
        # 验证管理员密码
        if not self.verify_master_password():
            return
            
        # 验证2FA
        if self.verify_2fa("查看密码验证", "请验证2FA以查看密码:"):
            try:
                # 获取完整记录
                record = self.db.get_password(record_id)
                if record:
                    # 显示密码详情对话框
                    dialog = PasswordDetailDialog(record, self)
                    dialog.exec_()
            except Exception as e:
                QMessageBox.critical(self, "错误", f"获取密码详情时发生错误: {str(e)}")
    
    def import_csv(self):
        """导入CSV文件"""
        # 验证管理员密码
        if not self.verify_master_password():
            return
            
        # 检查是否已绑定2FA设备
        from config.settings import SECRET_KEY_FILE
        if not SECRET_KEY_FILE.exists():
            QMessageBox.warning(self, "警告", "请先绑定2FA设备再导入密码！")
            return
        
        # 选择CSV文件
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择CSV文件", 
            "", 
            "CSV文件 (*.csv)"
        )
        
        if not file_path:
            return
        
        # 读取并解析CSV文件
        try:
            import csv
            with open(file_path, 'r', encoding='utf-8') as file:
                # 检测CSV格式
                sample = file.read(1024)
                file.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.reader(file, delimiter=delimiter)
                rows = list(reader)
                
                # 检查是否有标题行
                if len(rows) < 1:
                    QMessageBox.warning(self, "警告", "CSV文件为空！")
                    return
                
                # 确定列索引（支持不同的CSV格式）
                header = rows[0]
                url_index = -1
                username_index = -1
                password_index = -1
                
                # 尝试匹配常见的列名
                for i, col in enumerate(header):
                    col_lower = col.lower()
                    if 'url' in col_lower or '网站' in col_lower or 'site' in col_lower:
                        url_index = i
                    elif 'username' in col_lower or '用户名' in col_lower or 'user' in col_lower:
                        username_index = i
                    elif 'password' in col_lower or '密码' in col_lower or 'pass' in col_lower:
                        password_index = i
                
                # 如果无法自动匹配，提示用户
                if url_index == -1 or username_index == -1 or password_index == -1:
                    QMessageBox.warning(
                        self, 
                        "警告", 
                        "无法自动识别CSV文件格式，请确保文件包含URL/网站、用户名和密码列！"
                    )
                    return
                
                # 导入数据
                imported_count = 0
                for row in rows[1:]:  # 跳过标题行
                    if len(row) > max(url_index, username_index, password_index):
                        url = row[url_index]
                        username = row[username_index]
                        password = row[password_index]
                        
                        # 如果URL为空，跳过
                        if not url.strip():
                            continue
                            
                        # 提取域名作为服务名称
                        from urllib.parse import urlparse
                        try:
                            parsed_url = urlparse(url)
                            service_name = parsed_url.netloc or url
                        except:
                            service_name = url
                        
                        # 添加到数据库（使用加密）
                        try:
                            self.db.add_password(service_name, username, password)
                            imported_count += 1
                        except Exception as e:
                            QMessageBox.critical(self, "错误", f"导入密码记录时发生错误: {str(e)}")
                            return
                
                # 刷新列表
                self.refresh_password_list()
                
                # 显示结果
                QMessageBox.information(
                    self, 
                    "导入完成", 
                    f"成功导入 {imported_count} 条密码记录！"
                )
                self.status_bar.showMessage(f"成功导入 {imported_count} 条密码记录")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入CSV文件时发生错误: {str(e)}")
    
    def switch_language(self):
        """切换语言"""
        current_lang = self.lang_manager.current_language
        if current_lang == "en":
            self.lang_manager.set_language("zh")
        else:
            self.lang_manager.set_language("en")
    
    def on_language_changed(self, language):
        """语言切换时的处理"""
        # 更新窗口标题
        self.setWindowTitle(self.lang_manager.get_text("app_title"))
        
        # 更新按钮文本
        self.qr_button.setText(self.lang_manager.get_text("show_qr"))
        self.add_button.setText(self.lang_manager.get_text("add_password"))
        self.import_button.setText(self.lang_manager.get_text("import_csv"))
        self.edit_button.setText(self.lang_manager.get_text("edit_password"))
        self.delete_button.setText(self.lang_manager.get_text("delete_password"))
        self.refresh_button.setText(self.lang_manager.get_text("refresh_list"))
        self.reset_button.setText(self.lang_manager.get_text("reset_data"))
        
        # 更新语言切换按钮文本
        if language == "en":
            self.lang_button.setText(self.lang_manager.get_text("switch_to_cn"))
        else:
            self.lang_button.setText(self.lang_manager.get_text("switch_to_en"))
        
        # 更新表格列标题
        self.password_table.setHorizontalHeaderLabels([
            self.lang_manager.get_text("id"),
            self.lang_manager.get_text("service_name"),
            self.lang_manager.get_text("username"),
            self.lang_manager.get_text("created_at")
        ])
        
        # 更新状态栏
        records = self.db.get_all_passwords()
        self.status_bar.showMessage(self.lang_manager.get_text_with_args("records_count", count=len(records)))
    
    def reset_data(self):
        """清空所有数据"""
        reply = QMessageBox.question(
            self, 
            self.lang_manager.get_text("confirm_reset"), 
            self.lang_manager.get_text("reset_message"),
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 删除数据库文件
            from config.settings import DATABASE_FILE, ENCRYPTION_KEY_FILE, SECRET_KEY_FILE
            import os
            
            try:
                # 删除数据库文件
                if DATABASE_FILE.exists():
                    os.remove(DATABASE_FILE)
                
                # 删除加密密钥文件
                if ENCRYPTION_KEY_FILE.exists():
                    os.remove(ENCRYPTION_KEY_FILE)
                
                # 删除2FA密钥文件
                if SECRET_KEY_FILE.exists():
                    os.remove(SECRET_KEY_FILE)
                
                # 重新初始化数据库
                from core.database import get_database
                self.db = get_database()
                # 确保表已创建
                self.db._create_tables()
                
                # 刷新列表
                self.refresh_password_list()
                
                self.status_bar.showMessage(self.lang_manager.get_text("data_cleared"))
                QMessageBox.information(self, self.lang_manager.get_text("reset_success"), self.lang_manager.get_text("reset_success"))
            except Exception as e:
                self.status_bar.showMessage(self.lang_manager.get_text("reset_failed"))
                QMessageBox.critical(self, self.lang_manager.get_text("error"), 
                                   self.lang_manager.get_text_with_args("reset_failed") + f": {str(e)}")
    
    def check_and_setup_master_password(self):
        """检查并设置管理员密码"""
        # 检查是否需要设置管理员密码
        # 只有在数据库为空且未设置管理员密码时才允许设置
        records = self.db.get_all_passwords()
        master_hash = self.db.get_master_password_hash()
        
        if len(records) == 0 and master_hash is None:
            # 显示设置管理员密码对话框
            dialog = SetMasterPasswordDialog(self)
            if dialog.exec_():
                password = dialog.get_password()
                if password:
                    self.db.set_master_password(password)
                    QMessageBox.information(self, "成功", "管理员密码设置成功！")
            else:
                # 用户取消设置密码，但这是首次使用，我们仍需要设置一个默认密码
                # 或者提示用户必须设置密码
                QMessageBox.warning(self, "警告", "必须设置管理员密码才能使用程序！")
                self.check_and_setup_master_password()  # 重新尝试
    
    def verify_master_password(self):
        """验证管理员密码"""
        # 创建输入对话框
        dialog = QDialog(self)
        dialog.setWindowTitle(self.lang_manager.get_text("verify_master_password_title"))
        dialog.setModal(True)
        dialog.setMinimumWidth(300)
        
        layout = QFormLayout(dialog)
        
        password_edit = QLineEdit()
        password_edit.setEchoMode(QLineEdit.Password)
        password_edit.setPlaceholderText(self.lang_manager.get_text("enter_master_password"))
        
        layout.addRow(self.lang_manager.get_text("master_password_label"), password_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, dialog
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        # 设置回车键确认
        password_edit.returnPressed.connect(dialog.accept)
        
        if dialog.exec_():
            password = password_edit.text()
            if self.db.verify_master_password(password):
                # 初始化加密器
                self.db.initialize_encryption_with_password(password)
                return True
            else:
                QMessageBox.warning(self, self.lang_manager.get_text("warning"), 
                                  self.lang_manager.get_text("master_password_incorrect"))
                return False
        else:
            return False
    
    def change_master_password(self):
        """更改管理员密码"""
        # 检查是否已设置管理员密码
        master_hash = self.db.get_master_password_hash()
        if not master_hash:
            # 没有设置管理员密码，显示设置密码对话框
            dialog = SetMasterPasswordDialog(self)
            if dialog.exec_():
                password = dialog.get_password()
                if password:
                    self.db.set_master_password(password)
                    QMessageBox.information(self, "成功", "管理员密码设置成功！")
            return
            
        # 显示更改密码对话框
        dialog = ChangeMasterPasswordDialog(self.db, self)
        if dialog.exec_():
            # 更新密码
            self.db.set_master_password(dialog.new_password)
            QMessageBox.information(self, "成功", "管理员密码已更改！")
