import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 数据
x = np.array([50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
y = np.array([100, 120, 140, 160, 180, 200, 220, 240, 260, 280])
n = len(x)

# 初始化
w, b = 0, 0
alpha = 0.00001
iterations = 20
losses = []
w_history = []
b_history = []

# 梯度下降
for i in range(iterations):
    y_pred = w * x + b
    loss = np.mean((y - y_pred) ** 2)
    losses.append(loss)
    w_history.append(w)
    b_history.append(b)

    dw = -2 / n * np.sum(x * (y - y_pred))
    db = -2 / n * np.sum(y - y_pred)

    w -= alpha * dw
    b -= alpha * db

    print(f"第{i + 1:2d}次迭代: w={w:.4f}, b={b:.4f}, loss={loss:.2f}")

# 创建图表
plt.figure(figsize=(16, 6))

# 子图1：拟合直线逐步逼近（展示第1、5、10、20次迭代的直线）
plt.subplot(1, 2, 1)
plt.scatter(x, y, color='blue', s=50, label='原始数据', zorder=5)

# 绘制不同迭代次数的拟合直线
iterations_to_show = [0, 4, 9, 19]  # 第1、5、10、20次（索引从0开始）
colors = ['red', 'orange', 'green', 'purple']
labels = ['第1次迭代', '第5次迭代', '第10次迭代', '第20次迭代']

for idx, iter_idx in enumerate(iterations_to_show):
    w_tmp = w_history[iter_idx]
    b_tmp = b_history[iter_idx]
    y_line = w_tmp * x + b_tmp
    plt.plot(x, y_line, color=colors[idx], linewidth=2, label=f'{labels[idx]}: y={w_tmp:.2f}x+{b_tmp:.2f}')

plt.xlabel('面积 (㎡)', fontsize=12)
plt.ylabel('房价 (万元)', fontsize=12)
plt.title('图1-1：拟合直线逐步逼近过程', fontsize=14)
plt.legend()
plt.grid(True, alpha=0.3)

# 子图2：Loss下降曲线
plt.subplot(1, 2, 2)
plt.plot(range(1, iterations + 1), losses, 'b-o', linewidth=2, markersize=6)
plt.xlabel('迭代次数', fontsize=12)
plt.ylabel('Loss值', fontsize=12)
plt.title('图1-2：Loss随迭代次数下降曲线', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, iterations + 1, 2))

# 标注最终Loss
plt.annotate(f'最终Loss: {losses[-1]:.2f}',
             xy=(iterations, losses[-1]),
             xytext=(iterations - 5, losses[-1] + 2000),
             arrowprops=dict(arrowstyle='->', color='red'))

plt.tight_layout()
plt.savefig('linear_regression_results.png', dpi=300, bbox_inches='tight')
plt.show()

# 打印最终结果
print(f"\n最终结果: w={w:.4f}, b={b:.4f}")
print(f"理论理想值: w=2.0000, b=0.0000")
