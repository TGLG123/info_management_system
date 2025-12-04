import base64
import os
import json
from django.db import models


from django.db.models.signals import pre_delete, post_delete
from django.db.models.signals import pre_delete, post_save

from records.models import (
    GeologicalSketchRecordBackup,
    OverUnderExcavationCalculationBackup,
    ExcavationDiagnosisBackup,
    TunnelContourInfoBackup, TunnelContourInfo,
)
from records.signals import log_delete, log_update_or_create

BACKUP_DIR = os.path.join(os.getcwd(), "backups")

def get_backup_files():
    """
    获取备份目录中的所有 JSON 文件
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    return [f for f in os.listdir(BACKUP_DIR) if f.endswith(".json")]


# 下面是可以屏蔽信号的版本，如果想不屏蔽信号，删除try的前两句和finally就行
# 根据json文件恢复单个表（会删除存取恢复数据的表里面之前的内容，然后根据json文件进行恢复）
def restore_table_from_backup(file_path, model_class):
    """
    根据备份文件恢复指定的表数据
    """
    try:
        # 临时断开信号
        pre_delete.disconnect(receiver=log_delete, sender=model_class)  # 屏蔽删除日志
        post_save.disconnect(receiver=log_update_or_create, sender=model_class)  # 屏蔽保存或更新日志

        # 检查是否断开成功
        if not pre_delete.has_listeners(model_class):
            print("pre_delete 信号已成功断开")
        else:
            print("pre_delete 信号断开失败")
        if not post_save.has_listeners(model_class):
            print("post_save 信号已成功断开")
        else:
            print("post_save 信号断开失败")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 获取模型字段名
        model_fields = [field.name for field in model_class._meta.get_fields()]

        # 获取外键字段映射
        foreign_key_fields = {
            field.attname: field.name
            for field in model_class._meta.get_fields() if field.is_relation
        }

        # 清空目标表中的所有数据
        model_class.objects.all().delete()
        print("信号屏蔽失败")

        # 恢复数据
        for record in data:
            # 过滤无效字段
            valid_data = {key: value for key, value in record.items() if key in model_fields or key in foreign_key_fields}

            # 特殊字段处理：二进制字段
            for key, value in valid_data.items():
                if isinstance(model_class._meta.get_field(key), models.BinaryField):  # 检查是否是 BinaryField
                    if value is not None:  # 跳过空值
                        valid_data[key] = base64.b64decode(value)  # 解码 Base64 数据

            # 外键字段处理
            for attname, field_name in foreign_key_fields.items():
                if attname in valid_data:
                    # 跳过 None 值的外键字段
                    if valid_data[attname] is None:
                        valid_data[field_name] = None
                        continue

                    # 转换外键 ID 为模型实例
                    related_model = model_class._meta.get_field(field_name).related_model
                    valid_data[field_name] = related_model.objects.get(pk=valid_data[attname])
                    # 移除 _id 字段
                    valid_data.pop(attname)

            # 插入数据
            model_class.objects.create(**valid_data)

        print("恢复成功")
        return {"status": "success", "message": f"{model_class.__name__} 恢复成功"}
    except Exception as e:
        return {"status": "error", "message": f"恢复 {model_class.__name__} 时发生错误：{str(e)}"}
    finally:
        # 恢复信号
        pre_delete.connect(receiver=log_delete, sender=model_class)
        post_save.connect(receiver=log_update_or_create, sender=model_class)




def restore_all_tables(file_name):
    """
    恢复所有表的数据
    """
    file_path = os.path.join(BACKUP_DIR, file_name)
    if not os.path.exists(file_path):
        return {"status": "error", "message": "备份文件不存在"}

    tables = [
        (file_path, GeologicalSketchRecordBackup),
        (file_path, OverUnderExcavationCalculationBackup),
        (file_path, ExcavationDiagnosisBackup),
        (file_path, TunnelContourInfoBackup),
    ]

    results = []
    for table_file, model_class in tables:
        result = restore_table_from_backup(file_path, model_class)
        results.append(result)

    if all(res["status"] == "success" for res in results):
        return {"status": "success", "message": "所有表恢复成功"}
    else:
        error_messages = [res["message"] for res in results if res["status"] == "error"]
        return {"status": "error", "message": "部分表恢复失败", "details": error_messages}
