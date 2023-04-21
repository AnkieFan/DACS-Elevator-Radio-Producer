# DACS-Elevator-Radio-Producer
Find the topics of lyrics in the top 100 songs and analyze how they change over time by clustering the topics of each song and visualizing the clustering results.

## Basic ideas
1. Get the hottest 100 songs for a year and their lyrics(optional: a playlist from user input)
2. Get a topic for each song (LDA, BERTopic)
3. Cluster the topics for 100 songs this year (word2vec, k-means)
4. Visualize the clustering results of each year (PCA/t-SNE, plot)
