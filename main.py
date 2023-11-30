import random
from tkinter import *

from Clustering import Clustering
from constants import *


def recalculate_position(value):
    resize_value = ACTUAL_WINDOW_SIZE / VIRTUAL_WINDOW_SIZE
    return resize_value * value


def is_color_dark(hex_color):
    # Convert hex to RGB
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)

    # Calculate luminance (perceived brightness)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b

    # You can adjust the luminance threshold as needed
    luminance_threshold = 128

    # Return True if the color is considered dark, False otherwise
    return luminance < luminance_threshold


def show_clustering_point(point, number, w_map, c):
    # Check if the cluster color is dark
    contrast_color = "white" if is_color_dark(c) else "black"

    w_map.create_oval(
        recalculate_position(point[0]) - POINT_DIAMETER * 2,
        recalculate_position(point[1]) - POINT_DIAMETER * 2,
        recalculate_position(point[0]) + POINT_DIAMETER * 2,
        recalculate_position(point[1]) + POINT_DIAMETER * 2,
        outline=contrast_color, fill=c
    )
    w_map.create_text(
        recalculate_position(point[0]),
        recalculate_position(point[1]), text=number,
        fill=contrast_color,
        font=f'"Comic Sans MS" {POINT_DIAMETER * 2} normal'
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


def handle_points_number_input():
    while True:
        points = input("🔢 Input number of points >> ")
        if points.isdigit():
            if int(points) >= 0:
                return int(points)
            else:
                print("‼️ Error ‼️\n\t- Number of points must be positive")
        else:
            print("‼️ Error ‼️\n\t- Input numeric value")


def handle_clustering_type_input():
    while True:
        option = input("⚙️ Choose clustering type using centroid 1️⃣ or medoid 2️⃣ >> ")
        if option.isdigit():
            if int(option) in [1, 2]:
                return int(option)
            else:
                print(f"‼️ Error ‼️\n\t- Clustering type {option} not supported")
        else:
            print("‼️ Error ‼️\n\t- Clustering type must be numeric value")


if __name__ == '__main__':
    seed = input("Input world seed 🫘 >> ")
    amount_of_clusters = number_of_clusters()
    clustering_type = handle_clustering_type_input()
    amount_of_points = handle_points_number_input()

    clustering = Clustering(amount_of_points, amount_of_clusters, clustering_type, seed)
    clusters: list = clustering.clusters
    centroids: list = clustering.clustering_points

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
        show_clustering_point(centroids[i], i, world_map, color)
        clustering.evaluate_cluster(i, cluster, color)

    print("\nℹ️ INFO: RESULT IS DISPLAYED IN WINDOW\n\t- Clustering")
    mainloop()
