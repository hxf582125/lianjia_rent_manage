# -*- coding: utf-8 -*-
"""
Flask应用工厂模块
使用应用工厂模式创建Flask应用，便于配置和扩展管理
"""

from flask import Flask
from app.config import get_config
from app.extensions import db


def create_app(config_name=None):
    """
    Flask应用工厂函数
    
    参数:
        config_name: 配置名称，可选值: 'development', 'production', 'default'
        
    返回:
        Flask: 初始化后的Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 加载配置
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # 初始化数据库扩展
    db.init_app(app)
    
    # 注册蓝图（如果有API路由的话）
    # from app.routes import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    
    # 创建数据库表（如果不存在的话）
    # 注意：在生产环境中应该使用数据库迁移工具
    with app.app_context():
        db.create_all()
    
    return app
