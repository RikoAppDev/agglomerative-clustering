import random
from tkinter import *

from Clustering import Clustering
from constants import *


def recalculate_position(value):
    resize_value = ACTUAL_WINDOW_SIZE / VIRTUAL_WINDOW_SIZE
    return resize_value * value


def show_centroids_points(point, w_map, c):
    w_map.create_oval(
        recalculate_position(point[0]) - POINT_DIAMETER,
        recalculate_position(point[1]) - POINT_DIAMETER,
        recalculate_position(point[0]) + POINT_DIAMETER,
        recalculate_position(point[1]) + POINT_DIAMETER,
        outline="black", fill=c
    )


def show_all_points(points, w_map, c):
    for point in points:
        w_map.create_oval(
            recalculate_position(point[0]) - POINT_DIAMETER / 2,
            recalculate_position(point[1]) - POINT_DIAMETER / 2,
            recalculate_position(point[0]) + POINT_DIAMETER / 2,
            recalculate_position(point[1]) + POINT_DIAMETER / 2,
            outline=c, fill=c
        )


def random_color(palette):
    c = random.choice(list(palette))
    colors.remove(c)
    return c


def number_of_clusters():
    while True:
        cluster_count = input("🔢 Input number of clusters (15 - 20) >> ")
        if cluster_count.isdigit():
            if 15 <= int(cluster_count) <= 20:
                return int(cluster_count)
            else:
                print("‼️ Error ‼️\n\t- Number of clusters out of range")
        else:
            print("‼️ Error ‼️\n\t- Input numeric value")


if __name__ == '__main__':
    seed = input("Input world seed 🫘 >> ")
    amount_of_clusters = number_of_clusters()

    clustering = Clustering(INITIAL_POINTS, amount_of_clusters, seed)
    clusters: list = clustering.clusters
    centroids: list = clustering.centroids

    root = Tk()
    root.attributes('-topmost', True)
    root.geometry(
        '%dx%d+%d+%d' % (ACTUAL_WINDOW_SIZE, ACTUAL_WINDOW_SIZE, root.winfo_screenwidth() - ACTUAL_WINDOW_SIZE - 10, 0))
    root.resizable(False, False)
    root.title("Clustering")

    world_map = Canvas(root, width=ACTUAL_WINDOW_SIZE, height=ACTUAL_WINDOW_SIZE)
    world_map.pack()

    colors = COLORS[:]
    print("\nCluster evaluation:")
    for i, cluster in enumerate(clusters):
        color = random_color(colors)
        show_all_points(cluster, world_map, color)
        show_centroids_points(centroids[i], world_map, color)
        clustering.evaluate_cluster(i, cluster, color)

    print("\nℹ️ INFO: RESULT IS DISPLAYED IN WINDOW\n\t- Clustering")
    mainloop()
