# -*- coding: utf-8 -*-
"""
图表生成模块
使用Plotly库生成各种数据可视化图表，包括：
1. 柱状图（用于单批次分析）
2. 连线图（用于多批次对比趋势）
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_bar_chart(data, title, x_label, y_label, top_n=None):
    """
    创建柱状图
    
    参数:
        data: 数据列表，每个元素为字典，包含'name'和'count'键
            例如: [{'name': '朝阳区', 'count': 100}, {'name': '海淀区', 'count': 80}]
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
        top_n: 显示前N条数据，None表示显示所有
        
    返回:
        plotly.graph_objects.Figure: 柱状图对象
    """
    if not data:
        # 如果没有数据，返回空图表
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            annotations=[{
                'text': '暂无数据',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig
    
    # 按数量降序排序
    sorted_data = sorted(data, key=lambda x: x['count'], reverse=True)
    
    # 如果指定了top_n，只取前N条
    if top_n and top_n > 0:
        sorted_data = sorted_data[:top_n]
    
    # 提取X轴和Y轴数据
    x_values = [item['name'] for item in sorted_data]
    y_values = [item['count'] for item in sorted_data]
    
    # 创建柱状图
    fig = go.Figure(data=[
        go.Bar(
            x=x_values,
            y=y_values,
            text=y_values,
            textposition='auto',
            marker_color='rgb(55, 83, 109)',
            hovertemplate='<b>%{x}</b><br>' +
                         '数量: %{y}<extra></extra>'
        )
    ])
    
    # 更新图表布局
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis={
            'tickangle': -45 if len(x_values) > 5 else 0,
            'automargin': True
        },
        yaxis={
            'gridcolor': 'rgba(0, 0, 0, 0.1)'
        },
        plot_bgcolor='white',
        height=500,
        margin={'l': 50, 'r': 50, 't': 80, 'b': 150 if len(x_values) > 5 else 80}
    )
    
    return fig


def create_line_chart(data_dict, title, x_label, y_label, metric_key):
    """
    创建连线图（趋势图）
    
    参数:
        data_dict: 数据字典，键为批次ID，值为包含各指标的字典
            例如: {'batch_1': {'total_count': 100, 'avg_price': 5000}, 
                   'batch_2': {'total_count': 120, 'avg_price': 5500}}
        title: 图表标题
        x_label: X轴标签
        y_label: Y轴标签
        metric_key: 要显示的指标键名
        
    返回:
        plotly.graph_objects.Figure: 连线图对象
    """
    if not data_dict:
        # 如果没有数据，返回空图表
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            annotations=[{
                'text': '暂无数据',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig
    
    # 提取批次ID和对应指标值
    # 保持批次的原始顺序
    batch_ids = list(data_dict.keys())
    values = [data_dict[batch_id].get(metric_key, 0) for batch_id in batch_ids]
    
    # 创建连线图
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=batch_ids,
        y=values,
        mode='lines+markers+text',
        name=metric_key,
        line=dict(
            color='rgb(55, 83, 109)',
            width=3
        ),
        marker=dict(
            size=10,
            color='rgb(55, 83, 109)',
            line=dict(
                width=2,
                color='white'
            )
        ),
        text=[f'{v}' for v in values],
        textposition='top center',
        hovertemplate='<b>批次: %{x}</b><br>' +
                     f'{y_label}: ' + '%{y}<extra></extra>'
    ))
    
    # 更新图表布局
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        yaxis_title=y_label,
        xaxis={
            'tickangle': -45,
            'automargin': True
        },
        yaxis={
            'gridcolor': 'rgba(0, 0, 0, 0.1)',
            'zeroline': True,
            'zerolinecolor': 'rgba(0, 0, 0, 0.2)'
        },
        plot_bgcolor='white',
        height=450,
        margin={'l': 50, 'r': 50, 't': 80, 'b': 120}
    )
    
    return fig


def create_multi_line_chart(data_dict, title, x_label, y_labels, metric_keys):
    """
    创建多线条连线图（用于同时展示多个指标）
    
    参数:
        data_dict: 数据字典，键为批次ID，值为包含各指标的字典
        title: 图表标题
        x_label: X轴标签
        y_labels: Y轴标签列表，与metric_keys一一对应
        metric_keys: 要显示的指标键名列表
        
    返回:
        plotly.graph_objects.Figure: 多线条连线图对象
    """
    if not data_dict or not metric_keys:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            annotations=[{
                'text': '暂无数据',
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 20}
            }]
        )
        return fig
    
    batch_ids = list(data_dict.keys())
    colors = [
        'rgb(55, 83, 109)',
        'rgb(26, 118, 255)',
        'rgb(127, 127, 127)',
        'rgb(255, 140, 0)'
    ]
    
    fig = go.Figure()
    
    for i, (metric_key, y_label) in enumerate(zip(metric_keys, y_labels)):
        values = [data_dict[batch_id].get(metric_key, 0) for batch_id in batch_ids]
        
        fig.add_trace(go.Scatter(
            x=batch_ids,
            y=values,
            mode='lines+markers+text',
            name=y_label,
            line=dict(
                color=colors[i % len(colors)],
                width=3
            ),
            marker=dict(
                size=8,
                color=colors[i % len(colors)],
                line=dict(
                    width=2,
                    color='white'
                )
            ),
            text=[f'{v}' for v in values],
            textposition='top center',
            hovertemplate='<b>批次: %{x}</b><br>' +
                         f'{y_label}: ' + '%{y}<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=x_label,
        xaxis={
            'tickangle': -45,
            'automargin': True
        },
        yaxis={
            'gridcolor': 'rgba(0, 0, 0, 0.1)',
            'zeroline': True,
            'zerolinecolor': 'rgba(0, 0, 0, 0.2)'
        },
        plot_bgcolor='white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        height=450,
        margin={'l': 50, 'r': 50, 't': 100, 'b': 120}
    )
    
    return fig
