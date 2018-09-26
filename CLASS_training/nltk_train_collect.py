#Sam Shahriary
#Lin 127
# Script to pull tweets from twitter API and store each tweet in its own file

# twitter API: 	GET statuses/user_timeline
# 				limited to 900 requests per 15 min window
# 				each request can grab max 200 tweets

# references: 	https://developer.twitter.com/en/docs/tweets/timelines/api-reference/get-statuses-user_timeline.html
#				https://developer.twitter.com/en/docs/tweets/timelines/guides/working-with-timelines
import twitter

#authentication of my Twitter api account
def oauth_login():
	consumer_key = '********************'
	consumer_secret = '****************************************'
	access_token = '************************************************************'
	access_token_secret = '****************************************'
	auth = twitter.oauth.OAuth( access_token,
								access_token_secret,
								consumer_key,
								consumer_secret)
	twitter_api = twitter.Twitter(auth=auth)
	return twitter_api

#retrieves 300 tweets from user
def get_all_user_tweets(screen_name, twitter_api):
	#list of statuses (900reqs/15min)
	all_tweets = []
	#list of max 200 tweet objects (200 tweets/req)
	statuses = []

	#gets first 200 tweets from user with screen_name
	statuses = twitter_api.statuses.user_timeline(screen_name= screen_name, include_rts=False, count=200)
	#appends request for tweets to all_tweets
	all_tweets.append(statuses)
	#update oldest tweet id to start tweet search from this point on
	oldest_tweet_id = all_tweets[len(all_tweets)-1][len(statuses)-1]['id']

	#gets next 100 tweets starting from where oldest tweet left off
	statuses = twitter_api.statuses.user_timeline(screen_name= screen_name, include_rts=False, count=100, max_id = oldest_tweet_id)
	all_tweets.append(statuses)

	return all_tweets

#writes each tweet out to it's own file
def write_out(user_tweets, tweet_count, filename):
	for statuses in user_tweets:
		for tweet in statuses:
			f = open(filename+'.'+str(tweet_count).zfill(5)+'.txt', 'w')
			f.write(tweet['text'])
			f.close()
			tweet_count = tweet_count + 1
	return tweet_count

def main():
	#twitter accounts where data is being collected
	list_News = ['cnn', 'FoxNews', 'ABC', 'DailyMail', 'PMBreakingNews','RT_com','ndtv','PressTV','cnni','BBCWorld']
	list_Sports = ['NBA','NFL','FIFAcom','SInow', 'GolfChannel','Olympics','HBOboxing','SportsCenter','UFC', 'MLB']
	list_Music = ['iHeartRadio','MTV','WORLDMUSICAWARD','SIRIUSXM','BBCR1','RollingStone','pandoramusic','warnermusic','UMG','SonyMusicGlobal','Shazam']
	list_Entertainment = ['netflix','HBO','AMC_TV','wbpictures','SonyPictures','TMZ','HollywoodLife','usweekly','EW','InStyle']
	list_ScienceTech = ['neiltyson', 'NASA','SpaceX','ScienceNews','molecular','sciencemagazine','ChemistryWorld','cnntech','Samsung','techinsider']
	
	#num of tweets collected for each type
	news_tweet_count = 1
	sports_tweet_count = 1
	music_tweet_count = 1
	ent_tweet_count = 1
	science_tweet_count = 1

	# Creation of the actual interface, using authentication
	twitter_api = oauth_login()

	#for each twitter account
		#retrieve all tweets by user
		#write each tweet to it's own file and update tweet_count

	for news_source in list_News:
		user_tweets = get_all_user_tweets(news_source, twitter_api)
		news_tweet_count = write_out(user_tweets, news_tweet_count, 'news')

	for sports_source in list_Sports:
		user_tweets = get_all_user_tweets(sports_source, twitter_api)
		sports_tweet_count = write_out(user_tweets, sports_tweet_count, 'sports')

	for music_source in list_Music:
		user_tweets = get_all_user_tweets(music_source, twitter_api)
		music_tweet_count = write_out(user_tweets, music_tweet_count, 'music')

	for ent_source in list_Entertainment:
		user_tweets = get_all_user_tweets(ent_source, twitter_api)
		ent_tweet_count = write_out(user_tweets, ent_tweet_count, 'ent')

	for science_source in list_ScienceTech:
		user_tweets = get_all_user_tweets(science_source, twitter_api)
		science_tweet_count = write_out(user_tweets, science_tweet_count, 'science')
	
	#write number of tweets out to stats file
	f = open('CLASS_training2_stats.txt', 'w')
	f.write('news tweet count: '+str(news_tweet_count)+'\n')
	f.write('sports tweet count:'+str(sports_tweet_count)+'\n')
	f.write('music tweet count:'+str(music_tweet_count)+'\n')
	f.write('entertainment tweet count:'+str(ent_tweet_count)+'\n')
	f.write('science tweet count:'+str(science_tweet_count)+'\n')
	f.close()
	

if __name__ == '__main__':
   main()
