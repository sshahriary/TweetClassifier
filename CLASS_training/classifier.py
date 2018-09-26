import nltk
import pickle
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize, word_tokenize

corpus = PlaintextCorpusReader("./CLASS_training", ".*\.txt")

files=corpus.fileids()

news_corpus = sports_corpus = music_corpus = entertainment_corpus = sciencetech_corpus = ""
news_count = sports_count = music_count = entertainment_count = sciencetech_count = 0
count = 0

for f in files:
    #check the first letter of file (H for ham and else for spam)
    if f[0] == 'n':
        #appending all text of hams into one variable
        news_corpus = corpus.raw(f) + news_corpus
        news_count += 1
    elif f[1] == 'p':
        #appending all text of spams into one variable
        sports_corpus = corpus.raw(f) + sports_corpus
        sports_count += 1
    elif f[0] == 'm':
        #appending all text of spams into one variable
        music_corpus = corpus.raw(f) + music_corpus
        music_count += 1
    elif f[0] == 'e':
        #appending all text of spams into one variable
        entertainment_corpus = corpus.raw(f) + entertainment_corpus
        entertainment_count += 1
    elif f[1] == 'c':
        #appending all text of spams into one variable
        sciencetech_corpus = corpus.raw(f) + sciencetech_corpus
        sciencetech_count += 1

#converting the string each to list for frequency distribution
word_list_news = news_corpus.split()
news_fd = nltk.FreqDist(word_list_news)

word_list_sports = sports_corpus.split()
sports_fd = nltk.FreqDist(word_list_sports)

word_list_music = music_corpus.split()
music_fd = nltk.FreqDist(word_list_music)

word_list_entertainment = entertainment_corpus.split()
entertainment_fd = nltk.FreqDist(word_list_entertainment)

word_list_sciencetech = sciencetech_corpus.split()
sciencetech_fd = nltk.FreqDist(word_list_sciencetech)

total_count = news_count + sports_count + music_count + entertainment_count + sciencetech_count
all_corpus = news_corpus + sports_corpus + music_corpus + entertainment_corpus + sciencetech_corpus
word_list_all_corpus = all_corpus.split()
all_corpus_fd = nltk.FreqDist(word_list_all_corpus)
#creating dictionary
model = {
 'news_count': news_count,
 'sports_count': sports_count,
 'music_count': music_count,
 'entertainment_count': entertainment_count,
 'sciencetech_count': sciencetech_count,
 'total_count': total_count,
 'news_fd': news_fd,
 'sports_fd': sports_fd,
 'music_fd': music_fd,
 'entertainment_fd': entertainment_fd,
 'sciencetech_fd': sciencetech_fd,
 'total_fd': all_corpus_fd,
}

print(model)

pickle.dump(model, open('categories.nb', 'wb'))
