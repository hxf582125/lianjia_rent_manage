# -*- coding: utf-8 -*-
"""
Flask扩展模块
统一初始化和管理所有Flask扩展，避免循环导入问题
"""

from flask_sqlalchemy import SQLAlchemy


# 初始化SQLAlchemy扩展
# 使用延迟初始化模式，在应用工厂中调用init_app()
db = SQLAlchemy()
