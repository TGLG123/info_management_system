# import json
#
# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.models import User
# from django.http import JsonResponse
# from .check import check_geological_data_validity
# from .models import User, MySQLGeneralLog, OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo, \
#     GeologicalSketchRecordBackup
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib import messages  # 导入消息框架
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from django.contrib.auth import logout
# from django.shortcuts import redirect
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from .forms import GeologicalSketchRecordForm, ExcavationDiagnosisForm, OverUnderExcavationForm, TunnelContourForm
# from .models import GeologicalSketchRecord
# from django.db.models.signals import pre_save, post_delete
# from .signals import log_update_or_create, log_delete
# from django.db import transaction
# from .check import (
#     check_geological_data_validity,
#     check_excavation_diagnosis_validity,
#     check_excavation_calculation_validity,
#     check_tunnel_data_validity,
# )
# from django.shortcuts import render
# from .models import DataAuditTrail
# #下面是上传文件系统(file_management_project)的代码
# import os
# from django.shortcuts import render, redirect, get_object_or_404
# import hashlib
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from django.utils import timezone
# from django.http import HttpResponse, FileResponse
# from django.shortcuts import redirect
# import mimetypes
# from django.contrib import messages  # 用于发送消息
# from django.utils.http import urlquote
# from django.db import connection
# from records.models import DataStorage  # 假设 DataStorage 是在 records 应用中的模型
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.utils.timezone import now
# from .models import GeologicalSketchRecord
# from django.http import JsonResponse
# from django.utils.timezone import now
# from simple_history.utils import update_change_reason
# from django.core.paginator import Paginator
# #用户查看自己的待审批内容
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import GeologicalSketchRecord
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from django.db.models import Q
# import matplotlib.pyplot as plt
# import pandas as pd
# import io
# import base64
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import GeologicalSketchRecord
# import pandas as pd
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import GeologicalSketchRecord
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from records.backup import backup_all_tables, backup_table
# import logging
# logger = logging.getLogger(__name__)
# from django.db import DatabaseError
# from django.http import JsonResponse
# from django.shortcuts import render
# from .restore import get_backup_files, BACKUP_DIR ,restore_table_from_backup
# from records.models import (
#     GeologicalSketchRecordBackup,
#     OverUnderExcavationCalculationBackup,
#     ExcavationDiagnosisBackup,
#     TunnelContourInfoBackup,
# )
# import requests
#
# #主界面
# def index_view(request):
#     """主界面视图"""
#     print("主界面")
#     user = request.user if request.user.is_authenticated else None  # 检查用户是否登录
#     # return render(request, 'index.html', {'user': user})
#     return render(request, 'main.html', {'user': user})
#
#
# #注册
# def register_view(request):
#     """
#     处理用户注册请求。
#     支持普通用户 (user)、管理员 (admin)、审计员 (auditor) 的角色选择。
#     """
#     if request.method == 'POST':  # 处理 POST 请求
#         # 获取前端提交的注册表单数据
#         username = request.POST.get('username')  # 用户名
#         password = request.POST.get('password')  # 密码
#         confirm_password = request.POST.get('confirm-password')  # 确认密码
#         email = request.POST.get('email')  # 邮箱
#         role = request.POST.get('role', 'user')  # 用户角色，默认为普通用户 (user)
#
#         # 验证两次输入的密码是否一致
#         if password != confirm_password:
#             messages.error(request, '两次输入的密码不一致')  # 添加错误消息
#             return render(request, 'register.html')
#
#         # 检查用户名是否已存在
#         if User.objects.filter(username=username).exists():
#             messages.error(request, '用户名已存在')  # 添加错误消息
#             return render(request, 'register.html')
#
#         # 检查密码强度（可选，增强安全性）
#         if len(password) < 6 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
#             messages.error(request, '密码必须包含大小写字母、数字，且长度不少于6个字符')  # 添加错误消息
#             return render(request, 'register.html')
#
#         # 创建用户对象并保存到数据库
#         try:
#             user = User.objects.create(
#                 username=username,
#                 password=make_password(password),  # 对密码进行哈希加密
#                 email=email,
#                 role=role  # 分配角色：普通用户、管理员或审计员
#             )
#             user.save()  # 保存用户对象
#             messages.success(request, '注册成功！请登录')  # 添加成功消息
#             return redirect('login')  # 注册成功后跳转到登录页面
#         except Exception as e:
#             # 如果保存失败，返回错误信息到页面
#             messages.error(request, f'注册失败：{str(e)}')  # 添加错误消息
#             return render(request, 'register.html')
#
#     # 如果是 GET 请求，渲染注册页面
#     return render(request, 'register.html')
#
#
# #登录
# def login_view(request):
#     """登录视图"""
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         # 验证用户凭据
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#
#             # 强制将 next 参数设置为 index
#             next_url = request.GET.get('next', '/') #这样就可以登录之后跳到index了
#             print(f"Redirecting to: {next_url}")
#             return redirect(next_url)
#         else:
#             return render(request, 'login.html', {'error': '用户名或密码错误'})
#
#     return render(request, 'login.html')
#
#
# #退出登录
# def logout_view(request):
#     """登出视图"""
#     logout(request)  # 执行登出操作
#     return redirect('login')  # 登出后跳转到登录页面
#
#
# #掌子面信息上传（管理员）（支持excel导入版本）
# @login_required
# def upload_geological_info(request):
#     """
#     管理员上传地质信息视图（支持单条记录提交和 Excel 批量导入）。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")  # 调试输出提交类型
#
#         if submit_type == 'single':  # 单条记录提交
#             print("开始单条记录提交处理")
#             form = GeologicalSketchRecordForm(request.POST)
#             if form.is_valid():
#                 print("单条记录验证通过，准备保存")
#                 geological_record = form.save(commit=False)  # 保存表单数据到实例，但不提交到数据库
#                 geological_record.created_by = request.user  # 设置当前用户为创建者
#                 geological_record.status = 'uploaded_approved'  # 设置状态为已审批
#                 geological_record.save()  # 保存数据到数据库
#                 print("单条记录保存成功")
#                 return redirect('geological_list')  # 成功后重定向到地质记录列表页面
#             else:
#                 print("单条记录表单验证失败")
#                 print(f"表单错误: {form.errors}")  # 调试输出表单错误
#                 return render(
#                     request,
#                     'upload_geological_info.html',
#                     {'form': form, 'errors': form.errors}
#                 )
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 print("开始批量导入处理")
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     # 读取 Excel 文件，指定 openpyxl 引擎
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#                     print(f"读取到的 Excel 数据:\n{data.head()}")  # 调试输出 Excel 文件的前几行
#
#                     # 检查 Excel 数据的必填字段
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'distance',
#                         'design_section', 'inspector', 'measurement_date', 'excavation_width',
#                         'excavation_height', 'excavation_area', 'excavation_method',
#                         'face_condition', 'excavation_condition', 'rock_strength',
#                         'weathering_degree', 'crack_width', 'crack_shape', 'water_condition',
#                         'rockburst_tendency', 'rock_grade', 'karst_development', 'water_status'
#                     ]
#
#                     # 检查缺少的字段
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         return JsonResponse({
#                             "status": "error",
#                             "message": f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
#                         })
#
#                     # 强制转换字段类型
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = ['design_section', 'distance', 'excavation_width', 'excavation_height', 'excavation_area',
#                    'rock_strength', 'crack_width']
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')  # 转换为日期字符串
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce')  # 非数值将被置为 NaN
#                             if data[col].isnull().any():  # 如果存在 NaN 值
#                                 print(f"列 {col} 包含无法转换为数字的值。将替换为 0。")
#                                 print(f"问题值:\n{data[data[col].isnull()][col]}")  # 输出问题值
#                                 data[col] = data[col].fillna(0)  # 替换 NaN 为默认值 0
#
#                     # 保存每一行数据
#                     errors = []
#                     success_count = 0
#                     with transaction.atomic():  # 确保事务一致性
#                         for index, row in data.iterrows():
#                             print(f"正在处理第 {index + 1} 行数据: {row.to_dict()}")  # 调试输出当前行数据
#                             form_data = row.to_dict()  # 转换为字典格式
#                             form = GeologicalSketchRecordForm(form_data)
#
#                             if form.is_valid():
#                                 geological_record = form.save(commit=False)
#                                 geological_record.created_by = request.user
#                                 geological_record.status = 'uploaded_approved'
#                                 geological_record.save()
#                                 success_count += 1
#                                 print(f"第 {index + 1} 行数据保存成功")
#                             else:
#                                 print(f"第 {index + 1} 行数据验证失败: {form.errors}")  # 调试输出当前行错误
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     if errors:
#                         print(f"部分数据导入失败，共成功导入 {success_count} 条记录")
#                         return JsonResponse({
#                             "status": "partial_success",
#                             "message": f"批量导入完成，但有部分错误。",
#                             "success_count": success_count,
#                             "errors": errors
#                         })
#
#                     print(f"批量导入成功，共导入 {success_count} 条记录")
#                     return redirect('geological_list')  # 成功后重定向到地质记录列表页面
#
#                 except Exception as e:
#                     print(f"批量导入失败: {str(e)}")  # 调试输出异常信息
#                     return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})
#
#             print("未上传 Excel 文件")
#             return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})
#
#         else:
#             print("无效的提交类型")
#             return JsonResponse({"status": "error", "message": "无效的提交类型。"})
#
#     else:  # GET 请求
#         print("GET 请求，渲染空表单")
#         form = GeologicalSketchRecordForm()
#         return render(request, 'upload_geological_info.html', {'form': form})
#
#
# #清空session的
# @login_required
# def clear_message(request):
#     """清除 session 消息"""
#     request.session.pop('message', None)
#     request.session.pop('message_type', None)
#     return JsonResponse({'status': 'success'})
#
# ##掌子面信息上传（用户）
# # @login_required
# # def upload_geological_info_user(request):
# #     """
# #     用户上传地质信息视图。
# #     - 用户提交的数据状态设置为 `pending`。
# #     - 用户需要填写操作理由。
# #     """
# #     if request.method == 'POST':  # 处理表单提交
# #         form = GeologicalSketchRecordForm(request.POST)  # 将提交的数据绑定到表单
# #         if form.is_valid():  # 验证表单数据
# #             geological_record = form.save(commit=False)  # 保存表单数据到实例，但不提交到数据库
# #             geological_record.created_by = request.user  # 设置当前用户为创建者
# #             geological_record.status = 'pending'  # 设置记录状态为待审批
# #             geological_record.operation_reason = request.POST.get('operation_reason')  # 保存操作理由
# #             geological_record.save()  # 保存数据到数据库
# #             return redirect('user_records_view') #进入个人信息中心
# #         else:
# #             # 打印表单错误信息，方便调试
# #             print("Form Errors:", form.errors)
# #             return render(
# #                 request,
# #                 'upload_geological_info_user.html',  # 渲染用户上传模板
# #                 {'form': form, 'errors': form.errors}
# #             )
# #     else:
# #         # 如果是 GET 请求，渲染空表单
# #         form = GeologicalSketchRecordForm()
# #     return render(request, 'upload_geological_info_user.html', {'form': form})
#
#
# ## 掌子面信息上传（用户）（支持批量导入）
# @login_required
# def upload_geological_info_user(request):
#     """
#     用户上传地质信息视图。
#     - 支持单条记录和 Excel 批量导入。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")  # 调试输出提交类型
#
#         if submit_type == 'single':  # 单条记录提交
#             form = GeologicalSketchRecordForm(request.POST)
#             if form.is_valid():
#                 geological_record = form.save(commit=False)
#                 geological_record.created_by = request.user
#                 geological_record.operation_reason = request.POST.get('operation_reason')
#
#                 is_valid, validation_errors = check_geological_data_validity(geological_record)
#
#                 if is_valid:
#                     geological_record.status = 'uploaded_approved'
#                 else:
#                     geological_record.status = 'pending'
#
#                 geological_record.save()
#                 if not is_valid:
#                     request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
#                     request.session['message_type'] = "warning"
#
#                 return redirect('user_records_view')  # 跳转到个人信息中心
#
#             else:
#                 request.session['message'] = "单条提交失败，请检查数据格式。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#
#                     # 必填字段校验
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'distance',
#                         'design_section', 'inspector', 'measurement_date', 'excavation_width',
#                         'excavation_height', 'excavation_area', 'excavation_method',
#                         'face_condition', 'excavation_condition', 'rock_strength',
#                         'weathering_degree', 'crack_width', 'crack_shape', 'water_condition',
#                         'rockburst_tendency', 'rock_grade', 'karst_development', 'water_status', 'operation_reason'
#                     ]
#
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     # 数据类型转换
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = ['distance', 'design_section', 'excavation_width', 'excavation_height', 'excavation_area',
#                                        'rock_strength', 'crack_width']
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     # 保存记录
#                     errors = []
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = GeologicalSketchRecordForm(form_data)
#
#                             if form.is_valid():
#                                 geological_record = form.save(commit=False)
#                                 geological_record.created_by = request.user
#
#                                 is_valid, _ = check_geological_data_validity(geological_record)
#
#                                 if is_valid:
#                                     geological_record.status = 'uploaded_approved'
#                                 else:
#                                     geological_record.status = 'pending'
#
#                                 geological_record.save()
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     # 判断批量导入结果
#                     if errors:
#                         request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     return redirect('user_records_view')  # 全部成功直接跳转
#
#                 except Exception as e:
#                     request.session['message'] = f"批量导入失败: {str(e)}"
#                     request.session['message_type'] = "error"
#                     return redirect('user_records_view')
#
#             else:
#                 request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#     else:
#         form = GeologicalSketchRecordForm()
#     return render(request, 'upload_geological_info_user.html', {'form': form})
#
#
# ## 超欠挖计算信息上传（用户，支持批量导入）
# @login_required
# def upload_excavation_calculation_user(request):
#     """
#     用户上传超欠挖计算信息视图。
#     - 支持单条记录和 Excel 批量导入。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")  # 调试输出提交类型
#
#         if submit_type == 'single':  # 单条记录提交
#             form = OverUnderExcavationForm(request.POST)
#             if form.is_valid():
#                 calculation_record = form.save(commit=False)
#                 calculation_record.created_by = request.user
#                 calculation_record.operation_reason = request.POST.get('operation_reason')
#
#                 is_valid, validation_errors = check_excavation_diagnosis_validity(calculation_record)
#
#                 if is_valid:
#                     calculation_record.status = 'uploaded_approved'
#                 else:
#                     calculation_record.status = 'pending'
#
#                 calculation_record.save()
#                 if not is_valid:
#                     request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
#                     request.session['message_type'] = "warning"
#
#                 return redirect('user_records_view')  # 跳转到个人信息中心
#
#             else:
#                 request.session['message'] = "单条提交失败，请检查数据格式。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#
#                     # 必填字段校验
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#                         'line_name', 'north_direction_angle', 'radius', 'length',
#                         'east_coordinate', 'north_coordinate', 'start_offset', 'height',
#                         'radius_section', 'angle_increment', 'operation_reason'
#                     ]
#
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     # 数据类型转换
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = [
#                         'north_direction_angle', 'radius', 'length', 'east_coordinate',
#                         'north_coordinate', 'start_offset', 'height', 'radius_section', 'angle_increment'
#                     ]
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     # 保存记录
#                     errors = []
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = OverUnderExcavationForm(form_data)
#
#                             if form.is_valid():
#                                 calculation_record = form.save(commit=False)
#                                 calculation_record.created_by = request.user
#
#                                 is_valid, _ = check_excavation_diagnosis_validity(calculation_record)
#
#                                 if is_valid:
#                                     calculation_record.status = 'uploaded_approved'
#                                 else:
#                                     calculation_record.status = 'pending'
#
#                                 calculation_record.save()
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     # 判断批量导入结果
#                     if errors:
#                         request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     return redirect('user_records_view')  # 全部成功直接跳转
#
#                 except Exception as e:
#                     request.session['message'] = f"批量导入失败: {str(e)}"
#                     request.session['message_type'] = "error"
#                     return redirect('user_records_view')
#
#             else:
#                 request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#     else:
#         form = OverUnderExcavationForm()
#     return render(request, 'upload_info3_user.html', {'form': form})
#
#
#
# ## 超欠挖诊断信息上传（用户，支持批量导入）
# @login_required
# def upload_excavation_diagnosis_user(request):
#     """
#     用户上传超欠挖诊断信息视图。
#     - 支持单条记录和 Excel 批量导入。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")  # 调试输出提交类型
#
#         if submit_type == 'single':  # 单条记录提交
#             form = ExcavationDiagnosisForm(request.POST)
#             if form.is_valid():
#                 diagnosis_record = form.save(commit=False)
#                 diagnosis_record.created_by = request.user
#                 diagnosis_record.operation_reason = request.POST.get('operation_reason')
#
#                 is_valid, validation_errors = check_excavation_calculation_validity(diagnosis_record)
#
#                 if is_valid:
#                     diagnosis_record.status = 'uploaded_approved'
#                 else:
#                     diagnosis_record.status = 'pending'
#
#                 diagnosis_record.save()
#                 if not is_valid:
#                     request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
#                     request.session['message_type'] = "warning"
#
#                 return redirect('user_records_view')  # 跳转到个人信息中心
#
#             else:
#                 request.session['message'] = "单条提交失败，请检查数据格式。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#
#                     # 必填字段校验
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#                         'scale', 'mileage', 'design_section', 'line_x', 'line_y',
#                         'measured_section', 'reference_section', 'line_height', 'over_excavation_area',
#                         'under_excavation_area', 'max_over_excavation', 'max_under_excavation',
#                         'average_over_excavation', 'average_under_excavation', 'diagnosis_result', 'inspector', 'operation_reason'
#                     ]
#
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     # 数据类型转换
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = [
#                         'scale', 'mileage', 'design_section', 'line_x', 'line_y',
#                         'measured_section', 'reference_section', 'line_height',
#                         'over_excavation_area', 'under_excavation_area',
#                         'max_over_excavation', 'max_under_excavation',
#                         'average_over_excavation', 'average_under_excavation'
#                     ]
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     # 保存记录
#                     errors = []
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = ExcavationDiagnosisForm(form_data)
#
#                             if form.is_valid():
#                                 diagnosis_record = form.save(commit=False)
#                                 diagnosis_record.created_by = request.user
#
#                                 is_valid, _ = check_excavation_calculation_validity(diagnosis_record)
#
#                                 if is_valid:
#                                     diagnosis_record.status = 'uploaded_approved'
#                                 else:
#                                     diagnosis_record.status = 'pending'
#
#                                 diagnosis_record.save()
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     # 判断批量导入结果
#                     if errors:
#                         request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     return redirect('user_records_view')  # 全部成功直接跳转
#
#                 except Exception as e:
#                     request.session['message'] = f"批量导入失败: {str(e)}"
#                     request.session['message_type'] = "error"
#                     return redirect('user_records_view')
#
#             else:
#                 request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#     else:
#         form = ExcavationDiagnosisForm()
#     return render(request, 'upload_info2_user.html', {'form': form})
#
#
# ## 隧道信息上传（用户，支持批量导入）
# @login_required
# def upload_tunnel_info_user(request):
#     """
#     用户上传隧道信息视图。
#     - 支持单条记录和 Excel 批量导入。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")  # 调试输出提交类型
#
#         if submit_type == 'single':  # 单条记录提交
#             form = TunnelContourForm(request.POST)
#             if form.is_valid():
#                 tunnel_info = form.save(commit=False)
#                 tunnel_info.created_by = request.user
#                 tunnel_info.operation_reason = request.POST.get('operation_reason')
#
#                 is_valid, validation_errors = check_tunnel_data_validity(tunnel_info)
#
#                 if is_valid:
#                     tunnel_info.status = 'uploaded_approved'
#                 else:
#                     tunnel_info.status = 'pending'
#
#                 tunnel_info.save()
#                 if not is_valid:
#                     request.session['message'] = f"单条提交成功，但部分数据未达标: {', '.join(validation_errors)}"
#                     request.session['message_type'] = "warning"
#
#                 return redirect('user_records_view')  # 跳转到个人信息中心
#
#             else:
#                 request.session['message'] = "单条提交失败，请检查数据格式。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#
#                     # 必填字段校验
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#                         'inspector', 'od', 'rcl', 'vo', 'cr',
#                         'w1', 'w2', 'w3', 'c1', 'c2', 'c3', 'operation_reason'
#                     ]
#
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         request.session['message'] = f"批量导入失败: 缺少必要字段 {', '.join(missing_columns)}"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     # 数据类型转换
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = ['od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3']
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     # 保存记录
#                     errors = []
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = TunnelContourForm(form_data)
#
#                             if form.is_valid():
#                                 tunnel_info = form.save(commit=False)
#                                 tunnel_info.created_by = request.user
#
#                                 is_valid, _ = check_tunnel_data_validity(tunnel_info)
#
#                                 if is_valid:
#                                     tunnel_info.status = 'uploaded_approved'
#                                 else:
#                                     tunnel_info.status = 'pending'
#
#                                 tunnel_info.save()
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     # 判断批量导入结果
#                     if errors:
#                         request.session['message'] = f"批量导入部分失败，共 {len(errors)} 条记录有问题。"
#                         request.session['message_type'] = "error"
#                         return redirect('user_records_view')
#
#                     return redirect('user_records_view')  # 全部成功直接跳转
#
#                 except Exception as e:
#                     request.session['message'] = f"批量导入失败: {str(e)}"
#                     request.session['message_type'] = "error"
#                     return redirect('user_records_view')
#
#             else:
#                 request.session['message'] = "未上传 Excel 文件，无法进行批量导入。"
#                 request.session['message_type'] = "error"
#                 return redirect('user_records_view')
#
#     else:
#         form = TunnelContourForm()
#     return render(request, 'upload_info1_user.html', {'form': form})
#
#
#
#
#
# # 超欠挖诊断信息上传（管理员）（支持excel导入版本）
# @login_required
# def upload_info2(request):
#     """
#     管理员上传超欠挖诊断信息视图（支持单条记录提交和 Excel 批量导入）。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')  # 获取提交类型
#         print(f"提交类型: {submit_type}")
#
#         if submit_type == 'single':  # 单条记录提交
#             form = ExcavationDiagnosisForm(request.POST)
#             if form.is_valid():
#                 diagnosis_record = form.save(commit=False)
#                 diagnosis_record.created_by = request.user
#                 diagnosis_record.status = 'uploaded_approved'
#                 diagnosis_record.save()
#                 print("单条记录保存成功")
#                 return redirect('excavation_diagnosis_list')
#             else:
#                 print("单条记录表单验证失败")
#                 return render(request, 'upload_info2.html', {'form': form, 'errors': form.errors})
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#                     required_columns = [
#                         'face_id', 'project_id', 'measurement_date', 'inspection_date',
#                         'scale', 'mileage', 'design_section', 'line_x', 'line_y',
#                         'measured_section', 'reference_section', 'line_height',
#                         'over_excavation_area', 'under_excavation_area',
#                         'max_over_excavation', 'max_under_excavation',
#                         'average_over_excavation', 'average_under_excavation',
#                         'diagnosis_result', 'inspector'
#                     ]
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})
#
#                     date_columns = ['measurement_date', 'inspection_date']
#                     numeric_columns = ['scale', 'mileage', 'design_section',
#                                        'line_x', 'line_y', 'measured_section',
#                                        'reference_section', 'line_height',
#                                        'over_excavation_area', 'under_excavation_area',
#                                        'max_over_excavation', 'max_under_excavation',
#                                        'average_over_excavation', 'average_under_excavation']
#
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     errors = []
#                     success_count = 0
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form = ExcavationDiagnosisForm(row.to_dict())
#                             if form.is_valid():
#                                 diagnosis_record = form.save(commit=False)
#                                 diagnosis_record.created_by = request.user
#                                 diagnosis_record.status = 'uploaded_approved'
#                                 diagnosis_record.save()
#                                 success_count += 1
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     if errors:
#                         return JsonResponse({
#                             "status": "partial_success",
#                             "message": f"批量导入完成，但有部分错误。",
#                             "success_count": success_count,
#                             "errors": errors
#                         })
#
#                     return redirect('excavation_diagnosis_list')
#
#                 except Exception as e:
#                     return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})
#
#             return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})
#
#         else:
#             return JsonResponse({"status": "error", "message": "无效的提交类型。"})
#
#     else:
#         form = ExcavationDiagnosisForm()
#         return render(request, 'upload_info2.html', {'form': form})
#
#
# # 超欠挖计算信息上传（管理员）（支持excel导入版本）
# @login_required
# def upload_info3(request):
#     """
#     管理员上传超欠挖计算信息视图（支持单条记录提交和 Excel 批量导入）。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')
#         print(f"提交类型: {submit_type}")
#
#         if submit_type == 'single':  # 单条记录提交
#             form = OverUnderExcavationForm(request.POST)
#             if form.is_valid():
#                 calculation_record = form.save(commit=False)
#                 calculation_record.created_by = request.user
#                 calculation_record.status = 'uploaded_approved'
#                 calculation_record.save()
#                 print("单条记录保存成功")
#                 return redirect('excavation_calculation_list')
#             else:
#                 print("单条记录表单验证失败")
#                 return render(request, 'upload_info3.html', {'form': form, 'errors': form.errors})
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#                     print(f"读取到的 Excel 数据:\n{data.head()}")
#
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#                         'inspector', 'line_name', 'north_direction_angle', 'radius',
#                         'length', 'east_coordinate', 'north_coordinate', 'start_offset',
#                         'height', 'radius_section', 'angle_increment'
#                     ]
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})
#
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = [
#                         'north_direction_angle', 'radius', 'length', 'east_coordinate',
#                         'north_coordinate', 'start_offset', 'height', 'radius_section',
#                         'angle_increment'
#                     ]
#
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     errors = []
#                     success_count = 0
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = OverUnderExcavationForm(form_data)
#                             if form.is_valid():
#                                 calculation_record = form.save(commit=False)
#                                 calculation_record.created_by = request.user
#                                 calculation_record.status = 'uploaded_approved'
#                                 calculation_record.save()
#                                 success_count += 1
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     if errors:
#                         return JsonResponse({
#                             "status": "partial_success",
#                             "message": f"批量导入完成，但有部分错误。",
#                             "success_count": success_count,
#                             "errors": errors
#                         })
#
#                     print(f"批量导入成功，共导入 {success_count} 条记录")
#                     return redirect('excavation_calculation_list')
#
#                 except Exception as e:
#                     print(f"批量导入失败: {str(e)}")
#                     return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})
#
#             return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})
#
#         else:
#             return JsonResponse({"status": "error", "message": "无效的提交类型。"})
#
#     else:
#         form = OverUnderExcavationForm()
#         return render(request, 'upload_info3.html', {'form': form})
#
#
# # 隧道轮廓信息上传（管理员）（支持excel导入版本）
# @login_required
# def upload_info1(request):
#     """
#     管理员上传隧道轮廓信息视图（支持单条记录提交和 Excel 批量导入）。
#     """
#     if request.method == 'POST':
#         submit_type = request.POST.get('submit_type', 'single')
#         print(f"提交类型: {submit_type}")
#
#         if submit_type == 'single':  # 单条记录提交
#             form = TunnelContourForm(request.POST)
#             if form.is_valid():
#                 profile_record = form.save(commit=False)
#                 profile_record.created_by = request.user
#                 profile_record.status = 'uploaded_approved'
#                 profile_record.save()
#                 print("单条记录保存成功")
#                 return redirect('tunnel_contour_info_list')
#             else:
#                 print("单条记录表单验证失败")
#                 return render(request, 'upload_info1.html', {'form': form, 'errors': form.errors})
#
#         elif submit_type == 'bulk':  # 批量导入
#             if 'excel_file' in request.FILES:
#                 excel_file = request.FILES['excel_file']
#                 try:
#                     data = pd.read_excel(excel_file, engine='openpyxl')
#                     print(f"读取到的 Excel 数据:\n{data.head()}")
#
#                     required_columns = [
#                         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#                         'inspector', 'od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3'
#                     ]
#                     missing_columns = [col for col in required_columns if col not in data.columns]
#                     if missing_columns:
#                         return JsonResponse({"status": "error", "message": f"缺少必要字段 {', '.join(missing_columns)}"})
#
#                     date_columns = ['inspection_date', 'measurement_date']
#                     numeric_columns = ['od', 'rcl', 'vo', 'cr', 'w1', 'w2', 'w3', 'c1', 'c2', 'c3']
#
#                     for col in date_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_datetime(data[col], errors='coerce').dt.strftime('%Y-%m-%d')
#                     for col in numeric_columns:
#                         if col in data.columns:
#                             data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)
#
#                     errors = []
#                     success_count = 0
#                     with transaction.atomic():
#                         for index, row in data.iterrows():
#                             form_data = row.to_dict()
#                             form = TunnelContourForm(form_data)
#                             if form.is_valid():
#                                 profile_record = form.save(commit=False)
#                                 profile_record.created_by = request.user
#                                 profile_record.status = 'uploaded_approved'
#                                 profile_record.save()
#                                 success_count += 1
#                             else:
#                                 errors.append({"row": index + 1, "errors": form.errors.as_json()})
#
#                     if errors:
#                         return JsonResponse({
#                             "status": "partial_success",
#                             "message": f"批量导入完成，但有部分错误。",
#                             "success_count": success_count,
#                             "errors": errors
#                         })
#
#                     print(f"批量导入成功，共导入 {success_count} 条记录")
#                     return redirect('tunnel_contour_info_list')
#
#                 except Exception as e:
#                     print(f"批量导入失败: {str(e)}")
#                     return JsonResponse({"status": "error", "message": f"批量导入失败: {str(e)}"})
#
#             return JsonResponse({"status": "error", "message": "未上传 Excel 文件。"})
#
#         else:
#             return JsonResponse({"status": "error", "message": "无效的提交类型。"})
#
#     else:
#         form = TunnelContourForm()
#         return render(request, 'upload_info1.html', {'form': form})
#
#
#
#
# #地质信息展示
# #掌子面信息记录
# @login_required
# def geological_list(request):
#     """
#     掌子面信息展示视图，支持按 face_id 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 获取所有地质记录，状态筛选
#     records = GeologicalSketchRecord.objects.filter(
#         status__in=['uploaded_approved', 'modified_approved', 'deleted']
#     )
#
#     # 根据搜索条件过滤数据
#     if search_query:
#         records = records.filter(face_id__icontains=search_query)
#
#     # 设置分页
#     paginator = Paginator(records, 8)  # 每页显示8条记录
#     page_number = request.GET.get('page')  # 获取当前页码
#     page_obj = paginator.get_page(page_number)  # 获取当前页的数据
#
#     # 渲染模板并传递上下文
#     return render(request, 'geological_list.html', {
#         'page_obj': page_obj,
#         'search_query': search_query,  # 用于保留搜索条件
#     })
#
# # # 超欠挖计算记录
# @login_required
# def excavation_calculation_list(request):
#     """
#     超欠挖计算信息展示视图，支持按 face_id 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 获取所有记录，状态筛选
#     records = OverUnderExcavationCalculation.objects.filter(
#         status__in=['uploaded_approved', 'modified_approved', 'deleted']
#     )
#
#     # 根据搜索条件过滤数据
#     if search_query:
#         records = records.filter(face_id__icontains=search_query)
#
#     # 设置分页
#     paginator = Paginator(records, 8)  # 每页显示 8 条记录
#     page_number = request.GET.get('page')  # 获取当前页码
#     page_obj = paginator.get_page(page_number)  # 获取当前页的数据
#
#     # 渲染模板并传递上下文
#     return render(request, 'excavation_calculation_list.html', {
#         'page_obj': page_obj,
#         'search_query': search_query,  # 用于保留搜索条件
#     })
#
# # 超欠挖诊断记录
# @login_required
# def excavation_diagnosis_list(request):
#     """
#     超欠挖诊断信息展示视图，支持按 face_id 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 获取所有记录，状态筛选
#     records = ExcavationDiagnosis.objects.filter(
#         status__in=['uploaded_approved', 'modified_approved', 'deleted']
#     )
#
#     # 根据搜索条件过滤数据
#     if search_query:
#         records = records.filter(face_id__icontains=search_query)
#
#     # 设置分页
#     paginator = Paginator(records, 8)  # 每页显示 8 条记录
#     page_number = request.GET.get('page')  # 获取当前页码
#     page_obj = paginator.get_page(page_number)  # 获取当前页的数据
#
#     # 渲染模板并传递上下文
#     return render(request, 'excavation_diagnosis_list.html', {
#         'page_obj': page_obj,
#         'search_query': search_query,  # 用于保留搜索条件
#     })
#
# # 隧道轮廓信息记录
# @login_required
# def tunnel_contour_info_list(request):
#     """
#     隧道轮廓信息展示视图，支持按 face_id 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 获取所有记录，状态筛选
#     records = TunnelContourInfo.objects.filter(
#         status__in=['uploaded_approved', 'modified_approved', 'deleted']
#     )
#
#     # 根据搜索条件过滤数据
#     if search_query:
#         records = records.filter(face_id__icontains=search_query)
#
#     # 设置分页
#     paginator = Paginator(records, 8)  # 每页显示 8 条记录
#     page_number = request.GET.get('page')  # 获取当前页码
#     page_obj = paginator.get_page(page_number)  # 获取当前页的数据
#
#     # 渲染模板并传递上下文
#     return render(request, 'tunnel_contour_list.html', {
#         'page_obj': page_obj,
#         'search_query': search_query,  # 用于保留搜索条件
#     })
#
# #查看修改日志
# @login_required
# def view_geological_logs(request):
#     # 查询日志中包含 `UPDATE geological_sketch_record` 的记录
#     logs = MySQLGeneralLog.objects.filter(argument__icontains='UPDATE geological_sketch_record')
#     return render(request, 'view_logs.html', {'logs': logs})
#
#
# #修改掌子面信息(管理员)
# def edit_geological_record(request, pk):  # 参数名为 pk，与 URL 配置一致
#     record = get_object_or_404(GeologicalSketchRecord, pk=pk)
#
#     if request.method == "POST":
#         form = GeologicalSketchRecordForm(request.POST, instance=record)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.modified_by = request.user  # 设置修改人
#             record.save()  # 保存记录
#             return redirect('geological_record_detail', pk=record.pk)
#     else:
#         form = GeologicalSketchRecordForm(instance=record)
#
#     return render(request, 'edit_geological_record.html', {'form': form, 'record': record})
#
# # 修改超欠挖计算信息（管理员）
# @login_required
# def edit_over_under_excavation(request, pk):
#     """
#     管理员修改超欠挖计算记录视图：
#     - 根据记录 ID 加载相应记录
#     - 提交表单时保存修改，并记录修改人
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, pk=pk)
#
#     if request.method == "POST":
#         form = OverUnderExcavationForm(request.POST, instance=record)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.modified_by = request.user  # 设置修改人
#             record.save()  # 保存修改后的记录
#             return redirect('over_under_excavation_record_detail', pk=record.pk)
#     else:
#         form = OverUnderExcavationForm(instance=record)
#
#     return render(request, 'edit_over_under_excavation.html', {'form': form, 'record': record})
#
# # 修改超欠挖诊断信息（管理员）
# @login_required
# def edit_excavation_diagnosis(request, pk):
#     """
#     管理员修改超欠挖诊断记录视图：
#     - 根据记录 ID 加载相应记录
#     - 提交表单时保存修改，并记录修改人
#     """
#     record = get_object_or_404(ExcavationDiagnosis, pk=pk)
#
#     if request.method == "POST":
#         form = ExcavationDiagnosisForm(request.POST, instance=record)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.modified_by = request.user  # 设置修改人
#             record.save()  # 保存修改后的记录
#             return redirect('excavation_diagnosis_record_detail', pk=record.pk)
#     else:
#         form = ExcavationDiagnosisForm(instance=record)
#
#     return render(request, 'edit_excavation_diagnosis.html', {'form': form, 'record': record})
#
# # 修改隧道轮廓信息（管理员）
# @login_required
# def edit_tunnel_contour(request, pk):
#     """
#     管理员修改隧道轮廓信息记录视图：
#     - 根据记录 ID 加载相应记录
#     - 提交表单时保存修改，并记录修改人
#     """
#     record = get_object_or_404(TunnelContourInfo, pk=pk)
#
#     if request.method == "POST":
#         form = TunnelContourForm(request.POST, instance=record)
#         if form.is_valid():
#             record = form.save(commit=False)
#             record.modified_by = request.user  # 设置修改人
#             record.save()  # 保存修改后的记录
#             return redirect('tunnel_contour_record_detail', pk=record.pk)
#     else:
#         form = TunnelContourForm(instance=record)
#
#     return render(request, 'edit_tunnel_contour.html', {'form': form, 'record': record})
#
#
#
# #掌子面删除（管理员）
# @login_required
# def delete_geological_record(request, record_id):
#     """
#     管理员删除地质记录。
#     """
#     print(f"User: {request.user}, Role: {getattr(request.user, 'role', None)}")
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id)
#
#     # 使用自定义字段检查管理员权限
#     if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
#         return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)
#
#     if request.method == 'POST':
#         record.delete()
#         print(f"Record {record_id} deleted successfully.")
#         return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})
#
#     return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)
#
# #超欠挖计算删除（管理员）
# @login_required
# def delete_over_under_excavation_record(request, record_id):
#     """
#     管理员删除超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)
#
#     # 使用自定义字段检查管理员权限
#     if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
#         return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)
#
#     if request.method == 'POST':
#         record.delete()
#         return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})
#
#     return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)
#
#
# #超欠挖诊断删除（管理员）
# @login_required
# def delete_excavation_diagnosis_record(request, record_id):
#     """
#     管理员删除超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id)
#
#     # 使用自定义字段检查管理员权限
#     if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
#         return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)
#
#     if request.method == 'POST':
#         record.delete()
#         return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})
#
#     return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)
#
#
# #隧道轮廓信息删除（管理员）
# @login_required
# def delete_tunnel_contour_record(request, record_id):
#     """
#     管理员删除隧道轮廓记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id)
#
#     # 使用自定义字段检查管理员权限
#     if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
#         return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)
#
#     if request.method == 'POST':
#         record.delete()
#         return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})
#
#     return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)
#
#
# # 日志信息列表
# def view_audit_logs(request):
#     # 获取筛选条件
#     user = request.GET.get('user', '')  # 默认为空字符串，表示不筛选用户
#     operation_type = request.GET.get('operation_type', '')  # 筛选操作类型
#     table_name = request.GET.get('table_name', '')  # 筛选操作表
#     date_from = request.GET.get('date_from', '')  # 筛选起始日期
#     date_to = request.GET.get('date_to', '')  # 筛选结束日期
#
#     # 初始化查询集
#     logs_list = DataAuditTrail.objects.all()
#
#     # 应用筛选条件
#     if user:
#         logs_list = logs_list.filter(user__username__icontains=user)
#     if operation_type:
#         logs_list = logs_list.filter(operation_type=operation_type)
#     if table_name:
#         logs_list = logs_list.filter(table_name=table_name)
#     if date_from:
#         logs_list = logs_list.filter(operation_time__gte=date_from)
#     if date_to:
#         logs_list = logs_list.filter(operation_time__lte=date_to)
#
#     logs_list = logs_list.order_by('-operation_time')  # 按操作时间倒序排序
#
#     # 分页
#     paginator = Paginator(logs_list, 10)  # 每页 10 条记录
#     page = request.GET.get('page')
#     try:
#         logs = paginator.page(page)
#     except PageNotAnInteger:
#         logs = paginator.page(1)
#     except EmptyPage:
#         logs = paginator.page(paginator.num_pages)
#
#     # 保留筛选条件的查询参数
#     query_params = request.GET.copy()  # 将筛选参数复制为可变的 QueryDict
#     query_params.pop('page', None)  # 移除分页参数，防止重复
#     query_params_encoded = query_params.urlencode()  # 编码为 URL 查询字符串
#
#     # 传递筛选条件和分页数据
#     return render(request, 'view_audit_logs.html', {
#         'logs': logs,
#         'filters': {
#             'user': user,
#             'operation_type': operation_type,
#             'table_name': table_name,
#             'date_from': date_from,
#             'date_to': date_to,
#         },
#         'operation_types': DataAuditTrail.objects.values_list('operation_type', flat=True).distinct(),
#         'table_names': DataAuditTrail.objects.values_list('table_name', flat=True).distinct(),
#         'query_params': query_params_encoded,  # 将筛选参数编码并传递给模板
#     })
#
#
#
# # 详细日志信息
# def view_log_detail(request, log_id):
#     # 获取指定日志记录
#     log = get_object_or_404(DataAuditTrail, id=log_id)
#
#     # 解析 JSON 数据
#     try:
#         data_snapshot = json.loads(log.data_snapshot) if log.data_snapshot else None
#         updated_data = json.loads(log.updated_data) if log.updated_data else None
#         change_details = json.loads(log.change_details) if log.change_details else None
#     except json.JSONDecodeError:
#         data_snapshot = updated_data = change_details = None  # 防止解析失败
#
#     return render(request, 'log_detail.html', {
#         'log': log,
#         'data_snapshot': data_snapshot,
#         'updated_data': updated_data,
#         'change_details': change_details,
#     })
#
#
# #展示修改后的详细掌子面信息
# def geological_record_detail(request, pk):
#     record = get_object_or_404(GeologicalSketchRecord, pk=pk)
#     return render(request, 'geological_record_detail.html', {'record': record})
#
# #展示修改后的详细超欠挖诊断信息
# @login_required
# def excavation_diagnosis_detail(request, pk):
#     """
#     展示超欠挖诊断详细信息。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, pk=pk)
#     return render(request, 'excavation_diagnosis_detail.html', {'record': record})
#
# #展示修改后的详细超欠挖计算信息
# @login_required
# def over_under_excavation_detail(request, pk):
#     """
#     展示超欠挖计算详细信息。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, pk=pk)
#     return render(request, 'over_under_excavation_detail.html', {'record': record})
#
# #展示修改后的隧道信息
# @login_required
# def tunnel_contour_detail(request, pk):
#     """
#     展示隧道轮廓详细信息。
#     """
#     record = get_object_or_404(TunnelContourInfo, pk=pk)
#     return render(request, 'tunnel_contour_detail.html', {'record': record})
#
#
# #哈希函数
# def hash_file(file):
#     hasher = hashlib.sha256()
#     for chunk in file.chunks():
#         hasher.update(chunk)
#     return hasher.hexdigest()
#
# #文件上传
# @login_required
# def upload_file(request):
#     """
#     文件上传视图，支持选择文件关联类别和关联记录编号。
#     """
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#         file_name = uploaded_file.name
#         mime_type = uploaded_file.content_type
#
#         # 文件类型映射
#         if mime_type.startswith('image/'):
#             file_type = 'image'
#         elif mime_type == 'application/pdf':
#             file_type = 'pdf'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#             'application/msword'
#         ]:
#             file_type = 'word'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#             'application/vnd.ms-excel'
#         ]:
#             file_type = 'excel'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.presentationml.presentation',
#             'application/vnd.ms-powerpoint',
#             'application/powerpoint',
#             'application/x-mspowerpoint'
#         ]:
#             file_type = 'ppt'
#         elif mime_type == 'text/plain':
#             file_type = 'text'
#         elif mime_type in [
#             'application/zip',
#             'application/x-zip-compressed',
#             'multipart/x-zip'
#         ]:
#             file_type = 'zip'
#         elif mime_type == 'application/vnd.rar':
#             file_type = 'rar'
#         elif mime_type == 'application/x-7z-compressed':
#             file_type = '7z'
#         elif mime_type == 'application/octet-stream':
#             file_type = 'binary'
#         else:
#             file_type = os.path.splitext(file_name)[1]  # 未知类型时取文件后缀
#
#         # 读取文件数据和计算哈希值
#         file_data = uploaded_file.read()
#         file_hash = hash_file(uploaded_file)
#         uploaded_file.seek(0)  # 重置文件指针
#
#         # 检查重复文件
#         if DataStorage.objects.filter(file_hash=file_hash).exists():
#             messages.error(request, "该文件已存在，不能重复上传。")
#             return redirect('upload')
#
#         # 使用 default_storage 保存文件到文件系统
#         file_path = default_storage.save(f'uploads/{file_name}', ContentFile(file_data))
#
#         # 获取其他表单字段
#         file_description = request.POST.get('file_description', '')
#         category = request.POST.get('file_category', '')  # 修改为 file_category
#         related_record_id = request.POST.get('related_record_id', None)
#         operation_reason = request.POST.get('operation_reason', '')
#
#         # 校验 file_category 是否合法
#         valid_categories = ['geological', 'excavation_diagnosis', 'excavation_calculation', 'tunnel', 'other']
#         if category not in valid_categories:
#             messages.error(request, "请选择有效的文件关联类别！")
#             return redirect('upload')
#
#         # 保存文件记录到数据库
#         DataStorage.objects.create(
#             file_name=file_name,
#             file_path=file_path,
#             file_data=file_data,
#             file_type=file_type,
#             file_hash=file_hash,
#             file_description=file_description,
#             category=category,  # 修改为 file_category
#             related_record_id=related_record_id,
#             uploaded_by=request.user,
#             status='uploaded_approved',  # 默认设置为管理员审批通过
#             approved_by=request.user,
#             approved_at=timezone.now(),
#             operation_reason=operation_reason
#         )
#
#         messages.success(request, "文件上传成功！")
#         return redirect('upload')
#
#     return render(request, 'upload.html')
#
#
#
# #修改文件
# @login_required
# def update_file(request, file_id):
#     """
#     文件修改视图：支持上传新文件替换现有文件，并保留上传视图的所有逻辑。
#     """
#     # 获取文件记录
#     file_record = get_object_or_404(DataStorage, id=file_id)
#
#     if request.method == 'POST' and request.FILES.get('file'):
#         uploaded_file = request.FILES['file']
#         file_name = uploaded_file.name
#         mime_type = uploaded_file.content_type
#
#         # 文件类型映射
#         if mime_type.startswith('image/'):
#             file_type = 'image'
#         elif mime_type == 'application/pdf':
#             file_type = 'pdf'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
#             'application/msword'
#         ]:
#             file_type = 'word'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
#             'application/vnd.ms-excel'
#         ]:
#             file_type = 'excel'
#         elif mime_type in [
#             'application/vnd.openxmlformats-officedocument.presentationml.presentation',
#             'application/vnd.ms-powerpoint',
#             'application/powerpoint',
#             'application/x-mspowerpoint'
#         ]:
#             file_type = 'ppt'
#         elif mime_type == 'text/plain':
#             file_type = 'text'
#         elif mime_type in [
#             'application/zip',
#             'application/x-zip-compressed',
#             'multipart/x-zip'
#         ]:
#             file_type = 'zip'
#         elif mime_type == 'application/vnd.rar':
#             file_type = 'rar'
#         elif mime_type == 'application/x-7z-compressed':
#             file_type = '7z'
#         elif mime_type == 'application/octet-stream':
#             file_type = 'binary'
#         else:
#             file_type = os.path.splitext(file_name)[1]  # 未知类型时取文件后缀
#
#         # 读取文件数据和计算哈希值
#         file_data = uploaded_file.read()
#         file_hash = hash_file(uploaded_file)
#         uploaded_file.seek(0)  # 重置文件指针
#
#         # 检查重复文件
#         if DataStorage.objects.filter(file_hash=file_hash).exclude(id=file_id).exists():
#             messages.error(request, "该文件已存在，不能重复上传。")
#             return redirect('update_file', file_id=file_id)
#
#         # 使用 default_storage 保存新文件到文件系统
#         new_file_path = default_storage.save(f'uploads/{file_name}', ContentFile(file_data))
#
#         # 删除旧文件（如果存在）
#         if file_record.file_path:
#             default_storage.delete(file_record.file_path)
#
#         # 获取其他表单字段
#         file_description = request.POST.get('file_description', file_record.file_description)
#         category = request.POST.get('file_category', file_record.category)
#         related_record_id = request.POST.get('related_record_id', file_record.related_record_id)
#         operation_reason = request.POST.get('operation_reason', '')
#
#         # 校验 file_category 是否合法
#         valid_categories = ['geological', 'excavation_diagnosis', 'excavation_calculation', 'tunnel', 'other']
#         if category not in valid_categories:
#             messages.error(request, "请选择有效的文件关联类别！")
#             return redirect('update_file', file_id=file_id)
#
#         # 更新文件记录到数据库
#         file_record.file_name = file_name
#         file_record.file_path = new_file_path
#         file_record.file_data = file_data
#         file_record.file_type = file_type
#         file_record.file_hash = file_hash
#         file_record.file_description = file_description
#         file_record.category = category
#         file_record.related_record_id = related_record_id
#         file_record.uploaded_by = request.user
#         file_record.upload_date = timezone.now()  # 更新上传日期
#         file_record.operation_reason = operation_reason
#         file_record.save()
#
#         messages.success(request, "文件修改成功！")
#         return redirect('update_file', file_id=file_id)
#
#     # 如果是 GET 请求，展示修改文件的表单，预填当前文件的信息
#     return render(request, 'update.html', {'file': file_record})
#
#
# # 文件列表（管理员）
# def preview_files(request):
#     """
#     展示文件列表，并支持按文件名和文件类型搜索及分页。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索的文件名或文件类型
#
#     # 获取所有文件记录并按上传时间降序排序
#     files_list = DataStorage.objects.all().order_by('-upload_date')
#
#     # 根据搜索条件过滤数据（支持文件名和文件类型的模糊查询）
#     if search_query:
#         files_list = files_list.filter(
#             Q(file_name__icontains=search_query) | Q(file_type__icontains=search_query)
#         )
#
#     # 设置分页，每页显示 10 条记录
#     paginator = Paginator(files_list, 10)
#     page = request.GET.get('page')
#
#     try:
#         # 获取当前页的数据
#         files = paginator.page(page)
#     except PageNotAnInteger:
#         # 如果 page 参数不是整数，显示第一页
#         files = paginator.page(1)
#     except EmptyPage:
#         # 如果页数超出范围，显示最后一页
#         files = paginator.page(paginator.num_pages)
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板并传递分页后的文件数据
#     return render(request, 'preview.html', {
#         'files': files,
#         'total_pages': paginator.num_pages,  # 总页数
#         'current_page': files.number,  # 当前页码
#         'search_query': search_query,  # 搜索条件
#         'query_params': query_params_encoded,  # 用于分页链接
#     })
#
# # 文件列表（用户）
# @login_required
# def user_files(request):
#     """
#     用户文件列表：仅显示当前用户上传的文件，并支持按文件名和文件类型搜索及分页。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索的文件名或文件类型
#
#     # 获取当前用户上传的文件记录，并按上传时间降序排序
#     user_files_list = DataStorage.objects.filter(uploaded_by=request.user).order_by('-upload_date')
#
#     # 根据搜索条件过滤数据（支持文件名和文件类型的模糊查询）
#     if search_query:
#         user_files_list = user_files_list.filter(
#             Q(file_name__icontains=search_query) | Q(file_type__icontains=search_query)
#         )
#
#     # 设置分页，每页显示 10 条记录
#     paginator = Paginator(user_files_list, 10)
#     page = request.GET.get('page')
#
#     try:
#         # 获取当前页的数据
#         files = paginator.page(page)
#     except PageNotAnInteger:
#         # 如果 page 参数不是整数，显示第一页
#         files = paginator.page(1)
#     except EmptyPage:
#         # 如果页数超出范围，显示最后一页
#         files = paginator.page(paginator.num_pages)
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板并传递分页后的文件数据
#     return render(request, 'user_files.html', {
#         'files': files,
#         'total_pages': paginator.num_pages,  # 总页数
#         'current_page': files.number,  # 当前页码
#         'search_query': search_query,  # 搜索条件
#         'query_params': query_params_encoded,  # 用于分页链接
#     })
#
#
# #下面是把浏览器浏览与下载分成两个函数处理的结果（等同于上面的合在一起的），但是可以解决下载不了的bug
# def preview_file(request, file_id):
#     file_record = get_object_or_404(DataStorage, id=file_id)
#     content_type, _ = mimetypes.guess_type(file_record.file_name)
#     content_type = content_type or 'application/octet-stream'
#     response = HttpResponse(file_record.file_data, content_type=content_type)
#     # 使用 urlquote 确保文件名正确编码，这个urlquote很重要，没有的话下载就有bug
#     response['Content-Disposition'] = f'inline; filename="{urlquote(file_record.file_name)}"'
#     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     return response
#
# def download_file(request, file_id):
#     file_record = get_object_or_404(DataStorage, id=file_id)
#     content_type, _ = mimetypes.guess_type(file_record.file_name)
#     content_type = content_type or 'application/octet-stream'
#     response = HttpResponse(file_record.file_data, content_type=content_type)
#     # 使用 urlquote 确保文件名正确编码
#     response['Content-Disposition'] = f'attachment; filename="{urlquote(file_record.file_name)}"'
#     response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     return response
#
#
#
# from django.http import Http404
# def delete_file(request, file_id):
#     print("删除文件")
#     try:
#         # 获取文件记录
#         file_record = get_object_or_404(DataStorage, id=file_id)
#
#         # 删除文件记录
#         file_record.delete()
#         messages.success(request, "文件已成功删除！")
#     except Http404:
#         messages.error(request, "未找到指定的文件记录！")
#     except Exception as e:
#         messages.error(request, f"删除文件时出错：{e}")
#
#     # 重定向到文件预览页面
#     return redirect('preview')
#
#
#
# #管理员审批
# #下面四个是管理员审批的详细页面后端代码
# #掌子面管理员审批（详细页面）
# @login_required
# def approve_geological_record(request, record_id):
#     """
#     审批用户提交的地质记录。
#     - 支持审批上传、修改和删除。
#     - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id)
#
#     # 检查是否是修改审批
#     is_modification = record.status == 'modified_pending'
#     modifications = {}
#     if is_modification:
#     # 获取历史版本中的最后一条记录
#         try:
#             # 获取修改前的历史版本
#             original_record = record.history.filter(history_type='~').last()  # '~' 表示修改操作
#             if original_record:
#                 for field in record._meta.fields:
#                     field_name = field.name
#                     #过滤掉一些表单以外的后台信息
#                     if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
#                         continue
#                     original_value = getattr(original_record, field_name, None)
#                     new_value = getattr(record, field_name, None)
#                     if original_value != new_value:
#                         modifications[field_name] = {'old': original_value, 'new': new_value}
#         except Exception as e:
#             print(f"Error fetching history: {e}")
#
#     if request.method == 'POST':
#         action = request.POST.get('action')  # 获取管理员的操作类型（approve 或 reject）
#         approval_reason = request.POST.get('approval_reason')  # 获取审批理由
#
#         if action == 'approve':
#             if record.status == 'pending':
#                 # 审批上传
#                 record.status = 'uploaded_approved'
#             elif record.status == 'modified_pending':
#                 # 审批修改
#                 record.status = 'modified_approved'
#             elif record.status == 'deleted_pending':
#                 # 审批删除
#                 record.status = 'deleted'
#
#             record.approved_by = request.user  # 设置审批人
#             print(record.approved_by)
#             record.approval_reason = approval_reason  # 设置审批理由
#             record.approved_at = now()  # 设置审批时间
#             record.save()  # 保存状态更新
#
#         elif action == 'reject':
#             # 驳回逻辑：状态保持不变，但记录审批理由和驳回人
#             record.approval_reason = approval_reason  # 保存驳回理由
#             record.rejected_by = request.user  # 设置驳回人
#             record.rejected_at = now()  # 设置驳回时间
#             if record.status in ['modified_pending', 'deleted_pending']:
#                 record.status = 'rejected'  # 设置为驳回状态
#             else:
#                 record.status = 'pending'  # 上传驳回仍保持 `pending`
#             record.save()
#
#         return redirect('approval_list')  # 返回到审批列表页面
#
#     return render(request, 'approve_geological_record.html', {
#         'record': record,
#         'is_modification': is_modification,
#         'modifications': modifications,
#     })
#
# @login_required
# def approve_excavation_diagnosis(request, record_id):
#     """
#     审批用户提交的超欠挖诊断记录。
#     - 支持审批上传、修改和删除。
#     - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id)
#
#     # 检查是否是修改审批
#     is_modification = record.status == 'modified_pending'
#     modifications = {}
#     if is_modification:
#         try:
#             # 获取修改前的历史版本
#             original_record = record.history.filter(history_type='~').last()
#             if original_record:
#                 for field in record._meta.fields:
#                     field_name = field.name
#                     #过滤掉一些表单以外的后台信息
#                     if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
#                         continue
#                     original_value = getattr(original_record, field_name, None)
#                     new_value = getattr(record, field_name, None)
#                     if original_value != new_value:
#                         modifications[field_name] = {'old': original_value, 'new': new_value}
#         except Exception as e:
#             print(f"Error fetching history: {e}")
#
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         approval_reason = request.POST.get('approval_reason')
#
#         if action == 'approve':
#             if record.status == 'pending':
#                 record.status = 'uploaded_approved'
#             elif record.status == 'modified_pending':
#                 record.status = 'modified_approved'
#             elif record.status == 'deleted_pending':
#                 record.status = 'deleted'
#
#             record.approved_by = request.user
#             record.approval_reason = approval_reason
#             record.approved_at = now()
#             record.save()
#
#         elif action == 'reject':
#             record.approval_reason = approval_reason
#             record.rejected_by = request.user
#             record.rejected_at = now()
#             if record.status in ['modified_pending', 'deleted_pending']:
#                 record.status = 'rejected'
#             else:
#                 record.status = 'pending'
#             record.save()
#
#         return redirect('approval_list')
#
#     return render(request, 'approve_excavation_diagnosis.html', {
#         'record': record,
#         'is_modification': is_modification,
#         'modifications': modifications,
#     })
#
# @login_required
# def approve_over_under_calculation(request, record_id):
#     """
#     审批用户提交的超欠挖计算记录。
#     - 支持审批上传、修改和删除。
#     - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)
#
#     # 检查是否是修改审批
#     is_modification = record.status == 'modified_pending'
#     modifications = {}
#     if is_modification:
#         try:
#             # 获取修改前的历史版本
#             original_record = record.history.filter(history_type='~').last()
#             if original_record:
#                 for field in record._meta.fields:
#                     field_name = field.name
#                     #过滤掉一些表单以外的后台信息
#                     if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
#                         continue
#                     original_value = getattr(original_record, field_name, None)
#                     new_value = getattr(record, field_name, None)
#                     if original_value != new_value:
#                         modifications[field_name] = {'old': original_value, 'new': new_value}
#         except Exception as e:
#             print(f"Error fetching history: {e}")
#
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         approval_reason = request.POST.get('approval_reason')
#
#         if action == 'approve':
#             if record.status == 'pending':
#                 record.status = 'uploaded_approved'
#             elif record.status == 'modified_pending':
#                 record.status = 'modified_approved'
#             elif record.status == 'deleted_pending':
#                 record.status = 'deleted'
#
#             record.approved_by = request.user
#             record.approval_reason = approval_reason
#             record.approved_at = now()
#             record.save()
#
#         elif action == 'reject':
#             record.approval_reason = approval_reason
#             record.rejected_by = request.user
#             record.rejected_at = now()
#             if record.status in ['modified_pending', 'deleted_pending']:
#                 record.status = 'rejected'
#             else:
#                 record.status = 'pending'
#             record.save()
#
#         return redirect('approval_list')
#
#     return render(request, 'approve_over_under_calculation.html', {
#         'record': record,
#         'is_modification': is_modification,
#         'modifications': modifications,
#     })
#
# @login_required
# def approve_tunnel_contour(request, record_id):
#     """
#     审批用户提交的隧道轮廓信息记录。
#     - 支持审批上传、修改和删除。
#     - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id)
#
#     # 检查是否是修改审批
#     is_modification = record.status == 'modified_pending'
#     modifications = {}
#     if is_modification:
#         try:
#             history_records = record.history.all()
#             print("历史记录条数:", len(history_records))
#             for hist in history_records:
#                 print(f"记录ID: {hist.id}, 类型: {hist.history_type}, 日期: {hist.history_date}")
#
#             # 获取修改前的历史版本
#             original_record = record.history.filter(history_type='~').last()
#             if original_record:
#                 print("原始记录找到，开始比较字段变化：")
#                 for field in record._meta.fields:
#                     field_name = field.name
#                     #过滤掉一些表单以外的后台信息
#                     if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
#                         continue
#
#                     # 获取原始值和当前值
#                     original_value = getattr(original_record, field_name, None)
#                     new_value = getattr(record, field_name, None)
#
#                     # 输出字段对比的调试信息
#                     print(f"字段: {field_name} | 原始值: {original_value} | 新值: {new_value}")
#
#                     if original_value != new_value:
#                         modifications[field_name] = {'old': original_value, 'new': new_value}
#                         print(f"字段 '{field_name}' 发生变化：原始值 -> {original_value}, 新值 -> {new_value}")
#             else:
#                 print("未找到修改前的历史记录！")
#         except Exception as e:
#             print(f"Error fetching history: {e}")
#
#
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         approval_reason = request.POST.get('approval_reason')
#
#         if action == 'approve':
#             if record.status == 'pending':
#                 record.status = 'uploaded_approved'
#             elif record.status == 'modified_pending':
#                 record.status = 'modified_approved'
#             elif record.status == 'deleted_pending':
#                 record.status = 'deleted'
#
#             record.approved_by = request.user
#             record.approval_reason = approval_reason
#             record.approved_at = now()
#             record.save()
#
#         elif action == 'reject':
#             record.approval_reason = approval_reason
#             record.rejected_by = request.user
#             record.rejected_at = now()
#             if record.status in ['modified_pending', 'deleted_pending']:
#                 record.status = 'rejected'
#             else:
#                 record.status = 'pending'
#             record.save()
#
#         return redirect('approval_list')
#
#     return render(request, 'approve_tunnel_contour.html', {
#         'record': record,
#         'is_modification': is_modification,
#         'modifications': modifications,
#     })
#
#
#
# #下面是四个驳回的
# #管理员驳回
# @login_required
# def reject_geological_record(request, record_id):
#     """
#     管理员驳回地质记录的审批请求。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id)
#
#     # 替换管理员权限检查逻辑
#     if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
#         messages.error(request, "您没有权限驳回记录。")
#         return redirect('approval_list')
#
#     if request.method == 'POST':
#         rejection_reason = request.POST.get('rejection_reason', '')
#         if not rejection_reason:
#             messages.error(request, "驳回理由不能为空。")
#             return redirect('approval_list')
#
#         # 更新记录状态为 "rejected"
#         record.status = 'rejected'
#         record.approval_reason = rejection_reason  # 保存驳回理由
#         record.approved_by = request.user  # 设置当前审批管理员
#         record.approved_at = timezone.now()  # 记录审批时间
#         record.save()
#
#         # 消息反馈
#         messages.success(request, f"记录 {record.face_id} 已成功驳回。")
#         return redirect('approval_list')
#
#     return render(request, 'reject_record.html', {'record': record})
#
# @login_required
# def reject_excavation_diagnosis(request, record_id):
#     """
#     管理员驳回超欠挖诊断记录的审批请求。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id)
#
#     # 替换管理员权限检查逻辑
#     if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
#         messages.error(request, "您没有权限驳回记录。")
#         return redirect('approval_list')
#
#     if request.method == 'POST':
#         rejection_reason = request.POST.get('rejection_reason', '')
#         if not rejection_reason:
#             messages.error(request, "驳回理由不能为空。")
#             return redirect('approval_list')
#
#         # 更新记录状态为 "rejected"
#         record.status = 'rejected'
#         record.approval_reason = rejection_reason  # 保存驳回理由
#         record.approved_by = request.user  # 设置当前审批管理员
#         record.approved_at = timezone.now()  # 记录审批时间
#         record.save()
#
#         # 消息反馈
#         messages.success(request, f"记录 {record.face_id} 已成功驳回。")
#         return redirect('approval_list')
#
#     return render(request, 'reject_record1.html', {'record': record})
#
# @login_required
# def reject_over_under_excavation(request, record_id):
#     """
#     管理员驳回超欠挖计算记录的审批请求。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)
#
#     # 替换管理员权限检查逻辑
#     if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
#         messages.error(request, "您没有权限驳回记录。")
#         return redirect('approval_list')
#
#     if request.method == 'POST':
#         rejection_reason = request.POST.get('rejection_reason', '')
#         if not rejection_reason:
#             messages.error(request, "驳回理由不能为空。")
#             return redirect('approval_list')
#
#         # 更新记录状态为 "rejected"
#         record.status = 'rejected'
#         record.approval_reason = rejection_reason  # 保存驳回理由
#         record.approved_by = request.user  # 设置当前审批管理员
#         record.approved_at = timezone.now()  # 记录审批时间
#         record.save()
#
#         # 消息反馈
#         messages.success(request, f"记录 {record.face_id} 已成功驳回。")
#         return redirect('approval_list')
#
#     return render(request, 'reject_record2.html', {'record': record})
#
# @login_required
# def reject_tunnel_contour(request, record_id):
#     """
#     管理员驳回隧道轮廓信息记录的审批请求。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id)
#
#     # 替换管理员权限检查逻辑
#     if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
#         messages.error(request, "您没有权限驳回记录。")
#         return redirect('approval_list')
#
#     if request.method == 'POST':
#         rejection_reason = request.POST.get('rejection_reason', '')
#         if not rejection_reason:
#             messages.error(request, "驳回理由不能为空。")
#             return redirect('approval_list')
#
#         # 更新记录状态为 "rejected"
#         record.status = 'rejected'
#         record.approval_reason = rejection_reason  # 保存驳回理由
#         record.approved_by = request.user  # 设置当前审批管理员
#         record.approved_at = timezone.now()  # 记录审批时间
#         record.save()
#
#         # 消息反馈
#         messages.success(request, f"记录 {record.face_id} 已成功驳回。")
#         return redirect('approval_list')
#
#     return render(request, 'reject_record3.html', {'record': record})
#
#
#
#
#
# #下面是四个审批的大页面
# #掌子面审批
# @login_required
# def approval_list(request):
#     """
#     审批列表视图：支持按 face_id 和提交人 (created_by_id 或 created_by__username) 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示的记录数
#     records_per_page = 10
#
#     # 搜索逻辑函数
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回过滤后的查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(
#                 Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
#             )
#         return base_queryset
#
#     # 掌子面记录审批
#     new_records_paginator = Paginator(
#         get_searched_queryset(GeologicalSketchRecord.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_records_paginator = Paginator(
#         get_searched_queryset(GeologicalSketchRecord.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_records_paginator = Paginator(
#         get_searched_queryset(GeologicalSketchRecord.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_records = new_records_paginator.get_page(request.GET.get('new_page'))
#     pending_modified_records = modified_records_paginator.get_page(request.GET.get('modified_page'))
#     pending_deleted_records = deleted_records_paginator.get_page(request.GET.get('deleted_page'))
#
#     # 超欠挖计算记录审批
#     new_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_excavation_calc = new_calc_paginator.get_page(request.GET.get('new_calc_page'))
#     pending_modified_excavation_calc = modified_calc_paginator.get_page(request.GET.get('modified_calc_page'))
#     pending_deleted_excavation_calc = deleted_calc_paginator.get_page(request.GET.get('deleted_calc_page'))
#
#     # 超欠挖诊断记录审批
#     new_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_diagnosis = new_diag_paginator.get_page(request.GET.get('new_diag_page'))
#     pending_modified_diagnosis = modified_diag_paginator.get_page(request.GET.get('modified_diag_page'))
#     pending_deleted_diagnosis = deleted_diag_paginator.get_page(request.GET.get('deleted_diag_page'))
#
#     # 隧道轮廓记录审批
#     new_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_tunnel = new_tunnel_paginator.get_page(request.GET.get('new_tunnel_page'))
#     pending_modified_tunnel = modified_tunnel_paginator.get_page(request.GET.get('modified_tunnel_page'))
#     pending_deleted_tunnel = deleted_tunnel_paginator.get_page(request.GET.get('deleted_tunnel_page'))
#
#     # 渲染模板并传递上下文
#     return render(
#         request,
#         'approval_list.html',
#         {
#             # GeologicalSketchRecord (掌子面记录)
#             'pending_new_records': pending_new_records,
#             'pending_modified_records': pending_modified_records,
#             'pending_deleted_records': pending_deleted_records,
#
#             # OverUnderExcavationCalculation (超欠挖计算记录)
#             'pending_new_excavation_calc': pending_new_excavation_calc,
#             'pending_modified_excavation_calc': pending_modified_excavation_calc,
#             'pending_deleted_excavation_calc': pending_deleted_excavation_calc,
#
#             # ExcavationDiagnosis (超欠挖诊断记录)
#             'pending_new_diagnosis': pending_new_diagnosis,
#             'pending_modified_diagnosis': pending_modified_diagnosis,
#             'pending_deleted_diagnosis': pending_deleted_diagnosis,
#
#             # TunnelContourInfo (隧道轮廓记录)
#             'pending_new_tunnel': pending_new_tunnel,
#             'pending_modified_tunnel': pending_modified_tunnel,
#             'pending_deleted_tunnel': pending_deleted_tunnel,
#
#             # 搜索相关
#             'search_query': search_query,
#         },
#     )
#
#
# #超欠挖计算审批
# @login_required
# def approval_excavation_calculation(request):
#     """
#     超欠挖计算审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示的记录数
#     records_per_page = 10
#
#     # 搜索逻辑函数
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回过滤后的查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(
#                 Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
#             )
#         return base_queryset
#
#     # 超欠挖计算记录审批
#     new_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_calc_paginator = Paginator(
#         get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_excavation_calc = new_calc_paginator.get_page(request.GET.get('new_page'))
#     pending_modified_excavation_calc = modified_calc_paginator.get_page(request.GET.get('modified_page'))
#     pending_deleted_excavation_calc = deleted_calc_paginator.get_page(request.GET.get('deleted_page'))
#
#     # 渲染模板并传递上下文
#     return render(
#         request,
#         'approval_list1.html',
#         {
#             'pending_new_excavation_calc': pending_new_excavation_calc,
#             'pending_modified_excavation_calc': pending_modified_excavation_calc,
#             'pending_deleted_excavation_calc': pending_deleted_excavation_calc,
#             'search_query': search_query,  # 搜索条件
#         }
#     )
#
# #超欠挖诊断审批
# @login_required
# def approval_excavation_diagnosis(request):
#     """
#     超欠挖诊断审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示的记录数
#     records_per_page = 10
#
#     # 搜索逻辑函数
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回过滤后的查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(
#                 Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
#             )
#         return base_queryset
#
#     # 超欠挖诊断记录审批
#     new_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_diag_paginator = Paginator(
#         get_searched_queryset(ExcavationDiagnosis.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_diagnosis = new_diag_paginator.get_page(request.GET.get('new_page'))
#     pending_modified_diagnosis = modified_diag_paginator.get_page(request.GET.get('modified_page'))
#     pending_deleted_diagnosis = deleted_diag_paginator.get_page(request.GET.get('deleted_page'))
#
#     # 渲染模板并传递上下文
#     return render(
#         request,
#         'approval_list2.html',
#         {
#             'pending_new_diagnosis': pending_new_diagnosis,
#             'pending_modified_diagnosis': pending_modified_diagnosis,
#             'pending_deleted_diagnosis': pending_deleted_diagnosis,
#             'search_query': search_query,  # 搜索条件
#         }
#     )
#
# #隧道审批
# @login_required
# def approval_tunnel_contour(request):
#     """
#     隧道轮廓审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示的记录数
#     records_per_page = 10
#
#     # 搜索逻辑函数
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回过滤后的查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(
#                 Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
#             )
#         return base_queryset
#
#     # 隧道轮廓记录审批
#     new_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='pending').order_by('-created_at')),
#         records_per_page
#     )
#     modified_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='modified_pending').order_by('-created_at')),
#         records_per_page
#     )
#     deleted_tunnel_paginator = Paginator(
#         get_searched_queryset(TunnelContourInfo.objects.filter(status='deleted_pending').order_by('-created_at')),
#         records_per_page
#     )
#
#     pending_new_tunnel = new_tunnel_paginator.get_page(request.GET.get('new_page'))
#     pending_modified_tunnel = modified_tunnel_paginator.get_page(request.GET.get('modified_page'))
#     pending_deleted_tunnel = deleted_tunnel_paginator.get_page(request.GET.get('deleted_page'))
#
#     # 渲染模板并传递上下文
#     return render(
#         request,
#         'approval_list3.html',
#         {
#             'pending_new_tunnel': pending_new_tunnel,
#             'pending_modified_tunnel': pending_modified_tunnel,
#             'pending_deleted_tunnel': pending_deleted_tunnel,
#             'search_query': search_query,  # 搜索条件
#         }
#     )
#
#
# #用户查看自己的待审批内容
# @login_required
# def user_pending_records(request):
#     """
#     查看用户自己提交的所有待审批记录。
#     """
#     # 查询当前用户提交的所有待审批记录
#     pending_records = GeologicalSketchRecord.objects.filter(
#         created_by=request.user, status='pending'
#     ).order_by('-created_at')  # 按提交时间降序排列
#
#     return render(request, 'user_pending_records.html', {
#         'pending_records': pending_records
#     })
#
#
# #用户个人信息中心（这个留着别删，这个对应于user_record.html里面前面800多行注释的代码，这个可以展示所有信息，可以用于测试）
# # @login_required
# # def user_records_view(request):
# #     """
# #     展示用户的所有数据记录，包括掌子面、超欠挖计算、诊断和隧道的记录。
# #     """
# #     # 掌子面的数据记录
# #     pending_new_geological = GeologicalSketchRecord.objects.filter(
# #         created_by=request.user, status='pending'
# #     )
# #     pending_modified_geological = GeologicalSketchRecord.objects.filter(
# #         created_by=request.user, status='modified_pending'
# #     )
# #     pending_deleted_geological = GeologicalSketchRecord.objects.filter(
# #         created_by=request.user, status='deleted_pending'
# #     )
# #     rejected_geological = GeologicalSketchRecord.objects.filter(
# #         created_by=request.user, status='rejected'
# #     )
# #     approved_geological = GeologicalSketchRecord.objects.filter(
# #         created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
# #     )
# #
# #     # 超欠挖计算的记录
# #     pending_new_excavation_calculation = OverUnderExcavationCalculation.objects.filter(
# #         created_by=request.user, status='pending'
# #     )
# #     pending_modified_excavation_calculation = OverUnderExcavationCalculation.objects.filter(
# #         created_by=request.user, status='modified_pending'
# #     )
# #     pending_deleted_excavation_calculation = OverUnderExcavationCalculation.objects.filter(
# #         created_by=request.user, status='deleted_pending'
# #     )
# #     rejected_excavation_calculation = OverUnderExcavationCalculation.objects.filter(
# #         created_by=request.user, status='rejected'
# #     )
# #     approved_excavation_calculation = OverUnderExcavationCalculation.objects.filter(
# #         created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
# #     )
# #
# #     # 超欠挖诊断的记录
# #     pending_new_excavation_diagnosis = ExcavationDiagnosis.objects.filter(
# #         created_by=request.user, status='pending'
# #     )
# #     pending_modified_excavation_diagnosis = ExcavationDiagnosis.objects.filter(
# #         created_by=request.user, status='modified_pending'
# #     )
# #     pending_deleted_excavation_diagnosis = ExcavationDiagnosis.objects.filter(
# #         created_by=request.user, status='deleted_pending'
# #     )
# #     rejected_excavation_diagnosis = ExcavationDiagnosis.objects.filter(
# #         created_by=request.user, status='rejected'
# #     )
# #     approved_excavation_diagnosis = ExcavationDiagnosis.objects.filter(
# #         created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
# #     )
# #
# #     # 隧道的记录
# #     pending_new_tunnel = TunnelContourInfo.objects.filter(
# #         created_by=request.user, status='pending'
# #     )
# #     pending_modified_tunnel = TunnelContourInfo.objects.filter(
# #         created_by=request.user, status='modified_pending'
# #     )
# #     pending_deleted_tunnel = TunnelContourInfo.objects.filter(
# #         created_by=request.user, status='deleted_pending'
# #     )
# #     rejected_tunnel = TunnelContourInfo.objects.filter(
# #         created_by=request.user, status='rejected'
# #     )
# #     approved_tunnel = TunnelContourInfo.objects.filter(
# #         created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
# #     )
# #
# #     # 渲染模板
# #     return render(
# #         request,
# #         'user_records.html',
# #         {
# #             # 掌子面数据
# #             'pending_new_geological': pending_new_geological,
# #             'pending_modified_geological': pending_modified_geological,
# #             'pending_deleted_geological': pending_deleted_geological,
# #             'rejected_geological': rejected_geological,
# #             'approved_geological': approved_geological,
# #             # 超欠挖计算
# #             'pending_new_excavation_calculation': pending_new_excavation_calculation,
# #             'pending_modified_excavation_calculation': pending_modified_excavation_calculation,
# #             'pending_deleted_excavation_calculation': pending_deleted_excavation_calculation,
# #             'rejected_excavation_calculation': rejected_excavation_calculation,
# #             'approved_excavation_calculation': approved_excavation_calculation,
# #             # 超欠挖诊断
# #             'pending_new_excavation_diagnosis': pending_new_excavation_diagnosis,
# #             'pending_modified_excavation_diagnosis': pending_modified_excavation_diagnosis,
# #             'pending_deleted_excavation_diagnosis': pending_deleted_excavation_diagnosis,
# #             'rejected_excavation_diagnosis': rejected_excavation_diagnosis,
# #             'approved_excavation_diagnosis': approved_excavation_diagnosis,
# #             # 隧道轮廓
# #             'pending_new_tunnel': pending_new_tunnel,
# #             'pending_modified_tunnel': pending_modified_tunnel,
# #             'pending_deleted_tunnel': pending_deleted_tunnel,
# #             'rejected_tunnel': rejected_tunnel,
# #             'approved_tunnel': approved_tunnel,
# #         },
# #     )
#
#
# #分页函数
# def paginate_queryset(queryset, request, items_per_page, page_param='page'):
#     paginator = Paginator(queryset, items_per_page)
#     page = request.GET.get(page_param, 1)  # 获取分页参数
#     try:
#         page_obj = paginator.page(page)
#     except PageNotAnInteger:
#         page_obj = paginator.page(1)  # 默认第 1 页
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)  # 超出范围返回最后一页
#     return page_obj
#
#
# #下面这四个是拆开的用户个人中心（掌子面，超欠挖计算，诊断，隧道）
# @login_required
# def user_records_view(request):
#     """
#     展示掌子面记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索的掌子面编号
#
#     # 每页显示条数
#     items_per_page = 10  # 调整为生产环境合适的值
#
#     # 使用搜索逻辑
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(face_id__icontains=search_query)
#         return base_queryset
#
#     # 应用搜索和分页
#     pending_new_page_obj = paginate_queryset(
#         get_searched_queryset(
#             GeologicalSketchRecord.objects.filter(
#                 created_by=request.user, status='pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_new_page'
#     )
#     pending_modified_page_obj = paginate_queryset(
#         get_searched_queryset(
#             GeologicalSketchRecord.objects.filter(
#                 created_by=request.user, status='modified_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_modified_page'
#     )
#     pending_deleted_page_obj = paginate_queryset(
#         get_searched_queryset(
#             GeologicalSketchRecord.objects.filter(
#                 created_by=request.user, status='deleted_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_deleted_page'
#     )
#     rejected_page_obj = paginate_queryset(
#         get_searched_queryset(
#             GeologicalSketchRecord.objects.filter(
#                 created_by=request.user, status='rejected'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='rejected_page'
#     )
#     approved_page_obj = paginate_queryset(
#         get_searched_queryset(
#             GeologicalSketchRecord.objects.filter(
#                 created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='approved_page'
#     )
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板
#     return render(
#         request,
#         'user_records.html',  # 模板文件
#         {
#             'pending_new_geological': pending_new_page_obj,
#             'pending_modified_geological': pending_modified_page_obj,
#             'pending_deleted_geological': pending_deleted_page_obj,
#             'rejected_geological': rejected_page_obj,
#             'approved_geological': approved_page_obj,
#             'search_query': search_query,  # 搜索条件
#             'query_params': query_params_encoded,  # 用于分页链接
#         },
#     )
#
#
#
#
#
# @login_required
# def excavation_calculation_records_view(request):
#     """
#     展示超欠挖计算记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索的超欠挖计算编号
#
#     # 每页显示条数
#     items_per_page = 10  # 调整为生产环境合适的值
#
#     # 使用搜索逻辑
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换字段为实际字段
#         return base_queryset
#
#     # 应用搜索和分页
#     pending_new_page_obj = paginate_queryset(
#         get_searched_queryset(
#             OverUnderExcavationCalculation.objects.filter(
#                 created_by=request.user, status='pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_new_page'
#     )
#     pending_modified_page_obj = paginate_queryset(
#         get_searched_queryset(
#             OverUnderExcavationCalculation.objects.filter(
#                 created_by=request.user, status='modified_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_modified_page'
#     )
#     pending_deleted_page_obj = paginate_queryset(
#         get_searched_queryset(
#             OverUnderExcavationCalculation.objects.filter(
#                 created_by=request.user, status='deleted_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_deleted_page'
#     )
#     rejected_page_obj = paginate_queryset(
#         get_searched_queryset(
#             OverUnderExcavationCalculation.objects.filter(
#                 created_by=request.user, status='rejected'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='rejected_page'
#     )
#     approved_page_obj = paginate_queryset(
#         get_searched_queryset(
#             OverUnderExcavationCalculation.objects.filter(
#                 created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='approved_page'
#     )
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板
#     return render(
#         request,
#         'user_records1.html',  # 模板文件
#         {
#             'pending_new_excavation_calculation': pending_new_page_obj,
#             'pending_modified_excavation_calculation': pending_modified_page_obj,
#             'pending_deleted_excavation_calculation': pending_deleted_page_obj,
#             'rejected_excavation_calculation': rejected_page_obj,
#             'approved_excavation_calculation': approved_page_obj,
#             'search_query': search_query,  # 搜索条件
#             'query_params': query_params_encoded,  # 用于分页链接
#         },
#     )
#
#
#
#
# @login_required
# def excavation_diagnosis_records_view(request):
#     """
#     展示超欠挖诊断记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示条数
#     items_per_page = 10  # 可以根据需求调整条目数
#
#     # 使用搜索逻辑
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换为实际搜索字段
#         return base_queryset
#
#     # 应用搜索和分页
#     pending_new_page_obj = paginate_queryset(
#         get_searched_queryset(
#             ExcavationDiagnosis.objects.filter(
#                 created_by=request.user, status='pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_new_page'
#     )
#     pending_modified_page_obj = paginate_queryset(
#         get_searched_queryset(
#             ExcavationDiagnosis.objects.filter(
#                 created_by=request.user, status='modified_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_modified_page'
#     )
#     pending_deleted_page_obj = paginate_queryset(
#         get_searched_queryset(
#             ExcavationDiagnosis.objects.filter(
#                 created_by=request.user, status='deleted_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_deleted_page'
#     )
#     rejected_page_obj = paginate_queryset(
#         get_searched_queryset(
#             ExcavationDiagnosis.objects.filter(
#                 created_by=request.user, status='rejected'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='rejected_page'
#     )
#     approved_page_obj = paginate_queryset(
#         get_searched_queryset(
#             ExcavationDiagnosis.objects.filter(
#                 created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='approved_page'
#     )
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板
#     return render(
#         request,
#         'user_records2.html',  # 模板文件
#         {
#             'pending_new_excavation_diagnosis': pending_new_page_obj,
#             'pending_modified_excavation_diagnosis': pending_modified_page_obj,
#             'pending_deleted_excavation_diagnosis': pending_deleted_page_obj,
#             'rejected_excavation_diagnosis': rejected_page_obj,
#             'approved_excavation_diagnosis': approved_page_obj,
#             'search_query': search_query,  # 搜索条件
#             'query_params': query_params_encoded,  # 用于分页链接
#         },
#     )
#
#
#
#
# @login_required
# def tunnel_contour_records_view(request):
#     """
#     展示隧道轮廓记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
#     """
#     # 获取搜索条件
#     search_query = request.GET.get('search', '')  # 获取搜索条件
#
#     # 每页显示条数
#     items_per_page = 10  # 根据需求调整条目数
#
#     # 使用搜索逻辑
#     def get_searched_queryset(base_queryset):
#         """
#         根据搜索条件返回查询集
#         """
#         if search_query:
#             base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换为实际搜索字段
#         return base_queryset
#
#     # 应用搜索和分页
#     pending_new_page_obj = paginate_queryset(
#         get_searched_queryset(
#             TunnelContourInfo.objects.filter(
#                 created_by=request.user, status='pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_new_page'
#     )
#     pending_modified_page_obj = paginate_queryset(
#         get_searched_queryset(
#             TunnelContourInfo.objects.filter(
#                 created_by=request.user, status='modified_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_modified_page'
#     )
#     pending_deleted_page_obj = paginate_queryset(
#         get_searched_queryset(
#             TunnelContourInfo.objects.filter(
#                 created_by=request.user, status='deleted_pending'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='pending_deleted_page'
#     )
#     rejected_page_obj = paginate_queryset(
#         get_searched_queryset(
#             TunnelContourInfo.objects.filter(
#                 created_by=request.user, status='rejected'
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='rejected_page'
#     )
#     approved_page_obj = paginate_queryset(
#         get_searched_queryset(
#             TunnelContourInfo.objects.filter(
#                 created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
#             )
#         ),
#         request,
#         items_per_page,
#         page_param='approved_page'
#     )
#
#     # 保留搜索参数的查询参数
#     query_params = request.GET.copy()
#     query_params.pop('page', None)  # 移除分页参数，避免重复
#     query_params_encoded = query_params.urlencode()  # 编码查询参数
#
#     # 渲染模板
#     return render(
#         request,
#         'user_records3.html',  # 模板文件
#         {
#             'pending_new_tunnel': pending_new_page_obj,
#             'pending_modified_tunnel': pending_modified_page_obj,
#             'pending_deleted_tunnel': pending_deleted_page_obj,
#             'rejected_tunnel': rejected_page_obj,
#             'approved_tunnel': approved_page_obj,
#             'search_query': search_query,  # 搜索条件
#             'query_params': query_params_encoded,  # 用于分页链接
#         },
#     )
#
#
#
# #下面四个是用户修改新增待审批的
# @login_required
# def edit_pending_record(request, record_id):
#     """
#     用户修改待审批的掌子面记录记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         form = GeologicalSketchRecordForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')
#     else:
#         form = GeologicalSketchRecordForm(instance=record)
#
#     return render(request, 'edit_pending_record.html', {'form': form, 'record': record})
#
# @login_required
# def edit_pending_excavation_diagnosis(request, record_id):
#     """
#     用户修改待审批的超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         form = ExcavationDiagnosisForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#     else:
#         form = ExcavationDiagnosisForm(instance=record)
#
#     return render(request, 'edit_pending_diagnosis.html', {'form': form, 'record': record})
#
# @login_required
# def edit_pending_over_under_excavation(request, record_id):
#     """
#     用户修改待审批的超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         form = OverUnderExcavationForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#     else:
#         form = OverUnderExcavationForm(instance=record)
#
#     return render(request, 'edit_pending_excavation.html', {'form': form, 'record': record})
#
# @login_required
# def edit_pending_tunnel_contour(request, record_id):
#     """
#     用户修改待审批的隧道轮廓记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         form = TunnelContourForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#     else:
#         form = TunnelContourForm(instance=record)
#
#     return render(request, 'edit_pending_tunnel_contour.html', {'form': form, 'record': record})
#
#
# #下面四个是用户删除新增待审批的
# @login_required
# def delete_pending_record(request, record_id):
#     """
#     用户删除待审批的掌子面信息记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_pending.html', {'record': record})
#
# @login_required
# def delete_pending_excavation_diagnosis(request, record_id):
#     """
#     用户删除待审批的超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#
#     return render(request, 'confirm_delete_pending_diagnosis.html', {'record': record})
#
# @login_required
# def delete_pending_over_under_excavation(request, record_id):
#     """
#     用户删除待审批的超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#
#     return render(request, 'confirm_delete_pending_excavation.html', {'record': record})
#
# @login_required
# def delete_pending_tunnel_contour(request, record_id):
#     """
#     用户删除待审批的隧道轮廓记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')  # 替换为用户记录列表的URL名称
#
#     return render(request, 'confirm_delete_pending_tunnel_contour.html', {'record': record})
#
#
#
#
# #下面八个是用户申请修改，删除已审批信息的
# #掌子面用户申请修改已审批记录
# @login_required
# def apply_edit_record(request, record_id):
#     """
#     用户申请修改已审批记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         form = GeologicalSketchRecordForm(request.POST, instance=record)  # 用表单绑定数据
#         if form.is_valid():
#             operation_reason = request.POST.get('operation_reason')  # 获取修改理由
#             if operation_reason:
#                 record.operation_reason = operation_reason  # 保存修改理由
#             record.status = 'modified_pending'  # 修改申请设置为待审批状态
#             record.save()
#             form.save()  # 保存表单中的修改
#             return redirect('user_records_view')
#         else:
#             print("表单验证失败，错误信息如下：")
#             print(form.errors)
#     else:
#         form = GeologicalSketchRecordForm(instance=record)  # 初始化表单，加载已有数据
#
#     return render(request, 'apply_edit_record.html', {'record': record})
#
# #掌子面用户申请删除已审批记录
# @login_required
# def apply_delete_record(request, record_id):
#     """
#     用户申请删除已审批记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         operation_reason = request.POST.get('operation_reason')  # 获取删除理由
#         print("理由如下：")
#         print(operation_reason)
#         if operation_reason:
#             record.operation_reason = operation_reason  # 保存删除理由
#         record.status = 'deleted_pending'  # 删除申请设置为待审批状态
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_application.html', {'record': record})
#
# @login_required
# def apply_edit_excavation_diagnosis(request, record_id):
#     """
#     用户申请修改已审批的超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         form = ExcavationDiagnosisForm(request.POST, instance=record)  # 用表单绑定数据
#         if form.is_valid():
#             operation_reason = request.POST.get('operation_reason')  # 获取修改理由
#             if operation_reason:
#                 record.operation_reason = operation_reason  # 保存修改理由
#             record.status = 'modified_pending'  # 修改申请设置为待审批状态
#             record.save()
#             form.save()  # 保存表单中的修改
#             return redirect('user_records_view')
#         else:
#             print("表单验证失败，错误信息如下：")
#             print(form.errors)
#     else:
#         form = ExcavationDiagnosisForm(instance=record)  # 初始化表单，加载已有数据
#
#     return render(request, 'apply_edit_excavation_diagnosis.html', {'record': record})
#
#
# @login_required
# def apply_delete_excavation_diagnosis(request, record_id):
#     """
#     用户申请删除已审批的超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         operation_reason = request.POST.get('operation_reason')  # 获取删除理由
#         print("理由如下：")
#         print(operation_reason)
#         if operation_reason:
#             record.operation_reason = operation_reason  # 保存删除理由
#         record.status = 'deleted_pending'  # 删除申请设置为待审批状态
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_excavation_diagnosis.html', {'record': record})
#
# @login_required
# def apply_edit_over_under_excavation_calculation(request, record_id):
#     """
#     用户申请修改已审批的超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         form = OverUnderExcavationForm(request.POST, instance=record)  # 用表单绑定数据
#         if form.is_valid():
#             operation_reason = request.POST.get('operation_reason')  # 获取修改理由
#             if operation_reason:
#                 record.operation_reason = operation_reason  # 保存修改理由
#             record.status = 'modified_pending'  # 修改申请设置为待审批状态
#             record.save()
#             form.save()  # 保存表单中的修改
#             return redirect('user_records_view')
#         else:
#             print("表单验证失败，错误信息如下：")
#             print(form.errors)
#     else:
#         form = OverUnderExcavationForm(instance=record)  # 初始化表单，加载已有数据
#
#     return render(request, 'apply_edit_over_under_excavation_calculation.html', {'record': record})
#
#
# @login_required
# def apply_delete_over_under_excavation_calculation(request, record_id):
#     """
#     用户申请删除已审批的超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#     if request.method == 'POST':
#         operation_reason = request.POST.get('operation_reason')  # 获取删除理由
#         print("理由如下：")
#         print(operation_reason)
#         if operation_reason:
#             record.operation_reason = operation_reason  # 保存删除理由
#         record.status = 'deleted_pending'  # 删除申请设置为待审批状态
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_over_under_excavation_calculation.html', {'record': record})
#
# @login_required
# def apply_edit_tunnel_contour_info(request, record_id):
#     """
#     用户申请修改已审批的隧道轮廓记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         form = TunnelContourForm(request.POST, instance=record)  # 用表单绑定数据
#         if form.is_valid():
#             operation_reason = request.POST.get('operation_reason')  # 获取修改理由
#             if operation_reason:
#                 record.operation_reason = operation_reason  # 保存修改理由
#             record.status = 'modified_pending'  # 修改申请设置为待审批状态
#             record.save()
#             form.save()  # 保存表单中的修改
#             return redirect('user_records_view')
#         else:
#             print("表单验证失败，错误信息如下：")
#             print(form.errors)
#     else:
#         form = TunnelContourForm(instance=record)  # 初始化表单，加载已有数据
#
#     return render(request, 'apply_edit_tunnel_contour_info.html', {'record': record})
#
#
# @login_required
# def apply_delete_tunnel_contour_info(request, record_id):
#     """
#     用户申请删除已审批的隧道轮廓信息记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
#
#     if request.method == 'POST':
#         operation_reason = request.POST.get('operation_reason')  # 获取删除理由
#         print("理由如下：")
#         print(operation_reason)
#         if operation_reason:
#             record.operation_reason = operation_reason  # 保存删除理由
#         record.status = 'deleted_pending'  # 删除申请设置为待审批状态
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_tunnel_contour_info.html', {'record': record})
#
#
#
# #下面四个是修改“修改待审批”的
# @login_required
# def edit_modified_pending_record(request, record_id):
#     """
#     用户修改掌子面“修改待审批”的记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         form = GeologicalSketchRecordForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')
#     else:
#         form = GeologicalSketchRecordForm(instance=record)
#
#     return render(request, 'edit_pending_record.html', {'form': form, 'record': record})
#
# @login_required
# def edit_modified_pending_excavation_diagnosis(request, record_id):
#     """
#     用户修改超欠挖诊断“修改待审批”的记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         form = ExcavationDiagnosisForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')
#     else:
#         form = ExcavationDiagnosisForm(instance=record)
#
#     return render(request, 'edit_pending_diagnosis.html', {'form': form, 'record': record})
#
# @login_required
# def edit_modified_pending_over_under_excavation(request, record_id):
#     """
#     用户修改超欠挖计算“修改待审批”的记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         form = OverUnderExcavationForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')
#     else:
#         form = OverUnderExcavationForm(instance=record)
#
#     return render(request, 'edit_pending_excavation.html', {'form': form, 'record': record})
#
# @login_required
# def edit_modified_pending_tunnel_contour(request, record_id):
#     """
#     用户修改隧道轮廓“修改待审批”的记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         form = TunnelContourForm(request.POST, instance=record)
#         if form.is_valid():
#             form.save()
#             return redirect('user_records_view')
#     else:
#         form = TunnelContourForm(instance=record)
#
#     return render(request, 'edit_pending_tunnel_contour.html', {'form': form, 'record': record})
#
#
# #下面四个是删除“修改待审批”的
# @login_required
# def delete_modified_pending_record(request, record_id):
#     """
#     用户删除掌子面“修改待审批”的记录。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_pending.html', {'record': record})
#
# @login_required
# def delete_modified_pending_excavation_diagnosis(request, record_id):
#     """
#     用户删除超欠挖诊断“修改待审批”的记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_pending_diagnosis.html', {'record': record})
#
# @login_required
# def delete_modified_pending_over_under_excavation(request, record_id):
#     """
#     用户删除超欠挖计算“修改待审批”的记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_pending_excavation.html', {'record': record})
#
# @login_required
# def delete_modified_pending_tunnel_contour(request, record_id):
#     """
#     用户删除隧道轮廓“修改待审批”的记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='modified_pending')
#
#     if request.method == 'POST':
#         record.delete()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_pending_tunnel_contour.html', {'record': record})
#
#
# #下面四个是取消“删除待审批”的
# @login_required
# def delete_deleted_pending_record(request, record_id):
#     """
#     用户取消“删除待审批”的记录（即撤销删除申请，将状态改为上传已审批）。
#     """
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='deleted_pending')
#
#     if request.method == 'POST':
#         # 将状态从 deleted_pending 改为 uploaded_approved
#         record.status = 'uploaded_approved'
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'confirm_delete_deleted_pending.html', {'record': record})
#
# @login_required
# def cancel_delete_pending_excavation_diagnosis(request, record_id):
#     """
#     用户取消“删除待审批”的超欠挖诊断记录。
#     """
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='deleted_pending')
#
#     if request.method == 'POST':
#         record.status = 'uploaded_approved'
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'cancel_delete_pending_excavation_diagnosis.html', {'record': record})
#
# @login_required
# def cancel_delete_pending_over_under_excavation(request, record_id):
#     """
#     用户取消“删除待审批”的超欠挖计算记录。
#     """
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='deleted_pending')
#
#     if request.method == 'POST':
#         record.status = 'uploaded_approved'
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'cancel_delete_pending_over_under_excavation.html', {'record': record})
#
# @login_required
# def cancel_delete_pending_tunnel_contour(request, record_id):
#     """
#     用户取消“删除待审批”的隧道轮廓记录。
#     """
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='deleted_pending')
#
#     if request.method == 'POST':
#         record.status = 'uploaded_approved'
#         record.save()
#         return redirect('user_records_view')
#
#     return render(request, 'cancel_delete_pending_tunnel_contour.html', {'record': record})
#
#
# #下面四个是重新申请的
# @login_required
# def reapply_record(request, record_id):
#     """
#     用户重新申请审批未通过的掌子面记录。
#     """
#     # 获取未通过的记录
#     record = get_object_or_404(
#         GeologicalSketchRecord, id=record_id, created_by=request.user, status='rejected'
#     )
#
#     if request.method == 'POST':
#         # 将用户提交的数据绑定到表单
#         form = GeologicalSketchRecordForm(request.POST, instance=record)
#         if form.is_valid():
#             # 更新记录状态为 pending，表示重新申请
#             record = form.save(commit=False)
#             record.status = 'pending'  # 重新进入待审批状态
#             record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
#             record.save()
#
#             # 提示用户操作成功
#             messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
#             return redirect('user_records_view')  # 重定向到用户记录页面
#         else:
#             # 打印表单错误，方便调试
#             print("Form Errors:", form.errors)
#             return render(request, 'reapply_record.html', {'form': form, 'record': record, 'errors': form.errors})
#     else:
#         # GET 请求，绑定已有数据到表单
#         form = GeologicalSketchRecordForm(instance=record)
#     return render(request, 'reapply_record.html', {'form': form, 'record': record})
#
# @login_required
# def reapply_excavation_diagnosis(request, record_id):
#     """
#     用户重新申请审批未通过的超欠挖诊断记录。
#     """
#     # 获取未通过的记录
#     record = get_object_or_404(
#         ExcavationDiagnosis, id=record_id, created_by=request.user, status='rejected'
#     )
#
#     if request.method == 'POST':
#         # 将用户提交的数据绑定到表单
#         form = ExcavationDiagnosisForm(request.POST, instance=record)
#         if form.is_valid():
#             # 更新记录状态为 pending，表示重新申请
#             record = form.save(commit=False)
#             record.status = 'pending'  # 重新进入待审批状态
#             record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
#             record.save()
#
#             # 提示用户操作成功
#             messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
#             return redirect('user_records_view')  # 重定向到用户记录页面
#         else:
#             # 打印表单错误，方便调试
#             print("Form Errors:", form.errors)
#             return render(request, 'reapply_excavation_diagnosis.html', {'form': form, 'record': record, 'errors': form.errors})
#     else:
#         # GET 请求，绑定已有数据到表单
#         form = ExcavationDiagnosisForm(instance=record)
#     return render(request, 'reapply_excavation_diagnosis.html', {'form': form, 'record': record})
#
# @login_required
# def reapply_over_under_calculation(request, record_id):
#     """
#     用户重新申请审批未通过的超欠挖计算记录。
#     """
#     # 获取未通过的记录
#     record = get_object_or_404(
#         OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='rejected'
#     )
#
#     if request.method == 'POST':
#         # 将用户提交的数据绑定到表单
#         form = OverUnderExcavationForm(request.POST, instance=record)
#         if form.is_valid():
#             # 更新记录状态为 pending，表示重新申请
#             record = form.save(commit=False)
#             record.status = 'pending'  # 重新进入待审批状态
#             record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
#             record.save()
#
#             # 提示用户操作成功
#             messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
#             return redirect('user_records_view')  # 重定向到用户记录页面
#         else:
#             # 打印表单错误，方便调试
#             print("Form Errors:", form.errors)
#             return render(request, 'reapply_over_under_calculation.html', {'form': form, 'record': record, 'errors': form.errors})
#     else:
#         # GET 请求，绑定已有数据到表单
#         form = OverUnderExcavationForm(instance=record)
#     return render(request, 'reapply_over_under_calculation.html', {'form': form, 'record': record})
#
# @login_required
# def reapply_tunnel_contour(request, record_id):
#     """
#     用户重新申请审批未通过的隧道轮廓信息记录。
#     """
#     # 获取未通过的记录
#     record = get_object_or_404(
#         TunnelContourInfo, id=record_id, created_by=request.user, status='rejected'
#     )
#
#     if request.method == 'POST':
#         # 将用户提交的数据绑定到表单
#         form = TunnelContourForm(request.POST, instance=record)
#         if form.is_valid():
#             # 更新记录状态为 pending，表示重新申请
#             record = form.save(commit=False)
#             record.status = 'pending'  # 重新进入待审批状态
#             record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
#             record.save()
#
#             # 提示用户操作成功
#             messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
#             return redirect('user_records_view')  # 重定向到用户记录页面
#         else:
#             # 打印表单错误，方便调试
#             print("Form Errors:", form.errors)
#             return render(request, 'reapply_tunnel_contour.html', {'form': form, 'record': record, 'errors': form.errors})
#     else:
#         # GET 请求，绑定已有数据到表单
#         form = TunnelContourForm(instance=record)
#     return render(request, 'reapply_tunnel_contour.html', {'form': form, 'record': record})
#
#
# #下面四个是用户查看信息的
# @login_required
# def view_GeologicalSketchRecord(request, record_id):
#     """
#     用户查看待审批的掌子面记录记录（只读）。
#     """
#     # 获取指定记录
#     record = get_object_or_404(GeologicalSketchRecord, id=record_id)
#     # 初始化表单实例
#     form = GeologicalSketchRecordForm(instance=record)
#     # 将所有字段设置为只读
#     for field_name, field in form.fields.items():
#         field.widget.attrs['readonly'] = 'readonly'
#         field.widget.attrs['class'] = 'form-control'
#     # 渲染模板并传递表单和记录
#     return render(request, 'view_GeologicalSketchRecord.html', {'form': form, 'record': record})
#
# @login_required
# def view_ExcavationDiagnosis(request, record_id):
#     """
#     用户查看超欠挖诊断记录（只读）。
#     """
#     # 获取记录
#     record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user)
#     # 初始化表单实例
#     form = ExcavationDiagnosisForm(instance=record)
#     # 设置所有字段为只读
#     for field_name, field in form.fields.items():
#         field.widget.attrs['readonly'] = 'readonly'
#         field.widget.attrs['class'] = 'form-control'
#     # 渲染模板
#     return render(request, 'view_ExcavationDiagnosis.html', {'form': form, 'record': record})
#
# @login_required
# def view_OverUnderExcavation(request, record_id):
#     """
#     用户查看超欠挖计算记录（只读）。
#     """
#     # 获取记录
#     record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user)
#     # 初始化表单实例
#     form = OverUnderExcavationForm(instance=record)
#     # 设置所有字段为只读
#     for field_name, field in form.fields.items():
#         field.widget.attrs['readonly'] = 'readonly'
#         field.widget.attrs['class'] = 'form-control'
#     # 渲染模板
#     return render(request, 'view_OverUnderExcavation.html', {'form': form, 'record': record})
#
# @login_required
# def view_TunnelContour(request, record_id):
#     """
#     用户查看隧道轮廓记录（只读）。
#     """
#     # 获取记录
#     record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user)
#     # 初始化表单实例
#     form = TunnelContourForm(instance=record)
#     # 设置所有字段为只读
#     for field_name, field in form.fields.items():
#         field.widget.attrs['readonly'] = 'readonly'
#         field.widget.attrs['class'] = 'form-control'
#     # 渲染模板
#     return render(request, 'view_TunnelContour.html', {'form': form, 'record': record})
#
#
#
# #用户管理
# @login_required
# def user_management(request):
#     """
#     用户管理视图。
#     - 显示所有用户。
#     - 支持按用户名或邮箱搜索用户。
#     """
#     User = get_user_model()
#     search_query = request.GET.get('search', '')  # 获取搜索框的输入
#     if search_query:
#         users = User.objects.filter(
#             Q(username__icontains=search_query) | Q(email__icontains=search_query)
#         )  # 按用户名或邮箱搜索
#     else:
#         users = User.objects.all()  # 默认展示所有用户
#
#     return render(request, 'user_management.html', {'users': users, 'search_query': search_query})
#
# @login_required
# def edit_user(request, user_id):
#     """
#     修改用户角色视图。
#     - 审计员 (auditor) 角色不可修改。
#     - 只能在管理员 (admin) 和普通用户 (user) 之间切换。
#     """
#     User = get_user_model()
#     user = get_object_or_404(User, id=user_id)
#
#     # 如果用户是审计员，显示不可修改提示
#     if user.role == 'auditor':
#         return render(request, 'edit_user.html', {'user': user, 'cannot_modify': True})
#
#     if request.method == 'POST':
#         role = request.POST.get('role')
#         if role in ['admin', 'user']:  # 验证提交的角色是否有效
#             user.role = role
#             user.save()
#             return redirect('user_management')
#         else:
#             return render(request, 'edit_user.html', {'user': user, 'error': '无效的角色选择'})
#
#     return render(request, 'edit_user.html', {'user': user, 'cannot_modify': False})
#
# @login_required
# def add_user(request):
#     """
#     新增用户视图。
#     - 支持选择所有角色 (admin, user, auditor)。
#     """
#     User = get_user_model()
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role')
#
#         # 验证输入数据
#         if username and email and password and role in ['admin', 'user', 'auditor']:
#             User.objects.create_user(username=username, email=email, password=password, role=role)
#             return redirect('user_management')
#         else:
#             return render(request, 'add_user.html', {'error': '请输入完整信息并选择有效的角色'})
#
#     return render(request, 'add_user.html')
#
# @login_required
# def delete_user(request, user_id):
#     """
#     删除用户视图。
#     """
#     User = get_user_model()
#     user = get_object_or_404(User, id=user_id)
#     user.delete()
#     return redirect('user_management')
#
#
#
#
# #下面四个是统计信息
# @login_required
# def geological_statistics(request):
#     """
#     Geological statistics view:
#     - Users see their own data statistics.
#     - Admins see global data statistics.
#     """
#
#     # Determine if the user is an admin
#     is_admin = request.user.role == 'admin'
#
#     # Get the dataset: Admins get all data, regular users get only their own data
#     if is_admin:
#         records = GeologicalSketchRecord.objects.all()
#     else:
#         records = GeologicalSketchRecord.objects.filter(created_by=request.user)
#
#     # Prepare the dataset
#     data = pd.DataFrame.from_records(
#         records.values(
#             'excavation_width',
#             'excavation_height',
#             'excavation_area',
#             'design_section',
#             'rock_strength',
#             'weathering_degree',
#             'created_at',  # Record creation time for trend analysis
#         )
#     )
#
#     # Initialize statistics and charts
#     statistics = {}
#     charts = {}
#
#     if not data.empty:
#         # Convert relevant columns to numeric and clean data
#         for col in ['excavation_width', 'excavation_height', 'excavation_area', 'rock_strength']:
#             data[col] = pd.to_numeric(data[col], errors='coerce')  # Convert to numeric, invalid entries become NaN
#
#         # Drop rows with NaN in critical numeric columns
#         data = data.dropna(subset=['excavation_width', 'excavation_height', 'excavation_area', 'rock_strength'])
#
#         # Compute statistics
#         statistics['record_count'] = len(data)  # Number of records uploaded
#         statistics['excavation_width_avg'] = data['excavation_width'].mean()  # Average excavation width
#         statistics['excavation_height_avg'] = data['excavation_height'].mean()  # Average excavation height
#         statistics['excavation_area_avg'] = data['excavation_area'].mean()  # Average excavation area
#         statistics['rock_strength_avg'] = data['rock_strength'].mean()  # Average rock strength
#
#         # Ensure 'created_at' is in datetime format
#         if 'created_at' in data:
#             data['created_at'] = pd.to_datetime(data['created_at'], errors='coerce')  # Convert to datetime
#             data = data.dropna(subset=['created_at'])  # Remove rows with invalid dates
#
#         # Generate excavation width distribution histogram
#         try:
#             plt.figure(figsize=(8, 4))
#             data['excavation_width'].plot(kind='hist', bins=10, color='blue', alpha=0.7, edgecolor='black')
#             plt.title('Excavation Width Distribution')
#             plt.xlabel('Excavation Width')
#             plt.ylabel('Frequency')
#             buf = io.BytesIO()
#             plt.savefig(buf, format='png')
#             buf.seek(0)
#             charts['excavation_width_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')
#             buf.close()
#             plt.close()
#         except Exception as e:
#             print("Error plotting excavation width distribution:", e)
#
#         # Generate excavation height vs. excavation area scatter plot
#         try:
#             plt.figure(figsize=(8, 4))
#             plt.scatter(data['excavation_height'], data['excavation_area'], alpha=0.6, color='green')
#             plt.title('Excavation Height vs Excavation Area')
#             plt.xlabel('Excavation Height')
#             plt.ylabel('Excavation Area')
#             buf = io.BytesIO()
#             plt.savefig(buf, format='png')
#             buf.seek(0)
#             charts['excavation_height_vs_area'] = base64.b64encode(buf.getvalue()).decode('utf-8')
#             buf.close()
#             plt.close()
#         except Exception as e:
#             print("Error plotting excavation height vs. area scatter plot:", e)
#
#         # Generate design section trend over time
#         try:
#             plt.figure(figsize=(8, 4))
#             plt.plot(data['created_at'], data['design_section'], marker='o', color='purple')
#             plt.title('Design Section Trend Over Time')
#             plt.xlabel('Time')
#             plt.ylabel('Design Section')
#             buf = io.BytesIO()
#             plt.savefig(buf, format='png')
#             buf.seek(0)
#             charts['design_section_trend'] = base64.b64encode(buf.getvalue()).decode('utf-8')
#             buf.close()
#             plt.close()
#         except Exception as e:
#             print("Error plotting design section trend:", e)
#
#     # Render the template
#     return render(
#         request,
#         'geological_statistics.html',
#         {
#             'statistics': statistics,
#             'charts': charts,
#             'is_admin': is_admin,
#         }
#     )
#
#
# @login_required
# def excavation_calculation_statistics(request):
#     """
#     超欠挖计算统计视图：
#     - 用户看到自己的数据统计。
#     - 管理员看到全局数据统计。
#     """
#     # 判断是否是管理员
#     is_admin = request.user.role == 'admin'
#
#     # 获取数据集：管理员获取所有数据，普通用户获取个人数据
#     if is_admin:
#         records = OverUnderExcavationCalculation.objects.all()
#     else:
#         records = OverUnderExcavationCalculation.objects.filter(created_by=request.user)
#
#     print("Records count:", records.count())  # 调试信息
#
#     # 准备数据
#     data = pd.DataFrame.from_records(
#         records.values(
#             'line_name',
#             'north_direction_angle',
#             'radius',
#             'length',
#             'height',
#             'angle_increment',
#             'created_at',
#         )
#     )
#
#     # 初始化统计结果
#     statistics = {}
#
#     if not data.empty:
#         # 基础统计
#         statistics['record_count'] = len(data)
#         statistics['radius_avg'] = data['radius'].mean()
#         statistics['length_avg'] = data['length'].mean()
#         statistics['height_avg'] = data['height'].mean()
#
#         # 处理半径分布数据
#         radius_stats = data.groupby('line_name')['radius'].agg(['mean', 'min', 'max']).reset_index()
#         statistics['radius_data'] = {
#             'labels': radius_stats['line_name'].tolist(),
#             'means': radius_stats['mean'].tolist(),
#             'mins': radius_stats['min'].tolist(),
#             'maxs': radius_stats['max'].tolist()
#         }
#
#         # 处理长度和高度数据
#         length_height_data = []
#         for _, row in data.iterrows():
#             length_height_data.append({
#                 'x': float(row['length']),
#                 'y': float(row['height'])
#             })
#         statistics['length_height_data'] = json.dumps(length_height_data)
#
#         # 处理角度增量的时间序列数据
#         data['year'] = pd.to_datetime(data['created_at']).dt.year
#         angle_by_year = data.groupby('year')['angle_increment'].agg(['mean', 'min', 'max']).reset_index()
#
#         # 确保包含2021-2025的所有年份数据
#         all_years = range(2021, 2026)
#         angle_data = []
#         for year in all_years:
#             year_stats = angle_by_year[angle_by_year['year'] == year]
#             if not year_stats.empty:
#                 angle_data.append({
#                     'mean': float(year_stats['mean'].iloc[0]),
#                     'min': float(year_stats['min'].iloc[0]),
#                     'max': float(year_stats['max'].iloc[0])
#                 })
#             else:
#                 angle_data.append({
#                     'mean': 0,
#                     'min': 0,
#                     'max': 0
#                 })
#
#         statistics['angle_data'] = {
#             'years': list(all_years),
#             'means': [d['mean'] for d in angle_data],
#             'mins': [d['min'] for d in angle_data],
#             'maxs': [d['max'] for d in angle_data]
#         }
#
#         # 汇总统计数据
#         statistics['summary_data'] = {
#             'radius': statistics['radius_avg'],
#             'length': statistics['length_avg'],
#             'height': statistics['height_avg'],
#             'angle': data['angle_increment'].mean()
#         }
#
#     print("Statistics data:", statistics)  # 调试信息
#
#     return render(
#         request,
#         'excavation_calculation_statistics.html',
#         {
#             'statistics': statistics,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def excavation_diagnosis_statistics(request):
#     """
#     超欠挖诊断统计视图：
#     - 用户看到自己的数据统计。
#     - 管理员看到全局数据统计。
#     """
#     # 判断是否是管理员
#     is_admin = request.user.role == 'admin'
#
#     # 获取数据集：管理员获取所有数据，普通用户获取个人数据
#     if is_admin:
#         records = ExcavationDiagnosis.objects.all()
#     else:
#         records = ExcavationDiagnosis.objects.filter(created_by=request.user)
#
#     print("Records count:", records.count())  # 调试信息
#
#     # 准备数据
#     data = pd.DataFrame.from_records(
#         records.values(
#             'over_excavation_area',
#             'under_excavation_area',
#             'max_over_excavation',
#             'max_under_excavation',
#             'average_over_excavation',
#             'average_under_excavation',
#             'created_at',
#         )
#     )
#
#     # 初始化统计结果
#     statistics = {}
#
#     if not data.empty:
#         # 基础统计
#         statistics['over_excavation_area_avg'] = data['over_excavation_area'].mean()
#         statistics['under_excavation_area_avg'] = data['under_excavation_area'].mean()
#         statistics['max_over_excavation'] = data['max_over_excavation'].max()
#         statistics['max_under_excavation'] = data['max_under_excavation'].min()  # 使用min因为欠挖是负值
#
#         # 处理散点图数据
#         scatter_data = []
#         for _, row in data.iterrows():
#             scatter_data.append({
#                 'x': float(row['over_excavation_area']),
#                 'y': float(row['under_excavation_area'])
#             })
#         statistics['scatter_data'] = json.dumps(scatter_data)
#
#         # 处理月度数据
#         data['month'] = pd.to_datetime(data['created_at']).dt.strftime('%Y-%m')
#         monthly_group = data.groupby('month').agg({
#             'over_excavation_area': 'sum',
#             'under_excavation_area': 'sum',
#             'max_over_excavation': 'max',
#             'max_under_excavation': 'min'  # 使用min因为欠挖是负值
#         }).reset_index()
#
#         # 按时间排序
#         monthly_group = monthly_group.sort_values('month')
#
#         statistics['months'] = monthly_group['month'].tolist()
#         statistics['monthly_data'] = {
#             'over': monthly_group['over_excavation_area'].tolist(),
#             'under': monthly_group['under_excavation_area'].tolist(),
#             'max_over': monthly_group['max_over_excavation'].tolist(),
#             'max_under': monthly_group['max_under_excavation'].tolist()
#         }
#
#         # 处理时间序列数据
#         data['date'] = pd.to_datetime(data['created_at']).dt.strftime('%Y-%m-%d')
#         time_series = data.groupby('date').agg({
#             'over_excavation_area': 'sum',
#             'under_excavation_area': 'sum'
#         }).reset_index()
#
#         # 计算累计变化趋势
#         time_series['cumulative'] = (time_series['over_excavation_area'] +
#                                      time_series['under_excavation_area']).cumsum()
#
#         # 按时间排序
#         time_series = time_series.sort_values('date')
#
#         # 添加到统计结果
#         statistics['time_series'] = {
#             'dates': time_series['date'].tolist(),
#             'over': time_series['over_excavation_area'].tolist(),
#             'under': time_series['under_excavation_area'].tolist(),
#             'cumulative': time_series['cumulative'].tolist()
#         }
#
#     print("Statistics data:", statistics)  # 调试信息
#
#     return render(
#         request,
#         'excavation_diagnosis_statistics.html',
#         {
#             'statistics': statistics,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def tunnel_statistics(request):
#     """
#     隧道轮廓统计视图：
#     - 用户看到自己的数据统计。
#     - 管理员看到全局数据统计。
#     """
#
#     # 判断是否是管理员
#     is_admin = request.user.role == 'admin'
#
#     # 获取数据集：管理员获取所有数据，普通用户获取个人数据
#     if is_admin:
#         records = TunnelContourInfo.objects.all()
#     else:
#         records = TunnelContourInfo.objects.filter(created_by=request.user)
#     print(records)
#     # 准备数据
#     data = pd.DataFrame.from_records(
#         records.values(
#             'cr',
#             'rcl',
#             'vo',
#             'c1',
#             'c2',
#             'c3',
#             'created_at',  # 记录创建时间，用于趋势分析
#         )
#     )
#
#     # 初始化统计结果和图表
#     statistics = {}
#     charts = {}
#
#     if not data.empty:
#         # 统计指标
#         statistics['record_count'] = len(data)  # 上传记录数
#         statistics['avg_cr'] = data['cr'].mean()  # 调整指数平均值
#         statistics['avg_rcl'] = data['rcl'].mean()  # 粗糙度平均值
#         statistics['avg_vo'] = data['vo'].mean()  # 纵向超挖变化平均值
#
#         # 调整指数分布图
#         plt.figure(figsize=(8, 4))
#         data['cr'].plot(kind='hist', bins=10, color='blue', alpha=0.7, edgecolor='black')
#         plt.title('Adjustment Index (CR) Distribution')
#         plt.xlabel('CR')
#         plt.ylabel('Frequency')
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         charts['cr_distribution'] = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         plt.close()
#
#         # RCL vs VO 散点图
#         plt.figure(figsize=(8, 4))
#         plt.scatter(data['rcl'], data['vo'], alpha=0.6, color='green')
#         plt.title('RCL vs VO')
#         plt.xlabel('RCL')
#         plt.ylabel('VO')
#         buf = io.BytesIO()
#         plt.savefig(buf, format='png')
#         buf.seek(0)
#         charts['rcl_vs_vo'] = base64.b64encode(buf.getvalue()).decode('utf-8')
#         buf.close()
#         plt.close()
#     time_series = data.groupby(
#         pd.Grouper(key='created_at', freq='Y')
#     )['vo'].mean().to_dict()
#
#     statistics['longitudinal_trend'] = list(time_series.values())
#     # 渲染模板
#     return render(
#         request,
#         'tunnel_statistics.html',
#         {
#             'statistics': statistics,
#             'charts': charts,
#             'is_admin': is_admin,
#         }
#     )
#
#
#
#
#
#
#
#
# #数据导出
# @login_required
# def export_geological_view(request):
#     """
#     渲染掌子面导出界面，用户可以选择字段。
#     """
#     # 判断用户角色
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 可选的所有字段
#     fields = [
#         {'name': 'face_id', 'label': '掌子面编号'},
#         {'name': 'project_id', 'label': '施工项目编号'},
#         {'name': 'inspection_date', 'label': '检查日期'},
#         {'name': 'distance', 'label': '里程'},
#         {'name': 'design_section', 'label': '设计断面'},
#         {'name': 'excavation_width', 'label': '开挖宽度'},
#         {'name': 'excavation_height', 'label': '开挖高度'},
#         {'name': 'excavation_area', 'label': '开挖面积'},
#         {'name': 'rock_strength', 'label': '岩石强度'},
#         {'name': 'weathering_degree', 'label': '风化程度'},
#         {'name': 'crack_width', 'label': '裂缝宽度'},
#         {'name': 'crack_shape', 'label': '裂缝形态'},
#         {'name': 'water_condition', 'label': '渗水状态'},
#         {'name': 'rockburst_tendency', 'label': '岩爆发育程度'},
#     ]
#
#     return render(
#         request,
#         'export_geological.html',
#         {
#             'fields': fields,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def export_geological_records(request):
#     """
#     导出掌子面数据为 Excel。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 获取数据集
#     if is_admin:
#         records = GeologicalSketchRecord.objects.all()
#     else:
#         records = GeologicalSketchRecord.objects.filter(created_by=request.user)
#
#     # 获取用户选择的字段
#     default_fields = [
#         'face_id', 'project_id', 'inspection_date', 'distance', 'design_section',
#         'excavation_width', 'excavation_height', 'excavation_area',
#         'rock_strength', 'weathering_degree', 'crack_width'
#     ]
#     selected_fields = request.GET.getlist('fields', default_fields)
#
#     if not selected_fields:
#         selected_fields = default_fields
#
#     # 转换数据为 DataFrame
#     data = pd.DataFrame.from_records(records.values(*selected_fields))
#
#     # 处理时区问题，将所有的时间字段转换为无时区的时间
#     for field in ['inspection_date', 'created_at', 'updated_at']:  # 修改为实际的时间字段名
#         if field in data.columns:
#             data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)
#
#     # 创建 Excel 响应
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="geological_records.xlsx"'
#
#     # 写入数据到 Excel
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         data.to_excel(writer, index=False, sheet_name='Geological Records')
#
#     return response
#
# @login_required
# def export_excavation_calculation_view(request):
#     """
#     渲染导出界面，用户可以选择超欠挖计算字段。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 可选的所有字段
#     fields = [
#         {'name': 'face_id', 'label': '掌子面编号'},
#         {'name': 'project_id', 'label': '施工项目编号'},
#         {'name': 'inspection_date', 'label': '检查日期'},
#         {'name': 'measurement_date', 'label': '测量日期'},
#         {'name': 'line_name', 'label': '线路名称'},
#         {'name': 'north_direction_angle', 'label': '北方向角'},
#         {'name': 'radius', 'label': '半径'},
#         {'name': 'length', 'label': '长度'},
#         {'name': 'east_coordinate', 'label': '东坐标'},
#         {'name': 'north_coordinate', 'label': '北坐标'},
#         {'name': 'height', 'label': '高度'},
#     ]
#
#     return render(
#         request,
#         'export_excavation_calculation.html',
#         {
#             'fields': fields,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def export_excavation_calculation_records(request):
#     """
#     导出超欠挖计算数据为 Excel。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 获取数据集
#     if is_admin:
#         records = OverUnderExcavationCalculation.objects.all()
#     else:
#         records = OverUnderExcavationCalculation.objects.filter(created_by=request.user)
#
#     # 获取用户选择的字段
#     default_fields = [
#         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#         'line_name', 'north_direction_angle', 'radius',
#         'length', 'east_coordinate', 'north_coordinate', 'height'
#     ]
#     selected_fields = request.GET.getlist('fields', default_fields)
#
#     if not selected_fields:
#         selected_fields = default_fields
#
#     # 转换数据为 DataFrame
#     data = pd.DataFrame.from_records(records.values(*selected_fields))
#
#     # 处理时区问题
#     for field in ['inspection_date', 'measurement_date']:
#         if field in data.columns:
#             data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)
#
#     # 创建 Excel 响应
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="excavation_calculation_records.xlsx"'
#
#     # 写入数据到 Excel
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         data.to_excel(writer, index=False, sheet_name='Excavation Calculation Records')
#
#     return response
#
# @login_required
# def export_excavation_diagnosis_view(request):
#     """
#     渲染导出界面，用户可以选择超欠挖诊断字段。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 可选的所有字段
#     fields = [
#         {'name': 'face_id', 'label': '掌子面编号'},
#         {'name': 'project_id', 'label': '施工项目编号'},
#         {'name': 'inspection_date', 'label': '检查日期'},
#         {'name': 'measurement_date', 'label': '测量日期'},
#         {'name': 'mileage', 'label': '里程'},
#         {'name': 'design_section', 'label': '设计断面'},
#         {'name': 'measured_section', 'label': '实测断面'},
#         {'name': 'over_excavation_area', 'label': '超挖面积'},
#         {'name': 'under_excavation_area', 'label': '欠挖面积'},
#         {'name': 'max_over_excavation', 'label': '最大超挖'},
#         {'name': 'max_under_excavation', 'label': '最大欠挖'},
#         {'name': 'average_over_excavation', 'label': '平均超挖'},
#         {'name': 'average_under_excavation', 'label': '平均欠挖'},
#     ]
#
#     return render(
#         request,
#         'export_excavation_diagnosis.html',
#         {
#             'fields': fields,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def export_excavation_diagnosis_records(request):
#     """
#     导出超欠挖诊断数据为 Excel。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 获取数据集
#     if is_admin:
#         records = ExcavationDiagnosis.objects.all()
#     else:
#         records = ExcavationDiagnosis.objects.filter(created_by=request.user)
#
#     # 获取用户选择的字段
#     default_fields = [
#         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#         'mileage', 'design_section', 'measured_section',
#         'over_excavation_area', 'under_excavation_area',
#         'max_over_excavation', 'max_under_excavation',
#         'average_over_excavation', 'average_under_excavation'
#     ]
#     selected_fields = request.GET.getlist('fields', default_fields)
#
#     if not selected_fields:
#         selected_fields = default_fields
#
#     # 转换数据为 DataFrame
#     data = pd.DataFrame.from_records(records.values(*selected_fields))
#
#     # 处理时区问题
#     for field in ['inspection_date', 'measurement_date']:
#         if field in data.columns:
#             data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)
#
#     # 创建 Excel 响应
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="excavation_diagnosis_records.xlsx"'
#
#     # 写入数据到 Excel
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         data.to_excel(writer, index=False, sheet_name='Excavation Diagnosis Records')
#
#     return response
#
# @login_required
# def export_tunnel_contour_view(request):
#     """
#     渲染导出界面，用户可以选择隧道轮廓字段。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 可选的所有字段
#     fields = [
#         {'name': 'face_id', 'label': '隧道编号'},
#         {'name': 'project_id', 'label': '施工项目编号'},
#         {'name': 'inspection_date', 'label': '检查日期'},
#         {'name': 'measurement_date', 'label': '测量日期'},
#         {'name': 'cr', 'label': '调整指数范围的常数 Cr'},
#         {'name': 'w1', 'label': '权重值 w1'},
#         {'name': 'w2', 'label': '权重值 w2'},
#         {'name': 'w3', 'label': '权重值 w3'},
#         {'name': 'od', 'label': '超挖深度 Od'},
#         {'name': 'rcl', 'label': '轮廓粗糙度 RCL'},
#         {'name': 'vo', 'label': '纵向超挖变化 Vo'},
#         {'name': 'c1', 'label': '修正因子 c1'},
#         {'name': 'c2', 'label': '修正因子 c2'},
#         {'name': 'c3', 'label': '修正因子 c3'},
#     ]
#
#     return render(
#         request,
#         'export_tunnel_contour.html',
#         {
#             'fields': fields,
#             'is_admin': is_admin,
#         }
#     )
#
# @login_required
# def export_tunnel_contour_records(request):
#     """
#     导出隧道轮廓数据为 Excel。
#     """
#     is_admin = request.user.role == 'admin' or 'auditor'
#
#     # 获取数据集
#     if is_admin:
#         records = TunnelContourInfo.objects.all()
#     else:
#         records = TunnelContourInfo.objects.filter(created_by=request.user)
#
#     # 获取用户选择的字段
#     default_fields = [
#         'face_id', 'project_id', 'inspection_date', 'measurement_date',
#         'cr', 'w1', 'w2', 'w3', 'od', 'rcl', 'vo', 'c1', 'c2', 'c3'
#     ]
#     selected_fields = request.GET.getlist('fields', default_fields)
#
#     if not selected_fields:
#         selected_fields = default_fields
#
#     # 转换数据为 DataFrame
#     data = pd.DataFrame.from_records(records.values(*selected_fields))
#
#     # 处理时区问题
#     for field in ['inspection_date', 'measurement_date']:
#         if field in data.columns:
#             data[field] = pd.to_datetime(data[field]).dt.tz_localize(None)
#
#     # 创建 Excel 响应
#     response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     response['Content-Disposition'] = 'attachment; filename="tunnel_contour_records.xlsx"'
#
#     # 写入数据到 Excel
#     with pd.ExcelWriter(response, engine='openpyxl') as writer:
#         data.to_excel(writer, index=False, sheet_name='Tunnel Contour Records')
#
#     return response
#
#
#
# #数据库备份
#
#
# # @login_required
# # def backup_view(request):
# #     """
# #     备份视图
# #     - GET 请求：渲染备份页面
# #     - POST 请求：触发备份操作
# #     """
# #     if request.method == 'POST':  # POST 请求触发备份
# #         try:
# #             result = backup_all_tables()  # 调用备份逻辑
# #             return JsonResponse(result)  # 返回结果给前端
# #         except Exception as e:
# #             return JsonResponse({"status": "error", "message": f"备份失败：{str(e)}"})
# #     else:  # GET 请求渲染 HTML 页面
# #         return render(request, 'backup.html')
#
# @login_required
# def backup_view(request):
#     """
#     备份视图
#     - GET 请求：渲染备份页面
#     - POST 请求：触发备份操作（支持备份单个表或多个表）
#     """
#     if request.method == 'POST':
#         try:
#             body = json.loads(request.body)  # 解析 JSON 数据
#             table_names = body.get("table_names", [])  # 获取表名称列表
#
#             if not table_names:
#                 return JsonResponse({"status": "error", "message": "未选择任何表进行备份"})
#
#             supported_tables = {
#                 "GeologicalSketchRecord": GeologicalSketchRecord.objects.all(),
#                 "OverUnderExcavationCalculation": OverUnderExcavationCalculation.objects.all(),
#                 "ExcavationDiagnosis": ExcavationDiagnosis.objects.all(),
#                 "TunnelContourInfo": TunnelContourInfo.objects.all(),
#                 "DataStorage": DataStorage.objects.all(),  # 新增 DataStorage 表
#             }
#
#             backup_results = []
#             success_count = 0
#
#             for table_name in table_names:
#                 if table_name in supported_tables:
#                     queryset = supported_tables[table_name]
#                     try:
#                         logger.info(f"开始备份表：{table_name}")
#                         result = backup_table(queryset, table_name)
#                         backup_results.append(result)
#
#                         if result.get("status") == "success":
#                             success_count += 1
#                     except Exception as table_error:
#                         logger.error(f"备份表 {table_name} 失败：{table_error}")
#                         backup_results.append({"status": "error", "message": f"表 {table_name} 备份失败：{str(table_error)}"})
#                 else:
#                     backup_results.append({"status": "error", "message": f"表 {table_name} 不存在"})
#
#             overall_status = "success" if success_count == len(table_names) else "partial_success"
#
#             return JsonResponse({
#                 "status": overall_status,
#                 "message": "备份完成" if overall_status == "success" else "部分表备份失败",
#                 "results": backup_results
#             })
#
#         except json.JSONDecodeError:
#             logger.error("请求数据格式错误，无法解析 JSON")
#             return JsonResponse({"status": "error", "message": "请求数据格式错误，无法解析 JSON"})
#         except DatabaseError as db_error:
#             logger.error(f"数据库错误：{db_error}")
#             return JsonResponse({"status": "error", "message": f"数据库错误：{str(db_error)}"})
#         except Exception as e:
#             logger.error(f"备份失败：{e}")
#             return JsonResponse({"status": "error", "message": f"备份失败：{str(e)}"})
#
#     else:
#         return render(request, 'backup.html')
#
#
#
# # 下面这些是数据库恢复的
# def restore_database(request):
#     """
#     恢复数据库的视图
#     :param request: 请求对象
#     :return: 恢复结果的 JSON 或 HTML 页面
#     """
#     if request.method == "POST":
#         # 获取前端提交的备份文件名
#         file_name = request.POST.get("backup_file")
#
#         if not file_name:
#             return JsonResponse({"status": "error", "message": "未选择备份文件"})
#
#         # 获取文件路径
#         file_path = os.path.join(BACKUP_DIR, file_name)
#         if not os.path.exists(file_path):
#             return JsonResponse({"status": "error", "message": "备份文件不存在"})
#
#         # 匹配目标表模型：通过文件名推断目标表
#         #这个是将数据库恢复到正常的四个表里面的（tunnelcontourinfo等等）
#         table_mapping = {
#             "GeologicalSketchRecord": GeologicalSketchRecord,
#             "OverUnderExcavationCalculation": OverUnderExcavationCalculation,
#             "ExcavationDiagnosis": ExcavationDiagnosis,
#             "TunnelContourInfo": TunnelContourInfo,  #这个如果删除Backup就是恢复原来的数据库了（就是把TunnelContourInfo表清空然后根据json重新恢复）
#             "DataStorage": DataStorage,  # 新增的表
#         }
#
#         # 下面的这个是将数据库恢复到四个备份表里面的（tunnelcontourinfobackup等等）
#         # table_mapping = {
#         #     "GeologicalSketchRecord": GeologicalSketchRecordBackup,
#         #     "OverUnderExcavationCalculation": OverUnderExcavationCalculationBackup,
#         #     "ExcavationDiagnosis": ExcavationDiagnosisBackup,
#         #     "TunnelContourInfo": TunnelContourInfoBackup,  #这个如果删除Backup就是恢复原来的数据库了（就是把TunnelContourInfo表清空然后根据json重新恢复）
#         # }
#
#         # 提取表名，例如从文件名中解析出 "GeologicalSketchRecordBackup"
#         table_name = None
#         for key in table_mapping.keys():
#             if key in file_name:
#                 table_name = key
#                 break
#
#         print(table_name)
#         if not table_name:
#             return JsonResponse({"status": "error", "message": "无法识别目标表，请检查备份文件名"})
#
#         model_class = table_mapping.get(table_name)
#
#         # 调用单个表恢复函数
#         result = restore_table_from_backup(file_path, model_class)
#         return JsonResponse(result)
#
#     else:
#         # GET 请求，显示可用备份文件
#         backup_files = get_backup_files()
#         return render(
#             request,
#             "restore_database.html",
#             {"backup_files": backup_files},
#         )
#
#
#
#
#
#
#
#
#
#
# #展示区块链页面（有问题）
# def blockchain_records_view(request):
#     """
#     从区块链获取存储数据并展示
#     """
#     # 假设我们有记录所有交易哈希
#     transactions = DataAuditTrail.objects.filter(operation_type="DELETE").order_by('-timestamp')
#     records = []
#
#     for tx in transactions:
#         tx_hash = tx.trace_id
#         # 调用 Conflux 测试网 API 查询交易详情
#         url = f"https://testnet.confluxscan.io/v1/transaction/{tx_hash}"
#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 tx_data = response.json()
#                 records.append({
#                     "tx_hash": tx_hash,
#                     "block_number": tx_data["blockNumber"],
#                     "data": tx_data["input"],
#                 })
#         except Exception as e:
#             print(f"查询交易 {tx_hash} 时出错: {e}")
#
#     return render(request, 'blockchain_records.html', {"records": records})
#
#
#
#
#
# # 查看文件
# @login_required
# def file_records_view(request):
#     """
#     展示文件记录，包括新增待审批、修改待审批、删除待审批、未通过审批和有效数据，并添加分页功能。
#     """
#     # 每页显示条数
#     items_per_page = 10
#
#     # 分页查询
#     pending_new_files_page_obj = paginate_queryset(
#         DataStorage.objects.filter(status='pending', uploaded_by=request.user),
#         request,
#         items_per_page,
#         page_param='pending_new_files_page'
#     )
#     pending_modified_files_page_obj = paginate_queryset(
#         DataStorage.objects.filter(status='modified_pending', uploaded_by=request.user),
#         request,
#         items_per_page,
#         page_param='pending_modified_files_page'
#     )
#     pending_deleted_files_page_obj = paginate_queryset(
#         DataStorage.objects.filter(status='deleted_pending',  uploaded_by=request.user),
#         request,
#         items_per_page,
#         page_param='pending_deleted_files_page'
#     )
#     rejected_files_page_obj = paginate_queryset(
#         DataStorage.objects.filter(status='rejected', uploaded_by=request.user),
#         request,
#         items_per_page,
#         page_param='rejected_files_page'
#     )
#     approved_files_page_obj = paginate_queryset(
#         DataStorage.objects.filter(status='uploaded_approved', uploaded_by=request.user),
#         request,
#         items_per_page,
#         page_param='approved_files_page'
#     )
#
#     # 渲染模板并传递分页对象
#     return render(
#         request,
#         'file_record.html',
#         {
#             'pending_new_files': pending_new_files_page_obj,
#             'pending_modified_files': pending_modified_files_page_obj,
#             'pending_deleted_files': pending_deleted_files_page_obj,
#             'rejected_files': rejected_files_page_obj,
#             'approved_files': approved_files_page_obj,
#         },
#     )
#
# #查看
# @login_required
# def view_file(request, file_id):
#     try:
#         file_record = DataStorage.objects.get(id=file_id, uploaded_by=request.user)
#     except DataStorage.DoesNotExist:
#         messages.error(request, "文件不存在或您无权查看此文件！")
#         return redirect('file_records_view')
#
#     # 根据文件类型，处理文件内容
#     file_data = None
#     if file_record.file_type in ['text', 'pdf']:
#         file_data = file_record.file_data.decode('utf-8', errors='ignore') if file_record.file_data else None
#
#     return render(request, 'view_file.html', {
#         'file_record': file_record,
#         'file_data': file_data,
#     })