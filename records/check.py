def check_geological_data_validity(record):
    """
    检查地质数据是否符合要求。
    :param record: GeologicalSketchRecord 对象
    :return: (bool, dict) - 数据是否有效以及错误信息
    """
    errors = {}
    valid = True

    # 定义数值字段的校验规则
    rules = {
        'distance': (0, 10000),  # 里程范围
        'design_section': (5, 50),  # 设计断面范围
        'excavation_width': (10, 20),  # 开挖宽度范围
        'excavation_height': (5, 15),  # 开挖高度范围
        'excavation_area': (50, 300),  # 开挖面积范围
    }

    # 校验数值字段
    for field, (min_val, max_val) in rules.items():
        value = getattr(record, field, None)
        if value is not None and not (min_val <= value <= max_val):
            valid = False
            errors[field] = f"{field} ({value}) 不在范围 {min_val} 到 {max_val} 之间"

    return valid, errors


def check_excavation_calculation_validity(record):
    """
    检查超欠挖计算数据是否符合要求。
    :param record: OverUnderExcavationCalculation 对象
    :return: (bool, dict) - 数据是否有效以及错误信息
    """
    errors = {}
    valid = True

    # 定义数值字段的校验规则
    rules = {
        'north_direction_angle': (0, 360),  # 北方向角范围
        'radius': (0, 1000),  # 半径范围
        'length': (0, 5000),  # 长度范围
        'east_coordinate': (-100000, 100000),  # 东坐标范围
        'north_coordinate': (-100000, 100000),  # 北坐标范围
        'start_offset': (0, 500),  # 起点偏移范围
        'height': (0, 100),  # 高度范围
        'radius_section': (0, 500),  # 横截面半径范围
        'angle_increment': (0, 90),  # 角度增量范围
    }

    # 校验数值字段
    for field, (min_val, max_val) in rules.items():
        value = getattr(record, field, None)
        if value is not None and not (min_val <= value <= max_val):
            valid = False
            errors[field] = f"{field} ({value}) 不在范围 {min_val} 到 {max_val} 之间"

    return valid, errors


def check_tunnel_data_validity(record):
    """
    检查隧道信息数据是否符合要求。
    :param record: TunnelContourInfo 对象
    :return: (bool, dict) - 数据是否有效以及错误信息
    """
    errors = {}
    valid = True

    # 定义数值字段的校验规则
    rules = {
        'cr': (0, 10),  # 调整指数范围的常数范围
        'w1': (0, 10),  # 权重值 w1 范围
        'w2': (0, 10),  # 权重值 w2 范围
        'w3': (0, 10),  # 权重值 w3 范围
        'od': (0, 50),  # 超挖深度范围
        'rcl': (0, 100),  # 轮廓粗糙度范围
        'vo': (0, 50),  # 纵向超挖变化范围
        'c1': (0, 5),  # 修正因子 c1 范围
        'c2': (0, 5),  # 修正因子 c2 范围
        'c3': (0, 5),  # 修正因子 c3 范围
    }

    # 校验数值字段
    for field, (min_val, max_val) in rules.items():
        value = getattr(record, field, None)
        if value is not None and not (min_val <= value <= max_val):
            valid = False
            errors[field] = f"{field} ({value}) 不在范围 {min_val} 到 {max_val} 之间"

    return valid, errors


def check_excavation_diagnosis_validity(record):
    """
    检查超欠挖诊断数据是否符合要求。
    :param record: ExcavationDiagnosis 对象
    :return: (bool, dict) - 数据是否有效以及错误信息
    """
    errors = {}
    valid = True

    # 定义数值字段的校验规则
    rules = {
        'scale': (0, 1000),  # 比例尺范围
        'mileage': (0, 10000),  # 里程范围
        'design_section': (5, 50),  # 设计断面范围
        'line_x': (-100000, 100000),  # 线路X坐标范围
        'line_y': (-100000, 100000),  # 线路Y坐标范围
        'measured_section': (0, 10000),  # 实测断面面积范围
        'reference_section': (0, 10000),  # 参考断面面积范围
        'line_height': (0, 5000),  # 线路高程范围
        'over_excavation_area': (0, 500),  # 超挖面积范围
        'under_excavation_area': (0, 500),  # 欠挖面积范围
        'max_over_excavation': (0, 50),  # 最大超挖范围
        'max_under_excavation': (0, 50),  # 最大欠挖范围
        'average_over_excavation': (0, 20),  # 平均超挖范围
        'average_under_excavation': (0, 20),  # 平均欠挖范围
    }

    # 校验数值字段
    for field, (min_val, max_val) in rules.items():
        value = getattr(record, field, None)
        if value is not None and not (min_val <= value <= max_val):
            valid = False
            errors[field] = f"{field} ({value}) 不在范围 {min_val} 到 {max_val} 之间"

    return valid, errors
