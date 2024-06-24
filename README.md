# Agglomerative Hierarchical Clustering

This project implements Agglomerative Hierarchical Clustering to cluster points in a 2D space using different methods:

1. Centroid-based Agglomerative Clustering
2. Medoid-based Agglomerative Clustering

## Assignment Overview

The project involves generating 20 random points in a 2D space and then expanding the dataset with 20,000 additional
points using a specified method. The goal is to develop clustering algorithms that partition the entire space into
clusters and evaluate their performance based on certain criteria.

## Implementation Details

The implementation includes:

- **Data Generation**: Random generation of initial points and subsequent points based on specific rules.
- **Clustering Algorithms**: Implementation of agglomerative clustering using both centroid and medoid as cluster
  centers.
- **Visualization**: Visualization of the resulting clusters in the 2D space for each clustering experiment.

## Algorithms Used

1. **Centroid-based Agglomerative Clustering**: Clusters are merged based on the centroid of the clusters.
2. **Medoid-based Agglomerative Clustering**: Clusters are merged based on the medoid of the clusters.

## Evaluation

The success of the clustering algorithms is evaluated based on the average distance of points within clusters from their
respective centers. A clustering is considered successful if no cluster has an average distance greater than 500.

## Documentation

The documentation includes:

- Detailed description of the algorithms used and data representation.
- Visualizations of multiple clustering experiments.
- Evaluation of results comparing different approaches.

For detailed documentation, please check [Technical Documentation](Dokumentacia_UI_P3.pdf) in the repository.

## User Interface

The user interface is divided into CLI and GUI:

- **CLI**: Allows users to set parameters such as seed, number of clusters, type of clustering (centroid or medoid), and
  number of points in the 2D space. Displays logs with cluster numbers and evaluations.
- **GUI**: Visualizes the final clusters using Tkinter, with each cluster represented by a unique random color. The
  centroid or medoid of each cluster is displayed as a larger point with the cluster number.
