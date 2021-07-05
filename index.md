# Abstract

We introduce the first large scale dataset and benchmark for non-categorical annotation and clustering of 3D CAD models. We use the geometric data of the ABC dataset, and we develop an interface to allow expert mechanical engineers to efficiently annotate pairwise CAD model similarities, which we use to evaluate the performance of seven baseline deep clustering methods. Our dataset contains a manually annotated subset of 22,968 shapes, and 252,648 annotations. Our dataset is the first to directly target deep clustering algorithm for geometric shapes, and we believe it will be an important building block to analyze and utilize the massive 3D shape collections that are starting to appear in deep geometric computing. Our results suggest that, differently from the already mature shape classification algorithms, deep clustering algorithms for 3D CAD models are at their infancy and there is much room for improving their performance

# Dataset

| File Name | Description |
| ------ | ------ |
| [similarity-#.npz](https://drive.google.com/drive/folders/1bv9QmKpPRyfGzLaj6DdND6K4M4KnfiRS?usp=sharing) | The annotation matrix for the dataset. There are three .npz files, and each is corresponding to one of our three annotators |
| [obj.csv](https://drive.google.com/file/d/1sgaH3VNHSrvRVITx35pAcol_9Vk86Wyy/view?usp=sharing) | row x or column x of the similarity.npz matrix corresponds to the object ID in the x position in the csv file |
| [group.csv](https://drive.google.com/file/d/11CZyD7Ts4JT3G3VjckrSsxBvZ3Z-iqz6/view?usp=sharing) | Object ID for initial groups for users to annotate |
| [data.json](https://drive.google.com/file/d/17Htwq1QGgt5k-e1rTdabKiIMhDUVsim4/view?usp=sharing) | The annotation. The similarities fields shows the grouping that annotator believe each group shares same features. The cluster ID field is corresponding to group.csv. |
