from ..models import User, MySQLGeneralLog, OverUnderExcavationCalculation, ExcavationDiagnosis, TunnelContourInfo
from ..forms import GeologicalSketchRecordForm, ExcavationDiagnosisForm, OverUnderExcavationForm, TunnelContourForm
from ..models import GeologicalSketchRecord
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from django.shortcuts import render



#地质信息展示
#掌子面信息记录
@login_required
def geological_list(request):
    """
    掌子面信息展示视图，支持按 face_id 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 获取所有地质记录，状态筛选
    records = GeologicalSketchRecord.objects.filter(
        status__in=['uploaded_approved', 'modified_approved', 'deleted']
    )

    # 根据搜索条件过滤数据
    if search_query:
        records = records.filter(face_id__icontains=search_query)

    # 设置分页
    paginator = Paginator(records, 8)  # 每页显示8条记录
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据

    # 渲染模板并传递上下文
    return render(request, 'info_list/geological_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,  # 用于保留搜索条件
    })

# # 超欠挖计算记录
@login_required
def excavation_calculation_list(request):
    """
    超欠挖计算信息展示视图，支持按 face_id 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 获取所有记录，状态筛选
    records = OverUnderExcavationCalculation.objects.filter(
        status__in=['uploaded_approved', 'modified_approved', 'deleted']
    )

    # 根据搜索条件过滤数据
    if search_query:
        records = records.filter(face_id__icontains=search_query)

    # 设置分页
    paginator = Paginator(records, 8)  # 每页显示 8 条记录
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据

    # 渲染模板并传递上下文
    return render(request, 'info_list/excavation_calculation_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,  # 用于保留搜索条件
    })

# 超欠挖诊断记录
@login_required
def excavation_diagnosis_list(request):
    """
    超欠挖诊断信息展示视图，支持按 face_id 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 获取所有记录，状态筛选
    records = ExcavationDiagnosis.objects.filter(
        status__in=['uploaded_approved', 'modified_approved', 'deleted']
    )

    # 根据搜索条件过滤数据
    if search_query:
        records = records.filter(face_id__icontains=search_query)

    # 设置分页
    paginator = Paginator(records, 8)  # 每页显示 8 条记录
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据

    # 渲染模板并传递上下文
    return render(request, 'info_list/excavation_diagnosis_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,  # 用于保留搜索条件
    })

# 隧道轮廓信息记录
@login_required
def tunnel_contour_info_list(request):
    """
    隧道轮廓信息展示视图，支持按 face_id 搜索。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索条件

    # 获取所有记录，状态筛选
    records = TunnelContourInfo.objects.filter(
        status__in=['uploaded_approved', 'modified_approved', 'deleted']
    )

    # 根据搜索条件过滤数据
    if search_query:
        records = records.filter(face_id__icontains=search_query)

    # 设置分页
    paginator = Paginator(records, 8)  # 每页显示 8 条记录
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据

    # 渲染模板并传递上下文
    return render(request, 'info_list/tunnel_contour_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,  # 用于保留搜索条件
    })


#修改掌子面信息(管理员)
def edit_geological_record(request, pk):  # 参数名为 pk，与 URL 配置一致
    record = get_object_or_404(GeologicalSketchRecord, pk=pk)

    if request.method == "POST":
        form = GeologicalSketchRecordForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.modified_by = request.user  # 设置修改人
            record.save()  # 保存记录
            return redirect('geological_record_detail', pk=record.pk)
    else:
        form = GeologicalSketchRecordForm(instance=record)

    return render(request, 'info_list/edit_geological_record.html', {'form': form, 'record': record})

# 修改超欠挖计算信息（管理员）
@login_required
def edit_over_under_excavation(request, pk):
    """
    管理员修改超欠挖计算记录视图：
    - 根据记录 ID 加载相应记录
    - 提交表单时保存修改，并记录修改人
    """
    record = get_object_or_404(OverUnderExcavationCalculation, pk=pk)

    if request.method == "POST":
        form = OverUnderExcavationForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.modified_by = request.user  # 设置修改人
            record.save()  # 保存修改后的记录
            return redirect('over_under_excavation_record_detail', pk=record.pk)
    else:
        form = OverUnderExcavationForm(instance=record)

    return render(request, 'info_list/edit_over_under_excavation.html', {'form': form, 'record': record})

# 修改超欠挖诊断信息（管理员）
@login_required
def edit_excavation_diagnosis(request, pk):
    """
    管理员修改超欠挖诊断记录视图：
    - 根据记录 ID 加载相应记录
    - 提交表单时保存修改，并记录修改人
    """
    record = get_object_or_404(ExcavationDiagnosis, pk=pk)

    if request.method == "POST":
        form = ExcavationDiagnosisForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.modified_by = request.user  # 设置修改人
            record.save()  # 保存修改后的记录
            return redirect('excavation_diagnosis_record_detail', pk=record.pk)
    else:
        form = ExcavationDiagnosisForm(instance=record)

    return render(request, 'info_list/edit_excavation_diagnosis.html', {'form': form, 'record': record})

# 修改隧道轮廓信息（管理员）
@login_required
def edit_tunnel_contour(request, pk):
    """
    管理员修改隧道轮廓信息记录视图：
    - 根据记录 ID 加载相应记录
    - 提交表单时保存修改，并记录修改人
    """
    record = get_object_or_404(TunnelContourInfo, pk=pk)

    if request.method == "POST":
        form = TunnelContourForm(request.POST, instance=record)
        if form.is_valid():
            record = form.save(commit=False)
            record.modified_by = request.user  # 设置修改人
            record.save()  # 保存修改后的记录
            return redirect('tunnel_contour_record_detail', pk=record.pk)
    else:
        form = TunnelContourForm(instance=record)

    return render(request, 'info_list/edit_tunnel_contour.html', {'form': form, 'record': record})



#掌子面删除（管理员）
@login_required
def delete_geological_record(request, record_id):
    """
    管理员删除地质记录。
    """
    print(f"User: {request.user}, Role: {getattr(request.user, 'role', None)}")
    record = get_object_or_404(GeologicalSketchRecord, id=record_id)

    # 使用自定义字段检查管理员权限
    if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
        return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)

    if request.method == 'POST':
        record.delete()
        print(f"Record {record_id} deleted successfully.")
        return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})

    return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)

#超欠挖计算删除（管理员）
@login_required
def delete_over_under_excavation_record(request, record_id):
    """
    管理员删除超欠挖计算记录。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, id=record_id)

    # 使用自定义字段检查管理员权限
    if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
        return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)

    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})

    return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)


#超欠挖诊断删除（管理员）
@login_required
def delete_excavation_diagnosis_record(request, record_id):
    """
    管理员删除超欠挖诊断记录。
    """
    record = get_object_or_404(ExcavationDiagnosis, id=record_id)

    # 使用自定义字段检查管理员权限
    if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
        return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)

    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})

    return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)


#隧道轮廓信息删除（管理员）
@login_required
def delete_tunnel_contour_record(request, record_id):
    """
    管理员删除隧道轮廓记录。
    """
    record = get_object_or_404(TunnelContourInfo, id=record_id)

    # 使用自定义字段检查管理员权限
    if not getattr(request.user, 'role', '') == 'admin':  # 假设 'role' 字段表示用户角色
        return JsonResponse({'success': False, 'message': "您没有权限删除记录。"}, status=403)

    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'message': f"记录 {record.face_id} 已成功删除。"})

    return JsonResponse({'success': False, 'message': "无效的请求方式。"}, status=400)

#展示修改后的详细掌子面信息
def geological_record_detail(request, pk):
    record = get_object_or_404(GeologicalSketchRecord, pk=pk)
    return render(request, 'info_list/geological_record_detail.html', {'record': record})

#展示修改后的详细超欠挖诊断信息
@login_required
def excavation_diagnosis_detail(request, pk):
    """
    展示超欠挖诊断详细信息。
    """
    record = get_object_or_404(ExcavationDiagnosis, pk=pk)
    return render(request, 'info_list/excavation_diagnosis_detail.html', {'record': record})

#展示修改后的详细超欠挖计算信息
@login_required
def over_under_excavation_detail(request, pk):
    """
    展示超欠挖计算详细信息。
    """
    record = get_object_or_404(OverUnderExcavationCalculation, pk=pk)
    return render(request, 'info_list/over_under_excavation_detail.html', {'record': record})

#展示修改后的隧道信息
@login_required
def tunnel_contour_detail(request, pk):
    """
    展示隧道轮廓详细信息。
    """
    record = get_object_or_404(TunnelContourInfo, pk=pk)
    return render(request, 'info_list/tunnel_contour_detail.html', {'record': record})