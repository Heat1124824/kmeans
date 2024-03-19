import matplotlib.pyplot as plt

def dist(p1, p2):
    squared_dis = 0
    for i in range (len(p1)):
        squared_dis += (p1[i] - p2[i])**2
    return (squared_dis) ** 0.5

def cluster(pts, center):
    clusters = []
    for _ in range(len(center)):
        clusters.append([])
    for p in pts:
        distances = []
        for c in center:
            distances.append(dist(p, c))
        closest_idx = distances.index(min(distances))
        clusters[closest_idx].append(p)
    return clusters

def update_center(clusters):
    centroids = []
    for cluster in clusters:
        if cluster:
            ce = []
            for i in range(len(cluster[0])):
                summation = 0
                for p in cluster:
                    summation += p[i]
                ce.append(summation / len(cluster))
            centroids.append(ce)
    return centroids

def kmeans(pts, center, max_it=100):
    distortions = []
    for _ in range(max_it):
        clusters = cluster(pts, center)
        new_center = update_center(clusters)
        distortions.append(distance_to_centroid(clusters, new_center, len(pts)))
        if new_center == center:
            break
        center = new_center
    return clusters, center, distortions

def distance_to_centroid(clusters, centroids, avg):
    sum_distances = 0
    for i, cl in enumerate(clusters):
        for j in range (0, len(cl)):
            sum_distances += dist(cl[j],centroids[i])
    return sum_distances / avg


pts = [[2,5],[3,2],[3,3],[3,4],[4,3],
       [4,4],[6,3],[6,4],[6,6],[7,2],
       [7,5],[7,6],[7,7],[8,6],[8,7]]
center = [[2,2],[4,6],[6,5],[8,8]]

clusters, new_center, distortions = kmeans(pts, center)
print(distortions)

colors = ['r', 'g', 'b', 'y']
for i, cluster in enumerate(clusters):
    n_cluster = []
    for p in cluster:
        n_pt = []
        for j in range(len(p)):
            n_pt.append(p[j])
        n_cluster.append(n_pt)
    cluster = n_cluster
    x_cluster = []
    y_cluster = []
    for p in cluster:
        x_cluster.append(p[0])
        y_cluster.append(p[1])
    plt.scatter(x_cluster, y_cluster, c=colors[i], label=f'Cluster {i+1}')
n_center = []
for p in new_center:
    new_point = []
    for j in range(len(p)):
        new_point.append(p[j])
    n_center.append(new_point)
new_center = n_center

x_newCenter = []
y_newCenter = []

for p in new_center:
    x_newCenter.append(p[0])
    y_newCenter.append(p[1])
plt.scatter(x_newCenter, y_newCenter, c='black', marker='x', label='Centroids')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('K-means')
plt.legend()
plt.show()

plt.plot(distortions, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('D-bar')
plt.title('Elbow Method')
plt.grid(True)
plt.show()