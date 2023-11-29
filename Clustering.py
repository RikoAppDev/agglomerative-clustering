import math
import random

from constants import *
from tqdm import tqdm
from itertools import combinations


class Clustering:
    def __init__(self, amount, cluster_count, seed):
        self.cluster_count = cluster_count
        self.clusters = []
        self.distance_matrix = []
        self.centroids = []
        self.generate_places_progress_bar = tqdm(
            desc="Generating points", total=amount + 20, unit="point"
        )
        self.init_points = self.generate_init_points(int(amount), seed)
        self.all_points = self.init_points[:]
        self.other_points = self.generate_other_points()
        self.colors = set(COLORS)

        self.agglomerative_clustering()

    def agglomerative_clustering(self):
        progress_bar = tqdm(
            desc="Agglomerative clustering", total=OTHER_POINTS + INITIAL_POINTS - self.cluster_count, unit="point"
        )

        while len(self.clusters) > self.cluster_count:
            # Find the two closest clusters
            min_distance = float('inf')
            merge_indices = (0, 1)

            for i, j in combinations(range(len(self.clusters)), 2):
                distance = self.calculate_cluster_distance(self.clusters[i], self.clusters[j])
                if distance < min_distance:
                    min_distance = distance
                    merge_indices = (i, j)

            # Merge the two closest clusters
            merged_cluster = self.clusters[merge_indices[0]] + self.clusters[merge_indices[1]]
            del self.clusters[merge_indices[1]]
            self.clusters[merge_indices[0]] = merged_cluster

            # Update the distance matrix
            self.update_distance_matrix(merge_indices)
            progress_bar.update(1)

        progress_bar.close()
        self.centroids = [self.calculate_cluster_centroid(cluster) for cluster in self.clusters]

    def calculate_cluster_distance(self, cluster1, cluster2):
        total_distance = 0
        pair_count = 0

        for point1 in cluster1:
            for point2 in cluster2:
                total_distance += self.calculate_distance(point1, point2)
                pair_count += 1

        return total_distance / pair_count

    def update_distance_matrix(self, merged_indices):
        # Update the distance matrix after merging clusters
        new_cluster_index = merged_indices[0]
        distances_to_new_cluster = []

        for i in range(len(self.clusters)):
            if i != new_cluster_index:
                distance = self.calculate_cluster_distance(self.clusters[new_cluster_index], self.clusters[i])
                distances_to_new_cluster.append(distance)

        # Remove the old distances related to the merged clusters
        self.distance_matrix = [row[:merged_indices[1]] + row[merged_indices[1] + 1:] for row in self.distance_matrix]
        del self.distance_matrix[merged_indices[1]]

    def calculate_cluster_centroid(self, cluster):
        points_amount = len(cluster)
        x = y = 0

        for point in cluster:
            x += point[0]
            y += point[1]

        x /= points_amount
        y /= points_amount

        centroid = (x, y)
        return centroid

    def evaluate_cluster(self, i, cluster, color):
        centroid = self.centroids[i]
        summary = 0
        for point in cluster:
            summary += self.calculate_distance(point, centroid)

        avg_distance = summary / len(cluster)
        if avg_distance > 500:
            print(
                f"❌ cluster number: {i} | ⭕ average point distance from centroid: {avg_distance} | 🎨 {color}")
        else:
            print(
                f"✅ cluster number: {i} | ⭕ average point distance from centroid: {avg_distance} | 🎨 {color}")

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
            self.distance_matrix.append(self.get_new_row(point))
            self.generate_places_progress_bar.update(1)

        return points

    def generate_other_points(self):
        points = []

        for i in range(OTHER_POINTS):
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
            self.distance_matrix.append(self.get_new_row(point))
            self.generate_places_progress_bar.update(1)

        self.generate_places_progress_bar.close()
        return points
