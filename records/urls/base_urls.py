from django.urls import path

from records.views.base_views import register_view, login_view, index_view, logout_view, view_audit_logs, \
    view_log_detail, backup_view, restore_database, clear_message, get_status_counts, geological_statistics_data

urlpatterns = [
    #基础页面
    path('register/', register_view, name='register'),  #注册
    path('login/', login_view, name='login'),   #登录
    path('', index_view, name='index'),     # 主界面
    path('logout/', logout_view, name='logout'),   # 退出登录
    path('audit_logs/', view_audit_logs, name='view_audit_logs'),  # 日志记录页面（全部日志列表）
    path('log/<int:log_id>/', view_log_detail, name='view_log_detail'), # 详细单条日志信息
    #数据库备份
    path('backup/', backup_view, name='backup'),  # 数据库备份
    #恢复数据库
    path("restore-database/", restore_database, name="restore_database"),
    #清理session
    path('clear_message/', clear_message, name='clear_message'),
    path('status_counts/', get_status_counts, name='get_status_counts'),
    path('geological-statistics-data/', geological_statistics_data, name='geological_statistics_data'),

]
