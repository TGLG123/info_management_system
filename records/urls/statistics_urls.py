from django.urls import path

from records.views.statistics_views import geological_statistics, excavation_calculation_statistics, \
    excavation_diagnosis_statistics, tunnel_statistics

urlpatterns = [
    # 统计数据
    path('geological/statistics/', geological_statistics, name='geological_statistics'),
    path('statistics/excavation/', excavation_calculation_statistics, name='excavation_statistics'),
    path('statistics/diagnosis/', excavation_diagnosis_statistics, name='diagnosis_statistics'),
    path('statistics/tunnel/', tunnel_statistics, name='tunnel_statistics'),
]