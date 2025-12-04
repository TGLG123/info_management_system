from ..forms import GeologicalSketchRecordForm, ExcavationDiagnosisForm, OverUnderExcavationForm, TunnelContourForm
from django.db import transaction
from ..check import (
    check_geological_data_validity,
    check_excavation_diagnosis_validity,
    check_excavation_calculation_validity,
    check_tunnel_data_validity,
)
from django.shortcuts import render, redirect, get_object_or_404
import pandas as pd
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from django.shortcuts import render


#掌子面信息上传（管理员）（支持excel导入版本）
@login_required
def upload_geological_info(request):
    """
    管理员上传地质信息视图（支持单条记录提交和 Excel 批量导入）。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")  # 调试输出提交类型

        if submit_type == 'single':  # 单条记录提交
            print("开始单条记录提交处理")
            form = GeologicalSketchRecordForm(request.POST)
            if form.is_valid():
                print("单条记录验证通过，准备保存")
                geological_record = form.save(commit=False)  # 保存表单数据到实例，但不提交到数据库
                geological_record.created_by = request.user  # 设置当前用户为创建者
                geological_record.status = 'uploaded_approved'  # 设置状态为已审批
                geological_record.save()  # 保存数据到数据库
                print("单条记录保存成功")
                return redirect('geological_list')  # 成功后重定向到地质记录列表页面
            else:
                print("单条记录表单验证失败")
                print(f"表单错误: {form.errors}")  # 调试输出表单错误
                return render(
                    request,
                    'upload/upload_geological_info.html',
                    {'form': form, 'errors': form.errors}
                )

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                print("开始批量导入处理")
                excel_file = request.FILES['excel_file']
                try:
                    # 读取 Excel 文件，指定 openpyxl 引擎
                    data = pd.read_excel(excel_file, engine='openpyxl')
                    print(f"读取到的 Excel 数据:\n{data.head()}")  # 调试输出 Excel 文件的前几行

                    # 检查 Excel 数据的必填字段
                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'distance',
                        'design_section', 'inspector', 'measurement_date', 'excavation_width',
                        'excavation_height', 'excavation_area', 'excavation_method',
                        'face_condition', 'excavation_condition', 'rock_strength',
                        'weathering_degree', 'crack_width', 'crack_shape', 'water_condition',
                        'rockburst_tendency', 'rock_grade', 'karst_development', 'water_status'
                    ]

                    # 检查缺少的字段
                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        return JsonResponse({
                            "status": "error",
                            "message": f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
                        })

                    # 强制转换字段类型
                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = ['design_section', 'distance', 'excavation_width', 'excavation_height', 'excavation_area',
                                       'rock_strength', 'crack_width']
                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')  # 转换为日期字符串
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce')  # 非数值将被置为 NaN
                            if data[col].isnull().any():  # 如果存在 NaN 值
                                print(f"列 {col} 包含无法转换为数字的值。将替换为 0。")
                                print(f"问题值:\n{data[data[col].isnull()][col]}")  # 输出问题值
                                data[col] = data[col].fillna(0)  # 替换 NaN 为默认值 0

                    # 保存每一行数据
                    errors = []
                    success_count = 0
                    with transaction.atomic():  # 确保事务一致性
                        for index, row in data.iterrows():
                            print(f"正在处理第 {index + 1} 行数据: {row.to_dict()}")  # 调试输出当前行数据
                            form_data = row.to_dict()  # 转换为字典格式
                            form = GeologicalSketchRecordForm(form_data)

                            if form.is_valid():
                                geological_record = form.save(commit=False)
                                geological_record.created_by = request.user
                                geological_record.status = 'uploaded_approved'
                                geological_record.save()
                                success_count += 1
                                print(f"第 {index + 1} 行数据保存成功")
                            else:
                                print(f"第 {index + 1} 行数据验证失败: {form.errors}")  # 调试输出当前行错误
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    if errors:
                        print(f"部分数据导入失败，共成功导入 {success_count} 条记录")
                        return JsonResponse({
                            "status": "partial_success",
                            "message": f"批量导入完成，但有部分错误。",
                            "success_count": success_count,
                            "errors": errors
                        })

                    print(f"批量导入成功，共导入 {success_count} 条记录")
                    return redirect('geological_list')  # 成功后重定向到地质记录列表页面

                except Exception as e:
                    print(f"批量导入失败: {str(e)}")  # 调试输出异常信息
                    return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})

            print("未上传 Excel 文件")
            return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})

        else:
            print("无效的提交类型")
            return JsonResponse({"status": "error", "message": "无效的提交类型。"})

    else:  # GET 请求
        print("GET 请求，渲染空表单")
        form = GeologicalSketchRecordForm()
        return render(request, 'upload/upload_geological_info.html', {'form': form})


## 掌子面信息上传（用户）（支持批量导入）
@login_required
def upload_geological_info_user(request):
    """
    用户上传地质信息视图。
    - 支持单条记录和 Excel 批量导入。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")  # 调试输出提交类型

        if submit_type == 'single':  # 单条记录提交
            form = GeologicalSketchRecordForm(request.POST)
            if form.is_valid():
                geological_record = form.save(commit=False)
                geological_record.created_by = request.user
                geological_record.operation_reason = request.POST.get('operation_reason')

                is_valid, validation_errors = check_geological_data_validity(geological_record)

                if is_valid:
                    geological_record.status = 'uploaded_approved'
                else:
                    geological_record.status = 'pending'

                geological_record.save()
                if not is_valid:
                    request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
                    request.session['message_type'] = "warning"

                return redirect('user_records_view')  # 跳转到个人信息中心

            else:
                request.session['message'] = "单条提交失败，请检查数据格式。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')

                    # 必填字段校验
                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'distance',
                        'design_section', 'inspector', 'measurement_date', 'excavation_width',
                        'excavation_height', 'excavation_area', 'excavation_method',
                        'face_condition', 'excavation_condition', 'rock_strength',
                        'weathering_degree', 'crack_width', 'crack_shape', 'water_condition',
                        'rockburst_tendency', 'rock_grade', 'karst_development', 'water_status', 'operation_reason'
                    ]

                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    # 数据类型转换
                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = ['distance', 'design_section', 'excavation_width', 'excavation_height', 'excavation_area',
                                       'rock_strength', 'crack_width']
                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    # 保存记录
                    errors = []
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = GeologicalSketchRecordForm(form_data)

                            if form.is_valid():
                                geological_record = form.save(commit=False)
                                geological_record.created_by = request.user

                                is_valid, _ = check_geological_data_validity(geological_record)

                                if is_valid:
                                    geological_record.status = 'uploaded_approved'
                                else:
                                    geological_record.status = 'pending'

                                geological_record.save()
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    # 判断批量导入结果
                    if errors:
                        request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    return redirect('user_records_view')  # 全部成功直接跳转

                except Exception as e:
                    request.session['message'] = f"批量导入失败: {str(e)}"
                    request.session['message_type'] = "error"
                    return redirect('user_records_view')

            else:
                request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

    else:
        form = GeologicalSketchRecordForm()
    return render(request, 'upload/upload_geological_info_user.html', {'form': form})


## 超欠挖计算信息上传（用户，支持批量导入）
@login_required
def upload_excavation_calculation_user(request):
    """
    用户上传超欠挖计算信息视图。
    - 支持单条记录和 Excel 批量导入。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")  # 调试输出提交类型

        if submit_type == 'single':  # 单条记录提交
            form = OverUnderExcavationForm(request.POST)
            if form.is_valid():
                calculation_record = form.save(commit=False)
                calculation_record.created_by = request.user
                calculation_record.operation_reason = request.POST.get('operation_reason')

                is_valid, validation_errors = check_excavation_diagnosis_validity(calculation_record)

                if is_valid:
                    calculation_record.status = 'uploaded_approved'
                else:
                    calculation_record.status = 'pending'

                calculation_record.save()
                if not is_valid:
                    request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
                    request.session['message_type'] = "warning"

                return redirect('user_records_view')  # 跳转到个人信息中心

            else:
                request.session['message'] = "单条提交失败，请检查数据格式。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')

                    # 必填字段校验
                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'measurement_date',
                        'line_name', 'north_direction_angle', 'radius', 'length',
                        'east_coordinate', 'north_coordinate', 'start_offset', 'height',
                        'radius_section', 'angle_increment', 'operation_reason'
                    ]

                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    # 数据类型转换
                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = [
                        'north_direction_angle', 'radius', 'length', 'east_coordinate',
                        'north_coordinate', 'start_offset', 'height', 'radius_section', 'angle_increment'
                    ]
                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    # 保存记录
                    errors = []
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = OverUnderExcavationForm(form_data)

                            if form.is_valid():
                                calculation_record = form.save(commit=False)
                                calculation_record.created_by = request.user

                                is_valid, _ = check_excavation_diagnosis_validity(calculation_record)

                                if is_valid:
                                    calculation_record.status = 'uploaded_approved'
                                else:
                                    calculation_record.status = 'pending'

                                calculation_record.save()
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    # 判断批量导入结果
                    if errors:
                        request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    return redirect('user_records_view')  # 全部成功直接跳转

                except Exception as e:
                    request.session['message'] = f"批量导入失败: {str(e)}"
                    request.session['message_type'] = "error"
                    return redirect('user_records_view')

            else:
                request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

    else:
        form = OverUnderExcavationForm()
    return render(request, 'upload/upload_info3_user.html', {'form': form})

## 超欠挖诊断信息上传（用户，支持批量导入）
@login_required
def upload_excavation_diagnosis_user(request):
    """
    用户上传超欠挖诊断信息视图。
    - 支持单条记录和 Excel 批量导入。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")  # 调试输出提交类型

        if submit_type == 'single':  # 单条记录提交
            form = ExcavationDiagnosisForm(request.POST)
            if form.is_valid():
                diagnosis_record = form.save(commit=False)
                diagnosis_record.created_by = request.user
                diagnosis_record.operation_reason = request.POST.get('operation_reason')

                is_valid, validation_errors = check_excavation_calculation_validity(diagnosis_record)

                if is_valid:
                    diagnosis_record.status = 'uploaded_approved'
                else:
                    diagnosis_record.status = 'pending'

                diagnosis_record.save()
                if not is_valid:
                    request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
                    request.session['message_type'] = "warning"

                return redirect('user_records_view')  # 跳转到个人信息中心

            else:
                request.session['message'] = "单条提交失败，请检查数据格式。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')

                    # 必填字段校验
                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'measurement_date',
                        'scale', 'mileage', 'design_section', 'line_x', 'line_y',
                        'measured_section', 'reference_section', 'line_height', 'over_excavation_area',
                        'under_excavation_area', 'max_over_excavation', 'max_under_excavation',
                        'average_over_excavation', 'average_under_excavation', 'diagnosis_result', 'inspector', 'operation_reason'
                    ]

                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    # 数据类型转换
                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = [
                        'scale', 'mileage', 'design_section', 'line_x', 'line_y',
                        'measured_section', 'reference_section', 'line_height',
                        'over_excavation_area', 'under_excavation_area',
                        'max_over_excavation', 'max_under_excavation',
                        'average_over_excavation', 'average_under_excavation'
                    ]
                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    # 保存记录
                    errors = []
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = ExcavationDiagnosisForm(form_data)

                            if form.is_valid():
                                diagnosis_record = form.save(commit=False)
                                diagnosis_record.created_by = request.user

                                is_valid, _ = check_excavation_calculation_validity(diagnosis_record)

                                if is_valid:
                                    diagnosis_record.status = 'uploaded_approved'
                                else:
                                    diagnosis_record.status = 'pending'

                                diagnosis_record.save()
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    # 判断批量导入结果
                    if errors:
                        request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    return redirect('user_records_view')  # 全部成功直接跳转

                except Exception as e:
                    request.session['message'] = f"批量导入失败: {str(e)}"
                    request.session['message_type'] = "error"
                    return redirect('user_records_view')

            else:
                request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

    else:
        form = ExcavationDiagnosisForm()
    return render(request, 'upload/upload_info2_user.html', {'form': form})

## 隧道信息上传（用户，支持批量导入）
@login_required
def upload_tunnel_info_user(request):
    """
    用户上传隧道信息视图。
    - 支持单条记录和 Excel 批量导入。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")  # 调试输出提交类型

        if submit_type == 'single':  # 单条记录提交
            form = TunnelContourForm(request.POST)
            if form.is_valid():
                tunnel_info = form.save(commit=False)
                tunnel_info.created_by = request.user
                tunnel_info.operation_reason = request.POST.get('operation_reason')

                is_valid, validation_errors = check_tunnel_data_validity(tunnel_info)

                if is_valid:
                    tunnel_info.status = 'uploaded_approved'
                else:
                    tunnel_info.status = 'pending'

                tunnel_info.save()
                if not is_valid:
                    request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
                    request.session['message_type'] = "warning"

                return redirect('user_records_view')  # 跳转到个人信息中心

            else:
                request.session['message'] = "单条提交失败，请检查数据格式。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')

                    # 必填字段校验
                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'measurement_date',
                        'inspector', 'od', 'rcl', 'vo', 'cr',
                        'w1', 'w2', 'w3', 'c1', 'c2', 'c3', 'operation_reason'
                    ]

                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    # 数据类型转换
                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = ['od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3']
                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    # 保存记录
                    errors = []
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = TunnelContourForm(form_data)

                            if form.is_valid():
                                tunnel_info = form.save(commit=False)
                                tunnel_info.created_by = request.user

                                is_valid, _ = check_tunnel_data_validity(tunnel_info)

                                if is_valid:
                                    tunnel_info.status = 'uploaded_approved'
                                else:
                                    tunnel_info.status = 'pending'

                                tunnel_info.save()
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    # 判断批量导入结果
                    if errors:
                        request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
                        request.session['message_type'] = "error"
                        return redirect('user_records_view')

                    return redirect('user_records_view')  # 全部成功直接跳转

                except Exception as e:
                    request.session['message'] = f"批量导入失败: {str(e)}"
                    request.session['message_type'] = "error"
                    return redirect('user_records_view')

            else:
                request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
                request.session['message_type'] = "error"
                return redirect('user_records_view')

    else:
        form = TunnelContourForm()
    return render(request, 'upload/upload_info1_user.html', {'form': form})

# 超欠挖诊断信息上传（管理员）（支持excel导入版本）
@login_required
def upload_info2(request):
    """
    管理员上传超欠挖诊断信息视图（支持单条记录提交和 Excel 批量导入）。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
        print(f"提交类型: {submit_type}")

        if submit_type == 'single':  # 单条记录提交
            form = ExcavationDiagnosisForm(request.POST)
            if form.is_valid():
                diagnosis_record = form.save(commit=False)
                diagnosis_record.created_by = request.user
                diagnosis_record.status = 'uploaded_approved'
                diagnosis_record.save()
                print("单条记录保存成功")
                return redirect('excavation_diagnosis_list')
            else:
                print("单条记录表单验证失败")
                return render(request, 'upload/upload_info2.html', {'form': form, 'errors': form.errors})

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')
                    required_columns = [
                        'face_id', 'project_id', 'measurement_date', 'inspection_date',
                        'scale', 'mileage', 'design_section', 'line_x', 'line_y',
                        'measured_section', 'reference_section', 'line_height',
                        'over_excavation_area', 'under_excavation_area',
                        'max_over_excavation', 'max_under_excavation',
                        'average_over_excavation', 'average_under_excavation',
                        'diagnosis_result', 'inspector'
                    ]
                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})

                    date_columns = ['measurement_date', 'inspection_date']
                    numeric_columns = ['scale', 'mileage', 'design_section',
                                       'line_x', 'line_y', 'measured_section',
                                       'reference_section', 'line_height',
                                       'over_excavation_area', 'under_excavation_area',
                                       'max_over_excavation', 'max_under_excavation',
                                       'average_over_excavation', 'average_under_excavation']

                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    errors = []
                    success_count = 0
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form = ExcavationDiagnosisForm(row.to_dict())
                            if form.is_valid():
                                diagnosis_record = form.save(commit=False)
                                diagnosis_record.created_by = request.user
                                diagnosis_record.status = 'uploaded_approved'
                                diagnosis_record.save()
                                success_count += 1
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    if errors:
                        return JsonResponse({
                            "status": "partial_success",
                            "message": f"批量导入完成，但有部分错误。",
                            "success_count": success_count,
                            "errors": errors
                        })

                    return redirect('excavation_diagnosis_list')

                except Exception as e:
                    return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})

            return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})

        else:
            return JsonResponse({"status": "error", "message": "无效的提交类型。"})

    else:
        form = ExcavationDiagnosisForm()
        return render(request, 'upload/upload_info2.html', {'form': form})


# 超欠挖计算信息上传（管理员）（支持excel导入版本）
@login_required
def upload_info3(request):
    """
    管理员上传超欠挖计算信息视图（支持单条记录提交和 Excel 批量导入）。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')
        print(f"提交类型: {submit_type}")

        if submit_type == 'single':  # 单条记录提交
            form = OverUnderExcavationForm(request.POST)
            if form.is_valid():
                calculation_record = form.save(commit=False)
                calculation_record.created_by = request.user
                calculation_record.status = 'uploaded_approved'
                calculation_record.save()
                print("单条记录保存成功")
                return redirect('excavation_calculation_list')
            else:
                print("单条记录表单验证失败")
                return render(request, 'upload/upload_info3.html', {'form': form, 'errors': form.errors})

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')
                    print(f"读取到的 Excel 数据:\n{data.head()}")

                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'measurement_date',
                        'inspector', 'line_name', 'north_direction_angle', 'radius',
                        'length', 'east_coordinate', 'north_coordinate', 'start_offset',
                        'height', 'radius_section', 'angle_increment'
                    ]
                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})

                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = [
                        'north_direction_angle', 'radius', 'length', 'east_coordinate',
                        'north_coordinate', 'start_offset', 'height', 'radius_section',
                        'angle_increment'
                    ]

                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    errors = []
                    success_count = 0
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = OverUnderExcavationForm(form_data)
                            if form.is_valid():
                                calculation_record = form.save(commit=False)
                                calculation_record.created_by = request.user
                                calculation_record.status = 'uploaded_approved'
                                calculation_record.save()
                                success_count += 1
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    if errors:
                        return JsonResponse({
                            "status": "partial_success",
                            "message": f"批量导入完成，但有部分错误。",
                            "success_count": success_count,
                            "errors": errors
                        })

                    print(f"批量导入成功，共导入 {success_count} 条记录")
                    return redirect('excavation_calculation_list')

                except Exception as e:
                    print(f"批量导入失败: {str(e)}")
                    return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})

            return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})

        else:
            return JsonResponse({"status": "error", "message": "无效的提交类型。"})

    else:
        form = OverUnderExcavationForm()
        return render(request, 'upload/upload_info3.html', {'form': form})


# 隧道轮廓信息上传（管理员）（支持excel导入版本）
@login_required
def upload_info1(request):
    """
    管理员上传隧道轮廓信息视图（支持单条记录提交和 Excel 批量导入）。
    """
    if request.method == 'POST':
        submit_type = request.POST.get('submit_type', 'single')
        print(f"提交类型: {submit_type}")

        if submit_type == 'single':  # 单条记录提交
            form = TunnelContourForm(request.POST)
            if form.is_valid():
                profile_record = form.save(commit=False)
                profile_record.created_by = request.user
                profile_record.status = 'uploaded_approved'
                profile_record.save()
                print("单条记录保存成功")
                return redirect('tunnel_contour_info_list')
            else:
                print("单条记录表单验证失败")
                return render(request, 'upload/upload_info1.html', {'form': form, 'errors': form.errors})

        elif submit_type == 'bulk':  # 批量导入
            if 'excel_file' in request.FILES:
                excel_file = request.FILES['excel_file']
                try:
                    data = pd.read_excel(excel_file, engine='openpyxl')
                    print(f"读取到的 Excel 数据:\n{data.head()}")

                    required_columns = [
                        'face_id', 'project_id', 'inspection_date', 'measurement_date',
                        'inspector', 'od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3'
                    ]
                    missing_columns = [col for col in required_columns if col not in data.columns]
                    if missing_columns:
                        return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})

                    date_columns = ['inspection_date', 'measurement_date']
                    numeric_columns = ['od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3']

                    for col in date_columns:
                        if col in data.columns:
                            data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
                    for col in numeric_columns:
                        if col in data.columns:
                            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

                    errors = []
                    success_count = 0
                    with transaction.atomic():
                        for index, row in data.iterrows():
                            form_data = row.to_dict()
                            form = TunnelContourForm(form_data)
                            if form.is_valid():
                                profile_record = form.save(commit=False)
                                profile_record.created_by = request.user
                                profile_record.status = 'uploaded_approved'
                                profile_record.save()
                                success_count += 1
                            else:
                                errors.append({"row": index + 1, "errors": form.errors.as_json()})

                    if errors:
                        return JsonResponse({
                            "status": "partial_success",
                            "message": f"批量导入完成，但有部分错误。",
                            "success_count": success_count,
                            "errors": errors
                        })

                    print(f"批量导入成功，共导入 {success_count} 条记录")
                    return redirect('tunnel_contour_info_list')

                except Exception as e:
                    print(f"批量导入失败: {str(e)}")
                    return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})

            return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})

        else:
            return JsonResponse({"status": "error", "message": "无效的提交类型。"})

    else:
        form = TunnelContourForm()
        return render(request, 'upload/upload_info1.html', {'form': form})