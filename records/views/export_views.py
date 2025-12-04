from ..models import  OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo, \
    GeologicalSketchRecord
import pandas as pd
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render


#数据导出
@login_required
def export_geological_view(request):
    """
    渲染掌子面导出界面，用户可以选择字段。
    """
    # 判断用户角色
    is_admin = request.user.role == 'admin' or 'auditor'

    # 可选的所有字段
    fields = [
        {'name': 'face_id', 'label': '掌子面编号'},
        {'name': 'project_id', 'label': '施工项目编号'},
        {'name': 'inspection_date', 'label': '检查日期'},
        {'name': 'distance', 'label': '里程'},
        {'name': 'design_section', 'label': '设计断面'},
        {'name': 'excavation_width', 'label': '开挖宽度'},
        {'name': 'excavation_height', 'label': '开挖高度'},
        {'name': 'excavation_area', 'label': '开挖面积'},
        {'name': 'rock_strength', 'label': '岩石强度'},
        {'name': 'weathering_degree', 'label': '风化程度'},
        {'name': 'crack_width', 'label': '裂缝宽度'},
        {'name': 'crack_shape', 'label': '裂缝形态'},
        {'name': 'water_condition', 'label': '渗水状态'},
        {'name': 'rockburst_tendency', 'label': '岩爆发育程度'},
    ]

    return render(
        request,
        'export/export_geological.html',
        {
            'fields': fields,
            'is_admin': is_admin,
        }
    )

@login_required
def export_geological_records(request):
    """
    导出掌子面数据为 Excel。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 获取数据集
    if is_admin:
        records = GeologicalSketchRecord.objects.all()
    else:
        records = GeologicalSketchRecord.objects.filter(created_by=request.user)

    # 获取用户选择的字段
    default_fields = [
        'face_id', 'project_id', 'inspection_date', 'distance', 'design_section',
        'excavation_width', 'excavation_height', 'excavation_area',
        'rock_strength', 'weathering_degree', 'crack_width'
    ]
    selected_fields = request.GET.getlist('fields', default_fields) #前端传来的要导出来的数据项

    if not selected_fields:
        selected_fields = default_fields

    # 转换数据为 DataFrame
    data = pd.DataFrame.from_records(records.values(*selected_fields))

    # 处理时区问题，将所有的时间字段转换为无时区的时间
    for field in ['inspection_date', 'created_at', 'updated_at']:  # 修改为实际的时间字段名
        if field in data.columns:
            data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)

    # 创建 Excel 响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="geological_records.xlsx"'

    # 写入数据到 Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Geological Records')

    return response

@login_required
def export_excavation_calculation_view(request):
    """
    渲染导出界面，用户可以选择超欠挖计算字段。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 可选的所有字段
    fields = [
        {'name': 'face_id', 'label': '掌子面编号'},
        {'name': 'project_id', 'label': '施工项目编号'},
        {'name': 'inspection_date', 'label': '检查日期'},
        {'name': 'measurement_date', 'label': '测量日期'},
        {'name': 'line_name', 'label': '线路名称'},
        {'name': 'north_direction_angle', 'label': '北方向角'},
        {'name': 'radius', 'label': '半径'},
        {'name': 'length', 'label': '长度'},
        {'name': 'east_coordinate', 'label': '东坐标'},
        {'name': 'north_coordinate', 'label': '北坐标'},
        {'name': 'height', 'label': '高度'},
    ]

    return render(
        request,
        'export/export_excavation_calculation.html',
        {
            'fields': fields,
            'is_admin': is_admin,
        }
    )

@login_required
def export_excavation_calculation_records(request):
    """
    导出超欠挖计算数据为 Excel。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 获取数据集
    if is_admin:
        records = OverUnderExcavationCalculation.objects.all()
    else:
        records = OverUnderExcavationCalculation.objects.filter(created_by=request.user)

    # 获取用户选择的字段
    default_fields = [
        'face_id', 'project_id', 'inspection_date', 'measurement_date',
        'line_name', 'north_direction_angle', 'radius',
        'length', 'east_coordinate', 'north_coordinate', 'height'
    ]
    selected_fields = request.GET.getlist('fields', default_fields)

    if not selected_fields:
        selected_fields = default_fields

    # 转换数据为 DataFrame
    data = pd.DataFrame.from_records(records.values(*selected_fields))

    # 处理时区问题
    for field in ['inspection_date', 'measurement_date']:
        if field in data.columns:
            data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)

    # 创建 Excel 响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excavation_calculation_records.xlsx"'

    # 写入数据到 Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Excavation Calculation Records')

    return response

@login_required
def export_excavation_diagnosis_view(request):
    """
    渲染导出界面，用户可以选择超欠挖诊断字段。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 可选的所有字段
    fields = [
        {'name': 'face_id', 'label': '掌子面编号'},
        {'name': 'project_id', 'label': '施工项目编号'},
        {'name': 'inspection_date', 'label': '检查日期'},
        {'name': 'measurement_date', 'label': '测量日期'},
        {'name': 'mileage', 'label': '里程'},
        {'name': 'design_section', 'label': '设计断面'},
        {'name': 'measured_section', 'label': '实测断面'},
        {'name': 'over_excavation_area', 'label': '超挖面积'},
        {'name': 'under_excavation_area', 'label': '欠挖面积'},
        {'name': 'max_over_excavation', 'label': '最大超挖'},
        {'name': 'max_under_excavation', 'label': '最大欠挖'},
        {'name': 'average_over_excavation', 'label': '平均超挖'},
        {'name': 'average_under_excavation', 'label': '平均欠挖'},
    ]

    return render(
        request,
        'export/export_excavation_diagnosis.html',
        {
            'fields': fields,
            'is_admin': is_admin,
        }
    )

@login_required
def export_excavation_diagnosis_records(request):
    """
    导出超欠挖诊断数据为 Excel。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 获取数据集
    if is_admin:
        records = ExcavationDiagnosis.objects.all()
    else:
        records = ExcavationDiagnosis.objects.filter(created_by=request.user)

    # 获取用户选择的字段
    default_fields = [
        'face_id', 'project_id', 'inspection_date', 'measurement_date',
        'mileage', 'design_section', 'measured_section',
        'over_excavation_area', 'under_excavation_area',
        'max_over_excavation', 'max_under_excavation',
        'average_over_excavation', 'average_under_excavation'
    ]
    selected_fields = request.GET.getlist('fields', default_fields)

    if not selected_fields:
        selected_fields = default_fields

    # 转换数据为 DataFrame
    data = pd.DataFrame.from_records(records.values(*selected_fields))

    # 处理时区问题
    for field in ['inspection_date', 'measurement_date']:
        if field in data.columns:
            data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)

    # 创建 Excel 响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="excavation_diagnosis_records.xlsx"'

    # 写入数据到 Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Excavation Diagnosis Records')

    return response

@login_required
def export_tunnel_contour_view(request):
    """
    渲染导出界面，用户可以选择隧道轮廓字段。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 可选的所有字段
    fields = [
        {'name': 'face_id', 'label': '隧道编号'},
        {'name': 'project_id', 'label': '施工项目编号'},
        {'name': 'inspection_date', 'label': '检查日期'},
        {'name': 'measurement_date', 'label': '测量日期'},
        {'name': 'cr', 'label': '调整指数范围的常数 Cr'},
        {'name': 'w1', 'label': '权重值 w1'},
        {'name': 'w2', 'label': '权重值 w2'},
        {'name': 'w3', 'label': '权重值 w3'},
        {'name': 'od', 'label': '超挖深度 Od'},
        {'name': 'rcl', 'label': '轮廓粗糙度 RCL'},
        {'name': 'vo', 'label': '纵向超挖变化 Vo'},
        {'name': 'c1', 'label': '修正因子 c1'},
        {'name': 'c2', 'label': '修正因子 c2'},
        {'name': 'c3', 'label': '修正因子 c3'},
    ]

    return render(
        request,
        'export/export_tunnel_contour.html',
        {
            'fields': fields,
            'is_admin': is_admin,
        }
    )

@login_required
def export_tunnel_contour_records(request):
    """
    导出隧道轮廓数据为 Excel。
    """
    is_admin = request.user.role == 'admin' or 'auditor'

    # 获取数据集
    if is_admin:
        records = TunnelContourInfo.objects.all()
    else:
        records = TunnelContourInfo.objects.filter(created_by=request.user)

    # 获取用户选择的字段
    default_fields = [
        'face_id', 'project_id', 'inspection_date', 'measurement_date',
        'cr', 'w1', 'w2', 'w3', 'od', 'rcl', 'vo', 'c1', 'c2', 'c3'
    ]
    selected_fields = request.GET.getlist('fields', default_fields)

    if not selected_fields:
        selected_fields = default_fields

    # 转换数据为 DataFrame
    data = pd.DataFrame.from_records(records.values(*selected_fields))

    # 处理时区问题
    for field in ['inspection_date', 'measurement_date']:
        if field in data.columns:
            data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)

    # 创建 Excel 响应
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="tunnel_contour_records.xlsx"'

    # 写入数据到 Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Tunnel Contour Records')

    return response