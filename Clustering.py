import math
import random

from constants import *
from tqdm import tqdm


class Clustering:
    def __init__(self, amount, cluster_count, clustering_type, seed):
        self.amount = amount
        self.cluster_count = cluster_count
        self.clustering_type = clustering_type
        if clustering_type == 1:
            self.clustering_point = self.calculate_cluster_centroid
        else:
            self.clustering_point = self.calculate_cluster_medoid
        self.clusters = []
        self.distance_matrix = []
        self.clustering_points = []
        self.generate_places_progress_bar = tqdm(
            desc="Generating points", total=amount + 20, unit="point"
        )
        self.init_points = self.generate_init_points(int(INITIAL_POINTS), seed)
        self.all_points = self.init_points[:]
        self.other_points = self.generate_other_points()
        self.colors = set(COLORS)

        self.agglomerative_clustering()

    def agglomerative_clustering(self):
        progress_bar = tqdm(
            desc="Agglomerative clustering", total=self.amount + INITIAL_POINTS - self.cluster_count, unit="cluster"
        )

        while len(self.clusters) > self.cluster_count:
            # Find the two closest clusters
            min_distance = float('inf')
            merge_indices = (0, 1)

            for i in range(len(self.distance_matrix)):
                for j in range(i):
                    if self.distance_matrix[i][j] < min_distance:
                        min_distance = self.distance_matrix[i][j]
                        merge_indices = (j, i)

            # Merge the two closest clusters
            self.clusters[merge_indices[0]].extend(self.clusters.pop(merge_indices[1]))

            # Merge clustering points
            self.clustering_points[merge_indices[0]] = self.clustering_point(self.clusters[merge_indices[0]])
            del self.clustering_points[merge_indices[1]]

            # Update the distance matrix
            self.update_distance_matrix(merge_indices)
            progress_bar.update(1)

        progress_bar.close()

    def update_distance_matrix(self, merged_indices):
        # Update the distance matrix after merging clusters
        new_cluster_index = merged_indices[0]
        distances_to_new_cluster = []

        for i in range(len(self.clusters)):
            if i != new_cluster_index:
                distance = self.calculate_distance(self.clustering_points[new_cluster_index], self.clustering_points[i])
                distances_to_new_cluster.append(distance)

        # Remove the old distances related to the merged clusters
        del self.distance_matrix[merged_indices[1]]
        for i in range(merged_indices[1] + 1, len(self.distance_matrix)):
            del self.distance_matrix[i][merged_indices[1]]

        # Update distance matrix to the merged cluster
        new_row_distances = distances_to_new_cluster[:merged_indices[0]]
        self.distance_matrix[merged_indices[0]] = new_row_distances + [0]

        # Update distance matrix from the merged cluster
        for i in range(merged_indices[0] + 1, len(self.distance_matrix)):
            self.distance_matrix[i][new_cluster_index] = distances_to_new_cluster[i - 1]

    @staticmethod
    def calculate_cluster_centroid(cluster):
        points_amount = len(cluster)
        x = y = 0

        for point in cluster:
            x += point[0]
            y += point[1]

        x /= points_amount
        y /= points_amount

        centroid = (x, y)
        return centroid

    def calculate_cluster_medoid(self, cluster):
        min_sum_distance = float('inf')
        medoid = None

        for p1 in cluster:
            sum_distance = 0
            for p2 in cluster:
                sum_distance += self.calculate_distance(p1, p2)

            if sum_distance < min_sum_distance:
                min_sum_distance = sum_distance
                medoid = p1

        return medoid

    def evaluate_cluster(self, i, cluster, color):
        centroid = self.clustering_points[i]
        summary = 0
        for point in cluster:
            summary += self.calculate_distance(point, centroid)

        avg_distance = summary / len(cluster)

        clustering_type = "centroid" if self.clustering_type == 1 else "medoid"

        if avg_distance > 500:
            print(
                f"❌ cluster number: {i} | ⭕ average point distance from {clustering_type}: {avg_distance} | 🎨 {color}")
        else:
            print(
                f"✅ cluster number: {i} | ⭕ average point distance from {clustering_type}: {avg_distance} | 🎨 {color}")

    def get_new_row(self, point):
        return [self.calculate_distance(point, cluster[0]) for cluster in self.clusters]

    @staticmethod
    def calculate_distance(p1, p2):
        return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    @staticmethod
    def check_initial_point_collision(x, y, initial_points: list):
        for p in initial_points:
            if (p[0] - POINT_DIAMETER - GAP < x < p[0] + POINT_DIAMETER + GAP and
                    p[1] - POINT_DIAMETER - GAP < y < p[1] + POINT_DIAMETER + GAP):
                return True

        return False

    def generate_init_points(self, count: int, seed: int):
        random.seed(seed)
        points = []

        while count != 0:
            count -= 1

            x = random.randint(GAP, VIRTUAL_WINDOW_SIZE - (POINT_DIAMETER + GAP))
            y = random.randint(GAP, VIRTUAL_WINDOW_SIZE - (POINT_DIAMETER + GAP))

            if self.check_initial_point_collision(x, y, points):
                count += 1
                continue

            point = (x, y)
            points.append(point)
            self.clusters.append([point])
            self.clustering_points.append(self.clustering_point([point]))
            self.distance_matrix.append(self.get_new_row(point))
            self.generate_places_progress_bar.update(1)

        return points

    def generate_other_points(self):
        points = []

        for i in range(self.amount):
            random_created_point = random.choice(self.all_points)

            x_offset = random.randint(
                max(-100, -random_created_point[0]),
                min(100, VIRTUAL_WINDOW_SIZE - POINT_DIAMETER - random_created_point[0])
            )

            y_offset = random.randint(
                max(-100, -random_created_point[1]),
                min(100, VIRTUAL_WINDOW_SIZE - POINT_DIAMETER - random_created_point[1])
            )

            point = (random_created_point[0] + x_offset, random_created_point[1] + y_offset)
            points.append(point)
            self.all_points.append(point)
            self.clusters.append([point])
            self.clustering_points.append(self.clustering_point([point]))
            self.distance_matrix.append(self.get_new_row(point))
            self.generate_places_progress_bar.update(1)

        self.generate_places_progress_bar.close()
        return points
