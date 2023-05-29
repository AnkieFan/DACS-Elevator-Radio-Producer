import math

def get_tfidf(lyrics_tokens:list, n_gram = (1,1)):
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

def expand_ngram_list(lyrics_tokens:list, n_gram:tuple):
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
    lyrics = [['come', 'on', 'harry', 'we', 'want', 'to', 'say', 'goodnight', 'to', 'you'], ['holding', 'me', 'back'], ['gravity', 'holding', 'me', 'back'], ['i', 'want', 'you', 'to', 'hold', 'out', 'palm', 'of', 'your', 'hand'], ['why', 'do', 'not', 'we', 'leave', 'it', 'at', 'that'], ['nothing', 'to', 'say'], ['when', 'everything', 'gets', 'in', 'way'], ['seems', 'you', 'can', 'not', 'be', 'replaced'], ['and', 'i', 'am', 'one', 'who', 'will', 'stay', 'oh-oh-oh'], ['in', 'this', 'world', 'it', 'just', 'us'], ['you', 'know', 'it', 'not', 'same', 'as', 'it', 'was'], ['in', 'this', 'world', 'it', 'just', 'us'], ['you', 'know', 'it', 'not', 'same', 'as', 'it', 'was'], ['as', 'it', 'was', 'as', 'it', 'was'], ['you', 'know', 'it', 'not', 'same'], ['answer', 'phone'], ['``', 'harry', 'you', 'are', 'no', 'good', 'alone'], ['why', 'are', 'you', 'sitting', 'at', 'home', 'on', 'floor'], ['what', 'kind', 'of', 'pills', 'are', 'you', 'on', '``'], ['ringing', 'bell'], ['and', 'nobody', 'coming', 'to', 'help'], ['your', 'daddy', 'lives', 'by', 'himself'], ['he', 'just', 'wants', 'to', 'know', 'that', 'you', 'are', 'well', 'oh-oh-oh'], ['you', 'might', 'also', 'like'], ['in', 'this', 'world', 'it', 'just', 'us'], ['you', 'know', 'it', 'not', 'same', 'as', 'it', 'was'], ['in', 'this', 'world', 'it', 'just', 'us'], ['you', 'know', 'it', 'not', 'same', 'as', 'it', 'was'], ['as', 'it', 'was', 'as', 'it', 'was'], ['you', 'know', 'it', 'not', 'same'], ['go', 'home', 'get', 'ahead', 'light-speed', 'internet'], ['i', 'do', 'not', 'want', 'to', 'talk', 'about', 'way', 'that', 'it', 'was'], ['leave', 'america', 'two', 'kids', 'follow', 'her'], ['i', 'do', 'not', 'want', 'to', 'talk', 'about', 'who', 'doing', 'it', 'first'], ['hey'], ['as', 'it', 'was'], ['you', 'know', 'it', 'not', 'same', 'as', 'it', 'was'], ['as', 'it', 'was', 'as', 'it', 'was', 'embed']]
    print(get_tfidf(lyrics, n_gram=(1,3))[1].items(), key=lambda x: x[1], reverse=True)
