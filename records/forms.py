from django import forms
from .models import GeologicalSketchRecord, ExcavationDiagnosis


#掌子面
class GeologicalSketchRecordForm(forms.ModelForm):
    class Meta:
        model = GeologicalSketchRecord  # 绑定的模型为 GeologicalSketchRecord
        fields = [  #fields指定表单中包含的字段
            'face_id',  # 掌子面编号
            'project_id',  # 施工项目编号
            'inspection_date',  # 检查日期
            'distance',  # 里程
            'design_section',  # 设计断面
            'inspector',  # 测量人员
            'measurement_date',  # 测量日期
            'excavation_width',  # 开挖宽度
            'excavation_height',  # 开挖高度
            'excavation_area',  # 开挖面积
            'excavation_method',  # 开挖方式
            'face_condition',  # 掌子面状态
            'excavation_condition',  # 毛开挖情况
            'rock_strength',  # 岩石强度
            'weathering_degree',  # 风化程度
            'crack_width',  # 裂缝宽度
            'crack_shape',  # 裂缝形态
            'water_condition',  # 渗水状态
            'rockburst_tendency',  # 岩爆发育程度
            'rock_grade',  # 岩层级别
            #新增的
            'karst_development',  # 岩溶发育程度
            'water_status',  # 消水状态
            'operation_reason',  # 添加修改理由字段
        ]
        widgets = {  #widgets控制样式，表单字段的外观和行为
            # 设置控件样式并支持日期选择器
            'face_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入掌子面编号'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入施工项目编号'}),
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'measurement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入里程'}),
            'design_section': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入设计断面'}),
            'excavation_width': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入开挖宽度'}),
            'excavation_height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入开挖高度'}),
            'excavation_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入开挖面积'}),
            'excavation_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入开挖方式'}),
            'face_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入掌子面状态'}),
            'excavation_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入毛开挖情况'}),
            'rock_strength': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入岩石强度'}),
            'weathering_degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入风化程度'}),
            'crack_width': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入裂缝宽度'}),
            'crack_shape': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入裂缝形态'}),
            'water_condition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入渗水状态'}),
            'rockburst_tendency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入岩爆发育程度'}),
            'rock_grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入岩层级别'}),
            #新增的
            'karst_development': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入岩溶发育程度'}),
            'water_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入消水状态'}),
            'operation_reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入修改或删除的理由', 'rows': 4}),
            'inspector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入测量人员'}),
        }
        labels = { #labels自定义字段的显示名称（本项目采用中文显示）
            'face_id': '掌子面编号',  # 中文显示字段名称
            'project_id': '施工项目编号',
            'inspection_date': '检查日期',
            'distance': '里程',
            'design_section': '设计断面',
            'inspector': '测量人员',
            'measurement_date': '测量日期',
            'excavation_width': '开挖宽度',
            'excavation_height': '开挖高度',
            'excavation_area': '开挖面积',
            'excavation_method': '开挖方式',
            'face_condition': '掌子面状态',
            'excavation_condition': '毛开挖情况',
            'rock_strength': '岩石强度',
            'weathering_degree': '风化程度',
            'crack_width': '裂缝宽度',
            'crack_shape': '裂缝形态',
            'water_condition': '渗水状态',
            'rockburst_tendency': '岩爆发育程度',
            'rock_grade': '岩层级别',
            #新增的
            'karst_development': '岩溶发育程度',
            'water_status': '消水状态',
            'operation_reason': '操作理由',  # 设置修改理由的标签
        }

    def clean_face_id(self):
        """
        验证掌子面编号的有效性。
        """
        face_id = self.cleaned_data.get('face_id')
        if not face_id:
            raise forms.ValidationError("掌子面编号不能为空")
        # 可以添加更多逻辑，例如检查编号格式或唯一性
        return face_id

    def clean_project_id(self):
        """
        验证施工项目编号的有效性。
        """
        project_id = self.cleaned_data.get('project_id')
        if not project_id:
            raise forms.ValidationError("施工项目编号不能为空")
        # 可以添加更多逻辑，例如检查编号格式或有效性
        return project_id



#超欠挖诊断
class ExcavationDiagnosisForm(forms.ModelForm):
    class Meta:
        model = ExcavationDiagnosis
        fields = [
            'inspection_date',
            'inspector',
            'scale',
            'mileage',
            'design_section',
            'inspector',
            'measurement_date',
            'line_x',
            'line_y',
            'measured_section',
            'reference_section',
            'line_height',
            'over_excavation_area',
            'under_excavation_area',
            'max_over_excavation',
            'max_under_excavation',
            'average_over_excavation',
            'average_under_excavation',
            'diagnosis_result',
            'face_id',
            'project_id',
            'operation_reason',
        ]
        widgets = {
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inspector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入测量人员'}),
            'measurement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scale': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入比例尺'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入里程'}),
            'design_section': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入设计断面'}),
            'line_x': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入线路X坐标'}),
            'line_y': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入线路Y坐标'}),
            'measured_section': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入实测断面面积'}),
            'reference_section': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入参考断面面积'}),
            'line_height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入线路高程'}),
            'over_excavation_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入超挖面积'}),
            'under_excavation_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入欠挖面积'}),
            'max_over_excavation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入最大超挖'}),
            'max_under_excavation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入最大欠挖'}),
            'average_over_excavation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入平均超挖'}),
            'average_under_excavation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入平均欠挖'}),
            'diagnosis_result': forms.Select(attrs={'class': 'form-control'}),
            'face_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入超欠挖诊断编号'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入施工项目编号'}),
            'operation_reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入操作理由'}),
        }
        labels = {
            'inspection_date': '检查日期',
            'inspector': '测量人员',
            'scale': '比例尺',
            'mileage': '里程',
            'design_section': '设计断面',
            'measurement_date': '测量日期',
            'line_x': '线路X坐标',
            'line_y': '线路Y坐标',
            'measured_section': '实测断面面积',
            'reference_section': '参考断面面积',
            'line_height': '线路高程',
            'over_excavation_area': '超挖面积',
            'under_excavation_area': '欠挖面积',
            'max_over_excavation': '最大超挖',
            'max_under_excavation': '最大欠挖',
            'average_over_excavation': '平均超挖',
            'average_under_excavation': '平均欠挖',
            'diagnosis_result': '诊断结果',
            'face_id': '超欠挖诊断编号',
            'project_id': '施工项目编号',
            'operation_reason': '操作理由',
        }


from django import forms
from .models import OverUnderExcavationCalculation
#超欠挖计算
class OverUnderExcavationForm(forms.ModelForm):
    class Meta:
        model = OverUnderExcavationCalculation
        fields = [
            # 基础信息字段
            'inspection_date',
            'inspector',
            'measurement_date',
            #其余信息
            'line_name',
            'north_direction_angle',
            'radius',
            'length',
            'east_coordinate',
            'north_coordinate',
            'start_offset',
            'height',
            'radius_section',
            'angle_increment',
            'face_id',
            'project_id',
            'operation_reason',
        ]
        widgets = {
            # 基础信息字段的 widgets
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inspector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入测量人员'}),
            'measurement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            #其余信息
            'line_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入线路名称'}),
            'north_direction_angle': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入北方向角'}),
            'radius': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入半径'}),
            'length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入长度'}),
            'east_coordinate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入东坐标'}),
            'north_coordinate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入北坐标'}),
            'start_offset': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入起点偏移'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入高度'}),
            'radius_section': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入横截面半径'}),
            'angle_increment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入角度增量'}),
            'face_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入超欠挖计算编号'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入施工项目编号'}),
            'operation_reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入操作理由'}),
        }
        labels = {
            # 基础信息字段的 labels
            'inspection_date': '检查日期',
            'inspector': '测量人员',
            'measurement_date': '测量日期',
            #其余
            'line_name': '线路名称',
            'north_direction_angle': '北方向角',
            'radius': '半径',
            'length': '长度',
            'east_coordinate': '东坐标',
            'north_coordinate': '北坐标',
            'start_offset': '起点偏移',
            'height': '高度',
            'radius_section': '横截面半径',
            'angle_increment': '角度增量',
            'face_id': '超欠挖计算编号',
            'project_id': '施工项目编号',
            'operation_reason': '操作理由',
        }


from django import forms
from .models import TunnelContourInfo
#隧道
class TunnelContourForm(forms.ModelForm):
    class Meta:
        model = TunnelContourInfo
        fields = [
            'face_id',
            'project_id',
            'inspection_date',
            'inspector',
            'measurement_date',
            'cr',
            'w1',
            'w2',
            'w3',
            'od',
            'rcl',
            'vo',
            'c1',
            'c2',
            'c3',
            'operation_reason',
        ]
        widgets = {
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'face_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入隧道编号'}),
            'project_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入施工项目编号'}),
            'inspector': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入测量人员'}),
            'measurement_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cr': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入调整指数范围的常数 Cr'}),
            'w1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入权重值 w1'}),
            'w2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入权重值 w2'}),
            'w3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入权重值 w3'}),
            'od': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入超挖深度 Od'}),
            'rcl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入轮廓粗糙度 RCL'}),
            'vo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入纵向超挖变化 Vo'}),
            'c1': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入修正因子 c1'}),
            'c2': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入修正因子 c2'}),
            'c3': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '请输入修正因子 c3'}),
            'operation_reason': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '请输入操作理由'}),
        }
        labels = {
            'face_id': '隧道编号',
            'project_id': '施工项目编号',
            'inspection_date': '检查日期',
            'inspector': '测量人员',
            'measurement_date': '测量日期',
            'cr': '调整指数范围的常数 Cr',
            'w1': '权重值 w1',
            'w2': '权重值 w2',
            'w3': '权重值 w3',
            'od': '超挖深度 Od',
            'rcl': '轮廓粗糙度 RCL',
            'vo': '纵向超挖变化 Vo',
            'c1': '修正因子 c1',
            'c2': '修正因子 c2',
            'c3': '修正因子 c3',
            'operation_reason': '操作理由',
        }
