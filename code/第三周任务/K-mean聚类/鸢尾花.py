import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# -----------------------------
# 1. 数据加载
# -----------------------------
def load_iris_data(filepath):
    data = pd.read_csv(filepath, header=None)
    X = data.iloc[:, :4].values.astype(float)
    y_str = data.iloc[:, 4].values
    unique_labels = np.unique(y_str)
    label_to_int = {label: idx for idx, label in enumerate(unique_labels)}
    y = np.array([label_to_int[label] for label in y_str])
    return X, y, unique_labels


# -----------------------------
# 2. PCA手动实现（降到2维）
# -----------------------------
def pca(X, n_components=2):
    X_mean = X.mean(axis=0)
    X_centered = X - X_mean
    cov_matrix = np.cov(X_centered, rowvar=False)
    eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)
    sorted_idx = np.argsort(eig_vals)[::-1]
    eig_vecs_sorted = eig_vecs[:, sorted_idx]
    components = eig_vecs_sorted[:, :n_components]
    X_pca = X_centered @ components
    return X_pca, components, X_mean


# -----------------------------
# 3. K-Means手动实现
# -----------------------------
def kmeans(X, k, max_iters=100, random_seed=42):
    np.random.seed(random_seed)
    n_samples = X.shape[0]
    indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[indices].copy()
    for i in range(max_iters):
        distances = np.linalg.norm(X[:, np.newaxis, :] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.array([X[labels == j].mean(axis=0) for j in range(k)])
        if np.allclose(centroids, new_centroids):
            print(f"K-Means收敛于第{i + 1}次迭代")
            break
        centroids = new_centroids
    return labels, centroids


# -----------------------------
# 4. 评估指标（熵、均一性、完整性、V-measure、轮廓系数）
# -----------------------------
def entropy(labels):
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / len(labels)
    return -np.sum(probs * np.log2(probs + 1e-12))


def homogeneity_completeness_vmeasure(true_labels, pred_labels):
    H_C = entropy(true_labels)
    H_K = entropy(pred_labels)

    pred_classes = np.unique(pred_labels)
    H_C_given_K = 0.0
    for k in pred_classes:
        mask = (pred_labels == k)
        true_in_cluster = true_labels[mask]
        if len(true_in_cluster) == 0:
            continue
        H_C_given_K += (len(true_in_cluster) / len(pred_labels)) * entropy(true_in_cluster)

    true_classes = np.unique(true_labels)
    H_K_given_C = 0.0
    for c in true_classes:
        mask = (true_labels == c)
        pred_in_class = pred_labels[mask]
        if len(pred_in_class) == 0:
            continue
        H_K_given_C += (len(pred_in_class) / len(true_labels)) * entropy(pred_in_class)

    homogeneity = 1 - (H_C_given_K / H_C) if H_C != 0 else 1.0
    completeness = 1 - (H_K_given_C / H_K) if H_K != 0 else 1.0
    v_measure = 2 * homogeneity * completeness / (homogeneity + completeness) if (
                                                                                             homogeneity + completeness) != 0 else 0.0
    return homogeneity, completeness, v_measure


def silhouette_score(X, labels):
    n_samples = len(X)
    unique_labels = np.unique(labels)
    if len(unique_labels) == 1:
        return 0.0
    s_values = []
    for i in range(n_samples):
        same_cluster_mask = (labels == labels[i])
        if np.sum(same_cluster_mask) == 1:
            a_i = 0.0
        else:
            distances_to_same = np.linalg.norm(X[same_cluster_mask] - X[i], axis=1)
            a_i = np.sum(distances_to_same) / (np.sum(same_cluster_mask) - 1)
        b_i = np.inf
        for label in unique_labels:
            if label == labels[i]:
                continue
            other_mask = (labels == label)
            distances_to_other = np.linalg.norm(X[other_mask] - X[i], axis=1)
            avg_dist = np.mean(distances_to_other)
            if avg_dist < b_i:
                b_i = avg_dist
        s_i = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) != 0 else 0.0
        s_values.append(s_i)
    return np.mean(s_values)


# -----------------------------
# 5. 标签重映射：使聚类标签的数字与占多数的真实标签数字一致
# -----------------------------
def remap_cluster_labels(true_labels, pred_labels):
    """
    重新映射聚类标签，使得每个簇的标签数字等于该簇内真实标签的众数。
    例如：如果簇0中大多数样本的真实标签是2，则将该簇所有样本的标签改为2。
    """
    unique_clusters = np.unique(pred_labels)
    mapping = {}
    for cl in unique_clusters:
        mask = (pred_labels == cl)
        true_in_cluster = true_labels[mask]
        # 计算众数（出现最多的真实标签）
        majority_label = Counter(true_in_cluster).most_common(1)[0][0]
        mapping[cl] = majority_label
    # 应用映射
    remapped_labels = np.array([mapping[label] for label in pred_labels])
    return remapped_labels, mapping


# -----------------------------
# 6. 可视化（两个子图使用相同的颜色映射）
# -----------------------------
def plot_clusters_aligned_colors(X_pca, true_labels, remapped_pred_labels, species_names):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 定义固定的颜色列表（对应真实标签0,1,2）
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # 蓝、橙、绿

    # 左图：真实标签
    for label_id in np.unique(true_labels):
        mask = (true_labels == label_id)
        ax1.scatter(X_pca[mask, 0], X_pca[mask, 1],
                    c=colors[label_id], label=species_names[label_id], edgecolor='k')
    ax1.set_title('True Labels (PCA-reduced space)')
    ax1.set_xlabel('Principal Component 1')
    ax1.set_ylabel('Principal Component 2')
    ax1.legend()

    # 右图：重映射后的聚类标签（颜色与真实标签对齐）
    for label_id in np.unique(remapped_pred_labels):
        mask = (remapped_pred_labels == label_id)
        ax2.scatter(X_pca[mask, 0], X_pca[mask, 1],
                    c=colors[label_id], label=f'Cluster (majority = {species_names[label_id]})', edgecolor='k')
    ax2.set_title('K-Means Clusters (labels aligned with true classes)')
    ax2.set_xlabel('Principal Component 1')
    ax2.set_ylabel('Principal Component 2')
    ax2.legend()

    plt.tight_layout()
    plt.show()


# -----------------------------
# 7. 主程序
# -----------------------------
if __name__ == "__main__":
    # 加载数据
    X, y_true, species_names = load_iris_data("Iris.csv")

    # PCA降维
    X_pca, _, _ = pca(X, n_components=2)
    print("PCA降维完成 (4→2)")

    # K-Means聚类 (k=3)
    k = 3
    y_pred, _ = kmeans(X_pca, k, random_seed=42)
    print("K-Means聚类完成")

    # 重映射聚类标签，使得颜色与真实标签对齐
    y_pred_aligned, mapping = remap_cluster_labels(y_true, y_pred)

    # 可视化（颜色对齐）
    plot_clusters_aligned_colors(X_pca, y_true, y_pred_aligned, species_names)

    # 评估（使用原始聚类标签，因为重映射不影响评估指标）
    homo, compl, vmeas = homogeneity_completeness_vmeasure(y_true, y_pred)
    sil = silhouette_score(X_pca, y_pred)
    print("=" * 50)
    print("PCA降维后K-Means聚类结果评估 (k=3, 2D PCA)")
    print("=" * 50)
    print(f"均一性 (Homogeneity)   : {homo:.4f}")
    print(f"完整性 (Completeness)  : {compl:.4f}")
    print(f"V-measure              : {vmeas:.4f}")
    print(f"轮廓系数 (Silhouette)  : {sil:.4f}")
    print("=" * 50)

