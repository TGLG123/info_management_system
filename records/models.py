import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
import json
from simple_history.models import HistoricalRecords

# 用户模型，自带用户名，密码，邮箱等
class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),      # 管理员
        ('user', 'User'),        # 普通用户
        ('auditor', 'Auditor'),  # 审计员
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user',
        help_text="用户角色：admin 为管理员，user 为普通用户，auditor 为审计员"
    )
    registration_date = models.DateTimeField(auto_now_add=True, help_text="用户注册时间")

    def is_admin(self):
        """判断用户是否为管理员"""
        return self.role == 'admin'

    def is_user(self):
        """判断用户是否为普通用户"""
        return self.role == 'user'

    def is_auditor(self):
        """判断用户是否为审计员"""
        return self.role == 'auditor'

    def __str__(self):
        """返回用户的友好名称，显示用户名和角色"""
        return f"{self.username} ({self.get_role_display()})"

#掌子面
class GeologicalSketchRecord(models.Model):
    """
    模型描述：用于记录掌子面的地质数据，包括地质特性、施工情况和相关人员信息。
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")  # 记录检查的时间
    distance = models.FloatField(help_text="里程")  # 掌子面的里程位置
    design_section = models.FloatField(help_text="设计断面")  # 设计断面的数据
    inspector = models.CharField(max_length=100, help_text="测量人员")  # 测量人员姓名
    measurement_date = models.DateField(help_text="测量日期")  # 测量时间

    # 掌子面数据
    excavation_width = models.FloatField(help_text="开挖宽度")  # 开挖宽度
    excavation_height = models.FloatField(help_text="开挖高度")  # 开挖高度
    excavation_area = models.FloatField(help_text="开挖面积")  # 开挖面积
    excavation_method = models.CharField(max_length=200, help_text="开挖方式")  # 开挖方式
    face_condition = models.CharField(max_length=100, help_text="掌子面状态")  # 掌子面状态
    excavation_condition = models.CharField(max_length=100, help_text="毛开挖情况")  # 毛开挖情况
    rock_strength = models.CharField(max_length=50, help_text="岩石强度")  # 岩石强度
    weathering_degree = models.CharField(max_length=50, help_text="风化程度")  # 风化程度
    crack_width = models.CharField(max_length=50, help_text="裂缝宽度")  # 裂缝宽度
    crack_shape = models.CharField(max_length=50, help_text="裂缝形态")  # 裂缝形态
    water_condition = models.CharField(max_length=100, help_text="渗水状态")  # 渗水情况
    rockburst_tendency = models.CharField(max_length=50, help_text="岩爆发育程度")  # 岩爆发育程度
    rock_grade = models.CharField(max_length=10, help_text="岩层级别")  # 岩层级别

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")  # 唯一标识掌子面
    project_id = models.CharField(max_length=50, help_text="施工项目编号")  # 唯一标识施工项目
    created_by = models.ForeignKey(
        User,
        related_name='created_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录创建者"
    )  # 创建数据的用户
    modified_by = models.ForeignKey(
        User,
        related_name='modified_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录修改者"
    )  # 修改数据的用户
    deleted_by = models.ForeignKey(
        User,
        related_name='deleted_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录删除者"
    )  # 删除数据的用户

    # **新增字段：审批流程相关字段**
    STATUS_CHOICES = [
        ('pending', '待审批'),                # 数据待管理员审批
        ('uploaded_approved', '上传已审批'),  # 上传后审批通过
        ('modified_pending', '修改待审批'),   # 修改后待审批
        ('modified_approved', '修改已审批'),  # 修改后审批通过
        ('deleted_pending', '删除待审批'),    # 删除请求待审批
        ('deleted', '已删除'),                # 已被批准删除
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )  # 新增字段：用于标识记录的审批状态

    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="用户发起操作时填写的理由（上传、修改或删除）"
    )  # 新增字段：用户发起操作时提供的理由

    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )  # 新增字段：管理员审批时提供的理由

    approved_by = models.ForeignKey(
        User,
        related_name='approved_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录审批的管理员"
    )  # 新增字段：审批操作的管理员

    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="记录被审批的时间"
    )  # 新增字段：审批通过的时间

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="记录的创建时间"
    )  # 记录的创建时间
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="记录的最后更新时间"
    )  # 记录的最后更新时间

    #下面是新增的
    karst_development = models.CharField(
        max_length=50,
        help_text="岩溶发育程度",
        blank=True,
        null=True
    )  # 新增字段：岩溶发育程度，页面1特有

    water_status = models.CharField(
        max_length=100,
        help_text="消水状态",
        blank=True,
        null=True
    )  # 新增字段：消水状态，页面1特有

    history = HistoricalRecords()  # 添加历史记录

    def __str__(self):
        """
        自定义模型字符串表示，便于管理后台显示。
        """
        return f"{self.inspection_date} - {self.face_id} - {self.inspector} - {self.get_status_display()}"


#超欠挖诊断
class ExcavationDiagnosis(models.Model):
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")  # 检查日期
    inspector = models.CharField(max_length=100, help_text="测量人员")  # 测量人员姓名
    measurement_date = models.DateField(help_text="测量日期")  # 测量时间

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")  # 唯一标识超欠挖诊断
    project_id = models.CharField(max_length=50, help_text="施工项目编号")  # 唯一标识施工项目
    created_by = models.ForeignKey(
        User,
        related_name='created_excavation_diagnoses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录创建者"
    )  # 创建数据的用户
    modified_by = models.ForeignKey(
        User,
        related_name='modified_excavation_diagnoses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录修改者"
    )  # 修改数据的用户
    deleted_by = models.ForeignKey(
        User,
        related_name='deleted_excavation_diagnoses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录删除者"
    )  # 删除数据的用户

    # 状态字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="用户发起操作时填写的理由（上传、修改或删除）"
    )
    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )
    approved_by = models.ForeignKey(
        User,
        related_name='approved_excavation_diagnoses',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录审批的管理员"
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="记录被审批的时间"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="记录的创建时间"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="记录的最后更新时间"
    )

    # 超欠挖诊断数据字段
    scale = models.FloatField(help_text="比例尺")  # 比例尺
    mileage = models.FloatField(help_text="里程")  # 里程
    design_section = models.FloatField(help_text="设计断面")  # 设计断面
    line_x = models.FloatField(help_text="线路X坐标")  # 线路X坐标
    line_y = models.FloatField(help_text="线路Y坐标")  # 线路Y坐标
    measured_section = models.FloatField(help_text="实测断面面积")  # 实测断面面积
    reference_section = models.FloatField(help_text="参考断面面积")  # 参考断面面积
    line_height = models.FloatField(help_text="线路高程")  # 线路高程
    over_excavation_area = models.FloatField(help_text="超挖面积")  # 超挖面积
    under_excavation_area = models.FloatField(help_text="欠挖面积")  # 欠挖面积
    max_over_excavation = models.FloatField(help_text="最大超挖")  # 最大超挖
    max_under_excavation = models.FloatField(help_text="最大欠挖")  # 最大欠挖
    average_over_excavation = models.FloatField(help_text="平均超挖")  # 平均超挖
    average_under_excavation = models.FloatField(help_text="平均欠挖")  # 平均欠挖

    # 可选的诊断结果字段
    DIAGNOSIS_RESULT_CHOICES = [
        ('within_limits', '超欠挖合格'),
        ('exceeds_limits', '超欠挖超标'),
    ]
    diagnosis_result = models.CharField(
        max_length=20,
        choices=DIAGNOSIS_RESULT_CHOICES,
        default='within_limits',
        help_text="诊断结果"
    )

    history = HistoricalRecords()  # 添加历史记录

    def __str__(self):
        return f"{self.face_id} - {self.mileage} - {self.get_status_display()} - {self.diagnosis_result}"


#超欠挖计算
class OverUnderExcavationCalculation(models.Model):
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")  # 检查日期
    inspector = models.CharField(max_length=100, help_text="测量人员")  # 测量人员
    measurement_date = models.DateField(help_text="测量日期")  # 测量日期

    # 线路定线表数据
    line_name = models.CharField(max_length=200, help_text="线路名称")  # 线路名称
    north_direction_angle = models.FloatField(help_text="北方向角")  # 北方向角
    radius = models.FloatField(help_text="半径")  # 半径
    length = models.FloatField(help_text="长度")  # 长度
    east_coordinate = models.FloatField(help_text="东坐标")  # 东坐标
    north_coordinate = models.FloatField(help_text="北坐标")  # 北坐标

    # 横截面表数据
    start_offset = models.FloatField(help_text="起点偏移")  # 起点偏移
    height = models.FloatField(help_text="高度")  # 高度
    radius_section = models.FloatField(help_text="横截面半径")  # 半径
    angle_increment = models.FloatField(help_text="角度增量")  # 角度增量

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")  # 超欠挖计算编号
    project_id = models.CharField(max_length=50, help_text="施工项目编号")  # 施工项目编号
    created_by = models.ForeignKey(
        User,
        related_name='created_over_under_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录创建者"
    )
    modified_by = models.ForeignKey(
        User,
        related_name='modified_over_under_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录修改者"
    )
    deleted_by = models.ForeignKey(
        User,
        related_name='deleted_over_under_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录删除者"
    )

    # 审批流程相关字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="用户发起操作时填写的理由（上传、修改或删除）"
    )
    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )
    approved_by = models.ForeignKey(
        User,
        related_name='approved_over_under_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录审批的管理员"
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="记录被审批的时间"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="记录的创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="记录的最后更新时间")

    history = HistoricalRecords()  # 添加历史记录

    def __str__(self):
        return f"{self.line_name} - {self.inspection_date}"


#隧道
class TunnelContourInfo(models.Model):
    """
    隧道轮廓信息模型
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")  # 检查日期
    inspector = models.CharField(max_length=100, help_text="测量人员")  # 测量人员
    measurement_date = models.DateField(help_text="测量日期")  # 测量日期

    # 隧道轮廓参数
    cr = models.FloatField(help_text="调整指数范围的常数 Cr")  # Cr
    w1 = models.FloatField(help_text="权重值 w1")  # 权重 w1
    w2 = models.FloatField(help_text="权重值 w2")  # 权重 w2
    w3 = models.FloatField(help_text="权重值 w3")  # 权重 w3
    od = models.FloatField(help_text="超挖深度 Od")  # Od
    rcl = models.FloatField(help_text="轮廓粗糙度 RCL")  # RCL
    vo = models.FloatField(help_text="纵向超挖变化 Vo")  # Vo
    c1 = models.FloatField(help_text="修正因子 c1")  # 修正因子 c1
    c2 = models.FloatField(help_text="修正因子 c2")  # 修正因子 c2
    c3 = models.FloatField(help_text="修正因子 c3")  # 修正因子 c3

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")  # 掌子面编号
    project_id = models.CharField(max_length=50, help_text="施工项目编号")  # 施工项目编号
    created_by = models.ForeignKey(
        User,
        related_name='created_tunnel_contour_records', #created_by 外鍵
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录创建者"
    )
    modified_by = models.ForeignKey(
        User,
        related_name='modified_tunnel_contour_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录修改者"
    )
    deleted_by = models.ForeignKey(
        User,
        related_name='deleted_tunnel_contour_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录删除者"
    )

    # 审批流程相关字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="用户发起操作时填写的理由（上传、修改或删除）"
    )
    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )
    approved_by = models.ForeignKey(
        User,
        related_name='approved_tunnel_contour_records',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="记录审批的管理员"
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="记录被审批的时间"
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="记录的创建时间")
    updated_at = models.DateTimeField(auto_now=True, help_text="记录的最后更新时间")

    history = HistoricalRecords()  # 添加历史记录

    def __str__(self):
        return f"{self.face_id} - {self.project_id} - {self.inspection_date}"


#自定义日志记录
class DataAuditTrail(models.Model):
    """
    日志记录模型，用于记录用户的增删改操作，包括审批流程。
    """
    # 基本操作信息
    trace_id = models.CharField(
        max_length=64,
        unique=True,
        default=uuid.uuid4,
        help_text="唯一追踪ID，用于标识操作"
    )
    operation_type = models.CharField(
        max_length=10,
        choices=[('CREATE', 'Create'), ('UPDATE', 'Update'), ('DELETE', 'Delete')],
        help_text="操作类型"
    )
    table_name = models.CharField(max_length=255, help_text="操作的表名称")
    record_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="被操作记录的主键ID"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='operation_user',
        help_text="发起操作的用户"
    )
    operation_time = models.DateTimeField(
        auto_now_add=True,
        help_text="操作时间"
    )
    # 数据快照和变更详情
    data_snapshot = models.TextField(
        help_text="操作前或删除的数据快照，JSON格式存储"
    )
    updated_data = models.TextField(
        blank=True,
        null=True,
        help_text="操作后的数据（针对UPDATE和CREATE操作，JSON格式）"
    )
    change_details = models.TextField(
        blank=True,
        null=True,
        help_text="字段级数据变更详情（针对UPDATE操作，JSON格式）"
    )
    # 审批信息
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_operations',
        help_text="批准操作的管理员"
    )
    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )
    # 用户操作理由
    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="普通用户发起操作时填写的理由"
    )
    # 附加信息
    client_ip = models.GenericIPAddressField(
        blank=True,
        null=True,
        help_text="客户端IP地址"
    )
    user_agent = models.TextField(
        blank=True,
        null=True,
        help_text="用户的浏览器或客户端信息"
    )

    def __str__(self):
        return f"{self.operation_type} - {self.table_name} - {self.record_id} - {self.operation_time}"





# 映射 MySQL 自带日志的表结构
class MySQLGeneralLog(models.Model):
    event_time = models.DateTimeField(help_text="事件时间")
    user_host = models.CharField(max_length=255, help_text="用户和主机信息")
    thread_id = models.IntegerField(help_text="线程ID")
    server_id = models.IntegerField(help_text="服务器ID")
    command_type = models.CharField(max_length=64, help_text="命令类型，例如 QUERY、CONNECT")
    argument = models.TextField(help_text="SQL命令或操作内容")

    class Meta:
        managed = False  # 这个表不由 Django 管理，而是直接映射 MySQL 的 general_log 表
        db_table = 'mysql.general_log'

    def __str__(self):
        return f"{self.event_time} - {self.command_type} - {self.argument}"


# 映射 MySQL 二进制日志的表结构（可选）
class MySQLBinLog(models.Model):
    log_name = models.CharField(max_length=255, help_text="日志文件名")
    position = models.BigIntegerField(help_text="日志位置")
    event_time = models.DateTimeField(help_text="事件时间")
    event_type = models.CharField(max_length=50, help_text="事件类型，例如 WRITE_ROWS")
    table_name = models.CharField(max_length=255, help_text="目标表名")
    database_name = models.CharField(max_length=255, help_text="数据库名")
    data = models.TextField(help_text="事件具体数据")

    class Meta:
        managed = False  # 不由 Django 管理，而是映射 MySQL 二进制日志
        db_table = 'mysql.binlog'

    def __str__(self):
        return f"{self.event_time} - {self.event_type} - {self.table_name}"


# 文件上传
class DataStorage(models.Model):
    # 基本文件信息
    file_name = models.CharField(max_length=255, help_text="文件名称")
    file_path = models.CharField(max_length=512, blank=True, null=True, help_text="文件存储路径")
    file_data = models.BinaryField(blank=True, null=True, help_text="文件二进制数据")
    file_type = models.CharField(max_length=100, help_text="文件类型，如PDF、Excel等")  # 文件的具体格式类型
    file_hash = models.CharField(max_length=64, help_text="文件的唯一哈希值，用于防止重复上传")
    upload_date = models.DateTimeField(auto_now_add=True, help_text="文件上传时间")

    # 新增字段：文件描述
    file_description = models.TextField(
        blank=True,
        null=True,
        help_text="文件描述，例如用途或内容简介"
    )

    # 标识字段（与其余四个模型一致）
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="文件当前状态"
    )  # 审批状态

    operation_reason = models.TextField(
        blank=True,
        null=True,
        help_text="用户发起操作时填写的理由（上传、修改或删除）"
    )  # 用户操作的理由

    approval_reason = models.TextField(
        blank=True,
        null=True,
        help_text="管理员审批时填写的理由"
    )  # 审批理由

    approved_by = models.ForeignKey(
        User,
        related_name='approved_files',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="文件审批的管理员"
    )  # 审批操作的管理员

    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="文件被审批的时间"
    )  # 审批通过的时间

    CATEGORY_CHOICES = [
        ('geological', '掌子面'),
        ('excavation_diagnosis', '超欠挖诊断'),
        ('excavation_calculation', '超欠挖计算'),
        ('tunnel', '隧道'),
        ('other', '其他'),
    ]
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="文件所属类别（如掌子面、超欠挖诊断等）"
    )

# 文件与数据记录的关联字段
    related_record_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="关联的记录编号（如掌子面编号或隧道编号）"
    )  # 关联字段，用于链接到相关数据记录

    # 用户操作相关字段
    uploaded_by = models.ForeignKey(
        User,
        related_name='uploaded_files',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="文件上传的用户"
    )  # 上传的用户

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="记录的创建时间"
    )  # 记录的创建时间

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="记录的最后更新时间"
    )  # 记录的最后更新时间

    # 历史记录
    history = HistoricalRecords()

    class Meta:
        db_table = 'data_storage'  # 自定义数据库表名
        verbose_name = "文件存储"
        verbose_name_plural = "文件存储"

    def __str__(self):
        """
        自定义模型字符串表示，便于管理后台显示。
        """
        return f"{self.file_name} ({self.get_data_type_display()}) - {self.get_status_display()}"




#下面的四个是数据库还原的表（四个表分别是四种地址信息的表，用于还原，就是数据库恢复时的数据放置在这个里面）
class GeologicalSketchRecordBackup(models.Model):
    """
    备份表：掌子面数据备份
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")
    distance = models.FloatField(help_text="里程")
    design_section = models.FloatField(help_text="设计断面")
    inspector = models.CharField(max_length=100, help_text="测量人员")
    measurement_date = models.DateField(help_text="测量日期")

    # 掌子面数据
    excavation_width = models.FloatField(help_text="开挖宽度")
    excavation_height = models.FloatField(help_text="开挖高度")
    excavation_area = models.FloatField(help_text="开挖面积")
    excavation_method = models.CharField(max_length=200, help_text="开挖方式")
    face_condition = models.CharField(max_length=100, help_text="掌子面状态")
    excavation_condition = models.CharField(max_length=100, help_text="毛开挖情况")
    rock_strength = models.CharField(max_length=50, help_text="岩石强度")
    weathering_degree = models.CharField(max_length=50, help_text="风化程度")
    crack_width = models.CharField(max_length=50, help_text="裂缝宽度")
    crack_shape = models.CharField(max_length=50, help_text="裂缝形态")
    water_condition = models.CharField(max_length=100, help_text="渗水状态")
    rockburst_tendency = models.CharField(max_length=50, help_text="岩爆发育程度")
    rock_grade = models.CharField(max_length=10, help_text="岩层级别")
    karst_development = models.CharField(
        max_length=50, blank=True, null=True, help_text="岩溶发育程度"
    )
    water_status = models.CharField(
        max_length=100, blank=True, null=True, help_text="消水状态"
    )

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")
    project_id = models.CharField(max_length=50, help_text="施工项目编号")

    # 审批字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(blank=True, null=True, help_text="操作理由")
    approval_reason = models.TextField(blank=True, null=True, help_text="审批理由")
    approved_by = models.CharField(max_length=100, blank=True, null=True, help_text="审批管理员")
    approved_at = models.DateTimeField(blank=True, null=True, help_text="审批时间")

    # 时间字段
    created_at = models.DateTimeField(help_text="创建时间")
    updated_at = models.DateTimeField(help_text="更新时间")

    def __str__(self):
        return f"备份 - {self.face_id} - {self.inspection_date}"


class ExcavationDiagnosisBackup(models.Model):
    """
    备份表：超欠挖诊断数据备份
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")
    inspector = models.CharField(max_length=100, help_text="测量人员")
    measurement_date = models.DateField(help_text="测量日期")

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")
    project_id = models.CharField(max_length=50, help_text="施工项目编号")

    # 超欠挖诊断数据字段
    scale = models.FloatField(help_text="比例尺")
    mileage = models.FloatField(help_text="里程")
    design_section = models.FloatField(help_text="设计断面")
    line_x = models.FloatField(help_text="线路X坐标")
    line_y = models.FloatField(help_text="线路Y坐标")
    measured_section = models.FloatField(help_text="实测断面面积")
    reference_section = models.FloatField(help_text="参考断面面积")
    line_height = models.FloatField(help_text="线路高程")
    over_excavation_area = models.FloatField(help_text="超挖面积")
    under_excavation_area = models.FloatField(help_text="欠挖面积")
    max_over_excavation = models.FloatField(help_text="最大超挖")
    max_under_excavation = models.FloatField(help_text="最大欠挖")
    average_over_excavation = models.FloatField(help_text="平均超挖")
    average_under_excavation = models.FloatField(help_text="平均欠挖")
    diagnosis_result = models.CharField(
        max_length=20,
        choices=[
            ('within_limits', '超欠挖合格'),
            ('exceeds_limits', '超欠挖超标'),
        ],
        default='within_limits',
        help_text="诊断结果"
    )

    # 审批字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(blank=True, null=True, help_text="操作理由")
    approval_reason = models.TextField(blank=True, null=True, help_text="审批理由")
    approved_by = models.CharField(max_length=100, blank=True, null=True, help_text="审批管理员")
    approved_at = models.DateTimeField(blank=True, null=True, help_text="审批时间")

    # 时间字段
    created_at = models.DateTimeField(help_text="创建时间")
    updated_at = models.DateTimeField(help_text="更新时间")

    def __str__(self):
        return f"备份 - {self.face_id} - {self.inspection_date}"


class OverUnderExcavationCalculationBackup(models.Model):
    """
    备份表：超欠挖计算数据备份
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")
    inspector = models.CharField(max_length=100, help_text="测量人员")
    measurement_date = models.DateField(help_text="测量日期")

    # 线路定线表数据
    line_name = models.CharField(max_length=200, help_text="线路名称")
    north_direction_angle = models.FloatField(help_text="北方向角")
    radius = models.FloatField(help_text="半径")
    length = models.FloatField(help_text="长度")
    east_coordinate = models.FloatField(help_text="东坐标")
    north_coordinate = models.FloatField(help_text="北坐标")

    # 横截面表数据
    start_offset = models.FloatField(help_text="起点偏移")
    height = models.FloatField(help_text="高度")
    radius_section = models.FloatField(help_text="横截面半径")
    angle_increment = models.FloatField(help_text="角度增量")

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")
    project_id = models.CharField(max_length=50, help_text="施工项目编号")

    # 审批字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(blank=True, null=True, help_text="操作理由")
    approval_reason = models.TextField(blank=True, null=True, help_text="审批理由")
    approved_by = models.CharField(max_length=100, blank=True, null=True, help_text="审批管理员")
    approved_at = models.DateTimeField(blank=True, null=True, help_text="审批时间")

    # 时间字段
    created_at = models.DateTimeField(help_text="创建时间")
    updated_at = models.DateTimeField(help_text="更新时间")

    def __str__(self):
        return f"备份 - {self.face_id} - {self.inspection_date}"


class TunnelContourInfoBackup(models.Model):
    """
    备份表：隧道轮廓数据备份
    """
    # 基础信息字段
    inspection_date = models.DateTimeField(help_text="检查日期")
    inspector = models.CharField(max_length=100, help_text="测量人员")
    measurement_date = models.DateField(help_text="测量日期")

    # 隧道轮廓参数
    cr = models.FloatField(help_text="调整指数范围的常数 Cr")
    w1 = models.FloatField(help_text="权重值 w1")
    w2 = models.FloatField(help_text="权重值 w2")
    w3 = models.FloatField(help_text="权重值 w3")
    od = models.FloatField(help_text="超挖深度 Od")
    rcl = models.FloatField(help_text="轮廓粗糙度 RCL")
    vo = models.FloatField(help_text="纵向超挖变化 Vo")
    c1 = models.FloatField(help_text="修正因子 c1")
    c2 = models.FloatField(help_text="修正因子 c2")
    c3 = models.FloatField(help_text="修正因子 c3")

    # 标识字段
    face_id = models.CharField(max_length=50, help_text="掌子面编号")
    project_id = models.CharField(max_length=50, help_text="施工项目编号")

    # 审批字段
    STATUS_CHOICES = [
        ('pending', '待审批'),
        ('uploaded_approved', '上传已审批'),
        ('modified_pending', '修改待审批'),
        ('modified_approved', '修改已审批'),
        ('deleted_pending', '删除待审批'),
        ('deleted', '已删除'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="记录当前状态"
    )
    operation_reason = models.TextField(blank=True, null=True, help_text="操作理由")
    approval_reason = models.TextField(blank=True, null=True, help_text="审批理由")
    approved_by = models.CharField(max_length=100, blank=True, null=True, help_text="审批管理员")
    approved_at = models.DateTimeField(blank=True, null=True, help_text="审批时间")

    # 时间字段
    created_at = models.DateTimeField(help_text="创建时间")
    updated_at = models.DateTimeField(help_text="更新时间")

    def __str__(self):
        return f"备份 - {self.face_id} - {self.inspection_date}"

