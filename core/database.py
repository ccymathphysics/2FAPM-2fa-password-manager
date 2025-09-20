#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数据库模块
提供密码数据的存储和检索功能
"""

import sqlite3
import json
from config.settings import DATABASE_FILE
from core.encryption import get_encryption


class PasswordDatabase:
    """密码数据库管理器"""
    
    def __init__(self):
        """初始化数据库"""
        self.encryption = get_encryption()
        self.db_file = DATABASE_FILE
        self._create_tables()
    
    def _create_tables(self):
        """创建数据表"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            # 创建密码表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service_name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建元数据表（存储主密码哈希等）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                )
            ''')
            
            conn.commit()
    
    def set_master_password_hash(self, password_hash):
        """
        设置主密码哈希
        
        Args:
            password_hash (str): 主密码的哈希值
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO metadata (key, value)
                VALUES (?, ?)
            ''', ('master_password_hash', password_hash))
            conn.commit()
    
    def get_master_password_hash(self):
        """
        获取主密码哈希
        
        Returns:
            str or None: 主密码哈希值，如果不存在则返回None
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT value FROM metadata WHERE key = ?
            ''', ('master_password_hash',))
            result = cursor.fetchone()
            return result[0] if result else None
    
    def add_password(self, service_name, username, password):
        """
        添加密码记录
        
        Args:
            service_name (str): 服务名称
            username (str): 用户名
            password (str): 明文密码
            
        Returns:
            int: 新记录的ID
        """
        # 加密密码
        encrypted_password = self.encryption.encrypt(password)
        
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO passwords (service_name, username, encrypted_password)
                VALUES (?, ?, ?)
            ''', (service_name, username, encrypted_password))
            conn.commit()
            return cursor.lastrowid
    
    def get_password(self, record_id):
        """
        获取密码记录
        
        Args:
            record_id (int): 记录ID
            
        Returns:
            dict or None: 密码记录，如果不存在则返回None
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, service_name, username, encrypted_password
                FROM passwords WHERE id = ?
            ''', (record_id,))
            result = cursor.fetchone()
            
            if result:
                # 解密密码
                decrypted_password = self.encryption.decrypt(result[3])
                return {
                    'id': result[0],
                    'service_name': result[1],
                    'username': result[2],
                    'password': decrypted_password
                }
            return None
    
    def get_all_passwords(self):
        """
        获取所有密码记录（不包括密码字段）
        
        Returns:
            list: 密码记录列表
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, service_name, username, created_at, updated_at
                FROM passwords
                ORDER BY service_name
            ''')
            results = cursor.fetchall()
            
            return [
                {
                    'id': row[0],
                    'service_name': row[1],
                    'username': row[2],
                    'created_at': row[3],
                    'updated_at': row[4]
                }
                for row in results
            ]
    
    def update_password(self, record_id, service_name, username, password):
        """
        更新密码记录
        
        Args:
            record_id (int): 记录ID
            service_name (str): 服务名称
            username (str): 用户名
            password (str): 明文密码
            
        Returns:
            bool: 更新是否成功
        """
        # 加密密码
        encrypted_password = self.encryption.encrypt(password)
        
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE passwords
                SET service_name = ?, username = ?, encrypted_password = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (service_name, username, encrypted_password, record_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_password(self, record_id):
        """
        删除密码记录
        
        Args:
            record_id (int): 记录ID
            
        Returns:
            bool: 删除是否成功
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM passwords WHERE id = ?
            ''', (record_id,))
            conn.commit()
            return cursor.rowcount > 0


# 单例模式实例
_db_instance = None


def get_database():
    """获取数据库实例（单例模式）"""
    global _db_instance
    if _db_instance is None:
        _db_instance = PasswordDatabase()
    return _db_instance
