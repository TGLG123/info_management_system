#用于数据库备份
import os
import base64
import json
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from records.models import (
    GeologicalSketchRecord,
    OverUnderExcavationCalculation,
    ExcavationDiagnosis,
    TunnelContourInfo,
)

# 定义备份目录
BACKUP_DIR = os.path.join(os.getcwd(), "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

import os
import json
from datetime import datetime, date

def backup_table(queryset, table_name):
    """
    备份单张表的数据到 JSON 文件
    :param queryset: 查询集，包含需要备份的数据
    :param table_name: 表名称，用于生成备份文件名
    :return: 包含备份结果的字典
    """
    try:
        # 确保备份目录存在
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)

        # 生成带分隔符的时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 格式：YYYY-MM-DD_HH-MM-SS
        file_path = os.path.join(backup_dir, f"{table_name}_{timestamp}.json")

        # 将查询集转换为字典列表，并处理 `datetime` 和 `date` 类型字段
        #isinstance() 是 Python 内置函数，用于 检查变量是否属于某个特定类型。
        def convert_datetime(obj):
            if isinstance(obj, (datetime, date)): #
                return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj, datetime) else obj.strftime("%Y-%m-%d")
            if isinstance(obj, bytes):  # 新增对二进制字段的处理
                return base64.b64encode(obj).decode('utf-8')  # 转换为 Base64 字符串
            raise TypeError(f"Type {type(obj)} not serializable")

        data = list(queryset.values())  # 查询集转换为列表字典格式

        # 写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=convert_datetime)

        # 打印备份结果（用于调试）
        print(f"表 {table_name} 备份完成，文件路径：{file_path}")

        # 返回备份成功信息
        return {
            "status": "success",
            "message": f"表 {table_name} 备份成功",
            "file": file_path
        }
    except Exception as e:
        # 捕获异常并返回错误信息
        error_message = f"表 {table_name} 备份失败：{str(e)}"
        print(error_message)
        return {
            "status": "error",
            "message": error_message
        }


def backup_all_tables():
    """
    备份所有表的数据，输出备份状态和每张表的备份结果
    :return: 包含备份状态和备份文件列表的字典
    """
    try:
        # 定义需要备份的表
        tables = [
            {
                "queryset": GeologicalSketchRecord.objects.all(),
                "name": "GeologicalSketchRecord",
            },
            {
                "queryset": OverUnderExcavationCalculation.objects.all(),
                "name": "OverUnderExcavationCalculation",
            },
            {
                "queryset": ExcavationDiagnosis.objects.all(),
                "name": "ExcavationDiagnosis",
            },
            {
                "queryset": TunnelContourInfo.objects.all(),
                "name": "TunnelContourInfo",
            },
        ]

        backup_files = []  # 用于存储备份文件路径
        for table in tables:
            print(f"开始备份表 {table['name']}...")
            backup_file = backup_table(table["queryset"], table["name"])
            backup_files.append(backup_file)
            print(f"表 {table['name']} 备份完成，文件路径：{backup_file}")

        print("所有表备份成功！备份文件列表如下：")
        for file in backup_files:
            print(file)

        return {"status": "success", "message": "所有表备份成功！", "files": backup_files}
    except Exception as e:
        error_message = f"备份失败：{str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}
