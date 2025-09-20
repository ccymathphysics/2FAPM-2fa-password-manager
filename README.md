# 2FA Password Manager

## 项目概述

这是一个带有二次验证功能的密码管理器程序。用户可以通过手机2FA应用扫描二维码进行配对，然后安全地存储和管理账号密码。

## 功能特性

1. **2FA配对**：生成二维码供手机应用扫描配对
2. **密码存储**：加密存储用户账号和密码
3. **安全验证**：查看密码前需要通过2FA验证
4. **用户界面**：直观的图形用户界面
5. **数据安全**：本地加密存储所有数据

## 技术架构

### 核心组件

- `core/auth.py`：2FA认证功能
- `core/encryption.py`：数据加密解密
- `core/database.py`：数据存储管理
- `ui/main_window.py`：主界面
- `ui/auth_dialog.py`：认证对话框
- `ui/password_dialog.py`：密码管理对话框

### 依赖库

- `pyotp`：生成和验证TOTP令牌
- `qrcode`：生成二维码
- `cryptography`：数据加密
- `sqlite3`：本地数据库
- `PyQt5`：图形界面

## 使用说明

1. 启动程序
2. 扫描二维码与手机2FA应用配对
3. 设置主密码
4. 添加、查看和管理账号密码
5. 每次查看密码时需要进行2FA验证

## 安装依赖

```bash
pip install pyotp qrcode[pil] cryptography PyQt5
