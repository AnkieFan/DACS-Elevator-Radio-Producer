import math

def tfidf(lyrics_tokens:str, n_gram = 1):
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
            print(f'word {word} with tf = {tf} and idf = {idf}')
        except ValueError:
            print("math domain error on:",word)
            continue

        tfidf[word] = tf*idf

    return (count, tfidf)
    
if __name__ == '__main__':
    lyrics = [['lately', 'i', 'have', 'been', 'i', 'have', 'been', 'thinking'], ['i', 'want', 'you', 'to', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['when', 'morning', 'comes'], ['when', 'we', 'see', 'what', 'we', 'have', 'become'], ['in', 'cold', 'light', 'of', 'day', 'we', 'are', 'flame', 'in', 'wind'], ['not', 'fire', 'that', 'we', 'have', 'begun'], ['every', 'argument', 'every', 'word', 'we', 'can', 'not', 'take', 'back'], ['cause', 'with', 'all', 'that', 'has', 'happened'], ['i', 'think', 'that', 'we', 'both', 'know', 'way', 'that', 'this', 'story', 'ends'], ['then', 'only', 'for', 'minute'], ['i', 'want', 'to', 'change', 'my', 'mind'], ['cause', 'this', 'just', 'do', 'not', 'feel', 'right', 'to', 'me'], ['i', 'want', 'to', 'raise', 'your', 'spirits'], ['i', 'want', 'to', 'see', 'you', 'smile', 'but'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['lately', 'i', 'have', 'been', 'i', 'have', 'been', 'thinking'], ['i', 'want', 'you', 'to', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['you', 'might', 'also', 'like'], ['when', 'evening', 'falls'], ['and', 'i', 'am', 'left', 'there', 'with', 'my', 'thoughts'], ['and', 'image', 'of', 'you', 'being', 'with', 'someone', 'else'], ['well', 'it', 'eating', 'me', 'up', 'inside'], ['but', 'we', 'ran', 'our', 'course', 'we', 'pretended', 'we', 'are', 'okay'], ['now', 'if', 'we', 'jump', 'together', 'at', 'least', 'we', 'can', 'swim'], ['far', 'away', 'from', 'wreck', 'we', 'made'], ['then', 'only', 'for', 'minute'], ['i', 'want', 'to', 'change', 'my', 'mind'], ['cause', 'this', 'just', 'do', 'not', 'feel', 'right', 'to', 'me'], ['i', 'want', 'to', 'raise', 'your', 'spirits'], ['i', 'want', 'to', 'see', 'you', 'smile', 'but'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['lately', 'i', 'have', 'been', 'i', 'have', 'been', 'thinking'], ['i', 'want', 'you', 'to', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['so', 'i', 'will', 'go', 'i', 'will', 'go'], ['i', 'will', 'go', 'go', 'go'], ['so', 'i', 'will', 'go', 'i', 'will', 'go'], ['i', 'will', 'go', 'go', 'go'], ['lately', 'i', 'have', 'been', 'i', 'have', 'been', 'thinking'], ['i', 'want', 'you', 'to', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['even', 'though', 'i', 'might', 'not', 'like', 'this'], ['i', 'think', 'that', 'you', 'will', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['then', 'only', 'for', 'minute', 'only', 'for', 'minute'], ['i', 'want', 'to', 'change', 'my', 'mind'], ['cause', 'this', 'just', 'do', 'not', 'feel', 'right', 'to', 'me', 'right', 'to', 'me'], ['i', 'want', 'to', 'raise', 'your', 'spirits', 'wan', 'na', 'raise', 'your', 'spirits'], ['i', 'want', 'to', 'see', 'you', 'smile', 'but'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['know', 'that', 'means', 'i', 'will', 'have', 'to', 'leave'], ['lately', 'i', 'have', 'been', 'i', 'have', 'been', 'thinking'], ['i', 'want', 'you', 'to', 'be', 'happier', 'i', 'want', 'you', 'to', 'be', 'happier'], ['so', 'i', 'will', 'go', 'i', 'will', 'go'], ['i', 'will', 'go', 'go', 'go', 'embed']]
    print(sorted(tfidf(lyrics)[1].items(), key=lambda x: x[1], reverse=True))
