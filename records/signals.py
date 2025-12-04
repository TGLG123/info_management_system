from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict
from utils.thread_local import get_current_request
from .models import GeologicalSketchRecord,OverUnderExcavationCalculation,ExcavationDiagnosis,TunnelContourInfo,DataAuditTrail
from uuid import uuid4
import json
from datetime import datetime, date
from django.db.models import Max
from django.apps import apps

def json_serial(obj):
    """JSON 序列化辅助函数"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# 新增，修改
@receiver(pre_save, sender=OverUnderExcavationCalculation)
@receiver(pre_save, sender=ExcavationDiagnosis)
@receiver(pre_save, sender=TunnelContourInfo)
@receiver(pre_save, sender=GeologicalSketchRecord)
def log_update_or_create(sender, instance, **kwargs):
    print("新增修改信号触发")
    """
    日志记录逻辑：记录 CREATE、UPDATE、DELETE 操作，并在审批操作中记录审批人。
    """
    request = get_current_request()  # 获取当前请求对象
    client_ip = get_client_ip(request) if request else None  # 获取客户端 IP 地址

    # 跳过所有待审批状态（新增、修改、删除）
    if instance.status in ['pending', 'modified_pending', 'deleted_pending']:
        print("跳过")
        return  # 待审批状态的记录不记录日志

    if instance.pk:  # 修改操作（主键存在，说明已经存在这个记录，是修改）
        try:
            print("修改")
            # 获取数据库中原始数据
            original = sender.objects.get(pk=instance.pk)
            original_data = model_to_dict(original)
            updated_data = model_to_dict(instance)

            # 检查状态变更逻辑
            if original.status != instance.status:
                # 用户上传的审批逻辑：从 `pending` → `uploaded_approved`
                if original.status == 'pending' and instance.status == 'uploaded_approved':
                    DataAuditTrail.objects.create(
                        trace_id=str(uuid4()),
                        operation_type="CREATE",  # 用户上传的操作类型
                        table_name=sender._meta.db_table,
                        record_id=instance.pk,
                        user=original.created_by,  # 用户提交者
                        approved_by=instance.approved_by,  # 修改：记录审批人
                        data_snapshot=json.dumps(original_data, default=json_serial),
                        updated_data=json.dumps(updated_data, default=json_serial),
                        change_details=json.dumps({
                            "status": {"old": original.status, "new": instance.status}
                        }, default=json_serial),
                        client_ip=client_ip,
                        operation_reason=getattr(instance, 'operation_reason', "无"),  # 添加操作理由
                        approval_reason=getattr(instance, 'approval_reason', "无"),  # 添加审批理由
                    )

                # 用户修改的审批逻辑：从 `modified_pending` → `modified_approved`
                elif original.status == 'modified_pending' and instance.status == 'modified_approved':
                    DataAuditTrail.objects.create(
                        trace_id=str(uuid4()),
                        operation_type="UPDATE",  # 用户修改的操作类型
                        table_name=sender._meta.db_table,
                        record_id=instance.pk,
                        #user=original.modified_by,  # 用户发起者
                        user=original.created_by,  # 用户发起者
                        approved_by=instance.approved_by,  # 修改：记录审批人
                        data_snapshot=json.dumps(original_data, default=json_serial),
                        updated_data=json.dumps(updated_data, default=json_serial),
                        change_details=json.dumps({
                            "status": {"old": original.status, "new": instance.status}
                        }, default=json_serial),
                        client_ip=client_ip,
                        operation_reason=getattr(instance, 'operation_reason', "无"),  # 添加操作理由
                        approval_reason=getattr(instance, 'approval_reason', "无"),  # 添加审批理由
                    )

                # 用户删除的审批逻辑：从 `deleted_pending` → `deleted`
                elif original.status == 'deleted_pending' and instance.status == 'deleted':
                    DataAuditTrail.objects.create(
                        trace_id=str(uuid4()),
                        operation_type="DELETE",  # 用户删除的操作类型
                        table_name=sender._meta.db_table,
                        record_id=instance.pk,
                        #user=original.deleted_by,  # 用户发起者
                        user=original.created_by,  # 用户发起者
                        approved_by=instance.approved_by,  # 修改：记录审批人
                        data_snapshot=json.dumps(original_data, default=json_serial),
                        client_ip=client_ip,
                        operation_reason=getattr(instance, 'operation_reason', "无"),  # 添加操作理由
                        approval_reason=getattr(instance, 'approval_reason', "无"),  # 添加审批理由
                    )

            else:
                # 普通修改操作（非状态变更）
                change_details = {
                    field: {"old": original_data[field], "new": updated_data[field]}
                    for field in original_data
                    if original_data[field] != updated_data[field]
                }
                if change_details:
                    DataAuditTrail.objects.create(
                        trace_id=str(uuid4()),
                        operation_type="UPDATE",  # 普通修改操作
                        table_name=sender._meta.db_table,
                        record_id=instance.pk,
                        user=instance.modified_by,  # 修改的用户
                        data_snapshot=json.dumps(original_data, default=json_serial),
                        updated_data=json.dumps(updated_data, default=json_serial),
                        change_details=json.dumps(change_details, default=json_serial),
                        client_ip=client_ip,
                        operation_reason=getattr(instance, 'operation_reason', "无"),  # 添加操作理由
                        approval_reason=getattr(instance, 'approval_reason', "无"),  # 添加审批理由
                    )

        except sender.DoesNotExist:
            pass

    else:  # 新增操作
        # 区分管理员和用户的新增操作
        if instance.status == 'pending':  # 用户新增（未审批）
            print("用户新增")
            # 暂时不记录日志，待审批时记录
            pass
        else:  # 管理员直接新增
            # 动态获取模型
            table_name=sender._meta.db_table
            mymodel = apps.get_model(app_label=table_name.split('_')[0], model_name=table_name.split('_')[1])
            # 获取当前表的最大 ID，并推测下一个 ID
            print(mymodel)
            max_id = mymodel.objects.aggregate(Max('id'))['id__max']
            next_id = (max_id or 0) + 1
            print("管理员新增")
            DataAuditTrail.objects.create(
                trace_id=str(uuid4()),
                operation_type="CREATE",  # 管理员直接新增
                table_name=sender._meta.db_table,
                #record_id=instance.pk,
                record_id=next_id,
                user=instance.created_by,  # 创建人（管理员）
                updated_data=json.dumps(model_to_dict(instance), default=json_serial),
                client_ip=client_ip,
                operation_reason=getattr(instance, 'operation_reason', "无"),  # 添加操作理由
                approval_reason=getattr(instance, 'approval_reason', "无"),  # 添加审批理由
            )



#这个是不带区块链的正确删除
# @receiver(post_delete, sender=OverUnderExcavationCalculation)
# @receiver(post_delete, sender=ExcavationDiagnosis)
# @receiver(post_delete, sender=TunnelContourInfo)
# @receiver(post_delete, sender=GeologicalSketchRecord)
# def log_delete(sender, instance, **kwargs):
#     print("删除触发")
#     """
#     删除记录日志逻辑：
#     - 管理员直接删除：记录日志
#     - 用户删除申请（待审批删除）：不记录日志
#     - 管理员审批用户的删除申请：记录日志
#     """
#     request = get_current_request()  # 从线程安全存储中获取当前请求对象
#     client_ip = get_client_ip(request) if request else None  # 获取客户端 IP 地址
#
#     # 跳过待审批删除的记录（包括三种待审批状态）
#     if instance.status in ['deleted_pending', 'pending', 'modified_pending']:
#         print("这里的问题")
#         return  # 不记录日志
#
#     # 如果是管理员直接删除或者管理员审批后的删除
#     DataAuditTrail.objects.create(
#         trace_id=str(uuid4()),
#         operation_type="DELETE",  # 操作类型为 DELETE
#         table_name=sender._meta.db_table,
#         record_id=instance.pk,
#         user=instance.deleted_by if instance.deleted_by else instance.created_by,  # 删除者
#         data_snapshot=json.dumps(model_to_dict(instance), default=json_serial),  # 被删除的数据快照
#         client_ip=client_ip,  # 保存客户端 IP 地址
#     )
#     print("完整触发删除信号")


@receiver(post_delete, sender=OverUnderExcavationCalculation)
@receiver(post_delete, sender=ExcavationDiagnosis)
@receiver(post_delete, sender=TunnelContourInfo)
@receiver(post_delete, sender=GeologicalSketchRecord)
def log_delete(sender, instance, **kwargs):
    print("删除触发")
    """
    删除记录日志逻辑：
    - 管理员直接删除：记录日志
    - 用户删除申请（待审批删除）：不记录日志
    - 管理员审批用户的删除申请：记录日志
    """
    request = get_current_request()  # 从线程安全存储中获取当前请求对象
    client_ip = get_client_ip(request) if request else None  # 获取客户端 IP 地址

    # 跳过待审批删除的记录（包括三种待审批状态）
    if instance.status in ['deleted_pending', 'pending', 'modified_pending']:
        print("这里的问题")
        return  # 不记录日志

    # 获取操作理由和审批理由
    operation_reason = getattr(instance, 'operation_reason', "无")  # 获取操作理由，默认 "无"
    print(operation_reason)
    approval_reason = getattr(instance, 'approval_reason', "无")  # 获取审批理由，默认 "无"
    print(approval_reason)

    # 如果是管理员直接删除或者管理员审批后的删除
    DataAuditTrail.objects.create(
        trace_id=str(uuid4()),
        operation_type="DELETE",  # 操作类型为 DELETE
        table_name=sender._meta.db_table,
        record_id=instance.pk,
        user=instance.deleted_by if instance.deleted_by else instance.created_by,  # 删除者
        data_snapshot=json.dumps(model_to_dict(instance), default=json_serial),  # 被删除的数据快照
        client_ip=client_ip,  # 保存客户端 IP 地址
        operation_reason=operation_reason,  # 记录操作理由
        approval_reason=approval_reason,  # 记录审批理由
    )
    print("完整触发删除信号")




# from .blockchain_config import web3, ACCOUNT_ADDRESS, PRIVATE_KEY
# #带区块链的删除
# @receiver(post_delete, sender=OverUnderExcavationCalculation)
# @receiver(post_delete, sender=ExcavationDiagnosis)
# @receiver(post_delete, sender=TunnelContourInfo)
# @receiver(post_delete, sender=GeologicalSketchRecord)
# def log_delete(sender, instance, **kwargs):
#     print("删除触发")
#
#     """
#     删除记录日志逻辑：
#     - 管理员直接删除：记录日志
#     - 用户删除申请（待审批删除）：不记录日志
#     - 管理员审批用户的删除申请：记录日志
#     """
#     try:
#         request = get_current_request()  # 从线程安全存储中获取当前请求对象
#         client_ip = get_client_ip(request) if request else None  # 获取客户端 IP 地址
#
#         # 跳过待审批删除的记录（包括三种待审批状态）
#         if instance.status in ['deleted_pending', 'pending', 'modified_pending']:
#             print("跳过待审批状态记录")
#             return  # 不记录日志
#
#         # 生成日志记录
#         trace_id = str(uuid4())
#         operation_type = "DELETE"
#         table_name = sender._meta.db_table
#         record_id = instance.pk
#         user = instance.deleted_by if instance.deleted_by else instance.created_by
#
#         # 存储到本地日志表（如果需要）
#         DataAuditTrail.objects.create(
#             trace_id=trace_id,
#             operation_type=operation_type,
#             table_name=table_name,
#             record_id=record_id,
#             user=user,
#             data_snapshot=json.dumps(model_to_dict(instance), default=str),  # 快照暂时不存到区块链
#             client_ip=client_ip,
#         )
#
#         # 存储关键信息到区块链
#         blockchain_data = {
#             "trace_id": trace_id,
#             "operation_type": operation_type,
#             "table_name": table_name,
#             "record_id": record_id,
#             "user": str(user),
#         }
#
#         # 将数据编码为 JSON 字符串并转为 Hex 格式
#         encoded_data = web3.toHex(text=json.dumps(blockchain_data))
#
#         # 构造交易
#         transaction = {
#             "from": ACCOUNT_ADDRESS,
#             "to": ACCOUNT_ADDRESS,  # 如果你有智能合约地址，也可以替换为合约地址
#             "value": 0,
#             "gas": 21000,  # 根据数据大小调整 Gas
#             "gasPrice": web3.toWei("1", "gwei"),
#             "data": encoded_data,
#             "nonce": web3.eth.getTransactionCount(ACCOUNT_ADDRESS),
#         }
#
#         # 签名交易
#         signed_tx = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
#
#         # 发送交易到区块链
#         tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#
#         # 打印交易哈希，用于调试
#         print(f"存储到区块链的交易哈希: {tx_hash.hex()}")
#
#     except Exception as e:
#         print(f"在处理 post_delete 信号时发生错误: {e}")






# from .blockchain_config import send_to_blockchain
# #带区块链的版本2
# @receiver(post_delete, sender=OverUnderExcavationCalculation)
# @receiver(post_delete, sender=ExcavationDiagnosis)
# @receiver(post_delete, sender=TunnelContourInfo)
# @receiver(post_delete, sender=GeologicalSketchRecord)
# def log_delete(sender, instance, **kwargs):
#     print("删除触发")
#     try:
#         # 从线程安全存储中获取请求对象和 IP 地址
#         request = get_current_request()
#         client_ip = get_client_ip(request) if request else None
#
#         # 跳过待审批状态的记录
#         if hasattr(instance, 'status') and instance.status in ['deleted_pending', 'pending', 'modified_pending']:
#             print("跳过待审批状态记录")
#             return
#
#         # 生成关键信息
#         trace_id = str(uuid4())
#         operation_type = "DELETE"
#         table_name = sender._meta.db_table
#         record_id = instance.pk
#         user = instance.deleted_by if hasattr(instance, 'deleted_by') else instance.created_by
#
#         # 存储到本地日志表
#         DataAuditTrail.objects.create(
#             trace_id=trace_id,
#             operation_type=operation_type,
#             table_name=table_name,
#             record_id=record_id,
#             user=user,
#             data_snapshot=json.dumps(model_to_dict(instance), default=str),
#             client_ip=client_ip,
#         )
#
#         # 准备区块链存储的数据
#         blockchain_data = {
#             "trace_id": trace_id,
#             "operation_type": operation_type,
#             "table_name": table_name,
#             "record_id": record_id,
#             "user": str(user),
#         }
#
#         # 将数据发送到区块链
#         tx_hash = send_to_blockchain(json.dumps(blockchain_data))
#         if tx_hash:
#             print(f"数据已存储到区块链，交易哈希: {tx_hash}")
#         else:pyt
#             print("存储到区块链失败")
#     except Exception as e:
#         print(f"处理删除日志时出错: {e}")