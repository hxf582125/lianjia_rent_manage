# 链家租房数据分析系统

一个基于 Flask、Dash 和 SQLAlchemy 构建的租房数据可视化分析平台，支持单批次多维度分析和多批次趋势对比。

## 项目特性

### 📊 核心功能

1. **批次选择**
   - 支持单选批次 ID（用于单批次分析）
   - 支持多选批次 ID（用于多批次对比）
   - 批次列表按创建时间降序排列

2. **单批次分析**
   - **多维度统计**：支持区域、板块、小区三个维度
   - **房源数量分布**：柱状图展示各维度房源数量排名
   - **租金区间分布**：柱状图展示不同租金区间的房源数量
   - **面积区间分布**：柱状图展示不同面积区间的房源数量
   - **智能数据处理**：自动解析租金和面积字符串，计算区间分布

3. **多批次对比**
   - **趋势分析**：使用连线图展示各批次指标变化趋势
   - **多指标对比**：
     - 房源总数变化趋势
     - 平均租金变化趋势（元/月）
     - 平均面积变化趋势（㎡）
     - 平均单价变化趋势（元/㎡/月）

### 🏗️ 技术架构

- **后端框架**：Flask 3.1.3
- **前端可视化**：Dash 4.1.0 + Plotly 6.7.0
- **ORM 框架**：Flask-SQLAlchemy 3.1.1 + SQLAlchemy 2.0.49
- **数据库**：MySQL 8.0+
- **UI 组件**：feffery-antd-components + Dash Bootstrap Components
- **配置管理**：python-dotenv

## 项目结构

```
lianjia_rent_manage/
├── app/                          # 应用核心包
│   ├── __init__.py              # 包初始化文件
│   ├── config.py                # 配置模块
│   ├── extensions.py            # Flask扩展初始化
│   ├── factory.py               # Flask应用工厂
│   ├── models.py                # 数据模型和数据访问对象
│   └── dash_app/                # Dash应用子包
│       ├── __init__.py          # 包初始化文件
│       ├── app.py               # Dash应用初始化
│       ├── layout.py            # 页面布局定义
│       ├── charts.py            # 图表生成模块
│       └── callbacks.py         # 交互回调函数
├── data/                         # 数据文件目录
│   ├── houses.sql               # 房源数据SQL
│   └── rent_house.sql           # 表结构定义
├── .env                         # 环境变量配置
├── run.py                       # 应用启动入口
├── requirements.txt             # Python依赖列表
└── README.md                    # 项目说明文档
```

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- Conda 或 venv（推荐使用项目指定的虚拟环境）

### 安装步骤

1. **激活虚拟环境**

使用项目指定的 `flask_dash` 虚拟环境：

```bash
# Windows
C:\Users\Administrator\miniconda3\envs\flask_dash\python.exe -m pip install -r requirements.txt
```

或手动激活环境：

```bash
# 使用 conda 激活
conda activate flask_dash

# 安装依赖
pip install -r requirements.txt
```

2. **配置数据库**

首先在 MySQL 中创建数据库：

```sql
CREATE DATABASE lianjia_rent CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
```

然后导入表结构和数据：

```bash
# 导入表结构
mysql -u root -p lianjia_rent < data/rent_house.sql

# 导入数据（如果有）
mysql -u root -p lianjia_rent < data/houses.sql
```

3. **配置环境变量**

编辑 `.env` 文件，根据实际情况修改数据库连接信息：

```env
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=lianjia_rent
MYSQL_CHARSET=utf8mb4

# Flask应用配置
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=True
FLASK_PORT=5000
```

4. **启动应用**

```bash
# 使用指定的Python解释器
C:\Users\Administrator\miniconda3\envs\flask_dash\python.exe run.py

# 或激活环境后直接运行
python run.py
```

应用启动后，访问：
- 首页：http://localhost:5000
- Dash 应用：http://localhost:5000/dash/

## 核心模块说明

### 1. 配置模块 (`app/config.py`)

- 支持开发环境和生产环境配置切换
- 使用 `.env` 文件管理敏感信息
- 提供统一的配置访问接口

```python
from app.config import get_config

# 获取配置类
config = get_config('development')
```

### 2. 数据模型 (`app/models.py`)

- **RentHouse 模型**：ORM 映射 `rent_house` 表
- **HouseDAO 类**：数据访问对象，封装所有数据库查询

核心方法：
- `get_all_batch_ids()`：获取所有批次 ID
- `get_distribution_by_dimension()`：按维度统计房源数量
- `get_price_distribution()`：获取租金区间分布
- `get_area_distribution()`：获取面积区间分布
- `get_batch_stats()`：获取多批次统计数据

### 3. Dash 应用布局 (`app/dash_app/layout.py`)

页面结构：
1. **批次选择区**：单选/多选批次 ID
2. **标签页切换**：单批次分析 / 多批次对比
3. **单批次分析页**：
   - 维度选择器（区域/板块/小区）
   - 三个柱状图（数量分布、租金分布、面积分布）
4. **多批次对比页**：
   - 指标选择器（复选框）
   - 四个连线图（各指标趋势）

### 4. 图表生成 (`app/dash_app/charts.py`)

- `create_bar_chart()`：生成柱状图，支持自定义配色和布局
- `create_line_chart()`：生成连线图，支持标记点和数值显示
- `create_multi_line_chart()`：生成多线条连线图

### 5. 回调函数 (`app/dash_app/callbacks.py`)

- **标签页切换回调**：根据选中的标签页渲染对应内容
- **单批次分析回调**：监听批次和维度变化，更新所有柱状图
- **多批次对比回调**：监听批次选择变化，更新所有趋势图

## 数据说明

### 数据库表结构

参考 `data/rent_house.sql`，核心字段包括：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键 |
| batch_id | VARCHAR(255) | 批次 ID |
| district | VARCHAR(100) | 区域 |
| bankuai | VARCHAR(100) | 板块 |
| community | VARCHAR(100) | 小区 |
| total_price | VARCHAR(50) | 租金（字符串，如 "5000元/月"） |
| area | VARCHAR(50) | 面积（字符串，如 "100㎡"） |
| bedroom | INT | 室 |
| livingroom | INT | 厅 |

### 数据处理逻辑

租金和面积字段存储为字符串，在数据访问层进行解析：

1. **租金解析**：提取字符串中的数字部分，转换为整数
2. **面积解析**：
   - 单个数值（如 "100㎡"）：直接转换为浮点数
   - 范围格式（如 "50-60㎡"）：计算平均值

### 区间划分

- **租金区间**：0-2000, 2000-4000, 4000-6000, 6000-8000, 8000-10000, 10000-15000, 15000-20000, 20000+
- **面积区间**：0-30, 30-50, 50-70, 70-90, 90-120, 120-150, 150-200, 200+

## 开发指南

### 添加新的分析维度

1. 在 `app/models.py` 的 `get_distribution_by_dimension()` 方法中添加新维度映射
2. 在 `app/dash_app/layout.py` 的维度选择器中添加新选项
3. 在 `app/dash_app/callbacks.py` 中确保回调能正确处理新维度

### 修改图表样式

编辑 `app/dash_app/charts.py` 中的图表生成函数，支持：
- 自定义配色方案
- 修改图表尺寸
- 调整数据标签位置
- 添加动画效果

### 部署到生产环境

1. 修改 `.env` 配置：
   ```env
   FLASK_DEBUG=False
   FLASK_ENV=production
   ```

2. 使用 WSGI 服务器（如 Gunicorn）：
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

## 常见问题

### Q1: 数据库连接失败？

检查以下几点：
1. MySQL 服务是否启动
2. `.env` 中的数据库配置是否正确
3. 数据库用户是否有访问权限
4. 防火墙是否阻止了 3306 端口

### Q2: 页面显示 "暂无数据"？

可能原因：
1. 数据库中没有数据
2. 批次 ID 选择器未正确加载
3. 数据格式不符合预期（如租金/面积字段为空）

解决方法：
1. 检查 `rent_house` 表是否有数据
2. 确认 `batch_id` 字段有值
3. 查看应用控制台的错误日志

### Q3: 小区维度图表显示不完整？

小区数量通常较多，代码默认只显示前 20 个小区（按房源数量降序）。如需修改，在 `app/dash_app/callbacks.py` 中调整 `top_n` 参数。

## 更新日志

### v1.0.0 (2026-04-20)

- ✨ 初始版本发布
- ✨ 实现批次选择功能（单选/多选）
- ✨ 实现单批次分析功能（区域/板块/小区三维分析）
- ✨ 实现多批次对比功能（趋势图展示）
- ✨ 支持 MySQL 数据库连接
- ✨ 完整的配置管理和模块化架构
- ✨ 详细的代码注释和文档

## 许可证

本项目仅供学习和研究使用。

## 联系方式

如有问题或建议，欢迎提交 Issue。
