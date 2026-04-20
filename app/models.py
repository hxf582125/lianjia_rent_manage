# -*- coding: utf-8 -*-
"""
数据模型模块
定义数据库表对应的ORM模型，以及数据访问的工具方法
"""

from sqlalchemy import func, case, and_, not_
from app.extensions import db


class RentHouse(db.Model):
    """
    租房房源数据模型
    对应数据库中的rent_house表
    """
    
    __tablename__ = 'rent_house'
    
    # 主键字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # 房源核心标识字段
    biz_key = db.Column(db.String(255), nullable=False, default='',
                        comment='房源唯一key')
    batch_id = db.Column(db.String(255), nullable=False, default='',
                         comment='批次id')
    
    # 房源基本信息
    title = db.Column(db.String(100), nullable=False, default='',
                      comment='标题')
    community = db.Column(db.String(100), nullable=False, default='',
                          comment='小区')
    desc = db.Column(db.String(100), nullable=False, default='',
                     comment='房源描述')
    
    # 房源属性
    rent_type = db.Column(db.String(50), nullable=False, default='',
                          comment='出租方式')
    area = db.Column(db.String(50), nullable=False, default='',
                     comment='面积')
    orientation = db.Column(db.String(50), nullable=False, default='',
                            comment='朝向')
    floor_detail = db.Column(db.String(50), nullable=False, default='',
                              comment='详细楼层')
    loc_desc = db.Column(db.String(50), nullable=False, default='',
                         comment='位置描述')
    
    # 价格信息
    total_price = db.Column(db.String(50), nullable=False, default='',
                            comment='租金')
    tags = db.Column(db.String(100), nullable=False, default='',
                     comment='标签')
    
    # 地理信息
    district = db.Column(db.String(100), nullable=False, default='',
                         comment='区域')
    detail_district = db.Column(db.String(100), nullable=False, default='',
                                 comment='详情区域')
    bankuai = db.Column(db.String(100), nullable=False, default='',
                        comment='板块')
    
    # 户型信息
    layout = db.Column(db.String(50), nullable=False, default='',
                       comment='户型')
    bedroom = db.Column(db.Integer, nullable=False, default=0,
                        comment='室')
    livingroom = db.Column(db.Integer, nullable=False, default=0,
                           comment='厅')
    
    # 其他属性
    near_subway = db.Column(db.Integer, nullable=False, default=0,
                            comment='近地铁')
    check_in_time = db.Column(db.String(50), nullable=False, default='',
                              comment='入住时间')
    pay_type = db.Column(db.String(50), nullable=False, default='',
                         comment='付款方式')
    service_fee = db.Column(db.String(50), nullable=False, default='',
                            comment='服务费')
    agent_fee = db.Column(db.String(50), nullable=False, default='',
                          comment='中介费')
    deposit = db.Column(db.String(50), nullable=False, default='',
                        comment='押金')
    build_date = db.Column(db.String(50), nullable=False, default='',
                           comment='建成时间')
    build_type = db.Column(db.String(50), nullable=False, default='',
                           comment='建筑类型')
    project_source = db.Column(db.String(50), nullable=False, default='',
                                comment='项目来源')
    
    # 原始数据JSON
    payload_json = db.Column(db.Text, nullable=False, default='',
                             comment='完整数据')
    
    # 时间戳
    saved_at = db.Column(db.DateTime, default=func.current_timestamp(),
                         comment='创建时间')
    updated_at = db.Column(db.DateTime,
                           default=func.current_timestamp(),
                           onupdate=func.current_timestamp(),
                           comment='更新时间')

    def __repr__(self):
        """
        对象字符串表示
        """
        return f'<RentHouse {self.id}: {self.title}>'


class HouseDAO:
    """
    房源数据访问对象(Data Access Object)
    封装所有房源相关的数据库查询操作，提供统一的数据访问接口
    """
    
    @staticmethod
    def get_all_batch_ids():
        """
        获取所有批次ID列表，排除包含_error的错误批次
        
        返回:
            list: 批次ID列表，按创建时间降序排列
        """
        result = db.session.query(
            RentHouse.batch_id,
            func.min(RentHouse.saved_at).label('first_saved_at')
        ).filter(
            # 排除包含_error的批次
            not_(RentHouse.batch_id.like('%_error%'))
        ).group_by(
            RentHouse.batch_id
        ).order_by(
            func.min(RentHouse.saved_at).desc()
        ).all()
        
        return [row.batch_id for row in result]
    
    @staticmethod
    def _build_filter_conditions(batch_id, detail_districts=None, bankuais=None):
        """
        构建筛选条件的辅助方法
        
        参数:
            batch_id: 批次ID
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            list: 筛选条件列表
        """
        conditions = [
            RentHouse.batch_id == batch_id
        ]
        
        # 添加详情区域筛选
        if detail_districts:
            conditions.append(RentHouse.detail_district.in_(detail_districts))
        
        # 添加板块筛选
        if bankuais:
            conditions.append(RentHouse.bankuai.in_(bankuais))
        
        return conditions
    
    @staticmethod
    def get_detail_districts_by_batch(batch_id):
        """
        获取指定批次的所有详情区域列表
        
        参数:
            batch_id: 批次ID
            
        返回:
            list: 详情区域名称列表
        """
        result = db.session.query(
            RentHouse.detail_district
        ).filter(
            RentHouse.batch_id == batch_id,
            RentHouse.detail_district != ''
        ).group_by(
            RentHouse.detail_district
        ).order_by(
            RentHouse.detail_district
        ).all()
        
        return [row.detail_district for row in result]
    
    @staticmethod
    def get_bankuais_by_batch(batch_id):
        """
        获取指定批次的所有板块列表
        
        参数:
            batch_id: 批次ID
            
        返回:
            list: 板块名称列表
        """
        result = db.session.query(
            RentHouse.bankuai
        ).filter(
            RentHouse.batch_id == batch_id,
            RentHouse.bankuai != ''
        ).group_by(
            RentHouse.bankuai
        ).order_by(
            RentHouse.bankuai
        ).all()
        
        return [row.bankuai for row in result]
    
    @staticmethod
    def get_house_count_by_batch(batch_id, detail_districts=None, bankuais=None):
        """
        获取指定批次的房源总数，支持筛选条件
        
        参数:
            batch_id: 批次ID
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            int: 房源数量
        """
        conditions = HouseDAO._build_filter_conditions(batch_id, detail_districts, bankuais)
        
        return db.session.query(func.count(RentHouse.id)).filter(
            *conditions
        ).scalar()
    
    @staticmethod
    def get_distribution_by_dimension(batch_id, dimension, detail_districts=None, bankuais=None):
        """
        按指定维度统计房源数量分布，支持筛选条件
        
        参数:
            batch_id: 批次ID
            dimension: 统计维度，可选值: 'district'(区域), 'bankuai'(板块), 'community'(小区)
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            list: 包含维度名称和房源数量的字典列表
        """
        dimension_map = {
            'district': RentHouse.district,
            'bankuai': RentHouse.bankuai,
            'community': RentHouse.community
        }
        
        dimension_col = dimension_map.get(dimension, RentHouse.district)
        
        # 构建基础条件
        conditions = HouseDAO._build_filter_conditions(batch_id, detail_districts, bankuais)
        conditions.append(dimension_col != '')
        
        result = db.session.query(
            dimension_col.label('name'),
            func.count(RentHouse.id).label('count')
        ).filter(
            *conditions
        ).group_by(
            dimension_col
        ).order_by(
            func.count(RentHouse.id).desc()
        ).all()
        
        return [{'name': row.name, 'count': row.count} for row in result]
    
    @staticmethod
    def parse_area(area_str):
        """
        解析面积字符串为数值
        
        参数:
            area_str: 面积字符串，如 "100㎡", "50-60㎡"
            
        返回:
            float: 面积数值，解析失败返回None
        """
        if not area_str:
            return None
        
        # 移除单位和空格
        area_str = area_str.replace('㎡', '').replace(' ', '')
        
        # 处理范围格式，如 "50-60"，取平均值
        if '-' in area_str:
            try:
                min_area, max_area = area_str.split('-')
                return (float(min_area) + float(max_area)) / 2
            except ValueError:
                return None
        
        # 处理单个数值
        try:
            return float(area_str)
        except ValueError:
            return None
    
    @staticmethod
    def parse_price(price_str):
        """
        解析价格字符串为数值
        
        参数:
            price_str: 价格字符串，如 "5000", "5000元/月"
            
        返回:
            int: 价格数值，解析失败返回None
        """
        if not price_str:
            return None
        
        # 移除非数字字符
        import re
        numbers = re.findall(r'\d+', price_str)
        if numbers:
            return int(numbers[0])
        return None
    
    @staticmethod
    def get_price_distribution(batch_id, bins=None, detail_districts=None, bankuais=None):
        """
        获取租金区间分布，支持筛选条件
        
        参数:
            batch_id: 批次ID
            bins: 价格区间列表，默认使用预设区间
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            list: 包含区间名称和房源数量的字典列表
        """
        if bins is None:
            bins = [0, 2000, 4000, 6000, 8000, 10000, 15000, 20000, float('inf')]
        
        # 构建筛选条件
        conditions = HouseDAO._build_filter_conditions(batch_id, detail_districts, bankuais)
        conditions.append(RentHouse.total_price != '')
        
        # 查询数据
        houses = db.session.query(RentHouse.total_price).filter(
            *conditions
        ).all()
        
        distribution = {}
        for i in range(len(bins) - 1):
            lower = bins[i]
            upper = bins[i + 1]
            if upper == float('inf'):
                label = f'{lower}+'
            else:
                label = f'{lower}-{upper}'
            distribution[label] = 0
        
        for house in houses:
            price = HouseDAO.parse_price(house.total_price)
            if price is not None:
                for i in range(len(bins) - 1):
                    if bins[i] <= price < bins[i + 1]:
                        if bins[i + 1] == float('inf'):
                            label = f'{bins[i]}+'
                        else:
                            label = f'{bins[i]}-{bins[i + 1]}'
                        distribution[label] += 1
                        break
        
        return [{'name': k, 'count': v} for k, v in distribution.items()]
    
    @staticmethod
    def get_area_distribution(batch_id, bins=None, detail_districts=None, bankuais=None):
        """
        获取面积区间分布，支持筛选条件
        
        参数:
            batch_id: 批次ID
            bins: 面积区间列表，默认使用预设区间
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            list: 包含区间名称和房源数量的字典列表
        """
        if bins is None:
            bins = [0, 30, 50, 70, 90, 120, 150, 200, float('inf')]
        
        # 构建筛选条件
        conditions = HouseDAO._build_filter_conditions(batch_id, detail_districts, bankuais)
        conditions.append(RentHouse.area != '')
        
        # 查询数据
        houses = db.session.query(RentHouse.area).filter(
            *conditions
        ).all()
        
        distribution = {}
        for i in range(len(bins) - 1):
            lower = bins[i]
            upper = bins[i + 1]
            if upper == float('inf'):
                label = f'{lower}+'
            else:
                label = f'{lower}-{upper}'
            distribution[label] = 0
        
        for house in houses:
            area = HouseDAO.parse_area(house.area)
            if area is not None:
                for i in range(len(bins) - 1):
                    if bins[i] <= area < bins[i + 1]:
                        if bins[i + 1] == float('inf'):
                            label = f'{bins[i]}+'
                        else:
                            label = f'{bins[i]}-{bins[i + 1]}'
                        distribution[label] += 1
                        break
        
        return [{'name': k, 'count': v} for k, v in distribution.items()]
    
    @staticmethod
    def get_batch_stats(batch_ids, detail_districts=None, bankuais=None):
        """
        获取多个批次的统计数据，用于多批次对比，支持筛选条件
        
        参数:
            batch_ids: 批次ID列表
            detail_districts: 详情区域筛选列表（多选）
            bankuais: 板块筛选列表（多选）
            
        返回:
            dict: 包含各批次统计数据的字典
        """
        result = {}
        
        for batch_id in batch_ids:
            # 获取基础统计
            total_count = HouseDAO.get_house_count_by_batch(
                batch_id, detail_districts, bankuais
            )
            
            # 构建筛选条件
            conditions = HouseDAO._build_filter_conditions(
                batch_id, detail_districts, bankuais
            )
            conditions.append(RentHouse.total_price != '')
            conditions.append(RentHouse.area != '')
            
            # 获取价格数据
            houses = db.session.query(
                RentHouse.total_price,
                RentHouse.area
            ).filter(
                *conditions
            ).all()
            
            prices = []
            areas = []
            for house in houses:
                price = HouseDAO.parse_price(house.total_price)
                area = HouseDAO.parse_area(house.area)
                if price is not None:
                    prices.append(price)
                if area is not None:
                    areas.append(area)
            
            avg_price = round(sum(prices) / len(prices), 2) if prices else 0
            avg_area = round(sum(areas) / len(areas), 2) if areas else 0
            
            result[batch_id] = {
                'total_count': total_count,
                'avg_price': avg_price,
                'avg_area': avg_area,
                'price_per_sqm': round(avg_price / avg_area, 2) if avg_area > 0 else 0
            }
        
        return result
