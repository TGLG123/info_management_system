from ..models import User, MySQLGeneralLog, OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo
from django.utils import timezone
from django.contrib import messages  # 用于发送消息
from ..models import GeologicalSketchRecord
from django.utils.timezone import now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render



#下面是四个审批的大页面
#掌子面审批
@login_required
def approval_list(request):
    """
    审批列表视图：支持按 face_id 和提交人 (created_by_id 或 created_by__username) 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示的记录数
    records_per_page = 10

    # 搜索逻辑函数
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回过滤后的查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(
                Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
            )
        return base_queryset

    # 掌子面记录审批
    new_records_paginator = Paginator(
        get_searched_queryset(GeologicalSketchRecord.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_records_paginator = Paginator(
        get_searched_queryset(GeologicalSketchRecord.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_records_paginator = Paginator(
        get_searched_queryset(GeologicalSketchRecord.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_records = new_records_paginator.get_page(request.GET.get('new_page'))
    pending_modified_records = modified_records_paginator.get_page(request.GET.get('modified_page'))
    pending_deleted_records = deleted_records_paginator.get_page(request.GET.get('deleted_page'))

    # 超欠挖计算记录审批
    new_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_excavation_calc = new_calc_paginator.get_page(request.GET.get('new_calc_page'))
    pending_modified_excavation_calc = modified_calc_paginator.get_page(request.GET.get('modified_calc_page'))
    pending_deleted_excavation_calc = deleted_calc_paginator.get_page(request.GET.get('deleted_calc_page'))

    # 超欠挖诊断记录审批
    new_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_diagnosis = new_diag_paginator.get_page(request.GET.get('new_diag_page'))
    pending_modified_diagnosis = modified_diag_paginator.get_page(request.GET.get('modified_diag_page'))
    pending_deleted_diagnosis = deleted_diag_paginator.get_page(request.GET.get('deleted_diag_page'))

    # 隧道轮廓记录审批
    new_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_tunnel = new_tunnel_paginator.get_page(request.GET.get('new_tunnel_page'))
    pending_modified_tunnel = modified_tunnel_paginator.get_page(request.GET.get('modified_tunnel_page'))
    pending_deleted_tunnel = deleted_tunnel_paginator.get_page(request.GET.get('deleted_tunnel_page'))

    # 渲染模板并传递上下文
    return render(
        request,
        'approval/approval_list.html',
        {
            # GeologicalSketchRecord (掌子面记录)
            'pending_new_records': pending_new_records,
            'pending_modified_records': pending_modified_records,
            'pending_deleted_records': pending_deleted_records,

            # OverUnderExcavationCalculation (超欠挖计算记录)
            'pending_new_excavation_calc': pending_new_excavation_calc,
            'pending_modified_excavation_calc': pending_modified_excavation_calc,
            'pending_deleted_excavation_calc': pending_deleted_excavation_calc,

            # ExcavationDiagnosis (超欠挖诊断记录)
            'pending_new_diagnosis': pending_new_diagnosis,
            'pending_modified_diagnosis': pending_modified_diagnosis,
            'pending_deleted_diagnosis': pending_deleted_diagnosis,

            # TunnelContourInfo (隧道轮廓记录)
            'pending_new_tunnel': pending_new_tunnel,
            'pending_modified_tunnel': pending_modified_tunnel,
            'pending_deleted_tunnel': pending_deleted_tunnel,

            # 搜索相关
            'search_query': search_query,
        },
    )


#超欠挖计算审批
@login_required
def approval_excavation_calculation(request):
    """
    超欠挖计算审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示的记录数
    records_per_page = 10

    # 搜索逻辑函数
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回过滤后的查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(
                Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
            )
        return base_queryset

    # 超欠挖计算记录审批
    new_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_calc_paginator = Paginator(
        get_searched_queryset(OverUnderExcavationCalculation.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_excavation_calc = new_calc_paginator.get_page(request.GET.get('new_page'))
    pending_modified_excavation_calc = modified_calc_paginator.get_page(request.GET.get('modified_page'))
    pending_deleted_excavation_calc = deleted_calc_paginator.get_page(request.GET.get('deleted_page'))

    # 渲染模板并传递上下文
    return render(
        request,
        'approval/approval_list1.html',
        {
            'pending_new_excavation_calc': pending_new_excavation_calc,
            'pending_modified_excavation_calc': pending_modified_excavation_calc,
            'pending_deleted_excavation_calc': pending_deleted_excavation_calc,
            'search_query': search_query,  # 搜索条件
        }
    )

#超欠挖诊断审批
@login_required
def approval_excavation_diagnosis(request):
    """
    超欠挖诊断审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示的记录数
    records_per_page = 10

    # 搜索逻辑函数
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回过滤后的查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(
                Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
            )
        return base_queryset

    # 超欠挖诊断记录审批
    new_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_diag_paginator = Paginator(
        get_searched_queryset(ExcavationDiagnosis.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_diagnosis = new_diag_paginator.get_page(request.GET.get('new_page'))
    pending_modified_diagnosis = modified_diag_paginator.get_page(request.GET.get('modified_page'))
    pending_deleted_diagnosis = deleted_diag_paginator.get_page(request.GET.get('deleted_page'))

    # 渲染模板并传递上下文
    return render(
        request,
        'approval/approval_list2.html',
        {
            'pending_new_diagnosis': pending_new_diagnosis,
            'pending_modified_diagnosis': pending_modified_diagnosis,
            'pending_deleted_diagnosis': pending_deleted_diagnosis,
            'search_query': search_query,  # 搜索条件
        }
    )

#隧道审批
@login_required
def approval_tunnel_contour(request):
    """
    隧道轮廓审批视图：支持按 face_id 和提交人用户名 (created_by.username) 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示的记录数
    records_per_page = 10

    # 搜索逻辑函数
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回过滤后的查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(
                Q(face_id__icontains=search_query) | Q(created_by__username__icontains=search_query)
            )
        return base_queryset

    # 隧道轮廓记录审批
    new_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='pending').order_by('-created_at')),
        records_per_page
    )
    modified_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='modified_pending').order_by('-created_at')),
        records_per_page
    )
    deleted_tunnel_paginator = Paginator(
        get_searched_queryset(TunnelContourInfo.objects.filter(status='deleted_pending').order_by('-created_at')),
        records_per_page
    )

    pending_new_tunnel = new_tunnel_paginator.get_page(request.GET.get('new_page'))
    pending_modified_tunnel = modified_tunnel_paginator.get_page(request.GET.get('modified_page'))
    pending_deleted_tunnel = deleted_tunnel_paginator.get_page(request.GET.get('deleted_page'))

    # 渲染模板并传递上下文
    return render(
        request,
        'approval/approval_list3.html',
        {
            'pending_new_tunnel': pending_new_tunnel,
            'pending_modified_tunnel': pending_modified_tunnel,
            'pending_deleted_tunnel': pending_deleted_tunnel,
            'search_query': search_query,  # 搜索条件
        }
    )

#管理员审批
#下面四个是管理员审批的详细页面后端代码
#掌子面管理员审批（详细页面）
@login_required
def approve_geological_record(request, record_id):
    """
    审批用户提交的地质记录。
    - 支持审批上传、修改和删除。
    - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id)

    # 检查是否是修改审批
    is_modification = record.status == 'modified_pending'
    modifications = {}
    if is_modification:
        # 获取历史版本中的最后一条记录
        try:
            # 获取修改前的历史版本
            original_record = record.history.filter(history_type='~').last()  # '~' 表示修改操作
            if original_record:
                for field in record._meta.fields:
                    field_name = field.name
                    #过滤掉一些表单以外的后台信息
                    if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
                        continue
                    original_value = getattr(original_record, field_name, None)
                    new_value = getattr(record, field_name, None)
                    if original_value != new_value:
                        modifications[field_name] = {'old': original_value, 'new': new_value}
        except Exception as e:
            print(f"Error fetching history: {e}")

    if request.method == 'POST':
        action = request.POST.get('action')  # 获取管理员的操作类型（approve 或 reject）
        approval_reason = request.POST.get('approval_reason')  # 获取审批理由

        if action == 'approve':
            if record.status == 'pending':
                # 审批上传
                record.status = 'uploaded_approved'
            elif record.status == 'modified_pending':
                # 审批修改
                record.status = 'modified_approved'
            elif record.status == 'deleted_pending':
                # 审批删除
                record.status = 'deleted'

            record.approved_by = request.user  # 设置审批人
            print(record.approved_by)
            record.approval_reason = approval_reason  # 设置审批理由
            record.approved_at = now()  # 设置审批时间
            record.save()  # 保存状态更新

        elif action == 'reject':
            # 驳回逻辑：状态保持不变，但记录审批理由和驳回人
            record.approval_reason = approval_reason  # 保存驳回理由
            record.rejected_by = request.user  # 设置驳回人
            record.rejected_at = now()  # 设置驳回时间
            if record.status in ['modified_pending', 'deleted_pending']:
                record.status = 'rejected'  # 设置为驳回状态
            else:
                record.status = 'pending'  # 上传驳回仍保持 `pending`
            record.save()

        return redirect('approval_list')  # 返回到审批列表页面

    return render(request, 'approval/approve_geological_record.html', {
        'record': record,
        'is_modification': is_modification,
        'modifications': modifications,
    })

@login_required
def approve_excavation_diagnosis(request, record_id):
    """
    审批用户提交的超欠挖诊断记录。
    - 支持审批上传、修改和删除。
    - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id)

    # 检查是否是修改审批
    is_modification = record.status == 'modified_pending'
    modifications = {}
    if is_modification:
        try:
            # 获取修改前的历史版本
            original_record = record.history.filter(history_type='~').last()
            if original_record:
                for field in record._meta.fields:
                    field_name = field.name
                    #过滤掉一些表单以外的后台信息
                    if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
                        continue
                    original_value = getattr(original_record, field_name, None)
                    new_value = getattr(record, field_name, None)
                    if original_value != new_value:
                        modifications[field_name] = {'old': original_value, 'new': new_value}
        except Exception as e:
            print(f"Error fetching history: {e}")

    if request.method == 'POST':
        action = request.POST.get('action')
        approval_reason = request.POST.get('approval_reason')

        if action == 'approve':
            if record.status == 'pending':
                record.status = 'uploaded_approved'
            elif record.status == 'modified_pending':
                record.status = 'modified_approved'
            elif record.status == 'deleted_pending':
                record.status = 'deleted'

            record.approved_by = request.user
            record.approval_reason = approval_reason
            record.approved_at = now()
            record.save()

        elif action == 'reject':
            record.approval_reason = approval_reason
            record.rejected_by = request.user
            record.rejected_at = now()
            if record.status in ['modified_pending', 'deleted_pending']:
                record.status = 'rejected'
            else:
                record.status = 'pending'
            record.save()

        return redirect('approval_list')

    return render(request, 'approval/approve_excavation_diagnosis.html', {
        'record': record,
        'is_modification': is_modification,
        'modifications': modifications,
    })

@login_required
def approve_over_under_calculation(request, record_id):
    """
    审批用户提交的超欠挖计算记录。
    - 支持审批上传、修改和删除。
    - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)

    # 检查是否是修改审批
    is_modification = record.status == 'modified_pending'
    modifications = {}
    if is_modification:
        try:
            # 获取修改前的历史版本
            original_record = record.history.filter(history_type='~').last()
            if original_record:
                for field in record._meta.fields:
                    field_name = field.name
                    #过滤掉一些表单以外的后台信息
                    if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
                        continue
                    original_value = getattr(original_record, field_name, None)
                    new_value = getattr(record, field_name, None)
                    if original_value != new_value:
                        modifications[field_name] = {'old': original_value, 'new': new_value}
        except Exception as e:
            print(f"Error fetching history: {e}")

    if request.method == 'POST':
        action = request.POST.get('action')
        approval_reason = request.POST.get('approval_reason')

        if action == 'approve':
            if record.status == 'pending':
                record.status = 'uploaded_approved'
            elif record.status == 'modified_pending':
                record.status = 'modified_approved'
            elif record.status == 'deleted_pending':
                record.status = 'deleted'

            record.approved_by = request.user
            record.approval_reason = approval_reason
            record.approved_at = now()
            record.save()

        elif action == 'reject':
            record.approval_reason = approval_reason
            record.rejected_by = request.user
            record.rejected_at = now()
            if record.status in ['modified_pending', 'deleted_pending']:
                record.status = 'rejected'
            else:
                record.status = 'pending'
            record.save()

        return redirect('approval_list')

    return render(request, 'approval/approve_over_under_calculation.html', {
        'record': record,
        'is_modification': is_modification,
        'modifications': modifications,
    })

@login_required
def approve_tunnel_contour(request, record_id):
    """
    审批用户提交的隧道轮廓信息记录。
    - 支持审批上传、修改和删除。
    - 审批通过或驳回时更新状态，并记录日志（由 signal 自动处理）。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id)

    # 检查是否是修改审批
    is_modification = record.status == 'modified_pending'
    modifications = {}
    if is_modification:
        try:
            history_records = record.history.all()
            print("历史记录条数:", len(history_records))
            for hist in history_records:
                print(f"记录ID: {hist.id}, 类型: {hist.history_type}, 日期: {hist.history_date}")

            # 获取修改前的历史版本
            original_record = record.history.filter(history_type='~').last()
            if original_record:
                print("原始记录找到，开始比较字段变化：")
                for field in record._meta.fields:
                    field_name = field.name
                    #过滤掉一些表单以外的后台信息
                    if field_name in ['id', 'approved_at', 'uploaded_at', 'status', 'approved_by', 'created_by','modified_by','deleted_by','approval_reason','created_at','updated_at']:
                        continue

                    # 获取原始值和当前值
                    original_value = getattr(original_record, field_name, None)
                    new_value = getattr(record, field_name, None)

                    # 输出字段对比的调试信息
                    print(f"字段: {field_name} | 原始值: {original_value} | 新值: {new_value}")

                    if original_value != new_value:
                        modifications[field_name] = {'old': original_value, 'new': new_value}
                        print(f"字段 '{field_name}' 发生变化：原始值 -> {original_value}, 新值 -> {new_value}")
            else:
                print("未找到修改前的历史记录！")
        except Exception as e:
            print(f"Error fetching history: {e}")


    if request.method == 'POST':
        action = request.POST.get('action')
        approval_reason = request.POST.get('approval_reason')

        if action == 'approve':
            if record.status == 'pending':
                record.status = 'uploaded_approved'
            elif record.status == 'modified_pending':
                record.status = 'modified_approved'
            elif record.status == 'deleted_pending':
                record.status = 'deleted'

            record.approved_by = request.user
            record.approval_reason = approval_reason
            record.approved_at = now()
            record.save()

        elif action == 'reject':
            record.approval_reason = approval_reason
            record.rejected_by = request.user
            record.rejected_at = now()
            if record.status in ['modified_pending', 'deleted_pending']:
                record.status = 'rejected'
            else:
                record.status = 'pending'
            record.save()

        return redirect('approval_list')

    return render(request, 'approval/approve_tunnel_contour.html', {
        'record': record,
        'is_modification': is_modification,
        'modifications': modifications,
    })



#下面是四个驳回的
#管理员驳回
@login_required
def reject_geological_record(request, record_id):
    """
    管理员驳回地质记录的审批请求。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id)

    # 替换管理员权限检查逻辑
    if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
        messages.error(request, "您没有权限驳回记录。")
        return redirect('approval_list')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        if not rejection_reason:
            messages.error(request, "驳回理由不能为空。")
            return redirect('approval_list')

        # 更新记录状态为 "rejected"
        record.status = 'rejected'
        record.approval_reason = rejection_reason  # 保存驳回理由
        record.approved_by = request.user  # 设置当前审批管理员
        record.approved_at = timezone.now()  # 记录审批时间
        record.save()

        # 消息反馈
        messages.success(request, f"记录 {record.face_id} 已成功驳回。")
        return redirect('approval_list')

    return render(request, 'approval/reject_record.html', {'record': record})

@login_required
def reject_excavation_diagnosis(request, record_id):
    """
    管理员驳回超欠挖诊断记录的审批请求。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id)

    # 替换管理员权限检查逻辑
    if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
        messages.error(request, "您没有权限驳回记录。")
        return redirect('approval_list')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        if not rejection_reason:
            messages.error(request, "驳回理由不能为空。")
            return redirect('approval_list')

        # 更新记录状态为 "rejected"
        record.status = 'rejected'
        record.approval_reason = rejection_reason  # 保存驳回理由
        record.approved_by = request.user  # 设置当前审批管理员
        record.approved_at = timezone.now()  # 记录审批时间
        record.save()

        # 消息反馈
        messages.success(request, f"记录 {record.face_id} 已成功驳回。")
        return redirect('approval_list')

    return render(request, 'approval/reject_record1.html', {'record': record})

@login_required
def reject_over_under_excavation(request, record_id):
    """
    管理员驳回超欠挖计算记录的审批请求。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)

    # 替换管理员权限检查逻辑
    if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
        messages.error(request, "您没有权限驳回记录。")
        return redirect('approval_list')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        if not rejection_reason:
            messages.error(request, "驳回理由不能为空。")
            return redirect('approval_list')

        # 更新记录状态为 "rejected"
        record.status = 'rejected'
        record.approval_reason = rejection_reason  # 保存驳回理由
        record.approved_by = request.user  # 设置当前审批管理员
        record.approved_at = timezone.now()  # 记录审批时间
        record.save()

        # 消息反馈
        messages.success(request, f"记录 {record.face_id} 已成功驳回。")
        return redirect('approval_list')

    return render(request, 'approval/reject_record2.html', {'record': record})

@login_required
def reject_tunnel_contour(request, record_id):
    """
    管理员驳回隧道轮廓信息记录的审批请求。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id)

    # 替换管理员权限检查逻辑
    if not request.user.role == 'admin':  # 根据自定义的角色字段判断管理员权限
        messages.error(request, "您没有权限驳回记录。")
        return redirect('approval_list')

    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '')
        if not rejection_reason:
            messages.error(request, "驳回理由不能为空。")
            return redirect('approval_list')

        # 更新记录状态为 "rejected"
        record.status = 'rejected'
        record.approval_reason = rejection_reason  # 保存驳回理由
        record.approved_by = request.user  # 设置当前审批管理员
        record.approved_at = timezone.now()  # 记录审批时间
        record.save()

        # 消息反馈
        messages.success(request, f"记录 {record.face_id} 已成功驳回。")
        return redirect('approval_list')

    return render(request, 'approval/reject_record3.html', {'record': record})