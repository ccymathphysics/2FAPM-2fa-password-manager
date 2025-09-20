# 2FA Password Manager

## 项目概述

这是一个带有二次验证功能的密码管理器程序。用户可以通过手机2FA应用扫描二维码进行配对，然后安全地存储和管理账号密码。

![2FA Password Manager](screenshots/main_window.png)

## 功能特性

### 核心功能
- **2FA设备配对**：生成二维码供手机应用扫描配对
- **安全存储**：所有密码使用AES加密算法加密存储
- **多语言支持**：默认语言为英语，在主页面右上角可以切换语言（EN/CN）
- **CSV导入**：支持导入浏览器导出的CSV密码文件

### 安全特性
- 编辑和查看密码需要2FA验证
- 双击用户名即可查看完整密码信息（需2FA验证）
- 10秒内验证过不需要再次验证（缓存机制）
- 添加密码不需要2FA验证
- **管理员密码保护**：所有操作都需要管理员密码验证（新增）
- **双重验证**：敏感操作需要管理员密码+2FA双重验证（新增）

### 管理员密码功能（新增）
- 首次使用时设置管理员密码
- 所有密码操作前都需要验证管理员密码
- 提供更改管理员密码功能（需验证原密码和2FA）
- 管理员密码使用SHA512哈希存储，数据使用派生密钥加密

详情请参见 [管理员密码功能说明](ADMIN_PASSWORD_FEATURES.md)

## 程序结构

```
2fa_password_manager/
├── main.py              # 程序入口点
├── init.py              # 初始化脚本
├── requirements.txt     # 依赖文件
├── README.md            # 项目说明文档
├── README_ENGLISH.md    # 英文版项目说明文档
├── core/                # 核心功能模块
│   ├── auth.py          # 2FA认证功能
│   ├── encryption.py    # 数据加密解密
│   ├── database.py      # 数据库存储管理
│   └── language.py      # 多语言支持
├── ui/                  # 用户界面模块
│   ├── main_window.py   # 主窗口界面
│   ├── auth_dialog.py   # 认证对话框
│   ├── password_dialog.py # 密码管理对话框
│   ├── qr_dialog.py     # 二维码显示对话框
│   ├── totp_dialog.py   # TOTP验证对话框
│   └── password_detail_dialog.py # 密码详情对话框
└── config/              # 配置文件
    └── settings.py      # 程序配置
```

## 安装依赖

```bash
pip install pyotp qrcode[pil] cryptography PyQt5 pyperclip
```

或者运行初始化脚本：

```bash
python init.py
```

## 使用方法

1. 运行 `python main.py` 启动程序
2. 点击"显示配对二维码"进行2FA设备配对
3. 输入手机显示的验证码完成配对
4. 开始添加和管理密码
5. 双击用户名或使用编辑功能时需要2FA验证
6. 使用"清空数据"按钮可重置所有数据
7. 使用"导入CSV"按钮可批量导入密码
8. 在主页面右上角可以切换语言（EN/CN）

## 安全说明

1. 所有密码都使用AES加密算法加密存储
2. 2FA密钥安全存储
3. 加密密钥自动生成并安全保存
4. 敏感操作需要2FA验证
5. 数据本地存储，不上传到任何服务器
6. 10秒验证缓存机制，避免频繁验证

## 截图

### 主界面
![主界面](screenshots/main_window.png)

### 2FA配对
![2FA配对](screenshots/qr_code.png)

### 密码详情
![密码详情](screenshots/password_detail.png)

## 许可证

本项目采用MIT许可证，详情请见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
