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

#retrieves num_tweets tweets from user
def get_all_user_tweets(screen_name, twitter_api, num_tweets):
	#list of statuses (900reqs/15min)
	all_tweets = []
	#list of max 200 tweet objects (200 tweets/req)
	statuses = []

	#gets first 200 tweets from user with screen_name
	statuses = twitter_api.statuses.user_timeline(screen_name= screen_name, include_rts=False, count=num_tweets)
	#appends request for tweets to all_tweets
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
	#accounts for tweets to be collected from
	list_News = ['ChadPergram']
	list_Sports = ['GoldenKnights']
	list_Music = ['Top10songscom']
	list_Entertainment = ['CelebNewsGB', 'AmznMovieRevws']
	list_ScienceTech = ['IBM']
	
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
		user_tweets = get_all_user_tweets(news_source, twitter_api,20)
		news_tweet_count = write_out(user_tweets, news_tweet_count, 'news')

	for sports_source in list_Sports:
		user_tweets = get_all_user_tweets(sports_source, twitter_api,20)
		sports_tweet_count = write_out(user_tweets, sports_tweet_count, 'sports')

	for music_source in list_Music:
		user_tweets = get_all_user_tweets(music_source, twitter_api,20)
		music_tweet_count = write_out(user_tweets, music_tweet_count, 'music')

	for ent_source in list_Entertainment:
		user_tweets = get_all_user_tweets(ent_source, twitter_api,10)
		ent_tweet_count = write_out(user_tweets, ent_tweet_count, 'ent')

	for science_source in list_ScienceTech:
		user_tweets = get_all_user_tweets(science_source, twitter_api,20)
		science_tweet_count = write_out(user_tweets, science_tweet_count, 'science')
	
	#write number of tweets out to stats file
	f = open('CLASS_small_test_stats.txt', 'w')
	f.write('news tweet count: '+str(news_tweet_count)+'\n')
	f.write('sports tweet count:'+str(sports_tweet_count)+'\n')
	f.write('music tweet count:'+str(music_tweet_count)+'\n')
	f.write('entertainment tweet count:'+str(ent_tweet_count)+'\n')
	f.write('science tweet count:'+str(science_tweet_count)+'\n')
	f.close()
	

if __name__ == '__main__':
   main()
