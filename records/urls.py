# from django.urls import path
# from . import views
# from .views import register_view, logout_view, geological_list, upload_geological_info, edit_geological_record, \
#     view_geological_logs
# from .views import index_view, login_view
#
# urlpatterns = [
#     #基础页面
#     path('register/', register_view, name='register'),  #注册
#     path('login/', login_view, name='login'),   #登录
#     path('', views.index_view, name='index'),     # 主界面
#     path('logout/', logout_view, name='logout'),   # 退出登录
#     path('audit_logs/', views.view_audit_logs, name='view_audit_logs'),  # 日志记录页面（全部日志列表）
#     path('log/<int:log_id>/', views.view_log_detail, name='view_log_detail'), # 详细单条日志信息
#
#     #这四个是拆开的个人中心（掌子面，超欠挖计算，，超欠挖诊断，隧道）
#     path('geological-records/', views.user_records_view, name='user_records_view'),  # 掌子面用户记录页面（掌子面个人中心）
#     path('excavation-calculation-records/', views.excavation_calculation_records_view, name='excavation_calculation_records'),# 超欠挖计算记录
#     path('excavation-diagnosis-records/', views.excavation_diagnosis_records_view, name='excavation_diagnosis_records'),# 超欠挖诊断记录
#     path('tunnel-contour-records/', views.tunnel_contour_records_view, name='tunnel_contour_records'),# 隧道轮廓记录
#
#     #四个上传（管理员）
#     path('upload_geological_info/', upload_geological_info, name='upload_geological_info'),  # 管理员上传地质信息（四种都有，进去在掌子面这里）
#     path('upload/info1/', views.upload_info1, name='upload_info1'),  # 隧道信息管理员上传
#     path('upload/info2/', views.upload_info2, name='upload_info2'),  # 超欠挖诊断信息管理员上传
#     path('upload/info3/', views.upload_info3, name='upload_info3'),  # 超欠挖计算信息管理员上传
#
#     #四个信息列表（管理员）
#     path('geological_list/', geological_list, name='geological_list'),  # 掌子面地质信息列表（管理员版）（四种都有，进去在掌子面这里）
#     path('excavation-calculation/', views.excavation_calculation_list, name='excavation_calculation_list'), #超欠挖计算信息列表
#     path('excavation-diagnosis/', views.excavation_diagnosis_list, name='excavation_diagnosis_list'),  #超欠挖诊断信息列表
#     path('tunnel-contour-info/', views.tunnel_contour_info_list, name='tunnel_contour_info_list'), #隧道信息列表
#
#     #四个修改（管理员）
#     path('edit_geological_record/<int:pk>/', edit_geological_record, name='edit_geological_record'),#修改掌子面信息
#     path('diagnosis/edit/<int:pk>/', views.edit_excavation_diagnosis, name='edit_excavation_diagnosis'),    # 修改超欠挖诊断信息
#     path('calculation/edit/<int:pk>/', views.edit_over_under_excavation, name='edit_over_under_excavation'),    # 修改超欠挖计算信息
#     path('tunnel/edit/<int:pk>/', views.edit_tunnel_contour, name='edit_tunnel_contour'),    # 修改隧道轮廓信息
#
#     #四个删除（管理员）
#     path('geological/delete/<int:record_id>/', views.delete_geological_record, name='delete_geological_record'),#掌子面删除（管理员）
#     path('records/over_under_excavation/delete/<int:record_id>/', views.delete_over_under_excavation_record, name='delete_over_under_excavation'), # 超欠挖计算删除（管理员）
#     path('records/excavation_diagnosis/delete/<int:record_id>/', views.delete_excavation_diagnosis_record, name='delete_excavation_diagnosis'),    # 超欠挖诊断删除（管理员）
#     path('records/tunnel_contour/delete/<int:record_id>/', views.delete_tunnel_contour_record, name='delete_tunnel_contour'),    # 隧道轮廓删除（管理员）
#
#     #四个审批页面（管理员）（大页面）
#     path('approval/list/', views.approval_list, name='approval_list'),  # 审批掌子面信息列表页面
#     path('approval_excavation_calculation/', views.approval_excavation_calculation, name='approval_list1'),#超欠挖计算审批
#     path('approval_excavation_diagnosis/', views.approval_excavation_diagnosis, name='approval_list2'),#超欠挖诊断审批
#     path('approval_tunnel_contour/', views.approval_tunnel_contour, name='approval_list3'),#隧道审批
#
#     #四个详细的审批页面（管理员）
#     path('approval/<int:record_id>/', views.approve_geological_record, name='approve_geological_record'),   # 掌子面详细审批页面（审批上传、修改、删除）
#     path('approval/excavation/<int:record_id>/', views.approve_excavation_diagnosis, name='approve_excavation_diagnosis'),  # 超欠挖诊断详细审批页面（审批上传、修改、删除）
#     path('approval/over_under/<int:record_id>/', views.approve_over_under_calculation, name='approve_over_under_excavation'),  # 超欠挖计算详细审批页面（审批上传、修改、删除）
#     path('approval/tunnel/<int:record_id>/', views.approve_tunnel_contour, name='approve_tunnel_contour'),  # 隧道轮廓信息详细审批页面（审批上传、修改、删除）
#
#     #四个驳回
#     path('records/reject/<int:record_id>/', views.reject_geological_record, name='reject_geological_record'),#管理员驳回掌子面
#     path('diagnosis/reject/<int:record_id>/', views.reject_excavation_diagnosis, name='reject_excavation_diagnosis'),
#     path('calculation/reject/<int:record_id>/', views.reject_over_under_excavation, name='reject_over_under_calculation'),
#     path('tunnel/reject/<int:record_id>/', views.reject_tunnel_contour, name='reject_tunnel_contour'),
#
#     #四个用户上传页面
#     path('upload/user/', views.upload_geological_info_user, name='upload_geological_info_user'),    # 用户上传掌子面
#     path('upload/excavation-calculation/user/', views.upload_excavation_calculation_user, name='upload_excavation_calculation_user'),   # 用户上传超欠挖计算
#     path('upload/excavation-diagnosis/user/', views.upload_excavation_diagnosis_user, name='upload_excavation_diagnosis_user'), # 用户上传超欠挖诊断
#     path('upload/tunnel-info/user/', views.upload_tunnel_info_user, name='upload_tunnel_info_user'),    # 用户上传隧道信息
#
#     #用户修改，删除自己的新增待审批信息
#     path('records/edit/<int:record_id>/', views.edit_pending_record, name='edit_pending_record'),# 用户修改自己的掌子面待审批记录
#     path('records/delete/<int:record_id>/', views.delete_pending_record, name='delete_pending_record'),# 用户删除自己的掌子面待审批记录
#     path('edit/pending/excavation/<int:record_id>/', views.edit_pending_excavation_diagnosis, name='edit_pending_excavation_diagnosis'),
#     path('edit/pending/overunder/<int:record_id>/', views.edit_pending_over_under_excavation, name='edit_pending_over_under_excavation'),
#     path('edit/pending/tunnel/<int:record_id>/', views.edit_pending_tunnel_contour, name='edit_pending_tunnel_contour'),
#     path('delete/pending/excavation/<int:record_id>/', views.delete_pending_excavation_diagnosis, name='delete_pending_excavation_diagnosis'),
#     path('delete/pending/overunder/<int:record_id>/', views.delete_pending_over_under_excavation, name='delete_pending_over_under_excavation'),
#     path('delete/pending/tunnel/<int:record_id>/', views.delete_pending_tunnel_contour, name='delete_pending_tunnel_contour'),
#
#     #这八个是四张表（掌子面，超欠挖计算，诊断，隧道）的已审批信息的修改，删除的申请
#     path('records/apply_edit/<int:record_id>/', views.apply_edit_record, name='apply_edit_record'),# （掌子面）用户对已审批通过的记录申请修改，提交管理员审批
#     path('records/apply_delete/<int:record_id>/', views.apply_delete_record, name='apply_delete_record'),# 用户对已审批通过的记录申请删除，提交管理员审批
#     path('apply_edit_excavation_diagnosis/<int:record_id>/', views.apply_edit_excavation_diagnosis, name='apply_edit_excavation_diagnosis'),# 申请修改超欠挖诊断记录
#     path('apply_delete_excavation_diagnosis/<int:record_id>/', views.apply_delete_excavation_diagnosis, name='apply_delete_excavation_diagnosis'),# 申请删除超欠挖诊断记录
#     path('apply_edit_over_under_excavation_calculation/<int:record_id>/', views.apply_edit_over_under_excavation_calculation, name='apply_edit_over_under_excavation_calculation'),# 申请修改超欠挖计算记录
#     path('apply_delete_over_under_excavation_calculation/<int:record_id>/', views.apply_delete_over_under_excavation_calculation, name='apply_delete_over_under_excavation_calculation'),# 申请删除超欠挖计算记录
#     path('apply_edit_tunnel_contour_info/<int:record_id>/', views.apply_edit_tunnel_contour_info, name='apply_edit_tunnel_contour_info'),# 申请修改隧道轮廓信息记录
#     path('apply_delete_tunnel_contour_info/<int:record_id>/', views.apply_delete_tunnel_contour_info, name='apply_delete_tunnel_contour_info'),# 申请删除隧道轮廓信息记录
#
#     #修改，删除“修改待审批”信息
#     path('records/edit_modified/<int:record_id>/', views.edit_modified_pending_record, name='edit_modified_pending_record'),# 修改待审批的记录(掌子面）
#     path('records/delete_modified/<int:record_id>/', views.delete_modified_pending_record, name='delete_modified_pending_record'),# 删除修改待审批的记录（掌子面）
#     path('edit/modified/excavation/<int:record_id>/', views.edit_modified_pending_excavation_diagnosis, name='edit_modified_pending_excavation_diagnosis'),
#     path('edit/modified/overunder/<int:record_id>/', views.edit_modified_pending_over_under_excavation, name='edit_modified_pending_over_under_excavation'),
#     path('edit/modified/tunnel/<int:record_id>/', views.edit_modified_pending_tunnel_contour, name='edit_modified_pending_tunnel_contour'),
#     path('delete/modified/excavation/<int:record_id>/', views.delete_modified_pending_excavation_diagnosis, name='delete_modified_pending_excavation_diagnosis'),
#     path('delete/modified/overunder/<int:record_id>/', views.delete_modified_pending_over_under_excavation, name='delete_modified_pending_over_under_excavation'),
#     path('delete/modified/tunnel/<int:record_id>/', views.delete_modified_pending_tunnel_contour, name='delete_modified_pending_tunnel_contour'),
#
#     # 删除“删除待审批记录”（取消删除申请）
#     path('records/delete_deleted/<int:record_id>/', views.delete_deleted_pending_record, name='delete_deleted_pending_record'),
#     path('cancel/delete/excavation/<int:record_id>/', views.cancel_delete_pending_excavation_diagnosis, name='cancel_delete_pending_excavation_diagnosis'),
#     path('cancel/delete/overunder/<int:record_id>/', views.cancel_delete_pending_over_under_excavation, name='cancel_delete_pending_over_under_excavation'),
#     path('cancel/delete/tunnel/<int:record_id>/', views.cancel_delete_pending_tunnel_contour, name='cancel_delete_pending_tunnel_contour'),
#
#     #下面四个是重新申请的
#     path('records/reapply/<int:record_id>/', views.reapply_record, name='edit_record'),#用户重新申请被驳回的掌子面信息
#     path('excavation-diagnosis/reapply/<int:record_id>/', views.reapply_excavation_diagnosis, name='reapply_excavation_diagnosis'),
#     path('over-under-calculation/reapply/<int:record_id>/', views.reapply_over_under_calculation, name='reapply_over_under_calculation'),
#     path('tunnel-contour/reapply/<int:record_id>/', views.reapply_tunnel_contour, name='reapply_tunnel_contour'),
#
#     #下面四个是个人中心中查看详细信息的
#     path('view-geological/<int:record_id>/', views.view_GeologicalSketchRecord, name='view_GeologicalSketchRecord'), #掌子面
#     path('view-excavation-diagnosis/<int:record_id>/', views.view_ExcavationDiagnosis, name='view_ExcavationDiagnosis'), # 超欠挖诊断
#     path('view-over-under-excavation/<int:record_id>/', views.view_OverUnderExcavation, name='view_OverUnderExcavation'),    # 超欠挖计算
#     path('view-tunnel-contour/<int:record_id>/', views.view_TunnelContour, name='view_TunnelContour'),    # 隧道轮廓
#
#
#     #下面是用户管理
#     path('users/', views.user_management, name='user_management'),
#     path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
#     path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
#     path('users/add/', views.add_user, name='add_user'),
#
#     #统计数据
#     path('geological/statistics/', views.geological_statistics, name='geological_statistics'),
#     path('statistics/excavation/', views.excavation_calculation_statistics, name='excavation_statistics'),
#     path('statistics/diagnosis/', views.excavation_diagnosis_statistics, name='diagnosis_statistics'),
#     path('statistics/tunnel/', views.tunnel_statistics, name='tunnel_statistics'),
#
#     #掌子面导出
#     path('geological/export/', views.export_geological_view, name='export_geological_view'),
#     path('geological/export/records/', views.export_geological_records, name='export_geological_records'),
#     # 超欠挖计算导出
#     path('calculation/export/', views.export_excavation_calculation_view, name='export_excavation_calculation_view'),
#     path('calculation/export/records/', views.export_excavation_calculation_records, name='export_excavation_calculation_records'),
#     # 超欠挖诊断导出
#     path('diagnosis/export/', views.export_excavation_diagnosis_view, name='export_excavation_diagnosis_view'),
#     path('diagnosis/export/records/', views.export_excavation_diagnosis_records, name='export_excavation_diagnosis_records'),
#     # 隧道轮廓导出
#     path('tunnel/export/', views.export_tunnel_contour_view, name='export_tunnel_contour_view'),
#     path('tunnel/export/records/', views.export_tunnel_contour_records, name='export_tunnel_contour_records'),
#
#
#
#     #path('view_geological_logs/', view_geological_logs, name='view_geological_logs'),#查看日志
#     #path('view_audit_logs/', views.view_audit_logs, name='view_audit_logs'),    #查看日志记录
#     path('user/pending/', views.user_pending_records, name='user_pending_records'), # 用户待审批记录页面
#
#     #修改之后信息展示
#     path('geological_record/<int:pk>/', views.geological_record_detail, name='geological_record_detail'),  # 展示修改后掌子面信息的详情页面
#     path('excavation_diagnosis/detail/<int:pk>/', views.excavation_diagnosis_detail, name='excavation_diagnosis_record_detail'), # 修改后超欠挖诊断详细信息
#     path('over_under_excavation/detail/<int:pk>/', views.over_under_excavation_detail, name='over_under_excavation_record_detail'),# 修改后超欠挖计算详细信息
#     path('tunnel_contour/detail/<int:pk>/', views.tunnel_contour_detail, name='tunnel_contour_record_detail'),# 修改后隧道轮廓详细信息
#
#
#     #文件操作
#     path('upload/', views.upload_file, name='upload'),  # 文件上传页面
#     path('preview/', views.preview_files, name='preview'),  # 文件列表页面（管理员）
#     path('user/files/', views.user_files, name='preview_user'), # 文件列表页面（用户）
#     path('preview/<int:file_id>/', views.preview_file, name='preview_file'), #在线预览
#     path('download/<int:file_id>/', views.download_file, name='download_file'), #下载文件
#     path('delete/file/<int:file_id>/', views.delete_file, name='delete_file'),  # 删除文件
#     path('update/<int:file_id>/', views.update_file, name='update_file'),  # 修改文件页面
#     path('view/<int:file_id>/', views.view_file, name='view_file'),# 查看文件详细内容
#     #文件的个人中心（未使用）
#     #path('files/', views.file_records_view, name='file_records_view'), #文件的个人中心
#
#
#
#
#     #展示区块链页面
#     #path('blockchain-records/', views.blockchain_records_view, name='blockchain_records'),
#
#     #数据库备份
#     path('backup/', views.backup_view, name='backup'),  # 数据库备份
#     #恢复数据库
#     path("restore-database/", views.restore_database, name="restore_database"),
#     #清理session
#     path('clear_message/', views.clear_message, name='clear_message'),
#
#
# ]
