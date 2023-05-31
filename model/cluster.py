import gensim.downloader
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from adjustText import adjust_text
from collections import Counter
from sklearn.decomposition import PCA

def generate_word_list(df, word_no = 1):
    words = []
    for i in range(1,word_no+1):
        words.extend(df[f'topic{i}'])
    return words

def plot_one_per_song(df, cluster_no = 5, wv_model = None):
    words = generate_word_list(df, 1)
    wordvector, new_words, count = get_infos(Counter(words), wv_model)
    plot_results(wordvector, new_words, count, cluster_no)

def plot_five_per_song(df, cluster_no = 5, wv_model = None):
    words = generate_word_list(df, 5)
    c = Counter(words)
    c = sorted(c.items(), key=lambda x: x[1], reverse=True)
    wordvector, new_words, count = get_infos(dict(c[:100]), wv_model)
    plot_results(wordvector, new_words, count, cluster_no)

def get_cluster_without_project(words, cluster_no = 5):
    wordvector, new_words, count = get_infos(words)
    clf = KMeans(n_clusters=cluster_no, init="k-means++")
    clf.fit(wordvector)

    labels=clf.labels_

    classCollects={}
    for i in range(cluster_no):
        classCollects[i] = []

    for i in range(len(new_words)):
        if(labels[i] in list(classCollects.keys())):
            classCollects[labels[i]].append(list(new_words)[i])

    return classCollects

def plot_results(wordvector, new_words, count, cluster_no):
    '''
    Use PCA to project word vector to be 2 dimensional

    '''
    pca = PCA(n_components=2)
    result = pca.fit_transform(wordvector)
    fig, ax = plt.subplots(figsize=(10, 10))
    k_model = KMeans(n_clusters= cluster_no, random_state=0, init="k-means++")
    k_model = k_model.fit(result)  

    plt.scatter(result[:, 0], result[:, 1], c = k_model.labels_, s = count, alpha=0.5)
    plt.scatter(k_model.cluster_centers_[: , 0],k_model.cluster_centers_[:, 1], color = "red") 

    new_texts = [plt.text(x, y, text, fontsize=12) for x, y, text in zip(result[:, 0], result[:, 1], new_words)]
    adjust_text(new_texts, 
            only_move={'text': 'x'},
            arrowprops=dict(arrowstyle='-', color='grey'))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def get_infos(c, wv_model):
    if(wv_model == None):
        wv_model = gensim.downloader.load('word2vec-google-news-300')
    
    wordvector = []
    new_words = []
    count = []
    for key in c.keys():
        try:
            wordvector.append(wv_model[key])
            new_words.append(key)
            count.append(c[key]*80)
        except:
            print(f'word {key} dose not have vector')
            continue
    return wordvector, new_words, count

if __name__ == "__main__":
    df = pd.read_csv("./result/2019.csv")
    print(plot_one_per_song(df))