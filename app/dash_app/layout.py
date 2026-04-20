# -*- coding: utf-8 -*-
"""
Dash应用布局模块
定义Dash应用的页面布局结构，包括：
1. 批次选择组件（支持单选/多选）
2. 单批次分析标签页（柱状图展示）
3. 多批次对比标签页（连线图展示）
"""

import re
from dash import dcc, html
import dash_bootstrap_components as dbc


def format_batch_id(batch_id):
    """
    格式化批次ID，只保留时间部分
    
    参数:
        batch_id: 原始批次ID，格式如 'lianjia_rent_global_20260402115642_2f90f5d9'
        
    返回:
        str: 格式化后的时间字符串，格式如 '2026-04-02 11:56:42'
             如果解析失败则返回原始批次ID
    """
    # 使用正则表达式提取时间戳部分
    # 匹配格式: lianjia_rent_global_YYYYMMDDHHMMSS_随机字符
    pattern = r'lianjia_rent_global_(\d{14})_'
    match = re.search(pattern, batch_id)
    
    if match:
        timestamp = match.group(1)
        # 解析时间戳: YYYYMMDDHHMMSS
        # 20260402115642 -> 2026-04-02 11:56:42
        year = timestamp[0:4]
        month = timestamp[4:6]
        day = timestamp[6:8]
        hour = timestamp[8:10]
        minute = timestamp[10:12]
        second = timestamp[12:14]
        
        return f'{year}-{month}-{day} {hour}:{minute}:{second}'
    
    # 如果解析失败，返回原始批次ID
    return batch_id


def create_batch_options(batch_ids):
    """
    创建批次选择器的选项列表
    
    参数:
        batch_ids: 原始批次ID列表
        
    返回:
        list: 包含字典的列表，每个字典包含 'label' 和 'value' 键
              label 是格式化后的显示文本，value 是原始批次ID
    """
    return [
        {'label': format_batch_id(batch_id), 'value': batch_id}
        for batch_id in batch_ids
    ]


def create_layout(batch_ids):
    """
    创建Dash应用的完整布局
    
    参数:
        batch_ids: 可用的批次ID列表
        
    返回:
        html.Div: Dash应用的根布局组件
    """
    # 创建批次选项
    batch_options = create_batch_options(batch_ids)
    
    # 使用 dcc.Store 存储批次选项，供后续使用
    return html.Div([
        # 页面标题
        html.H1(
            '链家租房数据分析系统',
            style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '30px',
                'marginTop': '20px'
            }
        ),
        
        # 标签页区域
        dbc.Tabs([
            # 单批次分析标签页
            dbc.Tab(label='单批次分析', tab_id='single-batch-tab'),
            # 多批次对比标签页
            dbc.Tab(label='多批次对比', tab_id='multi-batch-tab')
        ], id='main-tabs', active_tab='single-batch-tab', style={'marginBottom': '20px'}),
        
        # 标签页内容区域
        html.Div(id='tabs-content'),
        
        # 隐藏的存储组件，用于缓存批次选项数据
        dcc.Store(id='batch-options-store', data=batch_options),
        dcc.Store(id='batch-ids-store', data=batch_ids),
        
        # 页面底部信息
        html.Footer(
            [
                html.Hr(),
                html.P(
                    '链家租房数据分析系统 © 2026',
                    style={'textAlign': 'center', 'color': '#7f8c8d'}
                )
            ],
            style={'marginTop': '50px'}
        )
    ], style={'padding': '0 20px'})


def create_single_batch_layout(batch_options):
    """
    创建单批次分析页面的布局
    
    参数:
        batch_options: 批次选项列表，格式为 [{'label': '显示文本', 'value': '批次ID'}, ...]
        
    返回:
        html.Div: 单批次分析页面布局
    """
    return html.Div([
        # 批次选择器
        dbc.Card([
            dbc.CardHeader(html.H5('批次选择')),
            dbc.CardBody([
                html.Label('请选择要分析的批次：'),
                dcc.Dropdown(
                    id='single-batch-selector',
                    options=batch_options,
                    value=None,
                    placeholder='请选择一个批次',
                    style={'width': '100%', 'marginTop': '10px'}
                )
            ])
        ], style={'marginBottom': '20px'}),
        
        # 维度选择器
        dbc.Card([
            dbc.CardHeader(html.H5('分析维度选择')),
            dbc.CardBody([
                dcc.RadioItems(
                    id='dimension-selector',
                    options=[
                        {'label': '区域维度', 'value': 'district'},
                        {'label': '板块维度', 'value': 'bankuai'},
                        {'label': '小区维度', 'value': 'community'}
                    ],
                    value='district',
                    labelStyle={'display': 'inline-block', 'marginRight': '20px'},
                    inputStyle={'marginRight': '5px'}
                )
            ])
        ], style={'marginBottom': '20px'}),
        
        # 房源数量分布柱状图
        dbc.Card([
            dbc.CardHeader(html.H5('房源数量分布')),
            dbc.CardBody([
                dcc.Graph(id='count-distribution-chart')
            ])
        ], style={'marginBottom': '20px'}),
        
        # 租金区间分布柱状图
        dbc.Card([
            dbc.CardHeader(html.H5('租金区间分布')),
            dbc.CardBody([
                dcc.Graph(id='price-distribution-chart')
            ])
        ], style={'marginBottom': '20px'}),
        
        # 面积区间分布柱状图
        dbc.Card([
            dbc.CardHeader(html.H5('面积区间分布')),
            dbc.CardBody([
                dcc.Graph(id='area-distribution-chart')
            ])
        ])
    ])


def create_multi_batch_layout(batch_options):
    """
    创建多批次对比页面的布局
    
    参数:
        batch_options: 批次选项列表，格式为 [{'label': '显示文本', 'value': '批次ID'}, ...]
        
    返回:
        html.Div: 多批次对比页面布局
    """
    return html.Div([
        # 批次选择器
        dbc.Card([
            dbc.CardHeader(html.H5('批次选择')),
            dbc.CardBody([
                html.Label('请选择要对比的批次（可多选）：'),
                dcc.Dropdown(
                    id='multi-batch-selector',
                    options=batch_options,
                    value=None,
                    multi=True,
                    placeholder='请选择多个批次（至少1个）',
                    style={'width': '100%', 'marginTop': '10px'}
                )
            ])
        ], style={'marginBottom': '20px'}),
        
        # 指标选择器
        dbc.Card([
            dbc.CardHeader(html.H5('对比指标选择')),
            dbc.CardBody([
                dcc.Checklist(
                    id='metric-selector',
                    options=[
                        {'label': '房源总数', 'value': 'total_count'},
                        {'label': '平均租金（元/月）', 'value': 'avg_price'},
                        {'label': '平均面积（㎡）', 'value': 'avg_area'},
                        {'label': '平均单价（元/㎡/月）', 'value': 'price_per_sqm'}
                    ],
                    value=['total_count', 'avg_price'],
                    labelStyle={'display': 'inline-block', 'marginRight': '20px'},
                    inputStyle={'marginRight': '5px'}
                )
            ])
        ], style={'marginBottom': '20px'}),
        
        # 趋势图展示区域
        dbc.Row([
            # 房源总数趋势图
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5('房源总数变化趋势')),
                    dbc.CardBody([
                        dcc.Graph(id='total-count-trend-chart')
                    ])
                ])
            ], md=6),
            
            # 平均租金趋势图
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5('平均租金变化趋势')),
                    dbc.CardBody([
                        dcc.Graph(id='avg-price-trend-chart')
                    ])
                ])
            ], md=6)
        ], style={'marginBottom': '20px'}),
        
        dbc.Row([
            # 平均面积趋势图
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5('平均面积变化趋势')),
                    dbc.CardBody([
                        dcc.Graph(id='avg-area-trend-chart')
                    ])
                ])
            ], md=6),
            
            # 平均单价趋势图
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5('平均单价变化趋势')),
                    dbc.CardBody([
                        dcc.Graph(id='price-per-sqm-trend-chart')
                    ])
                ])
            ], md=6)
        ])
    ])
