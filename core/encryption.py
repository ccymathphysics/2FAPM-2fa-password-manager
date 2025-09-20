#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
加密模块
提供数据加密和解密功能
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from config.settings import ENCRYPTION_KEY_FILE


class EncryptionManager:
    """加密管理器"""
    
    def __init__(self):
        """初始化"""
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self):
        """加载或创建加密密钥"""
        if ENCRYPTION_KEY_FILE.exists():
            with open(ENCRYPTION_KEY_FILE, 'rb') as f:
                key = f.read()
        else:
            # 生成新的密钥
            key = Fernet.generate_key()
            with open(ENCRYPTION_KEY_FILE, 'wb') as f:
                f.write(key)
        return key
    
    def encrypt(self, data):
        """
        加密数据
        
        Args:
            data (str): 要加密的明文数据
            
        Returns:
            bytes: 加密后的数据
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher.encrypt(data)
    
    def decrypt(self, encrypted_data):
        """
        解密数据
        
        Args:
            encrypted_data (bytes): 要解密的数据
            
        Returns:
            str: 解密后的明文数据
        """
        decrypted_data = self.cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')
    
    def derive_key_from_password(self, password, salt=None):
        """
        从密码派生加密密钥
        
        Args:
            password (str): 用户密码
            salt (bytes): 盐值，如果为None则自动生成
            
        Returns:
            tuple: (key, salt) 密钥和盐值
        """
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt


# 单例模式实例
_encryption_instance = None


def get_encryption():
    """获取加密实例（单例模式）"""
    global _encryption_instance
    if _encryption_instance is None:
        _encryption_instance = EncryptionManager()
    return _encryption_instance
