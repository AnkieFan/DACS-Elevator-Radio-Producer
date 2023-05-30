import math

def get_n_words(lyrics_tokens:list[list[str]], n_gram = (1,1), word_no = 5):
    return get_tfidf(lyrics_tokens, n_gram)[1][:word_no]

def get_tfidf(lyrics_tokens:list[list[str]], n_gram = (1,1)):
    '''

    Args:
    lyrics_tokens: a list of sentences(list containing word tokens)
    n_gram: a tuple which is the range of n_gram

    Returns:
    A tuple containing 2 dictionaries. The first one are term frequency of words. The second one are tfidf values of words.
    '''
    if(n_gram != (1,1)): lyrics_tokens = [expand_ngram_list(lyrics_tokens=sent, n_gram=n_gram) for sent in lyrics_tokens]

    count = {}
    tfidf = {}
    total_length = 0
    for sentence in lyrics_tokens:
        total_length += len(sentence)

        for word in sentence:
            count[word] = count[word] + 1 if(word in count) else 1

        l = list(set(sentence))
        for word in l:
            tfidf[word] = tfidf[word] + 1 if(word in tfidf) else 1
    
    for word in tfidf.keys():
        try:
            tf = count[word]
            idf = math.log(len(lyrics_tokens) / (tfidf[word]+1), math.e)
            #print(f'word {word} with tf = {tf} and idf = {idf}')
        except ValueError:
            print("math domain error on:",word)
            continue

        tfidf[word] = tf*idf

    return (sorted(count.items(), key=lambda x: x[1], reverse=True), sorted(tfidf.items(), key=lambda x: x[1], reverse=True))

def expand_ngram_list(lyrics_tokens:list[str], n_gram:tuple):
    new_list = []
    start, end = n_gram
    
    for i in range(start, end+1):
        if(i > len(lyrics_tokens)):
            break
        for j in range(len(lyrics_tokens)-i+1):
            new_item = ' '.join(lyrics_tokens[j:j+i])
            new_list.append(new_item)
    
    return new_list

if __name__ == '__main__':
    lyrics = [['it', 'been', 'long', 'day', 'without', 'you', 'my', 'friend'], ['and', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['we', 'have', 'come', 'long', 'way', 'from', 'where', 'we', 'began'], ['oh', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['when', 'i', 'see', 'you', 'again'], ['dang', 'who', 'knew'], ['all', 'planes', 'we', 'flew'], ['good', 'things', 'we', 'have', 'been', 'through'], ['that', 'i', 'will', 'be', 'standing', 'right', 'here', 'talking', 'to', 'you'], ['bout', 'another', 'path'], ['i', 'know', 'we', 'loved', 'to', 'hit', 'road', 'and', 'laugh'], ['but', 'something', 'told', 'me', 'that', 'it', 'would', 'not', 'last'], ['had', 'to', 'switch', 'up'], ['look', 'at', 'things', 'different', 'see', 'bigger', 'picture'], ['those', 'were', 'days'], ['hard', 'work', 'forever', 'pays'], ['now', 'i', 'see', 'you', 'in', 'better', 'place', 'see', 'you', 'in', 'better', 'place'], ['uh'], ['how', 'can', 'we', 'not', 'talk', 'about', 'family', 'when', 'family', 'all', 'that', 'we', 'got'], ['everything', 'i', 'went', 'through', 'you', 'were', 'standing', 'there', 'by', 'my', 'side'], ['and', 'now', 'you', 'gon', 'be', 'with', 'me', 'for', 'last', 'ride'], ['it', 'been', 'long', 'day', 'without', 'you', 'my', 'friend'], ['and', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['we', 'have', 'come', 'long', 'way', 'from', 'where', 'we', 'began'], ['oh', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['when', 'i', 'see', 'you', 'again'], ['you', 'might', 'also', 'like', 'aah', 'oh', 'aah', 'oh'], ['wooooh-oh-oh-oh-oh-oh'], ['yeah'], ['first', 'you', 'both', 'go', 'out', 'your', 'way'], ['and', 'vibe', 'is', 'feeling', 'strong'], ['and', 'what', 'small', 'turn', 'to', 'friendship'], ['a', 'friendship', 'turn', 'to', 'bond'], ['and', 'that', 'bond', 'will', 'never', 'be', 'broken'], ['the', 'love', 'will', 'never', 'get', 'lost'], ['and', 'when', 'brotherhood', 'come', 'first'], ['then', 'line', 'will', 'never', 'be', 'crossed'], ['established', 'it', 'on', 'our', 'own'], ['when', 'that', 'line', 'had', 'to', 'be', 'drawn'], ['and', 'that', 'line', 'is', 'what', 'we', 'reach'], ['so', 'remember', 'me', 'when', 'i', 'am', 'gone'], ['how', 'can', 'we', 'not', 'talk', 'about', 'family', 'when', 'family', 'all', 'that', 'we', 'got'], ['everything', 'i', 'went', 'through', 'you', 'were', 'standing', 'there', 'by', 'my', 'side'], ['and', 'now', 'you', 'gon', 'be', 'with', 'me', 'for', 'last', 'ride'], ['so', 'let', 'light', 'guide', 'your', 'way', 'yeah'], ['hold', 'every', 'memory', 'as', 'you', 'go'], ['and', 'every', 'road', 'you', 'take', 'will', 'always', 'lead', 'you', 'home', 'home'], ['it', 'been', 'long', 'day', 'without', 'you', 'my', 'friend'], ['and', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['we', 'have', 'come', 'long', 'way', 'from', 'where', 'we', 'began'], ['oh', 'i', 'will', 'tell', 'you', 'all', 'about', 'it', 'when', 'i', 'see', 'you', 'again'], ['when', 'i', 'see', 'you', 'again'], ['aah', 'oh', 'aah', 'oh'], ['wooooh-oh-oh-oh-oh-oh'], ['yeah'], ['when', 'i', 'see', 'you', 'again'], ['see', 'you', 'again'], ['when', 'i', 'see', 'you', 'again'], ['aah', 'oh', 'aah', 'oh'], ['wooooh-oh-oh-oh-oh-oh'], ['yeah'], ['when', 'i', 'see', 'you', 'againembed']]
    print(get_n_words(lyrics))
