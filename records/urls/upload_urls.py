from django.urls import path

from records.views.upload_views import upload_geological_info
from records.views.upload_views import (
    upload_geological_info,
    upload_info1,
    upload_info2,
    upload_info3,
    upload_geological_info_user,
    upload_excavation_calculation_user,
    upload_excavation_diagnosis_user,
    upload_tunnel_info_user,
)


urlpatterns = [
    # 四个上传（管理员）
    path('upload_geological_info/', upload_geological_info, name='upload_geological_info'),  # 管理员上传地质信息（四种都有，进去在掌子面这里）
    path('upload/info1/', upload_info1, name='upload_info1'),  # 隧道信息管理员上传
    path('upload/info2/', upload_info2, name='upload_info2'),  # 超欠挖诊断信息管理员上传
    path('upload/info3/', upload_info3, name='upload_info3'),  # 超欠挖计算信息管理员上传

    # 四个用户上传页面
    path('upload/user/', upload_geological_info_user, name='upload_geological_info_user'),  # 用户上传掌子面
    path('upload/excavation-calculation/user/', upload_excavation_calculation_user, name='upload_excavation_calculation_user'),  # 用户上传超欠挖计算
    path('upload/excavation-diagnosis/user/', upload_excavation_diagnosis_user, name='upload_excavation_diagnosis_user'),  # 用户上传超欠挖诊断
    path('upload/tunnel-info/user/', upload_tunnel_info_user, name='upload_tunnel_info_user'),  # 用户上传隧道信息

]