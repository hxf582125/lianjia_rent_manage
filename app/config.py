# -*- coding: utf-8 -*-
"""
应用配置模块
从.env文件加载配置信息，提供统一的配置访问接口
"""

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus


class Config:
    """
    基础配置类
    包含所有环境共享的配置项
    """
    
    # 加载.env文件中的环境变量
    load_dotenv()
    
    # Flask基础配置
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # 数据库连接配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'lianjia_rent')
    MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')
    
    # 构建SQLAlchemy数据库连接URI
    # 使用quote_plus对密码进行URL编码，处理特殊字符
    SQLALCHEMY_DATABASE_URI = (
        f'mysql+pymysql://{MYSQL_USER}:{quote_plus(MYSQL_PASSWORD)}@'
        f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset={MYSQL_CHARSET}'
    )
    
    # SQLAlchemy配置
    # 关闭追踪修改，提高性能
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示SQL语句，便于调试（生产环境建议关闭）
    SQLALCHEMY_ECHO = DEBUG
    
    # Dash应用配置
    DASH_REQUESTS_PATHNAME_PREFIX = os.getenv(
        'DASH_REQUESTS_PATHNAME_PREFIX', '/dash/'
    )


class DevelopmentConfig(Config):
    """
    开发环境配置
    继承基础配置，可覆盖或添加开发环境特定配置
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    生产环境配置
    继承基础配置，可覆盖或添加生产环境特定配置
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False


# 配置字典，便于根据环境选择配置
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """
    根据环境名称获取配置类
    
    参数:
        env: 环境名称，可选值: 'development', 'production', 'default'
    
    返回:
        对应的配置类
    """
    if env is None:
        env = os.getenv('FLASK_ENV', 'default')
    return config_map.get(env, config_map['default'])
