# -*- coding: utf-8 -*-
"""
Dash应用布局模块
定义Dash应用的页面布局结构，包括：
1. 批次选择组件（支持单选/多选）
2. 详情区域和板块多选筛选
3. 单批次分析标签页（柱状图展示）
4. 多批次对比标签页（连线图展示）
"""

import re
from dash import dcc, html
import dash_bootstrap_components as dbc


# 定义配色方案
COLORS = {
    'primary': '#1890ff',
    'secondary': '#6c757d',
    'success': '#52c41a',
    'warning': '#faad14',
    'danger': '#ff4d4f',
    'info': '#13c2c2',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'bg_primary': '#f0f5ff',
    'bg_secondary': '#fafafa',
    'text_primary': '#262626',
    'text_secondary': '#8c8c8c',
    'border': '#e8e8e8'
}


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


def create_card_header(title, icon=None):
    """
    创建美化的卡片头部
    
    参数:
        title: 标题文本
        icon: 可选的图标
        
    返回:
        dbc.CardHeader: 美化的卡片头部
    """
    return dbc.CardHeader(
        html.Div([
            html.H5(
                title,
                style={
                    'margin': '0',
                    'color': COLORS['text_primary'],
                    'fontWeight': '600'
                }
            )
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'gap': '8px'
        }),
        style={
            'backgroundColor': COLORS['bg_primary'],
            'borderBottom': f'1px solid {COLORS["border"]}',
            'padding': '12px 20px'
        }
    )


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
    
    return html.Div([
        # 页面标题区域
        html.Div([
            html.H1(
                '链家租房数据分析系统',
                style={
                    'textAlign': 'center',
                    'color': '#fff',
                    'margin': '0',
                    'fontSize': '28px',
                    'fontWeight': '600'
                }
            ),
            html.P(
                '多维度房源数据分析与趋势对比平台',
                style={
                    'textAlign': 'center',
                    'color': 'rgba(255, 255, 255, 0.8)',
                    'margin': '8px 0 0 0',
                    'fontSize': '14px'
                }
            )
        ], style={
            'background': f'linear-gradient(135deg, {COLORS["primary"]} 0%, #40a9ff 100%)',
            'padding': '30px 20px',
            'margin': '-20px -20px 30px -20px',
            'boxShadow': '0 4px 12px rgba(24, 144, 255, 0.3)'
        }),
        
        # 标签页区域
        dbc.Tabs([
            # 单批次分析标签页
            dbc.Tab(
                label='单批次分析',
                tab_id='single-batch-tab',
                label_style={
                    'fontWeight': '500',
                    'fontSize': '15px'
                }
            ),
            # 多批次对比标签页
            dbc.Tab(
                label='多批次对比',
                tab_id='multi-batch-tab',
                label_style={
                    'fontWeight': '500',
                    'fontSize': '15px'
                }
            )
        ], id='main-tabs', active_tab='single-batch-tab', style={
            'marginBottom': '24px',
            'borderBottom': f'2px solid {COLORS["border"]}'
        }),
        
        # 标签页内容区域
        html.Div(id='tabs-content'),
        
        # 隐藏的存储组件，用于缓存数据
        dcc.Store(id='batch-options-store', data=batch_options),
        dcc.Store(id='batch-ids-store', data=batch_ids),
        
        # 页面底部信息
        html.Footer(
            [
                html.Hr(style={
                    'borderColor': COLORS['border'],
                    'marginTop': '40px',
                    'marginBottom': '20px'
                }),
                html.P(
                    '链家租房数据分析系统 © 2026 | Powered by Flask + Dash + Plotly',
                    style={
                        'textAlign': 'center',
                        'color': COLORS['text_secondary'],
                        'fontSize': '13px',
                        'margin': '0'
                    }
                )
            ]
        )
    ], style={
        'padding': '0 20px',
        'minHeight': '100vh',
        'backgroundColor': COLORS['bg_secondary']
    })


def create_single_batch_layout(batch_options):
    """
    创建单批次分析页面的布局
    
    参数:
        batch_options: 批次选项列表，格式为 [{'label': '显示文本', 'value': '批次ID'}, ...]
        
    返回:
        html.Div: 单批次分析页面布局
    """
    return html.Div([
        # 左侧筛选面板 + 右侧图表区域
        dbc.Row([
            # 左侧：筛选面板
            dbc.Col([
                # 批次选择卡片
                dbc.Card([
                    create_card_header('批次选择'),
                    dbc.CardBody([
                        html.Label(
                            '请选择要分析的批次：',
                            style={
                                'fontWeight': '500',
                                'color': COLORS['text_primary'],
                                'marginBottom': '8px'
                            }
                        ),
                        dcc.Dropdown(
                            id='single-batch-selector',
                            options=batch_options,
                            value=None,
                            placeholder='请选择一个批次',
                            style={
                                'width': '100%'
                            },
                            className='custom-dropdown'
                        )
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '16px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 筛选条件卡片
                dbc.Card([
                    create_card_header('筛选条件'),
                    dbc.CardBody([
                        # 详情区域筛选
                        html.Div([
                            html.Label(
                                '详情区域（可多选）：',
                                style={
                                    'fontWeight': '500',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '8px',
                                    'display': 'block'
                                }
                            ),
                            dcc.Dropdown(
                                id='single-detail-district-selector',
                                options=[],
                                value=None,
                                multi=True,
                                placeholder='不选择则显示全部',
                                style={
                                    'width': '100%'
                                }
                            ),
                            html.Small(
                                '选择后将仅统计该区域的房源数据',
                                style={
                                    'color': COLORS['text_secondary'],
                                    'fontSize': '12px',
                                    'marginTop': '4px',
                                    'display': 'block'
                                }
                            )
                        ], style={
                            'marginBottom': '20px'
                        }),
                        
                        # 板块筛选
                        html.Div([
                            html.Label(
                                '板块（可多选）：',
                                style={
                                    'fontWeight': '500',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '8px',
                                    'display': 'block'
                                }
                            ),
                            dcc.Dropdown(
                                id='single-bankuai-selector',
                                options=[],
                                value=None,
                                multi=True,
                                placeholder='不选择则显示全部',
                                style={
                                    'width': '100%'
                                }
                            ),
                            html.Small(
                                '选择后将仅统计该板块的房源数据',
                                style={
                                    'color': COLORS['text_secondary'],
                                    'fontSize': '12px',
                                    'marginTop': '4px',
                                    'display': 'block'
                                }
                            )
                        ])
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '16px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 分析维度选择卡片
                dbc.Card([
                    create_card_header('分析维度'),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='dimension-selector',
                            options=[
                                {'label': '区域维度', 'value': 'district'},
                                {'label': '板块维度', 'value': 'bankuai'},
                                {'label': '小区维度', 'value': 'community'}
                            ],
                            value='district',
                            labelStyle={
                                'display': 'block',
                                'marginBottom': '12px',
                                'padding': '10px 15px',
                                'backgroundColor': COLORS['light'],
                                'borderRadius': '6px',
                                'border': f'1px solid {COLORS["border"]}',
                                'cursor': 'pointer'
                            },
                            inputStyle={
                                'marginRight': '10px',
                                'transform': 'scale(1.2)'
                            },
                            className='custom-radioitems'
                        )
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                })
            ], md=3, style={
                'paddingRight': '12px'
            }),
            
            # 右侧：图表区域
            dbc.Col([
                # 房源数量分布柱状图
                dbc.Card([
                    create_card_header('房源数量分布'),
                    dbc.CardBody([
                        dcc.Graph(id='count-distribution-chart', style={'height': '350px'})
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '20px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 租金区间分布柱状图
                dbc.Card([
                    create_card_header('租金区间分布'),
                    dbc.CardBody([
                        dcc.Graph(id='price-distribution-chart', style={'height': '350px'})
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '20px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 面积区间分布柱状图
                dbc.Card([
                    create_card_header('面积区间分布'),
                    dbc.CardBody([
                        dcc.Graph(id='area-distribution-chart', style={'height': '350px'})
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                })
            ], md=9, style={
                'paddingLeft': '12px'
            })
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
        # 左侧筛选面板 + 右侧图表区域
        dbc.Row([
            # 左侧：筛选面板
            dbc.Col([
                # 批次选择卡片
                dbc.Card([
                    create_card_header('批次选择'),
                    dbc.CardBody([
                        html.Label(
                            '请选择要对比的批次（可多选）：',
                            style={
                                'fontWeight': '500',
                                'color': COLORS['text_primary'],
                                'marginBottom': '8px'
                            }
                        ),
                        dcc.Dropdown(
                            id='multi-batch-selector',
                            options=batch_options,
                            value=None,
                            multi=True,
                            placeholder='请选择多个批次',
                            style={
                                'width': '100%'
                            }
                        ),
                        html.Small(
                            '建议选择2个及以上批次进行对比分析',
                            style={
                                'color': COLORS['text_secondary'],
                                'fontSize': '12px',
                                'marginTop': '4px',
                                'display': 'block'
                            }
                        )
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '16px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 筛选条件卡片
                dbc.Card([
                    create_card_header('筛选条件'),
                    dbc.CardBody([
                        # 详情区域筛选
                        html.Div([
                            html.Label(
                                '详情区域（可多选）：',
                                style={
                                    'fontWeight': '500',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '8px',
                                    'display': 'block'
                                }
                            ),
                            dcc.Dropdown(
                                id='multi-detail-district-selector',
                                options=[],
                                value=None,
                                multi=True,
                                placeholder='不选择则显示全部',
                                style={
                                    'width': '100%'
                                }
                            )
                        ], style={
                            'marginBottom': '20px'
                        }),
                        
                        # 板块筛选
                        html.Div([
                            html.Label(
                                '板块（可多选）：',
                                style={
                                    'fontWeight': '500',
                                    'color': COLORS['text_primary'],
                                    'marginBottom': '8px',
                                    'display': 'block'
                                }
                            ),
                            dcc.Dropdown(
                                id='multi-bankuai-selector',
                                options=[],
                                value=None,
                                multi=True,
                                placeholder='不选择则显示全部',
                                style={
                                    'width': '100%'
                                }
                            )
                        ])
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'marginBottom': '16px',
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                }),
                
                # 指标选择卡片
                dbc.Card([
                    create_card_header('对比指标'),
                    dbc.CardBody([
                        dcc.Checklist(
                            id='metric-selector',
                            options=[
                                {'label': '房源总数', 'value': 'total_count'},
                                {'label': '平均租金', 'value': 'avg_price'},
                                {'label': '平均面积', 'value': 'avg_area'},
                                {'label': '平均单价', 'value': 'price_per_sqm'}
                            ],
                            value=['total_count', 'avg_price'],
                            labelStyle={
                                'display': 'block',
                                'marginBottom': '12px',
                                'padding': '10px 15px',
                                'backgroundColor': COLORS['light'],
                                'borderRadius': '6px',
                                'border': f'1px solid {COLORS["border"]}',
                                'cursor': 'pointer'
                            },
                            inputStyle={
                                'marginRight': '10px',
                                'transform': 'scale(1.2)'
                            }
                        )
                    ], style={
                        'padding': '16px 20px'
                    })
                ], style={
                    'border': f'1px solid {COLORS["border"]}',
                    'borderRadius': '8px',
                    'overflow': 'hidden',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                })
            ], md=3, style={
                'paddingRight': '12px'
            }),
            
            # 右侧：图表区域
            dbc.Col([
                # 第一行图表
                dbc.Row([
                    # 房源总数趋势图
                    dbc.Col([
                        dbc.Card([
                            create_card_header('房源总数变化趋势'),
                            dbc.CardBody([
                                dcc.Graph(id='total-count-trend-chart', style={'height': '300px'})
                            ], style={
                                'padding': '16px 20px'
                            })
                        ], style={
                            'height': '100%',
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '8px',
                            'overflow': 'hidden',
                            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                        })
                    ], md=6),
                    
                    # 平均租金趋势图
                    dbc.Col([
                        dbc.Card([
                            create_card_header('平均租金变化趋势'),
                            dbc.CardBody([
                                dcc.Graph(id='avg-price-trend-chart', style={'height': '300px'})
                            ], style={
                                'padding': '16px 20px'
                            })
                        ], style={
                            'height': '100%',
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '8px',
                            'overflow': 'hidden',
                            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                        })
                    ], md=6)
                ], style={
                    'marginBottom': '20px'
                }),
                
                # 第二行图表
                dbc.Row([
                    # 平均面积趋势图
                    dbc.Col([
                        dbc.Card([
                            create_card_header('平均面积变化趋势'),
                            dbc.CardBody([
                                dcc.Graph(id='avg-area-trend-chart', style={'height': '300px'})
                            ], style={
                                'padding': '16px 20px'
                            })
                        ], style={
                            'height': '100%',
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '8px',
                            'overflow': 'hidden',
                            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                        })
                    ], md=6),
                    
                    # 平均单价趋势图
                    dbc.Col([
                        dbc.Card([
                            create_card_header('平均单价变化趋势'),
                            dbc.CardBody([
                                dcc.Graph(id='price-per-sqm-trend-chart', style={'height': '300px'})
                            ], style={
                                'padding': '16px 20px'
                            })
                        ], style={
                            'height': '100%',
                            'border': f'1px solid {COLORS["border"]}',
                            'borderRadius': '8px',
                            'overflow': 'hidden',
                            'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.06)'
                        })
                    ], md=6)
                ])
            ], md=9, style={
                'paddingLeft': '12px'
            })
        ])
    ])
