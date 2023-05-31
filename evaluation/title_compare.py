from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def get_score(df):
    avg_similarity = 0
    for row in df.iterrows():
        title = row[1]['name']
        title = title.split("_", 1)[1]

        words = []
        for i in range(1,6):
            words.append(row[1][f'topic{i}'])
        similarity = get_similarity(title, words)
        avg_similarity += similarity

        print(f'Song: {title}, Topics: {words}, Similarity:{similarity}')

    avg_similarity /= df.shape[0]
    return avg_similarity

def get_similarity(title:str, words:list):
    words = ' '.join(words)
    model = SentenceTransformer('all-mpnet-base-v2')
    sentence_embeddings = model.encode([title, words])
    return cosine_similarity([sentence_embeddings[0]],sentence_embeddings[1:])[0][0]
