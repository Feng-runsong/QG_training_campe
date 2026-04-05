import numpy as np
import pandas as pd

# 1. 加载数据
df = pd.read_csv('winequality-red.csv', sep=',')
X = df.drop('quality', axis=1).values
y = (df['quality'] > 6).astype(int).values.reshape(-1, 1)

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

# 添加偏置列
X_train_b = np.c_[np.ones(X_train.shape[0]), X_train]
X_test_b = np.c_[np.ones(X_test.shape[0]), X_test]

print(f"训练样本: {X_train.shape[0]}, 测试样本: {X_test.shape[0]}")
print(f"好酒比例 (训练集): {np.mean(y_train)*100:.1f}%")

# 4. 逻辑回归梯度下降
def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))

def compute_loss(y, y_pred):
    eps = 1e-12
    y_pred = np.clip(y_pred, eps, 1 - eps)
    return -np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))

def logistic_regression_gd(X, y, lr=0.1, epochs=1000):
    m, n = X.shape
    theta = np.zeros((n, 1))
    for epoch in range(epochs):
        y_pred = sigmoid(X @ theta)
        loss = compute_loss(y, y_pred)
        grad = (1 / m) * (X.T @ (y_pred - y))
        theta -= lr * grad
        if (epoch + 1) % 200 == 0:
            print(f"Epoch {epoch+1}/{epochs}, Loss: {loss:.6f}")
    return theta

theta = logistic_regression_gd(X_train_b, y_train, lr=0.1, epochs=1000)

# 5. 预测与评估
y_train_pred = (sigmoid(X_train_b @ theta) >= 0.5).astype(int)
y_test_pred = (sigmoid(X_test_b @ theta) >= 0.5).astype(int)

def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def confusion_matrix_stats(y_true, y_pred):
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    acc = (tp + tn) / (tp + tn + fp + fn)
    return acc, prec, rec, f1, tp, tn, fp, fn

train_acc = accuracy(y_train, y_train_pred)
test_acc, prec, rec, f1, tp, tn, fp, fn = confusion_matrix_stats(y_test, y_test_pred)

print("\n【逻辑回归评估结果】")
print(f"训练集准确率: {train_acc:.4f}")
print(f"测试集准确率: {test_acc:.4f}")
print(f"测试集精确率: {prec:.4f}, 召回率: {rec:.4f}, F1分数: {f1:.4f}")
print("混淆矩阵:")
print(f"           预测好酒  预测坏酒")
print(f"实际好酒      {tp:3d}      {fn:3d}")
print(f"实际坏酒      {fp:3d}      {tn:3d}")