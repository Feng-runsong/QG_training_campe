"""
作业任务
使用python，制作一个代码，完成要求：读取一个json，格式如下，其中包含一个坐标系内包含的原始向量，以及坐
标轴向量，和一个任务列表，任务有两种类型
坐标系转移
以当前坐标系为基准，将当前坐标系的向量，转移到目标坐标系，求出向量在目标坐标系的向量表示
注意！！进行过此项操作后，目标坐标系会变成新的基准坐标系，用于后续操作
现在完成如下任务：
1. 能够实现二维向量的坐标系转移
2. 能够计算二维向量的坐标系投影，坐标系夹角，坐标系面积
3. 将上述运算拓展至三维向量，任意维度向量
4. 所有的目标坐标系都可以进行坐标系转移吗，思考能构成坐标系的条件，判断task中的任务数据能否构成坐标
系
5. 运用面向对象的思想，将一个坐标系及其包含的所有向量封装成类，并且将上面四则坐标系运算做成类的方法
"""

import json
import numpy as np


class CoordinateSystem:
    def __init__(self, vectors, axes):
        """
        初始化坐标系系统
        :param vectors:向量数据
        :param axes:坐标系的基向量
        """
        self.vectors = np.array(vectors, dtype=float)
        self.axes = np.array(axes, dtype=float)
        self.dim = len(axes)

    def is_valid(self):
        """判断是否能构成坐标系：轴向量数量等于维度且线性无关"""
        # 判断轴向量数量是否等于维度
        if len(self.axes) != self.dim:
            return False
        # 判断向量是否线性无关
        return abs(np.linalg.det(self.axes)) > 1e-10

    def transform(self, new_axes):
        """
        坐标系转移：将向量转换到新坐标系
        :param new_axes:目标坐标系的基向量（新坐标系）
        :return:转换后的新坐标系
        """
        new_axes = np.array(new_axes, dtype=float)
        # 变换矩阵 M = (new_axes)^(-1) * (self.axes)
        # 矩阵转置
        transform_mat = np.linalg.inv(new_axes.T) @ self.axes.T
        # 矩阵乘法
        new_vectors = self.vectors @ transform_mat.T
        return CoordinateSystem(new_vectors, new_axes)

    def projection(self):
        """计算向量在每个轴上的投影长度"""
        # 创建空列表，用于存储所有向量的投影结果
        proj = []
        # 计算向量投影
        for v in self.vectors:
            proj.append([np.dot(v, a) / np.linalg.norm(a) for a in self.axes])
        # 将列表转换为numpy数组，并保留一位小数
        return np.round(np.array(proj), 1)

    def angle(self):
        """计算向量与每个轴的夹角（弧度）"""
        # 创建空列表，存储所有向量的夹角结果
        angles = []

        # 计算夹角
        for v in self.vectors:
            v_norm = np.linalg.norm(v)

            # 处理零向量
            if v_norm < 1e-10:
                angles.append([0.0] * self.dim)
                continue

            # 计算当前向量与每个轴的夹角
            # 创建空列表，存储当前向量与所有轴夹角的列表
            row_angles = []
            for a in self.axes:
                a_norm = np.linalg.norm(a)
                # 计算余弦值
                cos_theta = np.dot(v, a) / (v_norm * a_norm)
                # 限制在[-1,1]范围内，避免数值误差
                cos_theta = np.clip(cos_theta, -1, 1)
                # 计算夹角
                row_angles.append(np.arccos(cos_theta))

            # 将当前向量的所有夹角添加到结果中
            angles.append(row_angles)

        # 将列表转换为numpy数组，并保留一位小数
        return np.round(np.array(angles), 1)

    def area_scale(self):
        """计算面积/体积缩放倍数（相对于标准直角坐标系）"""
        # 保留一位小数
        return round(abs(np.linalg.det(self.axes)), 1)


def process_tasks(data):
    """处理JSON中的任务序列"""
    # 创建空列表，存储所有任务结果
    results = []

    for group in data:
        cs = CoordinateSystem(group["vectors"], group["ori_axis"])

        for task in group["tasks"]:
            task_type = task["type"]
            match task_type:
                # 坐标系转移
                case "change_axis":
                    cs = cs.transform(task["obj_axis"])
                    if not cs.is_valid():
                        print(f"{group['group_name']} 中的坐标系无效,请修改数据!!!")
                # 计算向量在每个轴上的投影长度
                case "axis_projection":
                    result = cs.projection()
                    results.append({
                        "group": group["group_name"],
                        "task": "axis_projection",
                        "result": result.tolist()
                    })
                # 计算向量与每个轴的夹角（弧度）,结果单位为rad
                case "axis_angle":
                    result = cs.angle()
                    results.append({
                        "group": group["group_name"],
                        "task": "axis_angle",
                        "result": result.tolist()
                    })
                # 计算面积 / 体积缩放倍数
                case "area":
                    result = cs.area_scale()
                    results.append({
                        "group": group["group_name"],
                        "task": "area",
                        "result": float(result)
                    })

    return results


# 运行程序
# 读取JSON文件
with open("data(1).json", "r") as f:
    data = json.load(f)

# 处理任务
results = process_tasks(data)

# 按组分组合结果
grouped_results = {}
for r in results:
    group_name = r["group"]
    if group_name not in grouped_results:
        grouped_results[group_name] = []
    grouped_results[group_name].append(r)

# 输出结果
for group_name in grouped_results:
    print("-" * 100)
    print(f"Group: {group_name}")

    for task in grouped_results[group_name]:
        print(f"Task: {task['task']}")

        # 格式化输出，保留一位小数
        match task['task'] :
            case 'axis_projection':
                print(f"Result (投影长度，保留一位小数):")
                for row in task['result']:
                    print(f"{row}")
            case 'axis_angle':
                print(f"Result (夹角，单位：弧度，保留一位小数):")
                for row in task['result']:
                    print(f"{row}")
            case 'area':
                print(f"Result (面积/体积缩放倍数): {task['result']:.1f}")

        print("-" * 40)

print("-"*100)
print("任务完成,Bye bye~~")