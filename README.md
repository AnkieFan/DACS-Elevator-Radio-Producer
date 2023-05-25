# DACS-Elevator-Radio-Producer
Find the topics of lyrics in the top 100 songs and analyze how they change over time by clustering the topics of each song and visualizing the clustering results.

## HOW TO USE
**暂时不用跑任何代码，但如果你想试试的话，最好用conda的虚拟环境跑**  
创建虚拟环境：`conda create -n nlp_project python=3.9`  
激活虚拟环境：`conda activate nlp_project`  

**之后依赖包还会更新，每一次代码更新都最好运行一次**  
安装依赖包: `pip install -r requirements.txt`    

## Proposal
### Motivation
The success of a pop song depends on many factors. Although the music charts are constantly changing, the types of topics included in the songs are limited, such as emotions, social issues, self and cultural identity, etc. We want to design a model that analyzes lyric themes to classify the theme of popular songs. We are curious whether the distribution of these topics in the list are immutable or changes in some way.

### Basic idea:
1. Get the hottest 100 songs for a year and their lyrics(optional: a playlist from user input)
2. Get a topic for each song (LDA, BERTopic)
3. Cluster the topics for 100 songs this year (word2vec, k-means)
4. Visualize the clustering results of each year (PCA/t-SNE, plot)

### Evaluation Metrics
C_V: a combined metric of normalized pointwise mutual information (NPMI) and cosine similarity (Mifrah and Benlahmar, 2020). We will call the gensim.models.coherencemodel library with topics, texts and dictionary in our model.

## Report:
+ Topics of 100 songs
  + Statistic number of topics
  + Word clustering of topics
+ Emotional Analysis of 100 lyrics
  + Statistic number of emotions
+ Visualization
+ Error handling
