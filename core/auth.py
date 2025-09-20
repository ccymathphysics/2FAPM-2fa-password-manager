#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
2FA认证模块
提供TOTP二次验证功能
"""

import pyotp
import qrcode
import base64
import os
from io import BytesIO
from PIL import Image
from config.settings import TOTP_ISSUER, TOTP_DIGITS, TOTP_INTERVAL, SECRET_KEY_FILE


class TOTPAuth:
    """TOTP二次验证类"""
    
    def __init__(self):
        """初始化"""
        self.secret = self._load_or_create_secret()
        self.totp = pyotp.TOTP(
            self.secret, 
            digits=TOTP_DIGITS, 
            interval=TOTP_INTERVAL
        )
    
    def _load_or_create_secret(self):
        """加载或创建密钥"""
        if SECRET_KEY_FILE.exists():
            with open(SECRET_KEY_FILE, 'r') as f:
                secret = f.read().strip()
        else:
            # 生成新的随机密钥
            secret = pyotp.random_base32()
            with open(SECRET_KEY_FILE, 'w') as f:
                f.write(secret)
        return secret
    
    def get_secret(self):
        """获取密钥"""
        return self.secret
    
    def generate_qr_code(self, account_name):
        """
        生成二维码供手机应用扫描
        
        Args:
            account_name (str): 账户名称
            
        Returns:
            PIL.Image: 二维码图像
        """
        # 创建TOTP URI
        totp_uri = self.totp.provisioning_uri(
            name=account_name,
            issuer_name=TOTP_ISSUER
        )
        
        # 生成二维码
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        # 创建图像
        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    def verify_token(self, token):
        """
        验证TOTP令牌
        
        Args:
            token (str): 用户输入的6位数字令牌
            
        Returns:
            bool: 验证是否成功
        """
        try:
            return self.totp.verify(token)
        except:
            return False
    
    def get_current_token(self):
        """
        获取当前有效的令牌
        
        Returns:
            str: 当前有效的6位数字令牌
        """
        return self.totp.now()


# 单例模式实例
_auth_instance = None


def get_auth():
    """获取认证实例（单例模式）"""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = TOTPAuth()
    return _auth_instance
