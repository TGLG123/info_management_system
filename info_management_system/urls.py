# from django.contrib import admin
# from django.urls import path, include
# #from records.views import index_view  # 引入主界面的视图
#
# urlpatterns = [
#     path('admin/', admin.site.urls),          # Django 管理页面
#     path('', include('records.urls')),       # 包含 records 应用的路由
#     path('records/', include('records.urls')), # 引入 records 应用的路由
# ]


from django.contrib import admin
from django.urls import path, include
from records.views.base_views import index_view  # 导入主界面视图

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理后台

    # 根路径跳转到主界面
    path('', index_view, name='index'),

    # 基础功能模块（如登录、退出）
    path('base/', include('records.urls.base_urls')),
    # 其他功能模块
    path('approval/', include('records.urls.approval_urls')),  # 审批模块
    path('export/', include('records.urls.export_urls')),  # 数据导出模块
    path('files/', include('records.urls.file_management_urls')),  # 文件管理模块
    path('info-list/', include('records.urls.info_list_urls')),  # 信息列表模块
    path('personal-center/', include('records.urls.personal_center_urls')),  # 个人中心模块
    path('statistics/', include('records.urls.statistics_urls')),  # 统计模块
    path('upload/', include('records.urls.upload_urls')),  # 上传模块
    path('user-management/', include('records.urls.user_management_urls')),  # 用户管理模块
]


