import os
import hashlib
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
import mimetypes
from django.contrib import messages  # 用于发送消息
from django.utils.http import urlquote
from records.models import DataStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render



#哈希函数
def hash_file(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


#文件上传
@login_required
def upload_file(request):
    """
    文件上传视图，支持选择文件关联类别和关联记录编号。
    """
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        mime_type = uploaded_file.content_type

        # 文件类型映射
        if mime_type.startswith('image/'):
            file_type = 'image'
        elif mime_type == 'application/pdf':
            file_type = 'pdf'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ]:
            file_type = 'word'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ]:
            file_type = 'excel'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.ms-powerpoint',
            'application/powerpoint',
            'application/x-mspowerpoint'
        ]:
            file_type = 'ppt'
        elif mime_type == 'text/plain':
            file_type = 'text'
        elif mime_type in [
            'application/zip',
            'application/x-zip-compressed',
            'multipart/x-zip'
        ]:
            file_type = 'zip'
        elif mime_type == 'application/vnd.rar':
            file_type = 'rar'
        elif mime_type == 'application/x-7z-compressed':
            file_type = '7z'
        elif mime_type == 'application/octet-stream':
            file_type = 'binary'
        else:
            file_type = os.path.splitext(file_name)[1]  # 未知类型时取文件后缀

        # 读取文件数据和计算哈希值
        file_data = uploaded_file.read()
        file_hash = hash_file(uploaded_file)
        uploaded_file.seek(0)  # 重置文件指针

        # 检查重复文件
        if DataStorage.objects.filter(file_hash=file_hash).exists():
            messages.error(request, "该文件已存在，不能重复上传。")
            return redirect('upload')

        # 使用 default_storage 保存文件到文件系统
        file_path = default_storage.save(f'uploads/{file_name}', ContentFile(file_data))

        # 获取其他表单字段
        file_description = request.POST.get('file_description', '')
        category = request.POST.get('file_category', '')  # 修改为 file_category
        related_record_id = request.POST.get('related_record_id', None)
        operation_reason = request.POST.get('operation_reason', '')

        # 校验 file_category 是否合法
        valid_categories = ['geological', 'excavation_diagnosis', 'excavation_calculation', 'tunnel', 'other']
        if category not in valid_categories:
            messages.error(request, "请选择有效的文件关联类别！")
            return redirect('upload')

        # 保存文件记录到数据库
        DataStorage.objects.create(
            file_name=file_name,
            file_path=file_path,
            file_data=file_data,
            file_type=file_type,
            file_hash=file_hash,
            file_description=file_description,
            category=category,  # 修改为 file_category
            related_record_id=related_record_id,
            uploaded_by=request.user,
            status='uploaded_approved',  # 默认设置为管理员审批通过
            approved_by=request.user,
            approved_at=timezone.now(),
            operation_reason=operation_reason
        )

        messages.success(request, "文件上传成功！")
        return redirect('upload')

    return render(request, 'file_management/upload.html')


# 文件修改
@login_required
def update_file(request, file_id):
    """
    文件修改视图：支持上传新文件替换现有文件，并保留上传视图的所有逻辑。
    """
    # 获取文件记录
    file_record = get_object_or_404(DataStorage, id=file_id)

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        mime_type = uploaded_file.content_type

        # 文件类型映射
        if mime_type.startswith('image/'):
            file_type = 'image'
        elif mime_type == 'application/pdf':
            file_type = 'pdf'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/msword'
        ]:
            file_type = 'word'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-excel'
        ]:
            file_type = 'excel'
        elif mime_type in [
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.ms-powerpoint',
            'application/powerpoint',
            'application/x-mspowerpoint'
        ]:
            file_type = 'ppt'
        elif mime_type == 'text/plain':
            file_type = 'text'
        elif mime_type in [
            'application/zip',
            'application/x-zip-compressed',
            'multipart/x-zip'
        ]:
            file_type = 'zip'
        elif mime_type == 'application/vnd.rar':
            file_type = 'rar'
        elif mime_type == 'application/x-7z-compressed':
            file_type = '7z'
        elif mime_type == 'application/octet-stream':
            file_type = 'binary'
        else:
            file_type = os.path.splitext(file_name)[1]  # 未知类型时取文件后缀

        # 读取文件数据和计算哈希值
        file_data = uploaded_file.read()
        file_hash = hash_file(uploaded_file)
        uploaded_file.seek(0)  # 重置文件指针

        # 检查重复文件
        if DataStorage.objects.filter(file_hash=file_hash).exclude(id=file_id).exists():
            messages.error(request, "该文件已存在，不能重复上传。")
            return redirect('update_file', file_id=file_id)

        # 使用 default_storage 保存新文件到文件系统
        new_file_path = default_storage.save(f'uploads/{file_name}', ContentFile(file_data))

        # 删除旧文件（如果存在）
        if file_record.file_path:
            default_storage.delete(file_record.file_path)

        # 获取其他表单字段
        file_description = request.POST.get('file_description', file_record.file_description)
        category = request.POST.get('file_category', file_record.category)
        related_record_id = request.POST.get('related_record_id', file_record.related_record_id)
        operation_reason = request.POST.get('operation_reason', '')

        # 校验 file_category 是否合法
        valid_categories = ['geological', 'excavation_diagnosis', 'excavation_calculation', 'tunnel', 'other']
        if category not in valid_categories:
            messages.error(request, "请选择有效的文件关联类别！")
            return redirect('update_file', file_id=file_id)

        # 更新文件记录到数据库
        file_record.file_name = file_name
        file_record.file_path = new_file_path
        file_record.file_data = file_data
        file_record.file_type = file_type
        file_record.file_hash = file_hash
        file_record.file_description = file_description
        file_record.category = category
        file_record.related_record_id = related_record_id
        file_record.uploaded_by = request.user
        file_record.upload_date = timezone.now()  # 更新上传日期
        file_record.operation_reason = operation_reason
        file_record.save()

        messages.success(request, "文件修改成功！")
        return redirect('update_file', file_id=file_id)

    # 如果是 GET 请求，展示修改文件的表单，预填当前文件的信息
    return render(request, 'file_management/update.html', {'file': file_record})


# 文件列表（管理员）
def preview_files(request):
    """
    展示文件列表，并支持按文件名和文件类型搜索及分页。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索的文件名或文件类型

    # 获取所有文件记录并按上传时间降序排序
    files_list = DataStorage.objects.all().order_by('-upload_date')

    # 根据搜索条件过滤数据（支持文件名和文件类型的模糊查询）
    if search_query:
        files_list = files_list.filter(
            Q(file_name__icontains=search_query) | Q(file_type__icontains=search_query)
        )

    # 设置分页，每页显示 10 条记录
    paginator = Paginator(files_list, 10)
    page = request.GET.get('page')

    try:
        # 获取当前页的数据
        files = paginator.page(page)
    except PageNotAnInteger:
        # 如果 page 参数不是整数，显示第一页
        files = paginator.page(1)
    except EmptyPage:
        # 如果页数超出范围，显示最后一页
        files = paginator.page(paginator.num_pages)

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板并传递分页后的文件数据
    return render(request, 'file_management/preview.html', {
        'files': files,
        'total_pages': paginator.num_pages,  # 总页数
        'current_page': files.number,  # 当前页码
        'search_query': search_query,  # 搜索条件
        'query_params': query_params_encoded,  # 用于分页链接
    })


# 文件列表（用户）
@login_required
def user_files(request):
    """
    用户文件列表：仅显示当前用户上传的文件，并支持按文件名和文件类型搜索及分页。
    """
    # 获取搜索条件
    search_query = request.GET.get('search', '')  # 获取搜索的文件名或文件类型

    # 获取当前用户上传的文件记录，并按上传时间降序排序
    user_files_list = DataStorage.objects.filter(uploaded_by=request.user).order_by('-upload_date')

    # 根据搜索条件过滤数据（支持文件名和文件类型的模糊查询）
    if search_query:
        user_files_list = user_files_list.filter(
            Q(file_name__icontains=search_query) | Q(file_type__icontains=search_query)
        )

    # 设置分页，每页显示 10 条记录
    paginator = Paginator(user_files_list, 10)
    page = request.GET.get('page')

    try:
        # 获取当前页的数据
        files = paginator.page(page)
    except PageNotAnInteger:
        # 如果 page 参数不是整数，显示第一页
        files = paginator.page(1)
    except EmptyPage:
        # 如果页数超出范围，显示最后一页
        files = paginator.page(paginator.num_pages)

    # 保留搜索参数的查询参数
    query_params = request.GET.copy()
    query_params.pop('page', None)  # 移除分页参数，避免重复
    query_params_encoded = query_params.urlencode()  # 编码查询参数

    # 渲染模板并传递分页后的文件数据
    return render(request, 'file_management/user_files.html', {
        'files': files,
        'total_pages': paginator.num_pages,  # 总页数
        'current_page': files.number,  # 当前页码
        'search_query': search_query,  # 搜索条件
        'query_params': query_params_encoded,  # 用于分页链接
    })


#下面是把浏览器浏览与下载分成两个函数处理的结果（等同于上面的合在一起的），但是可以解决下载不了的bug
def preview_file(request, file_id):
    file_record = get_object_or_404(DataStorage, id=file_id)
    content_type, _ = mimetypes.guess_type(file_record.file_name)
    content_type = content_type or 'application/octet-stream'
    response = HttpResponse(file_record.file_data, content_type=content_type)
    # 使用 urlquote 确保文件名正确编码，这个urlquote很重要，没有的话下载就有bug
    response['Content-Disposition'] = f'inline; filename="{urlquote(file_record.file_name)}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

def download_file(request, file_id):
    file_record = get_object_or_404(DataStorage, id=file_id)
    content_type, _ = mimetypes.guess_type(file_record.file_name)
    content_type = content_type or 'application/octet-stream'
    response = HttpResponse(file_record.file_data, content_type=content_type)
    # 使用 urlquote 确保文件名正确编码
    response['Content-Disposition'] = f'attachment; filename="{urlquote(file_record.file_name)}"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response



from django.http import Http404
def delete_file(request, file_id):
    print("删除文件")
    try:
        # 获取文件记录
        file_record = get_object_or_404(DataStorage, id=file_id)

        # 删除文件记录
        file_record.delete()
        messages.success(request, "文件已成功删除！")
    except Http404:
        messages.error(request, "未找到指定的文件记录！")
    except Exception as e:
        messages.error(request, f"删除文件时出错：{e}")

    # 重定向到文件预览页面
    return redirect('preview')

# 查看文件详细内容
@login_required
def view_file(request, file_id):
    try:
        file_record = DataStorage.objects.get(id=file_id, uploaded_by=request.user)
    except DataStorage.DoesNotExist:
        messages.error(request, "文件不存在或您无权查看此文件！")
        return redirect('file_records_view')

    # 根据文件类型，处理文件内容
    file_data = None
    if file_record.file_type in ['text', 'pdf']:
        file_data = file_record.file_data.decode('utf-8', errors='ignore') if file_record.file_data else None

    return render(request, 'file_management/view_file.html', {
        'file_record': file_record,
        'file_data': file_data,
    })