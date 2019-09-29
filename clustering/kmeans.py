from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    if len(points) == 0:
        raise ValueError("List of points cannot be empty")

    mean = []
    for j in range(len(points[0])):
        sum = 0
        for i in range(len(points)):
            sum += points[i][j] 
        mean.append(sum/len(points))
    return mean


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    clusters = {}
    for assignment,point in zip(assignments, data_set):
        if assignment not in clusters:
            clusters[assignment] = []
        clusters[assignment].append(point)
    centers = []
    for _,points in clusters.items():
        centers.append(point_avg(points))
    return centers


def assign_points(data_points, centers):
    """
    Accepts a list of points and centers of desired
    clusters,
    Returns a list of the indices of the center 
    which is closest to each point, in order
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    dist = 0
    for i in range(len(a)):
        dist += (a[i] - b[i]) ** 2
    dist = dist ** 0.5
    return dist


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    points = []
    indices = random.sample(range(len(data_set)), k)
    for index in indices:
        points.append(data_set[index])
    return points


def get_list_from_dataset_file(dataset_file):
    """
    Accepts the file destination for a csv file 
    containing the data to be clustered,
    Returns a list of the data points (which are
    lists themselves)
    """
    data_set = []
    with open(dataset_file, newline = '') as csvfile:
        data_reader = csv.reader(csvfile)
        for row in data_reader:
            data_set.append([float(r) for r in row])
    return data_set


def cost_function(clustering):
    """
    Computes the cost function for a particular
    clustering. In this case the cost is simply
    the sum of the distance of all points in a 
    cluster and the center of the cluster.
    Returns a float of the cost
    """
    cost = 0
    for _, points in clustering.items():
        centroid = point_avg(points)
        for point in points:
            cost += distance(point, centroid)
    return cost
        


def k_means(dataset_file, k):
    """
    Accepts a csv file of a dataset and a value of k,
    computes k-means clustering using Lloyd's algo.
    Returns dict with cluster label as key, list
    of points in cluster as value. This is a wrapper
    for the individual helper functions above.
    """
    dataset = get_list_from_dataset_file(dataset_file)
    
    if dataset == []:
        raise ValueError("Dataset cannot be empty")
    elif k <= 0 or k > len(dataset):
        raise ValueError("k must be greater than zero and " +
                         "smaller than the dataset.")
    
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
