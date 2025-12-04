from django.core.management.base import BaseCommand
from records.models import DataAuditTrail

class Command(BaseCommand):
    help = 'Inspect and display audit logs in the DataAuditTrail table'

    def handle(self, *args, **kwargs):
        # 获取 DataAuditTrail 表的所有记录
        logs = DataAuditTrail.objects.all()

        if not logs:
            self.stdout.write(self.style.SUCCESS('没有找到任何审计日志。'))
            return

        # 输出所有日志
        for log in logs:
            self.stdout.write(
                self.style.SUCCESS(f"Trace ID: {log.trace_id}, "
                                   f"操作类型: {log.operation_type}, "
                                   f"表名称: {log.table_name}, "
                                   f"记录ID: {log.record_id}, "
                                   f"操作时间: {log.operation_time}")
            )
