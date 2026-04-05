# 线性回归、逻辑回归、K-Means 与 PCA笔记



![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405173921025.png)

![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405174013470.png)

![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405174334601.png)

![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405174523716.png)

![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405174615097.png)

#### ![](https://raw.githubusercontent.com/Feng-runsong/Note/main/code/20260405174727225.png)



## 梯度下降的优化算法

#### 标准梯度下降存在收敛慢、易陷入局部最优等局限。业界发展出了多种优化器:

- 动量法 (Momentum):借鉴物理学惯性，给梯度加上“速度”，减少狭长山谷中的震荡。

- AdaGrad:为每个参数自动维护独立的学习率，适合处理稀疏数据。

- RMSProp: AdaGrad的改良，关注近期的梯度变化，避免学习率降到零，适合非平稳目标(如 RNN)。

- Adam (自适应矩估计):结合了动量(方向加速)和 RMSProp (自适应步幅)。它同时维护梯度的方向趋势和大小变化，既跑得快又稳。收敛快且对学习率不敏感，是目前深度学习中最广泛使用的默认首选优化器。


