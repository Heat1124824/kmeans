#using Plots
function euclidean_distance(p1, p2)
    d = sqrt(sum((p1[1] - p2[1]) .^ 2))
    return d
end

function cluster(pts, center)
    num_pts = size(pts, 1)
    num_clusters = size(center, 1)
    clusters = zeros(Int, num_pts)
    cluster_in_pts = [[] for _ in 1:num_clusters]
    cnt = 1
    
    for i in 1:num_pts
        min_distance = Inf
        min_cluster = 0
        for j in 1:num_clusters
            distance = euclidean_distance(pts[i,:], center[j,:])
            if distance < min_distance
                min_distance = distance
                min_cluster = j
            end
        end
        clusters[i] = min_cluster #closest_idx in python ver
    end
    for k in clusters
        push!(cluster_in_pts[k], pts[cnt])
        cnt +=1
    end
    return clusters, cluster_in_pts
end

function update_center(pts, clusters, k)
    m = size(pts, 1)
    centroids = zeros(k, 2)
    summation = zeros(k)
    for i in 1:m
            cl = clusters[i]
            centroids[cl, :] .+= pts[i, 1]
            summation[cl] += 1      
    end
    for j in 1:k
        if summation[j] != 0
            centroids[j, :] /= summation[j]
        end
    end
    centroids = [row[:] for row in eachrow(centroids)]
    return centroids 
end

function kmeanss(pts, center, max_it=100)
    k = size(center, 1)
    cluster_in_pts = nothing
    distortions = []
    for _ in 1:max_it
        clusters, cluster_in_pts = cluster(pts, center)
        new_centroids = update_center(pts, clusters, k)
        push!(distortions, distance_to_centroid(cluster_in_pts, new_centroids, length(pts)))
        println(distortions)
        if new_centroids == center
            break
        end
        center = new_centroids
    end
    return cluster_in_pts, center, distortions
end

function distance_to_centroid(clusters, centroids, avg)
    clusters = [[i for i in a] for a in clusters]
    n = size(centroids, 1)
    sum_distances = 0
    for (i, cl) in enumerate(clusters)
        for j in 1:length(cl)
            sum_distances += euclidean_distance(cl[j,:], centroids[i,:])
        end
    end
    return sum_distances / avg
end

pts = [[2,5],[3,2],[3,3],[3,4],[4,3],
       [4,4],[6,3],[6,4],[6,6],[7,2],
       [7,5],[7,6],[7,7],[8,6],[8,7]]
center = [[2,2],[4,6],[6,5],[8,8]]

clusters, new_center, distortion = kmeanss(pts, center)
println("Clusters: ", clusters)
println("New Centroids: ", new_center)
print("Distortions: ", distortion)