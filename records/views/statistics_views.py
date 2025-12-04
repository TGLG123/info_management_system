import json
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render
from ..models import GeologicalSketchRecord,OverUnderExcavationCalculation,ExcavationDiagnosis,TunnelContourInfo


#下面四个是统计信息
@login_required
def geological_statistics(request):
    """
    Geological statistics view:
    - Users see their own data statistics.
    - Admins see global data statistics.
    """

    # Determine if the user is an admin
    is_admin = request.user.role == 'admin'

    # Get the dataset: Admins get all data, regular users get only their own data
    if is_admin:
        records = GeologicalSketchRecord.objects.all()
    else:
        records = GeologicalSketchRecord.objects.filter(created_by=request.user)

    # Prepare the dataset
    data = pd.DataFrame.from_records(
        records.values(
            'excavation_width',
            'excavation_height',
            'excavation_area',
            'design_section',
            'rock_strength',
            'weathering_degree',
            'created_at',  # Record creation time for trend analysis
        )
    )

    # Initialize statistics and charts
    statistics = {}
    charts = {}

    if not data.empty:
        # Convert relevant columns to numeric and clean data
        for col in ['excavation_width', 'excavation_height', 'excavation_area', 'rock_strength']:
            data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric, invalid entries become NaN

        # Drop rows with NaN in critical numeric columns
        data = data.dropna(subset=['excavation_width', 'excavation_height', 'excavation_area', 'rock_strength'])

        # Compute statistics
        statistics['record_count'] = len(data)  # Number of records uploaded
        statistics['excavation_width_avg'] = data['excavation_width'].mean()  # Average excavation width
        statistics['excavation_height_avg'] = data['excavation_height'].mean()  # Average excavation height
        statistics['excavation_area_avg'] = data['excavation_area'].mean()  # Average excavation area
        statistics['rock_strength_avg'] = data['rock_strength'].mean()  # Average rock strength

        # Ensure 'created_at' is in datetime format
        if 'created_at' in data:
            data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')  # Convert to datetime
            data = data.dropna(subset=['created_at'])  # Remove rows with invalid dates

        # Generate excavation width distribution histogram
        try:
            plt.figure(figsize=(8, 4))
            data['excavation_width'].plot(kind='hist', bins=10, color='blue', alpha=0.7, edgecolor='black')
            plt.title('Excavation Width Distribution')
            plt.xlabel('Excavation Width')
            plt.ylabel('Frequency')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            charts['excavation_width_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()
        except Exception as e:
            print("Error plotting excavation width distribution:", e)

        # Generate excavation height vs. excavation area scatter plot
        try:
            plt.figure(figsize=(8, 4))
            plt.scatter(data['excavation_height'], data['excavation_area'], alpha=0.6, color='green')
            plt.title('Excavation Height vs Excavation Area')
            plt.xlabel('Excavation Height')
            plt.ylabel('Excavation Area')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            charts['excavation_height_vs_area'] = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()
        except Exception as e:
            print("Error plotting excavation height vs. area scatter plot:", e)

        # Generate design section trend over time
        try:
            plt.figure(figsize=(8, 4))
            plt.plot(data['created_at'], data['design_section'], marker='o', color='purple')
            plt.title('Design Section Trend Over Time')
            plt.xlabel('Time')
            plt.ylabel('Design Section')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            charts['design_section_trend'] = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()
            plt.close()
        except Exception as e:
            print("Error plotting design section trend:", e)

    # Render the template
    return render(
        request,
        'statics/geological_statistics.html',
        {
            'statistics': statistics,
            'charts': charts,
            'is_admin': is_admin,
        }
    )


@login_required
def excavation_calculation_statistics(request):
    """
    超欠挖计算统计视图：
    - 用户看到自己的数据统计。
    - 管理员看到全局数据统计。
    """
    # 判断是否是管理员
    is_admin = request.user.role == 'admin'

    # 获取数据集：管理员获取所有数据，普通用户获取个人数据
    if is_admin:
        records = OverUnderExcavationCalculation.objects.all()
    else:
        records = OverUnderExcavationCalculation.objects.filter(created_by=request.user)

    print("Records count:", records.count())  # 调试信息

    # 准备数据
    data = pd.DataFrame.from_records(
        records.values(
            'line_name',
            'north_direction_angle',
            'radius',
            'length',
            'height',
            'angle_increment',
            'created_at',
        )
    )

    # 初始化统计结果
    statistics = {}

    if not data.empty:
        # 基础统计
        statistics['record_count'] = len(data)
        statistics['radius_avg'] = data['radius'].mean()
        statistics['length_avg'] = data['length'].mean()
        statistics['height_avg'] = data['height'].mean()

        # 处理半径分布数据
        radius_stats = data.groupby('line_name')['radius'].agg(['mean', 'min', 'max']).reset_index()
        statistics['radius_data'] = {
            'labels': radius_stats['line_name'].tolist(),
            'means': radius_stats['mean'].tolist(),
            'mins': radius_stats['min'].tolist(),
            'maxs': radius_stats['max'].tolist()
        }

        # 处理长度和高度数据
        length_height_data = []
        for _, row in data.iterrows():
            length_height_data.append({
                'x': float(row['length']),
                'y': float(row['height'])
            })
        statistics['length_height_data'] = json.dumps(length_height_data)

        # 处理角度增量的时间序列数据
        data['year'] = pd.to_datetime(data['created_at']).dt.year
        angle_by_year = data.groupby('year')['angle_increment'].agg(['mean', 'min', 'max']).reset_index()

        # 确保包含2021-2025的所有年份数据
        all_years = range(2021, 2026)
        angle_data = []
        for year in all_years:
            year_stats = angle_by_year[angle_by_year['year'] == year]
            if not year_stats.empty:
                angle_data.append({
                    'mean': float(year_stats['mean'].iloc[0]),
                    'min': float(year_stats['min'].iloc[0]),
                    'max': float(year_stats['max'].iloc[0])
                })
            else:
                angle_data.append({
                    'mean': 0,
                    'min': 0,
                    'max': 0
                })

        statistics['angle_data'] = {
            'years': list(all_years),
            'means': [d['mean'] for d in angle_data],
            'mins': [d['min'] for d in angle_data],
            'maxs': [d['max'] for d in angle_data]
        }

        # 汇总统计数据
        statistics['summary_data'] = {
            'radius': statistics['radius_avg'],
            'length': statistics['length_avg'],
            'height': statistics['height_avg'],
            'angle': data['angle_increment'].mean()
        }

    print("Statistics data:", statistics)  # 调试信息

    return render(
        request,
        'statics/excavation_calculation_statistics.html',
        {
            'statistics': statistics,
            'is_admin': is_admin,
        }
    )

@login_required
def excavation_diagnosis_statistics(request):
    """
    超欠挖诊断统计视图：
    - 用户看到自己的数据统计。
    - 管理员看到全局数据统计。
    """
    # 判断是否是管理员
    is_admin = request.user.role == 'admin'

    # 获取数据集：管理员获取所有数据，普通用户获取个人数据
    if is_admin:
        records = ExcavationDiagnosis.objects.all()
    else:
        records = ExcavationDiagnosis.objects.filter(created_by=request.user)

    print("Records count:", records.count())  # 调试信息

    # 准备数据
    data = pd.DataFrame.from_records(
        records.values(
            'over_excavation_area',
            'under_excavation_area',
            'max_over_excavation',
            'max_under_excavation',
            'average_over_excavation',
            'average_under_excavation',
            'created_at',
        )
    )

    # 初始化统计结果
    statistics = {}

    if not data.empty:
        # 基础统计
        statistics['over_excavation_area_avg'] = data['over_excavation_area'].mean()
        statistics['under_excavation_area_avg'] = data['under_excavation_area'].mean()
        statistics['max_over_excavation'] = data['max_over_excavation'].max()
        statistics['max_under_excavation'] = data['max_under_excavation'].min()  # 使用min因为欠挖是负值

        # 处理散点图数据
        scatter_data = []
        for _, row in data.iterrows():
            scatter_data.append({
                'x': float(row['over_excavation_area']),
                'y': float(row['under_excavation_area'])
            })
        statistics['scatter_data'] = json.dumps(scatter_data)

        # 处理月度数据
        data['month'] = pd.to_datetime(data['created_at']).dt.strftime('%Y-%m')
        monthly_group = data.groupby('month').agg({
            'over_excavation_area': 'sum',
            'under_excavation_area': 'sum',
            'max_over_excavation': 'max',
            'max_under_excavation': 'min'  # 使用min因为欠挖是负值
        }).reset_index()

        # 按时间排序
        monthly_group = monthly_group.sort_values('month')

        statistics['months'] = monthly_group['month'].tolist()
        statistics['monthly_data'] = {
            'over': monthly_group['over_excavation_area'].tolist(),
            'under': monthly_group['under_excavation_area'].tolist(),
            'max_over': monthly_group['max_over_excavation'].tolist(),
            'max_under': monthly_group['max_under_excavation'].tolist()
        }

        # 处理时间序列数据
        data['date'] = pd.to_datetime(data['created_at']).dt.strftime('%Y-%m-%d')
        time_series = data.groupby('date').agg({
            'over_excavation_area': 'sum',
            'under_excavation_area': 'sum'
        }).reset_index()

        # 计算累计变化趋势
        time_series['cumulative'] = (time_series['over_excavation_area'] +
                                     time_series['under_excavation_area']).cumsum()

        # 按时间排序
        time_series = time_series.sort_values('date')

        # 添加到统计结果
        statistics['time_series'] = {
            'dates': time_series['date'].tolist(),
            'over': time_series['over_excavation_area'].tolist(),
            'under': time_series['under_excavation_area'].tolist(),
            'cumulative': time_series['cumulative'].tolist()
        }

    print("Statistics data:", statistics)  # 调试信息

    return render(
        request,
        'statics/excavation_diagnosis_statistics.html',
        {
            'statistics': statistics,
            'is_admin': is_admin,
        }
    )

@login_required
def tunnel_statistics(request):
    """
    隧道轮廓统计视图：
    - 用户看到自己的数据统计。
    - 管理员看到全局数据统计。
    """

    # 判断是否是管理员
    is_admin = request.user.role == 'admin'

    # 获取数据集：管理员获取所有数据，普通用户获取个人数据
    if is_admin:
        records = TunnelContourInfo.objects.all()
    else:
        records = TunnelContourInfo.objects.filter(created_by=request.user)
    print(records)
    # 准备数据
    data = pd.DataFrame.from_records(
        records.values(
            'cr',
            'rcl',
            'vo',
            'c1',
            'c2',
            'c3',
            'created_at',  # 记录创建时间，用于趋势分析
        )
    )

    # 初始化统计结果和图表
    statistics = {}
    charts = {}

    if not data.empty:
        # 统计指标
        statistics['record_count'] = len(data)  # 上传记录数
        statistics['avg_cr'] = data['cr'].mean()  # 调整指数平均值
        statistics['avg_rcl'] = data['rcl'].mean()  # 粗糙度平均值
        statistics['avg_vo'] = data['vo'].mean()  # 纵向超挖变化平均值

        # 调整指数分布图
        plt.figure(figsize=(8, 4))
        data['cr'].plot(kind='hist', bins=10, color='blue', alpha=0.7, edgecolor='black')
        plt.title('Adjustment Index (CR) Distribution')
        plt.xlabel('CR')
        plt.ylabel('Frequency')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        charts['cr_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()

        # RCL vs VO 散点图
        plt.figure(figsize=(8, 4))
        plt.scatter(data['rcl'], data['vo'], alpha=0.6, color='green')
        plt.title('RCL vs VO')
        plt.xlabel('RCL')
        plt.ylabel('VO')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        charts['rcl_vs_vo'] = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
    time_series = data.groupby(
        pd.Grouper(key='created_at', freq='Y')
    )['vo'].mean().to_dict()

    statistics['longitudinal_trend'] = list(time_series.values())
    # 渲染模板
    return render(
        request,
        'statics/tunnel_statistics.html',
        {
            'statistics': statistics,
            'charts': charts,
            'is_admin': is_admin,
        }
    )