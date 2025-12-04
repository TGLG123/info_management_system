from django.urls import path

from records.views.personal_center_views import tunnel_contour_records_view, user_records_view, \
    excavation_calculation_records_view, excavation_diagnosis_records_view, apply_delete_record, \
    apply_edit_over_under_excavation_calculation, apply_delete_tunnel_contour_info, delete_deleted_pending_record, \
    reapply_over_under_calculation, view_TunnelContour

from records.views.personal_center_views import (
    edit_pending_record,
    delete_pending_record,
    edit_pending_excavation_diagnosis,
    edit_pending_over_under_excavation,
    edit_pending_tunnel_contour,
    delete_pending_excavation_diagnosis,
    delete_pending_over_under_excavation,
    delete_pending_tunnel_contour,
    apply_edit_record,
    apply_edit_excavation_diagnosis,
    apply_delete_excavation_diagnosis,
    apply_edit_tunnel_contour_info,
    apply_delete_over_under_excavation_calculation,
    edit_modified_pending_record,
    delete_modified_pending_record,
    edit_modified_pending_excavation_diagnosis,
    edit_modified_pending_over_under_excavation,
    edit_modified_pending_tunnel_contour,
    delete_modified_pending_tunnel_contour,
    delete_modified_pending_excavation_diagnosis,
    delete_modified_pending_over_under_excavation,
    cancel_delete_pending_excavation_diagnosis,
    cancel_delete_pending_over_under_excavation,
    cancel_delete_pending_tunnel_contour,
    reapply_record,
    reapply_excavation_diagnosis,
    reapply_tunnel_contour,
    view_GeologicalSketchRecord,
    view_ExcavationDiagnosis,
    view_OverUnderExcavation,
)


urlpatterns = [
    #这四个是拆开的个人中心（掌子面，超欠挖计算，，超欠挖诊断，隧道）
    path('geological-records/', user_records_view, name='user_records_view'),  # 掌子面用户记录页面（掌子面个人中心）
    path('excavation-calculation-records/', excavation_calculation_records_view, name='excavation_calculation_records'),# 超欠挖计算记录
    path('excavation-diagnosis-records/', excavation_diagnosis_records_view, name='excavation_diagnosis_records'),# 超欠挖诊断记录
    path('tunnel-contour-records/', tunnel_contour_records_view, name='tunnel_contour_records'),# 隧道轮廓记录

    #用户修改，删除自己的新增待审批信息
    path('records/edit/<int:record_id>/', edit_pending_record, name='edit_pending_record'),# 用户修改自己的掌子面待审批记录
    path('records/delete/<int:record_id>/', delete_pending_record, name='delete_pending_record'),# 用户删除自己的掌子面待审批记录
    path('edit/pending/excavation/<int:record_id>/', edit_pending_excavation_diagnosis, name='edit_pending_excavation_diagnosis'),
    path('edit/pending/overunder/<int:record_id>/', edit_pending_over_under_excavation, name='edit_pending_over_under_excavation'),
    path('edit/pending/tunnel/<int:record_id>/', edit_pending_tunnel_contour, name='edit_pending_tunnel_contour'),
    path('delete/pending/excavation/<int:record_id>/', delete_pending_excavation_diagnosis, name='delete_pending_excavation_diagnosis'),
    path('delete/pending/overunder/<int:record_id>/', delete_pending_over_under_excavation, name='delete_pending_over_under_excavation'),
    path('delete/pending/tunnel/<int:record_id>/', delete_pending_tunnel_contour, name='delete_pending_tunnel_contour'),

    #这八个是四张表（掌子面，超欠挖计算，诊断，隧道）的已审批信息的修改，删除的申请
    path('records/apply_edit/<int:record_id>/', apply_edit_record, name='apply_edit_record'),# （掌子面）用户对已审批通过的记录申请修改，提交管理员审批
    path('records/apply_delete/<int:record_id>/', apply_delete_record, name='apply_delete_record'),# 用户对已审批通过的记录申请删除，提交管理员审批
    path('apply_edit_excavation_diagnosis/<int:record_id>/', apply_edit_excavation_diagnosis, name='apply_edit_excavation_diagnosis'),# 申请修改超欠挖诊断记录
    path('apply_delete_excavation_diagnosis/<int:record_id>/', apply_delete_excavation_diagnosis, name='apply_delete_excavation_diagnosis'),# 申请删除超欠挖诊断记录
    path('apply_edit_over_under_excavation_calculation/<int:record_id>/', apply_edit_over_under_excavation_calculation, name='apply_edit_over_under_excavation_calculation'),# 申请修改超欠挖计算记录
    path('apply_delete_over_under_excavation_calculation/<int:record_id>/', apply_delete_over_under_excavation_calculation, name='apply_delete_over_under_excavation_calculation'),# 申请删除超欠挖计算记录
    path('apply_edit_tunnel_contour_info/<int:record_id>/', apply_edit_tunnel_contour_info, name='apply_edit_tunnel_contour_info'),# 申请修改隧道轮廓信息记录
    path('apply_delete_tunnel_contour_info/<int:record_id>/', apply_delete_tunnel_contour_info, name='apply_delete_tunnel_contour_info'),# 申请删除隧道轮廓信息记录

    #修改，删除“修改待审批”信息
    path('records/edit_modified/<int:record_id>/', edit_modified_pending_record, name='edit_modified_pending_record'),# 修改待审批的记录(掌子面）
    path('records/delete_modified/<int:record_id>/', delete_modified_pending_record, name='delete_modified_pending_record'),# 删除修改待审批的记录（掌子面）
    path('edit/modified/excavation/<int:record_id>/', edit_modified_pending_excavation_diagnosis, name='edit_modified_pending_excavation_diagnosis'),
    path('edit/modified/overunder/<int:record_id>/', edit_modified_pending_over_under_excavation, name='edit_modified_pending_over_under_excavation'),
    path('edit/modified/tunnel/<int:record_id>/', edit_modified_pending_tunnel_contour, name='edit_modified_pending_tunnel_contour'),
    path('delete/modified/excavation/<int:record_id>/', delete_modified_pending_excavation_diagnosis, name='delete_modified_pending_excavation_diagnosis'),
    path('delete/modified/overunder/<int:record_id>/', delete_modified_pending_over_under_excavation, name='delete_modified_pending_over_under_excavation'),
    path('delete/modified/tunnel/<int:record_id>/', delete_modified_pending_tunnel_contour, name='delete_modified_pending_tunnel_contour'),

    # 删除“删除待审批记录”（取消删除申请）
    path('records/delete_deleted/<int:record_id>/', delete_deleted_pending_record, name='delete_deleted_pending_record'),
    path('cancel/delete/excavation/<int:record_id>/', cancel_delete_pending_excavation_diagnosis, name='cancel_delete_pending_excavation_diagnosis'),
    path('cancel/delete/overunder/<int:record_id>/', cancel_delete_pending_over_under_excavation, name='cancel_delete_pending_over_under_excavation'),
    path('cancel/delete/tunnel/<int:record_id>/', cancel_delete_pending_tunnel_contour, name='cancel_delete_pending_tunnel_contour'),

    #下面四个是重新申请的
    path('records/reapply/<int:record_id>/', reapply_record, name='edit_record'),#用户重新申请被驳回的掌子面信息
    path('excavation-diagnosis/reapply/<int:record_id>/', reapply_excavation_diagnosis, name='reapply_excavation_diagnosis'),
    path('over-under-calculation/reapply/<int:record_id>/', reapply_over_under_calculation, name='reapply_over_under_calculation'),
    path('tunnel-contour/reapply/<int:record_id>/', reapply_tunnel_contour, name='reapply_tunnel_contour'),

    #下面四个是个人中心中查看详细信息的
    path('view-geological/<int:record_id>/', view_GeologicalSketchRecord, name='view_GeologicalSketchRecord'), #掌子面
    path('view-excavation-diagnosis/<int:record_id>/', view_ExcavationDiagnosis, name='view_ExcavationDiagnosis'), # 超欠挖诊断
    path('view-over-under-excavation/<int:record_id>/', view_OverUnderExcavation, name='view_OverUnderExcavation'),    # 超欠挖计算
    path('view-tunnel-contour/<int:record_id>/', view_TunnelContour, name='view_TunnelContour'),    # 隧道轮廓

]