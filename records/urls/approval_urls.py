from django.urls import path

from records.views.approval_views import approval_list
from records.views.approval_views import (
    approval_list,
    approval_excavation_calculation,
    approval_excavation_diagnosis,
    approval_tunnel_contour,
    approve_geological_record,
    approve_excavation_diagnosis,
    approve_over_under_calculation,
    approve_tunnel_contour,
    reject_geological_record,
    reject_excavation_diagnosis,
    reject_over_under_excavation,
    reject_tunnel_contour,
)


urlpatterns = [
    # 四个审批页面（管理员）（大页面）
    path('approval/list/', approval_list, name='approval_list'),  # 审批掌子面信息列表页面
    path('approval_excavation_calculation/', approval_excavation_calculation, name='approval_list1'),  # 超欠挖计算审批
    path('approval_excavation_diagnosis/', approval_excavation_diagnosis, name='approval_list2'),  # 超欠挖诊断审批
    path('approval_tunnel_contour/', approval_tunnel_contour, name='approval_list3'),  # 隧道审批

    # 四个详细的审批页面（管理员）
    path('approval/<int:record_id>/', approve_geological_record, name='approve_geological_record'),  # 掌子面详细审批页面（审批上传、修改、删除）
    path('approval/excavation/<int:record_id>/', approve_excavation_diagnosis, name='approve_excavation_diagnosis'),  # 超欠挖诊断详细审批页面（审批上传、修改、删除）
    path('approval/over_under/<int:record_id>/', approve_over_under_calculation, name='approve_over_under_excavation'),  # 超欠挖计算详细审批页面（审批上传、修改、删除）
    path('approval/tunnel/<int:record_id>/', approve_tunnel_contour, name='approve_tunnel_contour'),  # 隧道轮廓信息详细审批页面（审批上传、修改、删除）

    # 四个驳回
    path('records/reject/<int:record_id>/', reject_geological_record, name='reject_geological_record'),  # 管理员驳回掌子面
    path('diagnosis/reject/<int:record_id>/', reject_excavation_diagnosis, name='reject_excavation_diagnosis'),
    path('calculation/reject/<int:record_id>/', reject_over_under_excavation, name='reject_over_under_calculation'),
    path('tunnel/reject/<int:record_id>/', reject_tunnel_contour, name='reject_tunnel_contour'),


]