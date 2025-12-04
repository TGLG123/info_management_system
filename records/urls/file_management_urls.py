from django.urls import path

from records.views.file_management_views import upload_file, preview_files, user_files, preview_file, download_file, \
    delete_file, update_file, view_file

urlpatterns = [
    #文件操作
    path('upload/', upload_file, name='upload'),  # 文件上传页面
    path('preview/', preview_files, name='preview'),  # 文件列表页面（管理员）
    path('user/files/', user_files, name='preview_user'), # 文件列表页面（用户）
    path('preview/<int:file_id>/', preview_file, name='preview_file'), #在线预览
    path('download/<int:file_id>/', download_file, name='download_file'), #下载文件
    path('delete/file/<int:file_id>/', delete_file, name='delete_file'),  # 删除文件
    path('update/<int:file_id>/', update_file, name='update_file'),  # 修改文件页面
    path('view/<int:file_id>/', view_file, name='view_file'),# 查看文件详细内容
]
