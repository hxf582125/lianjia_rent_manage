# -*- coding: utf-8 -*-
"""
Dash应用初始化模块
将Dash应用集成到Flask应用中，提供统一的Web服务
"""

import dash
from dash import html
import dash_bootstrap_components as dbc
from flask import Flask

from app.dash_app.layout import create_layout
from app.dash_app.callbacks import register_callbacks
from app.models import HouseDAO


def create_dash_app(flask_app: Flask):
    """
    创建并配置Dash应用，集成到Flask应用中
    
    参数:
        flask_app: Flask应用实例
        
    返回:
        dash.Dash: 配置好的Dash应用实例
    """
    # 使用Flask应用的配置获取Dash前缀
    routes_pathname_prefix = flask_app.config.get(
        'DASH_REQUESTS_PATHNAME_PREFIX', '/dash/'
    )
    
    # 创建Dash应用实例
    # 注意：Dash新版本中使用 routes_pathname_prefix 替代 url_base_pathname
    # routes_pathname_prefix: 后端API路由的前缀
    # requests_pathname_prefix: 前端AJAX请求的前缀（这里设置为相同值）
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        routes_pathname_prefix=routes_pathname_prefix,
        requests_pathname_prefix=routes_pathname_prefix,
        # 使用Bootstrap样式主题，提升UI美观度
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        # 抑制回调异常，避免页面崩溃
        suppress_callback_exceptions=True,
        # 启用调试模式下的热重载
        update_title=None
    )
    
    # 设置页面标题
    dash_app.title = '链家租房数据分析系统'
    
    # 在Flask应用上下文中获取批次ID列表
    with flask_app.app_context():
        batch_ids = HouseDAO.get_all_batch_ids()
    
    # 设置Dash应用布局
    dash_app.layout = html.Div([
        create_layout(batch_ids)
    ])
    
    # 注册所有回调函数
    register_callbacks(dash_app)
    
    return dash_app
