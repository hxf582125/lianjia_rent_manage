# -*- coding: utf-8 -*-
"""
Dash回调函数模块
定义所有Dash应用的交互回调函数，包括：
1. 标签页切换回调
2. 批次选择后动态加载筛选选项回调
3. 单批次分析图表更新回调（支持筛选条件）
4. 多批次对比图表更新回调（支持筛选条件）
"""

from dash import Input, Output, State, callback
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

from app.dash_app.layout import create_single_batch_layout, create_multi_batch_layout, format_batch_id
from app.dash_app.charts import create_bar_chart, create_line_chart
from app.models import HouseDAO


def register_callbacks(dash_app):
    """
    注册所有Dash回调函数
    
    参数:
        dash_app: Dash应用实例
    """
    
    @dash_app.callback(
        Output('tabs-content', 'children'),
        [Input('main-tabs', 'active_tab')],
        [State('batch-options-store', 'data')]
    )
    def render_tab_content(active_tab, batch_options):
        """
        根据选中的标签页渲染对应内容
        
        参数:
            active_tab: 当前激活的标签页ID
            batch_options: 从Store获取的批次选项数据
            
        返回:
            对应标签页的布局组件
        """
        if active_tab == 'single-batch-tab':
            return create_single_batch_layout(batch_options)
        elif active_tab == 'multi-batch-tab':
            return create_multi_batch_layout(batch_options)
        return html.Div('请选择一个标签页')
    
    # ============================================
    # 单批次分析 - 动态加载筛选选项回调
    # ============================================
    
    @dash_app.callback(
        [Output('single-detail-district-selector', 'options'),
         Output('single-detail-district-selector', 'value'),
         Output('single-bankuai-selector', 'options'),
         Output('single-bankuai-selector', 'value')],
        [Input('single-batch-selector', 'value')],
        prevent_initial_call=True
    )
    def update_single_filters(selected_batch):
        """
        当选择批次后，动态加载该批次的详情区域和板块选项
        
        参数:
            selected_batch: 选中的批次ID
            
        返回:
            tuple: (详情区域选项, 详情区域默认值, 板块选项, 板块默认值)
        """
        if not selected_batch:
            # 如果没有选择批次，清空筛选选项
            return [], None, [], None
        
        # 获取该批次的所有详情区域
        detail_districts = HouseDAO.get_detail_districts_by_batch(selected_batch)
        detail_district_options = [
            {'label': dd, 'value': dd}
            for dd in detail_districts
        ]
        
        # 获取该批次的所有板块
        bankuais = HouseDAO.get_bankuais_by_batch(selected_batch)
        bankuai_options = [
            {'label': bk, 'value': bk}
            for bk in bankuais
        ]
        
        # 返回选项，默认值为None（不选择任何筛选）
        return detail_district_options, None, bankuai_options, None
    
    # ============================================
    # 单批次分析图表更新回调
    # ============================================
    
    @dash_app.callback(
        [Output('count-distribution-chart', 'figure'),
         Output('price-distribution-chart', 'figure'),
         Output('area-distribution-chart', 'figure')],
        [Input('single-batch-selector', 'value'),
         Input('dimension-selector', 'value'),
         Input('single-detail-district-selector', 'value'),
         Input('single-bankuai-selector', 'value')],
        prevent_initial_call=False
    )
    def update_single_batch_charts(selected_batch, dimension, detail_districts, bankuais):
        """
        更新单批次分析的所有图表，支持筛选条件
        
        参数:
            selected_batch: 选中的批次ID（原始值）
            dimension: 分析维度（district/bankuai/community）
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            三个图表对象的元组：(数量分布图, 租金分布图, 面积分布图)
        """
        if not selected_batch:
            # 如果没有选择批次，返回空图表
            empty_fig = go.Figure()
            empty_fig.update_layout(
                annotations=[{
                    'text': '请选择一个批次',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20}
                }],
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            return empty_fig, empty_fig, empty_fig
        
        # 1. 获取房源数量分布数据（支持筛选）
        count_data = HouseDAO.get_distribution_by_dimension(
            selected_batch, dimension, detail_districts, bankuais
        )
        
        # 2. 获取租金区间分布数据（支持筛选）
        price_data = HouseDAO.get_price_distribution(
            selected_batch, None, detail_districts, bankuais
        )
        
        # 3. 获取面积区间分布数据（支持筛选）
        area_data = HouseDAO.get_area_distribution(
            selected_batch, None, detail_districts, bankuais
        )
        
        # 维度名称映射
        dimension_names = {
            'district': '区域',
            'bankuai': '板块',
            'community': '小区'
        }
        dim_name = dimension_names.get(dimension, '维度')
        
        # 获取格式化后的批次显示文本
        formatted_batch = format_batch_id(selected_batch)
        
        # 构建筛选说明文本
        filter_desc = []
        if detail_districts:
            filter_desc.append(f'区域: {", ".join(detail_districts[:3])}{"..." if len(detail_districts) > 3 else ""}')
        if bankuais:
            filter_desc.append(f'板块: {", ".join(bankuais[:3])}{"..." if len(bankuais) > 3 else ""}')
        filter_suffix = f'（筛选: {"; ".join(filter_desc)}）' if filter_desc else ''
        
        # 4. 创建柱状图
        # 房源数量分布图（小区维度只显示前20个，避免图表拥挤）
        top_n = 20 if dimension == 'community' else None
        count_fig = create_bar_chart(
            count_data,
            title=f'{dim_name}维度房源数量分布（批次：{formatted_batch}）{filter_suffix}',
            x_label=dim_name,
            y_label='房源数量',
            top_n=top_n
        )
        
        # 租金区间分布图
        price_fig = create_bar_chart(
            price_data,
            title=f'租金区间分布（批次：{formatted_batch}）{filter_suffix}',
            x_label='租金区间（元/月）',
            y_label='房源数量'
        )
        
        # 面积区间分布图
        area_fig = create_bar_chart(
            area_data,
            title=f'面积区间分布（批次：{formatted_batch}）{filter_suffix}',
            x_label='面积区间（㎡）',
            y_label='房源数量'
        )
        
        return count_fig, price_fig, area_fig
    
    # ============================================
    # 多批次对比 - 动态加载筛选选项回调
    # ============================================
    
    @dash_app.callback(
        [Output('multi-detail-district-selector', 'options'),
         Output('multi-detail-district-selector', 'value'),
         Output('multi-bankuai-selector', 'options'),
         Output('multi-bankuai-selector', 'value')],
        [Input('multi-batch-selector', 'value')],
        prevent_initial_call=True
    )
    def update_multi_filters(selected_batches):
        """
        当选择多批次后，动态加载这些批次的详情区域和板块选项（取并集）
        
        参数:
            selected_batches: 选中的批次ID列表
            
        返回:
            tuple: (详情区域选项, 详情区域默认值, 板块选项, 板块默认值)
        """
        if not selected_batches or len(selected_batches) == 0:
            # 如果没有选择批次，清空筛选选项
            return [], None, [], None
        
        # 获取所有选中批次的详情区域并集
        all_detail_districts = set()
        all_bankuais = set()
        
        for batch_id in selected_batches:
            detail_districts = HouseDAO.get_detail_districts_by_batch(batch_id)
            bankuais = HouseDAO.get_bankuais_by_batch(batch_id)
            all_detail_districts.update(detail_districts)
            all_bankuais.update(bankuais)
        
        # 转换为排序后的列表
        detail_district_options = [
            {'label': dd, 'value': dd}
            for dd in sorted(all_detail_districts)
        ]
        
        bankuai_options = [
            {'label': bk, 'value': bk}
            for bk in sorted(all_bankuais)
        ]
        
        # 返回选项，默认值为None（不选择任何筛选）
        return detail_district_options, None, bankuai_options, None
    
    # ============================================
    # 多批次对比图表更新回调
    # ============================================
    
    @dash_app.callback(
        [Output('total-count-trend-chart', 'figure'),
         Output('avg-price-trend-chart', 'figure'),
         Output('avg-area-trend-chart', 'figure'),
         Output('price-per-sqm-trend-chart', 'figure')],
        [Input('multi-batch-selector', 'value'),
         Input('multi-detail-district-selector', 'value'),
         Input('multi-bankuai-selector', 'value')],
        prevent_initial_call=False
    )
    def update_multi_batch_charts(selected_batches, detail_districts, bankuais):
        """
        更新多批次对比的所有趋势图，支持筛选条件
        
        参数:
            selected_batches: 选中的批次ID列表（原始值）
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            四个趋势图对象的元组：(房源总数趋势, 平均租金趋势, 平均面积趋势, 平均单价趋势)
        """
        if not selected_batches or len(selected_batches) < 1:
            # 如果没有选择批次或选择少于1个，返回空图表
            empty_fig = go.Figure()
            empty_fig.update_layout(
                annotations=[{
                    'text': '请选择至少1个批次',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 20}
                }],
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            return empty_fig, empty_fig, empty_fig, empty_fig
        
        # 获取各批次的统计数据（支持筛选）
        batch_stats = HouseDAO.get_batch_stats(
            selected_batches, detail_districts, bankuais
        )
        
        # 按照用户选择的顺序重新排序数据
        # 并将key替换为格式化后的批次显示文本
        ordered_stats = {}
        for batch_id in selected_batches:
            formatted_id = format_batch_id(batch_id)
            ordered_stats[formatted_id] = batch_stats.get(batch_id, {})
        
        # 构建筛选说明文本
        filter_desc = []
        if detail_districts:
            filter_desc.append(f'区域: {", ".join(detail_districts[:2])}{"..." if len(detail_districts) > 2 else ""}')
        if bankuais:
            filter_desc.append(f'板块: {", ".join(bankuais[:2])}{"..." if len(bankuais) > 2 else ""}')
        filter_suffix = f'（筛选: {"; ".join(filter_desc)}）' if filter_desc else ''
        
        # 创建各指标的趋势图
        # 1. 房源总数趋势图
        total_count_fig = create_line_chart(
            ordered_stats,
            title=f'房源总数变化趋势{filter_suffix}',
            x_label='批次时间',
            y_label='房源数量',
            metric_key='total_count'
        )
        
        # 2. 平均租金趋势图
        avg_price_fig = create_line_chart(
            ordered_stats,
            title=f'平均租金变化趋势{filter_suffix}',
            x_label='批次时间',
            y_label='平均租金（元/月）',
            metric_key='avg_price'
        )
        
        # 3. 平均面积趋势图
        avg_area_fig = create_line_chart(
            ordered_stats,
            title=f'平均面积变化趋势{filter_suffix}',
            x_label='批次时间',
            y_label='平均面积（㎡）',
            metric_key='avg_area'
        )
        
        # 4. 平均单价趋势图
        price_per_sqm_fig = create_line_chart(
            ordered_stats,
            title=f'平均单价变化趋势{filter_suffix}',
            x_label='批次时间',
            y_label='平均单价（元/㎡/月）',
            metric_key='price_per_sqm'
        )
        
        return total_count_fig, avg_price_fig, avg_area_fig, price_per_sqm_fig
