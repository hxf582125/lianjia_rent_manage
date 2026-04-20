# -*- coding: utf-8 -*-
"""
应用启动入口文件
使用Flask应用工厂创建应用，并集成Dash应用
"""

import os
from app.factory import create_app
from app.dash_app.app import create_dash_app


# 创建Flask应用实例
# 从环境变量FLASK_ENV获取环境配置，默认为'default'(开发环境)
app = create_app(os.getenv('FLASK_ENV', 'default'))

# 创建并集成Dash应用
dash_app = create_dash_app(app)


@app.route('/')
def index():
    """
    首页路由
    将用户重定向到Dash应用页面
    """
    from flask import redirect
    return redirect('/dash/')


if __name__ == '__main__':
    # 启动Flask开发服务器
    # 注意：生产环境应使用专业的WSGI服务器如Gunicorn或uWSGI
    print('=' * 60)
    print('链家租房数据分析系统启动中...')
    print(f'Flask应用运行在: http://localhost:{app.config["PORT"]}')
    print(f'Dash应用运行在: http://localhost:{app.config["PORT"]}/dash/')
    print('=' * 60)
    
    app.run(
        host='0.0.0.0',
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
