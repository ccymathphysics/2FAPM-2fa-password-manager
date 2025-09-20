#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
语言管理模块
"""

from PyQt5.QtCore import QObject, pyqtSignal


class LanguageManager(QObject):
    """语言管理器"""
    
    # 语言切换信号
    language_changed = pyqtSignal(str)
    
    def __init__(self):
        """初始化语言管理器"""
        super().__init__()
        self.current_language = "en"  # 默认语言为英语
        self.translations = {
            "en": {
                # 主窗口
                "app_title": "2FA Password Manager",
                "show_qr": "Show QR Code",
                "add_password": "Add Password",
                "import_csv": "Import CSV",
                "edit_password": "Edit Password",
                "delete_password": "Delete Password",
                "refresh_list": "Refresh List",
                "reset_data": "Reset Data",
                "change_master_password": "Change Master Password",
                "switch_to_cn": "CN",
                "switch_to_en": "EN",
                "id": "ID",
                "service_name": "Service Name",
                "username": "Username",
                "created_at": "Created At",
                "ready": "Ready",
                "records_count": "Total {count} records",
                "confirm_exit": "Confirm Exit",
                "exit_message": "Are you sure you want to exit the 2FA Password Manager?",
                "yes": "Yes",
                "no": "No",
                
                # 首次使用提示
                "welcome": "Welcome",
                "welcome_message": "Welcome to 2FA Password Manager!\nPlease pair your 2FA device first.",
                
                # 2FA验证
                "verify_2fa": "2FA Verification",
                "enter_code": "Please enter the 6-digit code:",
                "reverify_2fa": "Re-verify 2FA",
                "reverify_message": "Please verify 2FA to re-pair:",
                "view_password_verify": "View Password Verification",
                "view_password_message": "Please verify 2FA to view password:",
                "edit_password_verify": "Edit Password Verification",
                "edit_password_message": "Please verify 2FA to edit password:",
                
                # 密码操作
                "confirm_delete": "Confirm Delete",
                "delete_message": "Are you sure you want to delete the selected password record?",
                "delete_success": "Password deleted successfully",
                "delete_failed": "Delete failed",
                "add_success": "Password added successfully",
                "update_success": "Password updated successfully",
                
                # 清空数据
                "confirm_reset": "Confirm Reset",
                "reset_message": "Are you sure you want to clear all data and unbind 2FA? This operation cannot be undone!",
                "reset_success": "All data cleared!",
                "reset_failed": "Failed to clear data",
                
                # 导入CSV
                "import_csv_title": "Select CSV File",
                "csv_filter": "CSV Files (*.csv)",
                "bind_2fa_first": "Warning",
                "bind_2fa_message": "Please bind 2FA device before importing passwords!",
                "empty_csv": "Warning",
                "empty_csv_message": "CSV file is empty!",
                "invalid_csv": "Warning",
                "invalid_csv_message": "Unable to automatically identify CSV file format. Please ensure the file contains URL/site, username, and password columns!",
                "import_complete": "Import Complete",
                "import_complete_message": "Successfully imported {count} password records!",
                
                # 错误提示
                "error": "Error",
                "import_error": "Error importing CSV file: {error}",
                
                # 状态提示
                "bind_2fa_required": "Please bind 2FA device first, otherwise passwords are not accessible",
                "data_cleared": "Data cleared",
                
                # 密码详情对话框
                "password_detail": "Password Details",
                "service": "Service:",
                "user": "Username:",
                "password": "Password:",
                "show": "Show",
                "hide": "Hide",
                "copy": "Copy",
                "close": "Close",
                "copy_success": "Success",
                "copy_success_message": "Password copied to clipboard",
                "copy_failed": "Copy failed: {error}",
                
                # 密码对话框
                "add_password_title": "Add Password",
                "edit_password_title": "Edit Password",
                "service_label": "Service Name:",
                "username_label": "Username:",
                "password_label": "Password:",
                "save": "Save",
                "cancel": "Cancel",
                "service_required": "Service name is required",
                "username_required": "Username is required",
                "password_required": "Password is required",
                
                # QR对话框
                "qr_title": "2FA Pairing QR Code",
                "scan_qr": "Scan this QR code with your 2FA app",
                "enter_code_prompt": "Enter the 6-digit code from your 2FA app:",
                "pair_success": "2FA device paired successfully!",
                "pair_failed": "Invalid code. Please try again.",
                
                # 认证对话框
                "auth_title": "2FA Authentication",
                "auth_prompt": "Enter your 6-digit 2FA code:",
                "auth_success": "Authentication successful",
                "auth_failed": "Invalid code. Please try again.",
                
                # 管理员密码相关
                "set_master_password_title": "Set Master Password",
                "change_master_password_title": "Change Master Password",
                "verify_master_password_title": "Verify Master Password",
                "master_password_label": "Master Password:",
                "confirm_password_label": "Confirm Password:",
                "current_password_label": "Current Password:",
                "new_password_label": "New Password:",
                "confirm_new_password_label": "Confirm New Password:",
                "enter_master_password": "Please enter master password",
                "confirm_master_password": "Please confirm master password",
                "enter_current_password": "Please enter current password",
                "enter_new_password": "Please enter new password",
                "confirm_new_password": "Please confirm new password",
                "master_password_required": "Master password is required",
                "current_password_required": "Current password is required",
                "new_password_required": "New password is required",
                "password_mismatch": "Passwords do not match",
                "new_password_mismatch": "New passwords do not match",
                "master_password_incorrect": "Master password is incorrect",
                "current_password_incorrect": "Current password is incorrect",
                "2fa_verification": "2FA Verification",
                "enter_6_digit_code": "Please enter 6-digit code:",
                "2fa_required_to_change_password": "2FA verification is required to change password",
            },
            "zh": {
                # 主窗口
                "app_title": "2FA密码管理器",
                "show_qr": "显示配对二维码",
                "add_password": "添加密码",
                "import_csv": "导入CSV",
                "edit_password": "编辑密码",
                "delete_password": "删除密码",
                "refresh_list": "刷新列表",
                "reset_data": "清空数据",
                "change_master_password": "更改管理员密码",
                "switch_to_cn": "中",
                "switch_to_en": "英",
                "id": "ID",
                "service_name": "服务名称",
                "username": "用户名",
                "created_at": "创建时间",
                "ready": "就绪",
                "records_count": "共 {count} 条记录",
                "confirm_exit": "确认退出",
                "exit_message": "确定要退出2FA密码管理器吗？",
                "yes": "是",
                "no": "否",
                
                # 首次使用提示
                "welcome": "欢迎使用",
                "welcome_message": "欢迎使用2FA密码管理器！\n首次使用请先进行2FA设备配对。",
                
                # 2FA验证
                "verify_2fa": "2FA验证",
                "enter_code": "请输入6位验证码:",
                "reverify_2fa": "验证2FA",
                "reverify_message": "请验证2FA以重新配对:",
                "view_password_verify": "查看密码验证",
                "view_password_message": "请验证2FA以查看密码:",
                "edit_password_verify": "编辑密码验证",
                "edit_password_message": "请验证2FA以编辑密码:",
                
                # 密码操作
                "confirm_delete": "确认删除",
                "delete_message": "确定要删除选中的密码记录吗？",
                "delete_success": "密码删除成功",
                "delete_failed": "删除失败",
                "add_success": "密码添加成功",
                "update_success": "密码更新成功",
                
                # 清空数据
                "confirm_reset": "确认清空",
                "reset_message": "确定要清空所有数据并解绑2FA吗？此操作不可恢复！",
                "reset_success": "所有数据已清空！",
                "reset_failed": "清空数据失败",
                
                # 导入CSV
                "import_csv_title": "选择CSV文件",
                "csv_filter": "CSV文件 (*.csv)",
                "bind_2fa_first": "警告",
                "bind_2fa_message": "请先绑定2FA设备再导入密码！",
                "empty_csv": "警告",
                "empty_csv_message": "CSV文件为空！",
                "invalid_csv": "警告",
                "invalid_csv_message": "无法自动识别CSV文件格式，请确保文件包含URL/网站、用户名和密码列！",
                "import_complete": "导入完成",
                "import_complete_message": "成功导入 {count} 条密码记录！",
                
                # 错误提示
                "error": "错误",
                "import_error": "导入CSV文件时发生错误: {error}",
                
                # 状态提示
                "bind_2fa_required": "请先绑定2FA设备，否则密码不可访问",
                "data_cleared": "数据已清空",
                
                # 密码详情对话框
                "password_detail": "密码详情",
                "service": "服务名称:",
                "user": "用户名:",
                "password": "密码:",
                "show": "显示",
                "hide": "隐藏",
                "copy": "复制",
                "close": "关闭",
                "copy_success": "成功",
                "copy_success_message": "密码已复制到剪贴板",
                "copy_failed": "复制密码失败: {error}",
                
                # 密码对话框
                "add_password_title": "添加密码",
                "edit_password_title": "编辑密码",
                "service_label": "服务名称:",
                "username_label": "用户名:",
                "password_label": "密码:",
                "save": "保存",
                "cancel": "取消",
                "service_required": "服务名称不能为空",
                "username_required": "用户名不能为空",
                "password_required": "密码不能为空",
                
                # QR对话框
                "qr_title": "2FA配对二维码",
                "scan_qr": "请用您的2FA应用扫描此二维码",
                "enter_code_prompt": "请输入您2FA应用显示的6位验证码:",
                "pair_success": "2FA设备配对成功！",
                "pair_failed": "验证码无效，请重试。",
                
                # 认证对话框
                "auth_title": "2FA认证",
                "auth_prompt": "请输入您的6位2FA验证码:",
                "auth_success": "认证成功",
                "auth_failed": "验证码无效，请重试。",
                
                # 管理员密码相关
                "set_master_password_title": "设置管理员密码",
                "change_master_password_title": "更改管理员密码",
                "verify_master_password_title": "验证管理员密码",
                "master_password_label": "管理员密码:",
                "confirm_password_label": "确认密码:",
                "current_password_label": "当前密码:",
                "new_password_label": "新密码:",
                "confirm_new_password_label": "确认新密码:",
                "enter_master_password": "请输入管理员密码",
                "confirm_master_password": "请再次输入管理员密码",
                "enter_current_password": "请输入当前密码",
                "enter_new_password": "请输入新密码",
                "confirm_new_password": "请再次输入新密码",
                "master_password_required": "请输入管理员密码",
                "current_password_required": "请输入当前密码",
                "new_password_required": "请输入新密码",
                "password_mismatch": "两次输入的密码不一致",
                "new_password_mismatch": "两次输入的新密码不一致",
                "master_password_incorrect": "管理员密码错误",
                "current_password_incorrect": "当前密码错误",
                "2fa_verification": "2FA验证",
                "enter_6_digit_code": "请输入6位验证码:",
                "2fa_required_to_change_password": "必须通过2FA验证才能更改密码",
            }
        }
    
    def set_language(self, language):
        """设置语言"""
        if language in self.translations:
            self.current_language = language
            self.language_changed.emit(language)
            return True
        return False
    
    def get_text(self, key):
        """获取指定键的文本"""
        if self.current_language in self.translations:
            lang_dict = self.translations[self.current_language]
            if key in lang_dict:
                return lang_dict[key]
        # 如果当前语言没有该键，回退到英语
        if "en" in self.translations:
            lang_dict = self.translations["en"]
            if key in lang_dict:
                return lang_dict[key]
        return key  # 如果都没有，返回键名
    
    def get_text_with_args(self, key, **kwargs):
        """获取带参数的文本"""
        text = self.get_text(key)
        return text.format(**kwargs)


# 全局语言管理器实例
_language_manager = None


def get_language_manager():
    """获取全局语言管理器实例"""
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageManager()
    return _language_manager
