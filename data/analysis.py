import matplotlib.pyplot as plt
import wordcloud
from nltk.corpus import stopwords


def plot_word_cloud(words):
    text = " ".join(words)
    wc = wordcloud.WordCloud(
                         width = 1000,
                         height = 700,
                         background_color='white',
                         stopwords=stopwords.words('english'))
    wc.generate(text)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()