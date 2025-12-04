from ..models import User, MySQLGeneralLog, OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo
from ..forms import GeologicalSketchRecordForm, ExcavationDiagnosisForm, OverUnderExcavationForm, TunnelContourForm
from django.contrib import messages  # 用于发送消息
from ..models import GeologicalSketchRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render

#分页函数
def paginate_queryset(queryset, request, items_per_page, page_param='page'):
    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get(page_param, 1)  # 获取分页参数
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # 默认第 1 页
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # 超出范围返回最后一页
    return page_obj


#下面这四个是拆开的用户个人中心（掌子面，超欠挖计算，诊断，隧道）
@login_required
def user_records_view(request):
    """
    展示掌子面记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索的掌子面编号

    # 每页显示条数
    items_per_page = 10  # 调整为生产环境合适的值

    # 使用搜索逻辑
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(face_id__icontains=search_query)
        return base_queryset

    # 应用搜索和分页
    pending_new_page_obj = paginate_queryset(
        get_searched_queryset(
            GeologicalSketchRecord.objects.filter(
                created_by=request.user, status='pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_new_page'
    )
    pending_modified_page_obj = paginate_queryset(
        get_searched_queryset(
            GeologicalSketchRecord.objects.filter(
                created_by=request.user, status='modified_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_modified_page'
    )
    pending_deleted_page_obj = paginate_queryset(
        get_searched_queryset(
            GeologicalSketchRecord.objects.filter(
                created_by=request.user, status='deleted_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_deleted_page'
    )
    rejected_page_obj = paginate_queryset(
        get_searched_queryset(
            GeologicalSketchRecord.objects.filter(
                created_by=request.user, status='rejected'
            )
        ),
        request,
        items_per_page,
        page_param='rejected_page'
    )
    approved_page_obj = paginate_queryset(
        get_searched_queryset(
            GeologicalSketchRecord.objects.filter(
                created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
            )
        ),
        request,
        items_per_page,
        page_param='approved_page'
    )

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板
    return render(
        request,
        'personal_center/user_records.html',  # 模板文件
        {
            'pending_new_geological': pending_new_page_obj,
            'pending_modified_geological': pending_modified_page_obj,
            'pending_deleted_geological': pending_deleted_page_obj,
            'rejected_geological': rejected_page_obj,
            'approved_geological': approved_page_obj,
            'search_query': search_query,  # 搜索条件
            'query_params': query_params_encoded,  # 用于分页链接
        },
    )





@login_required
def excavation_calculation_records_view(request):
    """
    展示超欠挖计算记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索的超欠挖计算编号

    # 每页显示条数
    items_per_page = 10  # 调整为生产环境合适的值

    # 使用搜索逻辑
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换字段为实际字段
        return base_queryset

    # 应用搜索和分页
    pending_new_page_obj = paginate_queryset(
        get_searched_queryset(
            OverUnderExcavationCalculation.objects.filter(
                created_by=request.user, status='pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_new_page'
    )
    pending_modified_page_obj = paginate_queryset(
        get_searched_queryset(
            OverUnderExcavationCalculation.objects.filter(
                created_by=request.user, status='modified_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_modified_page'
    )
    pending_deleted_page_obj = paginate_queryset(
        get_searched_queryset(
            OverUnderExcavationCalculation.objects.filter(
                created_by=request.user, status='deleted_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_deleted_page'
    )
    rejected_page_obj = paginate_queryset(
        get_searched_queryset(
            OverUnderExcavationCalculation.objects.filter(
                created_by=request.user, status='rejected'
            )
        ),
        request,
        items_per_page,
        page_param='rejected_page'
    )
    approved_page_obj = paginate_queryset(
        get_searched_queryset(
            OverUnderExcavationCalculation.objects.filter(
                created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
            )
        ),
        request,
        items_per_page,
        page_param='approved_page'
    )

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板
    return render(
        request,
        'personal_center/user_records1.html',  # 模板文件
        {
            'pending_new_excavation_calculation': pending_new_page_obj,
            'pending_modified_excavation_calculation': pending_modified_page_obj,
            'pending_deleted_excavation_calculation': pending_deleted_page_obj,
            'rejected_excavation_calculation': rejected_page_obj,
            'approved_excavation_calculation': approved_page_obj,
            'search_query': search_query,  # 搜索条件
            'query_params': query_params_encoded,  # 用于分页链接
        },
    )




@login_required
def excavation_diagnosis_records_view(request):
    """
    展示超欠挖诊断记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示条数
    items_per_page = 10  # 可以根据需求调整条目数

    # 使用搜索逻辑
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换为实际搜索字段
        return base_queryset

    # 应用搜索和分页
    pending_new_page_obj = paginate_queryset(
        get_searched_queryset(
            ExcavationDiagnosis.objects.filter(
                created_by=request.user, status='pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_new_page'
    )
    pending_modified_page_obj = paginate_queryset(
        get_searched_queryset(
            ExcavationDiagnosis.objects.filter(
                created_by=request.user, status='modified_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_modified_page'
    )
    pending_deleted_page_obj = paginate_queryset(
        get_searched_queryset(
            ExcavationDiagnosis.objects.filter(
                created_by=request.user, status='deleted_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_deleted_page'
    )
    rejected_page_obj = paginate_queryset(
        get_searched_queryset(
            ExcavationDiagnosis.objects.filter(
                created_by=request.user, status='rejected'
            )
        ),
        request,
        items_per_page,
        page_param='rejected_page'
    )
    approved_page_obj = paginate_queryset(
        get_searched_queryset(
            ExcavationDiagnosis.objects.filter(
                created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
            )
        ),
        request,
        items_per_page,
        page_param='approved_page'
    )

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板
    return render(
        request,
        'personal_center/user_records2.html',  # 模板文件
        {
            'pending_new_excavation_diagnosis': pending_new_page_obj,
            'pending_modified_excavation_diagnosis': pending_modified_page_obj,
            'pending_deleted_excavation_diagnosis': pending_deleted_page_obj,
            'rejected_excavation_diagnosis': rejected_page_obj,
            'approved_excavation_diagnosis': approved_page_obj,
            'search_query': search_query,  # 搜索条件
            'query_params': query_params_encoded,  # 用于分页链接
        },
    )




@login_required
def tunnel_contour_records_view(request):
    """
    展示隧道轮廓记录，包括新增、修改、删除、未通过和有效数据，并添加搜索功能和分页功能。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 每页显示条数
    items_per_page = 10  # 根据需求调整条目数

    # 使用搜索逻辑
    def get_searched_queryset(base_queryset):
        """
        根据搜索条件返回查询集
        """
        if search_query:
            base_queryset = base_queryset.filter(face_id__icontains=search_query)  # 替换为实际搜索字段
        return base_queryset

    # 应用搜索和分页
    pending_new_page_obj = paginate_queryset(
        get_searched_queryset(
            TunnelContourInfo.objects.filter(
                created_by=request.user, status='pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_new_page'
    )
    pending_modified_page_obj = paginate_queryset(
        get_searched_queryset(
            TunnelContourInfo.objects.filter(
                created_by=request.user, status='modified_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_modified_page'
    )
    pending_deleted_page_obj = paginate_queryset(
        get_searched_queryset(
            TunnelContourInfo.objects.filter(
                created_by=request.user, status='deleted_pending'
            )
        ),
        request,
        items_per_page,
        page_param='pending_deleted_page'
    )
    rejected_page_obj = paginate_queryset(
        get_searched_queryset(
            TunnelContourInfo.objects.filter(
                created_by=request.user, status='rejected'
            )
        ),
        request,
        items_per_page,
        page_param='rejected_page'
    )
    approved_page_obj = paginate_queryset(
        get_searched_queryset(
            TunnelContourInfo.objects.filter(
                created_by=request.user, status__in=['uploaded_approved', 'modified_approved']
            )
        ),
        request,
        items_per_page,
        page_param='approved_page'
    )

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板
    return render(
        request,
        'personal_center/user_records3.html',  # 模板文件
        {
            'pending_new_tunnel': pending_new_page_obj,
            'pending_modified_tunnel': pending_modified_page_obj,
            'pending_deleted_tunnel': pending_deleted_page_obj,
            'rejected_tunnel': rejected_page_obj,
            'approved_tunnel': approved_page_obj,
            'search_query': search_query,  # 搜索条件
            'query_params': query_params_encoded,  # 用于分页链接
        },
    )

#下面四个是用户修改新增待审批的
@login_required
def edit_pending_record(request, record_id):
    """
    用户修改待审批的掌子面记录记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        form = GeologicalSketchRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')
    else:
        form = GeologicalSketchRecordForm(instance=record)

    return render(request, 'personal_center/edit_pending_record.html', {'form': form, 'record': record})

@login_required
def edit_pending_excavation_diagnosis(request, record_id):
    """
    用户修改待审批的超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        form = ExcavationDiagnosisForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')  # 替换为用户记录列表的URL名称
    else:
        form = ExcavationDiagnosisForm(instance=record)

    return render(request, 'personal_center/edit_pending_diagnosis.html', {'form': form, 'record': record})

@login_required
def edit_pending_over_under_excavation(request, record_id):
    """
    用户修改待审批的超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        form = OverUnderExcavationForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')  # 替换为用户记录列表的URL名称
    else:
        form = OverUnderExcavationForm(instance=record)

    return render(request, 'personal_center/edit_pending_excavation.html', {'form': form, 'record': record})

@login_required
def edit_pending_tunnel_contour(request, record_id):
    """
    用户修改待审批的隧道轮廓记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        form = TunnelContourForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')  # 替换为用户记录列表的URL名称
    else:
        form = TunnelContourForm(instance=record)

    return render(request, 'personal_center/edit_pending_tunnel_contour.html', {'form': form, 'record': record})


#下面四个是用户删除新增待审批的
@login_required
def delete_pending_record(request, record_id):
    """
    用户删除待审批的掌子面信息记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_pending.html', {'record': record})

@login_required
def delete_pending_excavation_diagnosis(request, record_id):
    """
    用户删除待审批的超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')  # 替换为用户记录列表的URL名称

    return render(request, 'personal_center/confirm_delete_pending_diagnosis.html', {'record': record})

@login_required
def delete_pending_over_under_excavation(request, record_id):
    """
    用户删除待审批的超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')  # 替换为用户记录列表的URL名称

    return render(request, 'personal_center/confirm_delete_pending_excavation.html', {'record': record})

@login_required
def delete_pending_tunnel_contour(request, record_id):
    """
    用户删除待审批的隧道轮廓记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')  # 替换为用户记录列表的URL名称

    return render(request, 'personal_center/confirm_delete_pending_tunnel_contour.html', {'record': record})

#下面八个是用户申请修改，删除已审批信息的
#掌子面用户申请修改已审批记录
@login_required
def apply_edit_record(request, record_id):
    """
    用户申请修改已审批记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        form = GeologicalSketchRecordForm(request.POST, instance=record)  # 用表单绑定数据
        if form.is_valid():
            operation_reason = request.POST.get('operation_reason')  # 获取修改理由
            if operation_reason:
                record.operation_reason = operation_reason  # 保存修改理由
            record.status = 'modified_pending'  # 修改申请设置为待审批状态
            record.save()
            form.save()  # 保存表单中的修改
            return redirect('user_records_view')
        else:
            print("表单验证失败，错误信息如下：")
            print(form.errors)
    else:
        form = GeologicalSketchRecordForm(instance=record)  # 初始化表单，加载已有数据

    return render(request, 'personal_center/apply_edit_record.html', {'record': record})

#掌子面用户申请删除已审批记录
@login_required
def apply_delete_record(request, record_id):
    """
    用户申请删除已审批记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        operation_reason = request.POST.get('operation_reason')  # 获取删除理由
        print("理由如下：")
        print(operation_reason)
        if operation_reason:
            record.operation_reason = operation_reason  # 保存删除理由
        record.status = 'deleted_pending'  # 删除申请设置为待审批状态
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_application.html', {'record': record})

@login_required
def apply_edit_excavation_diagnosis(request, record_id):
    """
    用户申请修改已审批的超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        form = ExcavationDiagnosisForm(request.POST, instance=record)  # 用表单绑定数据
        if form.is_valid():
            operation_reason = request.POST.get('operation_reason')  # 获取修改理由
            if operation_reason:
                record.operation_reason = operation_reason  # 保存修改理由
            record.status = 'modified_pending'  # 修改申请设置为待审批状态
            record.save()
            form.save()  # 保存表单中的修改
            return redirect('user_records_view')
        else:
            print("表单验证失败，错误信息如下：")
            print(form.errors)
    else:
        form = ExcavationDiagnosisForm(instance=record)  # 初始化表单，加载已有数据

    return render(request, 'personal_center/apply_edit_excavation_diagnosis.html', {'record': record})


@login_required
def apply_delete_excavation_diagnosis(request, record_id):
    """
    用户申请删除已审批的超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        operation_reason = request.POST.get('operation_reason')  # 获取删除理由
        print("理由如下：")
        print(operation_reason)
        if operation_reason:
            record.operation_reason = operation_reason  # 保存删除理由
        record.status = 'deleted_pending'  # 删除申请设置为待审批状态
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_excavation_diagnosis.html', {'record': record})

@login_required
def apply_edit_over_under_excavation_calculation(request, record_id):
    """
    用户申请修改已审批的超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        form = OverUnderExcavationForm(request.POST, instance=record)  # 用表单绑定数据
        if form.is_valid():
            operation_reason = request.POST.get('operation_reason')  # 获取修改理由
            if operation_reason:
                record.operation_reason = operation_reason  # 保存修改理由
            record.status = 'modified_pending'  # 修改申请设置为待审批状态
            record.save()
            form.save()  # 保存表单中的修改
            return redirect('user_records_view')
        else:
            print("表单验证失败，错误信息如下：")
            print(form.errors)
    else:
        form = OverUnderExcavationForm(instance=record)  # 初始化表单，加载已有数据

    return render(request, 'personal_center/apply_edit_over_under_excavation_calculation.html', {'record': record})


@login_required
def apply_delete_over_under_excavation_calculation(request, record_id):
    """
    用户申请删除已审批的超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])
    if request.method == 'POST':
        operation_reason = request.POST.get('operation_reason')  # 获取删除理由
        print("理由如下：")
        print(operation_reason)
        if operation_reason:
            record.operation_reason = operation_reason  # 保存删除理由
        record.status = 'deleted_pending'  # 删除申请设置为待审批状态
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_over_under_excavation_calculation.html', {'record': record})

@login_required
def apply_edit_tunnel_contour_info(request, record_id):
    """
    用户申请修改已审批的隧道轮廓记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        form = TunnelContourForm(request.POST, instance=record)  # 用表单绑定数据
        if form.is_valid():
            operation_reason = request.POST.get('operation_reason')  # 获取修改理由
            if operation_reason:
                record.operation_reason = operation_reason  # 保存修改理由
            record.status = 'modified_pending'  # 修改申请设置为待审批状态
            record.save()
            form.save()  # 保存表单中的修改
            return redirect('user_records_view')
        else:
            print("表单验证失败，错误信息如下：")
            print(form.errors)
    else:
        form = TunnelContourForm(instance=record)  # 初始化表单，加载已有数据

    return render(request, 'personal_center/apply_edit_tunnel_contour_info.html', {'record': record})


@login_required
def apply_delete_tunnel_contour_info(request, record_id):
    """
    用户申请删除已审批的隧道轮廓信息记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status__in=['uploaded_approved', 'modified_approved'])

    if request.method == 'POST':
        operation_reason = request.POST.get('operation_reason')  # 获取删除理由
        print("理由如下：")
        print(operation_reason)
        if operation_reason:
            record.operation_reason = operation_reason  # 保存删除理由
        record.status = 'deleted_pending'  # 删除申请设置为待审批状态
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_tunnel_contour_info.html', {'record': record})

#下面四个是修改“修改待审批”的
@login_required
def edit_modified_pending_record(request, record_id):
    """
    用户修改掌子面“修改待审批”的记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        form = GeologicalSketchRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')
    else:
        form = GeologicalSketchRecordForm(instance=record)

    return render(request, 'personal_center/edit_pending_record.html', {'form': form, 'record': record})

@login_required
def edit_modified_pending_excavation_diagnosis(request, record_id):
    """
    用户修改超欠挖诊断“修改待审批”的记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        form = ExcavationDiagnosisForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')
    else:
        form = ExcavationDiagnosisForm(instance=record)

    return render(request, 'personal_center/edit_pending_diagnosis.html', {'form': form, 'record': record})

@login_required
def edit_modified_pending_over_under_excavation(request, record_id):
    """
    用户修改超欠挖计算“修改待审批”的记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        form = OverUnderExcavationForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')
    else:
        form = OverUnderExcavationForm(instance=record)

    return render(request, 'personal_center/edit_pending_excavation.html', {'form': form, 'record': record})

@login_required
def edit_modified_pending_tunnel_contour(request, record_id):
    """
    用户修改隧道轮廓“修改待审批”的记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        form = TunnelContourForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('user_records_view')
    else:
        form = TunnelContourForm(instance=record)

    return render(request, 'personal_center/edit_pending_tunnel_contour.html', {'form': form, 'record': record})


#下面四个是删除“修改待审批”的
@login_required
def delete_modified_pending_record(request, record_id):
    """
    用户删除掌子面“修改待审批”的记录。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_pending.html', {'record': record})

@login_required
def delete_modified_pending_excavation_diagnosis(request, record_id):
    """
    用户删除超欠挖诊断“修改待审批”的记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_pending_diagnosis.html', {'record': record})

@login_required
def delete_modified_pending_over_under_excavation(request, record_id):
    """
    用户删除超欠挖计算“修改待审批”的记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_pending_excavation.html', {'record': record})

@login_required
def delete_modified_pending_tunnel_contour(request, record_id):
    """
    用户删除隧道轮廓“修改待审批”的记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='modified_pending')

    if request.method == 'POST':
        record.delete()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_pending_tunnel_contour.html', {'record': record})


#下面四个是取消“删除待审批”的
@login_required
def delete_deleted_pending_record(request, record_id):
    """
    用户取消“删除待审批”的记录（即撤销删除申请，将状态改为上传已审批）。
    """
    record = get_object_or_404(GeologicalSketchRecord, id=record_id, created_by=request.user, status='deleted_pending')

    if request.method == 'POST':
        # 将状态从 deleted_pending 改为 uploaded_approved
        record.status = 'uploaded_approved'
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/confirm_delete_deleted_pending.html', {'record': record})

@login_required
def cancel_delete_pending_excavation_diagnosis(request, record_id):
    """
    用户取消“删除待审批”的超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user, status='deleted_pending')

    if request.method == 'POST':
        record.status = 'uploaded_approved'
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/cancel_delete_pending_excavation_diagnosis.html', {'record': record})

@login_required
def cancel_delete_pending_over_under_excavation(request, record_id):
    """
    用户取消“删除待审批”的超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='deleted_pending')

    if request.method == 'POST':
        record.status = 'uploaded_approved'
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/cancel_delete_pending_over_under_excavation.html', {'record': record})

@login_required
def cancel_delete_pending_tunnel_contour(request, record_id):
    """
    用户取消“删除待审批”的隧道轮廓记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user, status='deleted_pending')

    if request.method == 'POST':
        record.status = 'uploaded_approved'
        record.save()
        return redirect('user_records_view')

    return render(request, 'personal_center/cancel_delete_pending_tunnel_contour.html', {'record': record})


#下面四个是重新申请的
@login_required
def reapply_record(request, record_id):
    """
    用户重新申请审批未通过的掌子面记录。
    """
    # 获取未通过的记录
    record = get_object_or_404(
        GeologicalSketchRecord, id=record_id, created_by=request.user, status='rejected'
    )

    if request.method == 'POST':
        # 将用户提交的数据绑定到表单
        form = GeologicalSketchRecordForm(request.POST, instance=record)
        if form.is_valid():
            # 更新记录状态为 pending，表示重新申请
            record = form.save(commit=False)
            record.status = 'pending'  # 重新进入待审批状态
            record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
            record.save()

            # 提示用户操作成功
            messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
            return redirect('user_records_view')  # 重定向到用户记录页面
        else:
            # 打印表单错误，方便调试
            print("Form Errors:", form.errors)
            return render(request, 'personal_center/reapply_record.html', {'form': form, 'record': record, 'errors': form.errors})
    else:
        # GET 请求，绑定已有数据到表单
        form = GeologicalSketchRecordForm(instance=record)
    return render(request, 'personal_center/reapply_record.html', {'form': form, 'record': record})

@login_required
def reapply_excavation_diagnosis(request, record_id):
    """
    用户重新申请审批未通过的超欠挖诊断记录。
    """
    # 获取未通过的记录
    record = get_object_or_404(
        ExcavationDiagnosis, id=record_id, created_by=request.user, status='rejected'
    )

    if request.method == 'POST':
        # 将用户提交的数据绑定到表单
        form = ExcavationDiagnosisForm(request.POST, instance=record)
        if form.is_valid():
            # 更新记录状态为 pending，表示重新申请
            record = form.save(commit=False)
            record.status = 'pending'  # 重新进入待审批状态
            record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
            record.save()

            # 提示用户操作成功
            messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
            return redirect('user_records_view')  # 重定向到用户记录页面
        else:
            # 打印表单错误，方便调试
            print("Form Errors:", form.errors)
            return render(request, 'personal_center/reapply_excavation_diagnosis.html', {'form': form, 'record': record, 'errors': form.errors})
    else:
        # GET 请求，绑定已有数据到表单
        form = ExcavationDiagnosisForm(instance=record)
    return render(request, 'personal_center/reapply_excavation_diagnosis.html', {'form': form, 'record': record})

@login_required
def reapply_over_under_calculation(request, record_id):
    """
    用户重新申请审批未通过的超欠挖计算记录。
    """
    # 获取未通过的记录
    record = get_object_or_404(
        OverUnderExcavationCalculation, id=record_id, created_by=request.user, status='rejected'
    )

    if request.method == 'POST':
        # 将用户提交的数据绑定到表单
        form = OverUnderExcavationForm(request.POST, instance=record)
        if form.is_valid():
            # 更新记录状态为 pending，表示重新申请
            record = form.save(commit=False)
            record.status = 'pending'  # 重新进入待审批状态
            record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
            record.save()

            # 提示用户操作成功
            messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
            return redirect('user_records_view')  # 重定向到用户记录页面
        else:
            # 打印表单错误，方便调试
            print("Form Errors:", form.errors)
            return render(request, 'personal_center/reapply_over_under_calculation.html', {'form': form, 'record': record, 'errors': form.errors})
    else:
        # GET 请求，绑定已有数据到表单
        form = OverUnderExcavationForm(instance=record)
    return render(request, 'personal_center/reapply_over_under_calculation.html', {'form': form, 'record': record})

@login_required
def reapply_tunnel_contour(request, record_id):
    """
    用户重新申请审批未通过的隧道轮廓信息记录。
    """
    # 获取未通过的记录
    record = get_object_or_404(
        TunnelContourInfo, id=record_id, created_by=request.user, status='rejected'
    )

    if request.method == 'POST':
        # 将用户提交的数据绑定到表单
        form = TunnelContourForm(request.POST, instance=record)
        if form.is_valid():
            # 更新记录状态为 pending，表示重新申请
            record = form.save(commit=False)
            record.status = 'pending'  # 重新进入待审批状态
            record.operation_reason = request.POST.get('operation_reason')  # 更新申请理由
            record.save()

            # 提示用户操作成功
            messages.success(request, f"记录 {record.face_id} 已成功重新申请审批。")
            return redirect('user_records_view')  # 重定向到用户记录页面
        else:
            # 打印表单错误，方便调试
            print("Form Errors:", form.errors)
            return render(request, 'personal_center/reapply_tunnel_contour.html', {'form': form, 'record': record, 'errors': form.errors})
    else:
        # GET 请求，绑定已有数据到表单
        form = TunnelContourForm(instance=record)
    return render(request, 'personal_center/reapply_tunnel_contour.html', {'form': form, 'record': record})


#下面四个是用户查看信息的
@login_required
def view_GeologicalSketchRecord(request, record_id):
    """
    用户查看待审批的掌子面记录记录（只读）。
    """
    # 获取指定记录
    record = get_object_or_404(GeologicalSketchRecord, id=record_id)
    # 初始化表单实例
    form = GeologicalSketchRecordForm(instance=record)
    # 将所有字段设置为只读
    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = 'readonly'
        field.widget.attrs['class'] = 'form-control'
    # 渲染模板并传递表单和记录
    return render(request, 'personal_center/view_GeologicalSketchRecord.html', {'form': form, 'record': record})

@login_required
def view_ExcavationDiagnosis(request, record_id):
    """
    用户查看超欠挖诊断记录（只读）。
    """
    # 获取记录
    record = get_object_or_404(ExcavationDiagnosis, id=record_id, created_by=request.user)
    # 初始化表单实例
    form = ExcavationDiagnosisForm(instance=record)
    # 设置所有字段为只读
    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = 'readonly'
        field.widget.attrs['class'] = 'form-control'
    # 渲染模板
    return render(request, 'personal_center/view_ExcavationDiagnosis.html', {'form': form, 'record': record})

@login_required
def view_OverUnderExcavation(request, record_id):
    """
    用户查看超欠挖计算记录（只读）。
    """
    # 获取记录
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id, created_by=request.user)
    # 初始化表单实例
    form = OverUnderExcavationForm(instance=record)
    # 设置所有字段为只读
    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = 'readonly'
        field.widget.attrs['class'] = 'form-control'
    # 渲染模板
    return render(request, 'personal_center/view_OverUnderExcavation.html', {'form': form, 'record': record})

@login_required
def view_TunnelContour(request, record_id):
    """
    用户查看隧道轮廓记录（只读）。
    """
    # 获取记录
    record = get_object_or_404(TunnelContourInfo, id=record_id, created_by=request.user)
    # 初始化表单实例
    form = TunnelContourForm(instance=record)
    # 设置所有字段为只读
    for field_name, field in form.fields.items():
        field.widget.attrs['readonly'] = 'readonly'
        field.widget.attrs['class'] = 'form-control'
    # 渲染模板
    return render(request, 'personal_center/view_TunnelContour.html', {'form': form, 'record': record})
