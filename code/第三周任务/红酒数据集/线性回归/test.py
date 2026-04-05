import numpy as np
import pandas as pd

# 1. 加载数据
df = pd.read_csv('winequality-red.csv', sep=',')
X = df.drop('quality', axis=1).values
y = df['quality'].values.reshape(-1, 1)

# 2. 手动标准化 (z-score)
mean_X = np.mean(X, axis=0)
std_X = np.std(X, axis=0)
std_X[std_X == 0] = 1
X_scaled = (X - mean_X) / std_X

# 3. 划分训练集和测试集 (80/20)
np.random.seed(42)
indices = np.random.permutation(len(X_scaled))
train_size = int(0.8 * len(X_scaled))
train_idx, test_idx = indices[:train_size], indices[train_size:]

X_train = X_scaled[train_idx]
X_test = X_scaled[test_idx]
y_train = y[train_idx]
y_test = y[test_idx]

# 添加偏置列（截距）
X_train_b = np.c_[np.ones(X_train.shape[0]), X_train]
X_test_b = np.c_[np.ones(X_test.shape[0]), X_test]

print(f"训练样本: {X_train.shape[0]}, 测试样本: {X_test.shape[0]}")

# 4. 正规方程求解线性回归
def linear_regression_normal_eq(X, y):
    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)
    theta = XtX_inv @ (X.T @ y)
    return theta

theta = linear_regression_normal_eq(X_train_b, y_train)
print("\n线性回归系数（第一个为截距）:")
print(theta.flatten())

# 5. 预测与评估
y_train_pred = X_train_b @ theta
y_test_pred = X_test_b @ theta

def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)

def r2_score(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot

train_mse = mse(y_train, y_train_pred)
test_mse = mse(y_test, y_test_pred)
train_r2 = r2_score(y_train, y_train_pred)
test_r2 = r2_score(y_test, y_test_pred)

print("\n【线性回归评估结果】")
print(f"训练集 MSE: {train_mse:.4f}, RMSE: {np.sqrt(train_mse):.4f}, R²: {train_r2:.4f}")
print(f"测试集 MSE: {test_mse:.4f}, RMSE: {np.sqrt(test_mse):.4f}, R²: {test_r2:.4f}")