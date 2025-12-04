import json
from django.contrib.auth.hashers import make_password
from django.db.models import Avg

from ..models import User, MySQLGeneralLog, OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from ..models import DataAuditTrail
import os
from django.contrib import messages  # 用于发送消息
from records.models import DataStorage  # 假设 DataStorage 是在 records 应用中的模型
from ..models import GeologicalSketchRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from records.backup import backup_all_tables, backup_table
import logging
logger = logging.getLogger(__name__)
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import render
from ..restore import get_backup_files, BACKUP_DIR ,restore_table_from_backup


#主界面
def index_view(request):
    """主界面视图"""
    user = request.user if request.user.is_authenticated else None  # 检查用户是否登录
    return render(request, 'main.html', {'user': user})


#注册
def register_view(request):
    """
    处理用户注册请求。
    支持普通用户 (user)、管理员 (admin)、审计员 (auditor) 的角色选择。
    """
    if request.method == 'POST':  # 处理 POST 请求
        # 获取前端提交的注册表单数据
        username = request.POST.get('username')  # 用户名
        password = request.POST.get('password')  # 密码
        confirm_password = request.POST.get('confirm-password')  # 确认密码
        email = request.POST.get('email')  # 邮箱
        role = request.POST.get('role', 'user')  # 用户角色，默认为普通用户 (user)

        # 验证两次输入的密码是否一致
        if password != confirm_password:
            messages.error(request, '两次输入的密码不一致')  # 添加错误消息
            return render(request, 'base/register.html')

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在')  # 添加错误消息
            return render(request, 'base/register.html')

        # 检查密码强度（可选，增强安全性）
        if len(password) < 6 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char.islower() for char in password):
            messages.error(request, '密码必须包含大小写字母、数字，且长度不少于6个字符')  # 添加错误消息
            return render(request, 'base/register.html')

        # 创建用户对象并保存到数据库
        try:
            user = User.objects.create(
                username=username,
                password=make_password(password),  # 对密码进行哈希加密
                email=email,
                role=role  # 分配角色：普通用户、管理员或审计员
            )
            user.save()  # 保存用户对象
            messages.success(request, '注册成功！请登录')  # 添加成功消息
            return redirect('login')  # 注册成功后跳转到登录页面
        except Exception as e:
            # 如果保存失败，返回错误信息到页面
            messages.error(request, f'注册失败：{str(e)}')  # 添加错误消息
            return render(request, 'base/register.html')

    # 如果是 GET 请求，渲染注册页面
    return render(request, 'base/register.html')


#登录
def login_view(request):
    """登录视图"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户凭据
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # 强制将 next 参数设置为 index
            next_url = request.GET.get('next', '/') #这样就可以登录之后跳到index了
            print(f"Redirecting to: {next_url}")
            return redirect(next_url)
        else:
            return render(request, 'base/login.html', {'error': '用户名或密码错误'})

    return render(request, 'base/login.html')


#退出登录
def logout_view(request):
    """登出视图"""
    logout(request)  # 执行登出操作
    return redirect('login')  # 登出后跳转到登录页面


# 日志信息列表
def view_audit_logs(request):
    # 获取筛选条件
    user = request.GET.get('user', '')  # 默认为空字符串，表示不筛选用户
    operation_type = request.GET.get('operation_type', '')  # 筛选操作类型
    table_name = request.GET.get('table_name', '')  # 筛选操作表
    date_from = request.GET.get('date_from', '')  # 筛选起始日期
    date_to = request.GET.get('date_to', '')  # 筛选结束日期

    # 初始化查询集
    logs_list = DataAuditTrail.objects.all()

    # 应用筛选条件（根据选择进行筛选）
    if user:
        logs_list = logs_list.filter(user__username__icontains=user)
    if operation_type:
        logs_list = logs_list.filter(operation_type=operation_type)
    if table_name:
        logs_list = logs_list.filter(table_name=table_name)
    if date_from:
        logs_list = logs_list.filter(operation_time__gte=date_from)
    if date_to:
        logs_list = logs_list.filter(operation_time__lte=date_to)

    logs_list = logs_list.order_by('-operation_time')  # 按操作时间倒序排序

    # 分页
    paginator = Paginator(logs_list, 10)  # 每页 10 条记录
    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        logs = paginator.page(1)
    except EmptyPage:
        logs = paginator.page(paginator.num_pages)

    # 保留筛选条件的查询参数
    query_params = request.GET.copy()  # 将筛选参数复制为可变的 QueryDict
    query_params.pop('page', None)  # 移除分页参数，防止重复
    query_params_encoded = query_params.urlencode()  # 编码为 URL 查询字符串

    # 传递筛选条件和分页数据
    return render(request, 'base/view_audit_logs.html', {
        'logs': logs,
        'filters': {
            'user': user,
            'operation_type': operation_type,
            'table_name': table_name,
            'date_from': date_from,
            'date_to': date_to,
        },
        'operation_types': DataAuditTrail.objects.values_list('operation_type', flat=True).distinct(),
        'table_names': DataAuditTrail.objects.values_list('table_name', flat=True).distinct(),
        'query_params': query_params_encoded,  # 将筛选参数编码并传递给模板
    })


# 详细日志信息
def view_log_detail(request, log_id):
    # 获取指定日志记录
    log = get_object_or_404(DataAuditTrail, id=log_id)

    # 解析 JSON 数据
    try:
        data_snapshot = json.loads(log.data_snapshot) if log.data_snapshot else None
        updated_data = json.loads(log.updated_data) if log.updated_data else None
        change_details = json.loads(log.change_details) if log.change_details else None
    except json.JSONDecodeError:
        data_snapshot = updated_data = change_details = None  # 防止解析失败

    return render(request, 'base/log_detail.html', {
        'log': log,
        'data_snapshot': data_snapshot,
        'updated_data': updated_data,
        'change_details': change_details,
    })

@login_required
def backup_view(request):
    """
    备份视图
    - GET 请求：渲染备份页面
    - POST 请求：触发备份操作（支持备份单个表或多个表）
    """
    if request.method == 'POST':
        try:
            body = json.loads(request.body)  # 解析 JSON 数据
            table_names = body.get("table_names", [])  # 获取表名称列表

            if not table_names:
                return JsonResponse({"status": "error", "message": "未选择任何表进行备份"})

            supported_tables = {
                "GeologicalSketchRecord": GeologicalSketchRecord.objects.all(),
                "OverUnderExcavationCalculation": OverUnderExcavationCalculation.objects.all(),
                "ExcavationDiagnosis": ExcavationDiagnosis.objects.all(),
                "TunnelContourInfo": TunnelContourInfo.objects.all(),
                "DataStorage": DataStorage.objects.all(),  # 新增 DataStorage 表
            }

            backup_results = []
            success_count = 0

            for table_name in table_names:
                if table_name in supported_tables:
                    queryset = supported_tables[table_name]
                    try:
                        logger.info(f"开始备份表：{table_name}")
                        result = backup_table(queryset, table_name)
                        backup_results.append(result)

                        if result.get("status") == "success":
                            success_count += 1
                    except Exception as table_error:
                        logger.error(f"备份表 {table_name} 失败：{table_error}")
                        backup_results.append({"status": "error", "message": f"表 {table_name} 备份失败：{str(table_error)}"})
                else:
                    backup_results.append({"status": "error", "message": f"表 {table_name} 不存在"})

            overall_status = "success" if success_count == len(table_names) else "partial_success"

            return JsonResponse({
                "status": overall_status,
                "message": "备份完成" if overall_status == "success" else "部分表备份失败",
                "results": backup_results
            })

        except json.JSONDecodeError:
            logger.error("请求数据格式错误，无法解析 JSON")
            return JsonResponse({"status": "error", "message": "请求数据格式错误，无法解析 JSON"})
        except DatabaseError as db_error:
            logger.error(f"数据库错误：{db_error}")
            return JsonResponse({"status": "error", "message": f"数据库错误：{str(db_error)}"})
        except Exception as e:
            logger.error(f"备份失败：{e}")
            return JsonResponse({"status": "error", "message": f"备份失败：{str(e)}"})

    else:
        return render(request, 'base/backup.html')



# 下面这些是数据库恢复的
def restore_database(request):
    """
    恢复数据库的视图
    :param request: 请求对象
    :return: 恢复结果的 JSON 或 HTML 页面
    """
    if request.method == "POST":
        # 获取前端提交的备份文件名
        file_name = request.POST.get("backup_file")

        if not file_name:
            return JsonResponse({"status": "error", "message": "未选择备份文件"})

        # 获取文件路径
        file_path = os.path.join(BACKUP_DIR, file_name)
        if not os.path.exists(file_path):
            return JsonResponse({"status": "error", "message": "备份文件不存在"})

        # 匹配目标表模型：通过文件名推断目标表
        #这个是将数据库恢复到正常的四个表里面的（tunnelcontourinfo等等）
        table_mapping = {
            "GeologicalSketchRecord": GeologicalSketchRecord,
            "OverUnderExcavationCalculation": OverUnderExcavationCalculation,
            "ExcavationDiagnosis": ExcavationDiagnosis,
            "TunnelContourInfo": TunnelContourInfo,  #这个如果删除Backup就是恢复原来的数据库了（就是把TunnelContourInfo表清空然后根据json重新恢复）
            "DataStorage": DataStorage,  # 新增的表
        }

        # 下面的这个是将数据库恢复到四个备份表里面的（tunnelcontourinfobackup等等）
        # table_mapping = {
        #     "GeologicalSketchRecord": GeologicalSketchRecordBackup,
        #     "OverUnderExcavationCalculation": OverUnderExcavationCalculationBackup,
        #     "ExcavationDiagnosis": ExcavationDiagnosisBackup,
        #     "TunnelContourInfo": TunnelContourInfoBackup,  #这个如果删除Backup就是恢复原来的数据库了（就是把TunnelContourInfo表清空然后根据json重新恢复）
        # }

        # 提取表名，例如从文件名中解析出 "GeologicalSketchRecordBackup"
        table_name = None
        for key in table_mapping.keys():
            if key in file_name:
                table_name = key
                break

        print(table_name)
        if not table_name:
            return JsonResponse({"status": "error", "message": "无法识别目标表，请检查备份文件名"})

        model_class = table_mapping.get(table_name)

        # 调用单个表恢复函数
        result = restore_table_from_backup(file_path, model_class)
        return JsonResponse(result)

    else:
        # GET 请求，显示可用备份文件
        backup_files = get_backup_files()
        return render(
            request,
            "base/restore_database.html",
            {"backup_files": backup_files},
        )

#清空session的
@login_required
def clear_message(request):
    """清除 session 消息"""
    request.session.pop('message', None)
    request.session.pop('message_type', None)
    return JsonResponse({'status': 'success'})


# 主界面数据展示
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import (
    GeologicalSketchRecord,
    ExcavationDiagnosis,
    OverUnderExcavationCalculation,
    TunnelContourInfo,
)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import GeologicalSketchRecord, ExcavationDiagnosis, OverUnderExcavationCalculation, TunnelContourInfo

@login_required
def get_status_counts(request):
    """
    返回当前用户每种审批状态的记录数量。
    """
    status_labels = {
        'pending': '新增待审批',
        'modified_pending': '修改待审批',
        'deleted_pending': '删除待审批',
        'rejected': '未通过审批',
        'uploaded_approved': '有效数据'
    }

    # 初始化计数
    status_counts = {label: 0 for label in status_labels.values()}

    # 累计各状态的记录数量
    for model in [GeologicalSketchRecord, ExcavationDiagnosis, OverUnderExcavationCalculation, TunnelContourInfo]:
        status_counts['新增待审批'] += model.objects.filter(created_by=request.user, status='pending').count()
        status_counts['修改待审批'] += model.objects.filter(created_by=request.user, status='modified_pending').count()
        status_counts['删除待审批'] += model.objects.filter(created_by=request.user, status='deleted_pending').count()
        status_counts['未通过审批'] += model.objects.filter(created_by=request.user, status='rejected').count()
        status_counts['有效数据'] += model.objects.filter(created_by=request.user, status='uploaded_approved').count()

    print(status_counts)
    return JsonResponse({'data': status_counts})


@login_required
def geological_statistics_data(request):
    """
    返回掌子面统计数据，用于主界面图表展示。
    """
    # 查询用户相关数据
    records = GeologicalSketchRecord.objects.filter(created_by=request.user)
    if not records.exists():
        return JsonResponse({'data': [0, 0, 0, 0]})  # 如果没有数据，返回全 0

    excavation_width_avg = records.aggregate(Avg('excavation_width'))['excavation_width__avg'] or 0
    excavation_height_avg = records.aggregate(Avg('excavation_height'))['excavation_height__avg'] or 0
    excavation_area_avg = records.aggregate(Avg('excavation_area'))['excavation_area__avg'] or 0
    rock_strength_avg = records.aggregate(Avg('rock_strength'))['rock_strength__avg'] or 0

    return JsonResponse({
        'data': [
            excavation_width_avg,
            excavation_height_avg,
            excavation_area_avg,
            rock_strength_avg,
        ]
    })

