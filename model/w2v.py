from gensim.models import Word2Vec

def train_wvmodel(lyrics_tokens:list[list[str]]):
    return Word2Vec(sentences=lyrics_tokens, vector_size=300, min_count=1, workers=4)

def save_wvmodel(model):
    model.save("./result/our_model.model")