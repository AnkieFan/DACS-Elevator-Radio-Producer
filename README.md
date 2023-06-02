# DACS-Elevator-Radio-Producer
Find the topics of lyrics in the top 100 songs and analyze how they change over time by clustering the topics of each song and visualizing the clustering results.

## How to use
Install the dependencies: `pip install -r requirements.txt`    

## Dataset
Dataset are already gathered from the APIs.

## Proposal
### Motivation
The success of a pop song depends on many factors. Although the music charts are constantly changing, the keywords and underlying meanings included in the songs are limited, such as emotions, social issues, self and cultural identity, etc. We want to design a model that analyzes lyric themes to classify the theme of popular songs. We are curious whether the distribution of these topics in the list are immutable or changes in some way.

### Basic idea:
1. Get the hottest 100 songs for a year and their lyrics(optional: a playlist from user input)
2. Get a topic for each song (TF-IDF, KeyBERT)
3. Cluster the topics for 100 songs this year (word2vec, k-means)
4. Visualize the clustering results of each year (PCA/t-SNE, plot)

### Evaluation Metrics
C_umass: a combined metric of  combines document cooccurrence counts, one-preceding segmentation, and logarithmic conditional probability (Mifrah
and Benlahmar, 2020).
Cosine Similarity: score besed on the sentence embeddings generated from the ’all-mpnet-base-v2’ model, employing the SBERT SentenceTransformers library (Reimers and Gurevych, 2019) to encode both the title and relevant keywords into their respective embeddings.
