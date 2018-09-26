import nltk
import pickle
import math
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import sent_tokenize, word_tokenize

corpus = PlaintextCorpusReader("./CLASS_test", ".*\.txt")

files = corpus.fileids()

file_corpus = ""

news_count_predicted = sports_count_predicted = music_count_predicted = entertainment_count_predicted = sciencetech_count_predicted = 0
news_count_correct = sports_count_correct = music_count_correct = entertainment_count_correct = sciencetech_count_correct = 0
news_count_actual = sports_count_actual = music_count_actual = entertainment_count_actual = sciencetech_count_actual = 0

with open('categories.nb', 'rb') as f:model = pickle.load(f)
news_prob = model['news_count']/(model['total_count'])
sports_prob = model['sports_count']/(model['total_count'])
music_prob = model['music_count']/(model['total_count'])
entertainment_prob = model['entertainment_count']/(model['total_count'])
sciencetech_prob = model['sciencetech_count']/(model['total_count'])

count = correct = 0
total_vocab = model['total_fd'].B()
print(total_vocab)
print('NEWS: ' + str(model['news_fd'].B()))
print('SPORTS: ' + str(model['sports_fd'].B()))
print('ENTERTAINMENT: ' + str(model['entertainment_fd'].B()))
print('MUSIC: ' + str(model['music_fd'].B()))
print('SCIENCE: ' + str(model['sciencetech_fd'].B()))

# go through each file
for f in files:
    file_news = math.log(news_prob)
    file_sports = math.log(sports_prob)
    file_music = math.log(music_prob)
    file_entertainment = math.log(entertainment_prob)
    file_sciencetech = math.log(sciencetech_prob)
    file_corpus=corpus.raw(f)
    word_list = file_corpus.split()
    # increment actual counts for recall
    if f[0] == 'n':
        news_count_actual += 1
    if f[1] == 'p':
        sports_count_actual += 1
    if f[0] == 'm':
        music_count_actual += 1
    if f[0] == 'e':
        entertainment_count_actual += 1
    if f[1] == 'c':
        sciencetech_count_actual += 1

# go through each word in the file
    for word in word_list:
        news_n= model['news_fd'].N()
        news_v= model['news_fd'].B()
        sports_n= model['sports_fd'].N()
        sports_v= model['sports_fd'].B()
        music_n= model['music_fd'].N()
        music_v= model['music_fd'].B()
        entertainment_n= model['entertainment_fd'].N()
        entertainment_v= model['entertainment_fd'].B()
        sciencetech_n= model['sciencetech_fd'].N()
        sciencetech_v= model['sciencetech_fd'].B()

        # calculate the respective probabilities
        cp_news= abs(math.log((model['news_fd'][word] +1) / (news_n + total_vocab)))
        file_news = file_news + cp_news
        cp_sports= abs(math.log((model['sports_fd'][word] +1) / (sports_n + total_vocab)))
        file_sports = file_sports + cp_sports
        cp_music= abs(math.log((model['music_fd'][word] +1) / (music_n + total_vocab)))
        file_music = file_music + cp_music
        cp_entertainment= abs(math.log((model['entertainment_fd'][word] +1) / (entertainment_n + total_vocab)))
        file_entertainment = file_entertainment + cp_entertainment
        cp_sciencetech= abs(math.log((model['sciencetech_fd'][word] +1) / (sciencetech_n + total_vocab)))
        file_sciencetech = file_sciencetech + cp_sciencetech

    max_count = min(file_news, file_sports, file_music, file_entertainment, file_sciencetech)
# calculates predicted count which is used for precision
# calculates correct count which is used for both precision and Recall
    if file_news == max_count:
        news_count_predicted += 1
        print(f + ' NEWS')
        if f[0] == 'n':
            correct += 1
            news_count_correct += 1
    elif file_sports == max_count:
        sports_count_predicted += 1
        print(f + ' SPORTS')
        if f[1] == 'p':
            correct += 1
            sports_count_correct += 1
    elif file_music == max_count:
        music_count_predicted += 1
        print(f + ' MUSIC')
        if f[0] == 'm':
            correct += 1
            music_count_correct += 1
    elif file_entertainment == max_count:
        entertainment_count_predicted += 1
        print(f + ' ENTERTAINMENT')
        if f[0] == 'e':
            correct += 1
            entertainment_count_correct += 1
    elif file_sciencetech == max_count:
        sciencetech_count_predicted += 1
        print(f + ' SCIENCE & TECH')
        if f[1] == 'c':
            correct += 1
            sciencetech_count_correct += 1
    else:
        print('ERROR!')
    # used for accuracy
    count += 1

# Uncomment line 118-136 for accuracy, precision, Recall and Fscores. 
# print('accuracy: ' + str(correct/count))
# print('News count | percentage:  ' + str(news_count_predicted) + ' | ' + str((news_count_predicted/count)))
# print('Sports count | percentage: ' + str(sports_count_predicted) + ' | ' + str((sports_count_predicted/count)))
# print('Music count | percentage: ' + str(music_count_predicted) + ' | ' + str((music_count_predicted/count)))
# print('ENTERTAINMENT count | percentage: ' + str(entertainment_count_predicted) + ' | ' + str((entertainment_count_predicted/count)))
# print('Science count | percentage: ' + str(sciencetech_count_predicted) + ' | ' + str((sciencetech_count_predicted/count)))
# print('File count: ' + str(count))
#
# print('news_precision | news_recall: ' + str((news_count_correct/news_count_predicted)) + ' | ' + str((news_count_correct/news_count_actual)))
# print('sports_precision | sports_recall: ' + str((sports_count_correct/sports_count_predicted)) + ' | ' + str((sports_count_correct/sports_count_actual)))
# print('music_precision | music_recall: ' + str((music_count_correct/music_count_predicted)) + ' | ' + str((music_count_correct/music_count_actual)))
# print('entertainment_precision | entertainment_recall: ' + str((entertainment_count_correct/entertainment_count_predicted)) + ' | ' + str((entertainment_count_correct/entertainment_count_actual)))
# print('sciencetech_precision | sciencetech_recall: ' + str((sciencetech_count_correct/sciencetech_count_predicted)) + ' | ' + str((sciencetech_count_correct/sciencetech_count_actual)))
#
# print('F_news: ' + str( (2*((news_count_correct/news_count_predicted)*(news_count_correct/news_count_actual))) / ((news_count_correct/news_count_predicted)+(news_count_correct/news_count_actual)) ))
# print('F_sports: ' + str( (2*((sports_count_correct/sports_count_predicted)*(sports_count_correct/sports_count_actual))) / ((sports_count_correct/sports_count_predicted)+(sports_count_correct/sports_count_actual)) ))
# print('F_music: ' + str( (2*((music_count_correct/music_count_predicted)*(music_count_correct/music_count_actual))) / ((music_count_correct/music_count_predicted)+(music_count_correct/music_count_actual)) ))
# print('F_entertainment: ' + str( (2*((entertainment_count_correct/entertainment_count_predicted)*(entertainment_count_correct/entertainment_count_actual))) / ((entertainment_count_correct/entertainment_count_predicted)+(entertainment_count_correct/entertainment_count_actual)) ))
# print('F_sciencetech: ' + str( (2*((sciencetech_count_correct/sciencetech_count_predicted)*(sciencetech_count_correct/sciencetech_count_actual))) / ((sciencetech_count_correct/sciencetech_count_predicted)+(sciencetech_count_correct/sciencetech_count_actual)) ))
