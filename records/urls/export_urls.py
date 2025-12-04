from django.urls import path

from records.views.export_views import export_geological_view, export_geological_records, \
    export_excavation_calculation_view, export_excavation_calculation_records, export_excavation_diagnosis_view, \
    export_excavation_diagnosis_records, export_tunnel_contour_view, export_tunnel_contour_records

urlpatterns = [
    #掌子面导出
    path('geological/export/', export_geological_view, name='export_geological_view'),
    path('geological/export/records/', export_geological_records, name='export_geological_records'),
    # 超欠挖计算导出
    path('calculation/export/', export_excavation_calculation_view, name='export_excavation_calculation_view'),
    path('calculation/export/records/', export_excavation_calculation_records, name='export_excavation_calculation_records'),
    # 超欠挖诊断导出
    path('diagnosis/export/', export_excavation_diagnosis_view, name='export_excavation_diagnosis_view'),
    path('diagnosis/export/records/', export_excavation_diagnosis_records, name='export_excavation_diagnosis_records'),
    # 隧道轮廓导出
    path('tunnel/export/', export_tunnel_contour_view, name='export_tunnel_contour_view'),
    path('tunnel/export/records/', export_tunnel_contour_records, name='export_tunnel_contour_records'),
]