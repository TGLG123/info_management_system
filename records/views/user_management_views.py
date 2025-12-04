from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required
def user_management(request):
    """
    用户管理视图。
    - 显示所有用户。
    - 支持按用户名或邮箱搜索用户。
    """
    User = get_user_model()
    search_query = request.GET.get('search', '')  # 获取搜索框的输入
    if search_query:
        users = User.objects.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query)
        )  # 按用户名或邮箱搜索
    else:
        users = User.objects.all()  # 默认展示所有用户

    return render(request, 'user_management/user_management.html', {'users': users, 'search_query': search_query})


@login_required
def edit_user(request, user_id):
    """
    修改用户角色视图。
    - 审计员 (auditor) 角色不可修改。
    - 只能在管理员 (admin) 和普通用户 (user) 之间切换。
    """
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)

    # 如果用户是审计员，显示不可修改提示
    if user.role == 'auditor':
        return render(request, 'user_management/edit_user.html', {'user': user, 'cannot_modify': True})

    if request.method == 'POST':
        role = request.POST.get('role')
        if role in ['admin', 'user']:  # 验证提交的角色是否有效
            user.role = role
            user.save()
            return redirect('user_management')
        else:
            return render(request, 'user_management/edit_user.html', {'user': user, 'error': '无效的角色选择'})

    return render(request, 'user_management/edit_user.html', {'user': user, 'cannot_modify': False})


@login_required
def add_user(request):
    """
    新增用户视图。
    - 支持选择所有角色 (admin, user, auditor)。
    """
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # 验证输入数据
        if username and email and password and role in ['admin', 'user', 'auditor']:
            User.objects.create_user(username=username, email=email, password=password, role=role)
            return redirect('user_management')
        else:
            return render(request, 'user_management/add_user.html', {'error': '请输入完整信息并选择有效的角色'})

    return render(request, 'user_management/add_user.html')


@login_required
def delete_user(request, user_id):
    """
    删除用户视图。
    """
    User = get_user_model()
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_management')