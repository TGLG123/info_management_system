from django.urls import path

from records.views.info_list_views import geological_list
from records.views.info_list_views import (
    geological_list,
    excavation_calculation_list,
    excavation_diagnosis_list,
    tunnel_contour_info_list,
    edit_geological_record,
    edit_excavation_diagnosis,
    edit_over_under_excavation,
    edit_tunnel_contour,
    delete_geological_record,
    delete_over_under_excavation_record,
    delete_excavation_diagnosis_record,
    delete_tunnel_contour_record,
    geological_record_detail,
    excavation_diagnosis_detail,
    over_under_excavation_detail,
    tunnel_contour_detail,
)

urlpatterns = [
    #四个信息列表（管理员）
    path('geological_list/', geological_list, name='geological_list'),  # 掌子面地质信息列表（管理员版）（四种都有，进去在掌子面这里）
    path('excavation-calculation/', excavation_calculation_list, name='excavation_calculation_list'), #超欠挖计算信息列表
    path('excavation-diagnosis/', excavation_diagnosis_list, name='excavation_diagnosis_list'),  #超欠挖诊断信息列表
    path('tunnel-contour-info/', tunnel_contour_info_list, name='tunnel_contour_info_list'), #隧道信息列表

    # 四个修改（管理员）
    path('edit_geological_record/<int:pk>/', edit_geological_record, name='edit_geological_record'),  # 修改掌子面信息
    path('diagnosis/edit/<int:pk>/', edit_excavation_diagnosis, name='edit_excavation_diagnosis'),  # 修改超欠挖诊断信息
    path('calculation/edit/<int:pk>/', edit_over_under_excavation, name='edit_over_under_excavation'),  # 修改超欠挖计算信息
    path('tunnel/edit/<int:pk>/', edit_tunnel_contour, name='edit_tunnel_contour'),  # 修改隧道轮廓信息

    # 四个删除（管理员）
    path('geological/delete/<int:record_id>/', delete_geological_record, name='delete_geological_record'),  # 掌子面删除（管理员）
    path('records/over_under_excavation/delete/<int:record_id>/', delete_over_under_excavation_record, name='delete_over_under_excavation'),  # 超欠挖计算删除（管理员）
    path('records/excavation_diagnosis/delete/<int:record_id>/', delete_excavation_diagnosis_record, name='delete_excavation_diagnosis'),  # 超欠挖诊断删除（管理员）
    path('records/tunnel_contour/delete/<int:record_id>/', delete_tunnel_contour_record, name='delete_tunnel_contour'),  # 隧道轮廓删除（管理员）

    # 修改之后信息展示
    path('geological_record/<int:pk>/', geological_record_detail, name='geological_record_detail'),  # 展示修改后掌子面信息的详情页面
    path('excavation_diagnosis/detail/<int:pk>/', excavation_diagnosis_detail, name='excavation_diagnosis_record_detail'),  # 修改后超欠挖诊断详细信息
    path('over_under_excavation/detail/<int:pk>/', over_under_excavation_detail, name='over_under_excavation_record_detail'),  # 修改后超欠挖计算详细信息
    path('tunnel_contour/detail/<int:pk>/', tunnel_contour_detail, name='tunnel_contour_record_detail'),  # 修改后隧道轮廓详细信息


]