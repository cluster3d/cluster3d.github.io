# Cluster3D: A Dataset and Benchmark for Clustering Non-Categorical 3D CAD Models

## Abstract
We introduce the first large scale dataset and benchmark for non-categorical annotation and clustering of 3D CAD models. We use the geometric data of the ABC dataset, and we develop an interface to allow expert mechanical engineers to efficiently annotate pairwise CAD model similarities, which we use to evaluate the performance of seven baseline deep clustering methods. Our dataset contains a manually annotated subset of 22,968 shapes, and 252,648 annotations. Our dataset is the first to directly target deep clustering algorithm for geometric shapes, and we believe it will be an important building block to analyze and utilize the massive 3D shape collections that are starting to appear in deep geometric computing. Our results suggest that, differently from the already mature shape classification algorithms, deep clustering algorithms for 3D CAD models are at their infancy and there is much room for improving their performance.

## Dataset
You can download the dataset via [our google drive link](https://drive.google.com/file/d/1F5MNIeYUi66CzjjxkaUEbgiwDMYALcTn/view?usp=sharing). This google drive folder contains three zip files: 
1. similarity.npz which contains the annotation matrix for the dataset
2. obj.csv such that row x or column x of the similarity.npz matrix corresponds to the object ID in the x position in the csv file.
