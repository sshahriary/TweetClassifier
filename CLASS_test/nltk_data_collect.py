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

#retrieves 1200 tweets from user
def get_all_user_tweets(screen_name, twitter_api):
	iterr = 0
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
	
	#while there are tweets still to be read and #tweets < 1200
	while(len(statuses) > 0 and iterr < 5):
		#gets next 200 tweets starting from where oldest ID of tweet left off
		iterr = iterr + 1
		statuses = twitter_api.statuses.user_timeline(screen_name= screen_name, include_rts=False, count=200, max_id = oldest_tweet_id)
		all_tweets.append(statuses)
		#uodate oldest tweet
		oldest_tweet_id = all_tweets[len(all_tweets)-1][len(statuses)-1]['id']
	
	return all_tweets

#writes each tweet out to it's own file
def write_out(user_tweets, tweet_count):
	for statuses in user_tweets:
		for tweet in statuses:
			#opens new file, formats filename
			f = open('TEST.'+str(tweet_count).zfill(5)+'.txt', 'w')
			f.write(tweet['text'])
			f.close()
			tweet_count = tweet_count + 1
	return tweet_count

def main():
	#random accounts to be used for tweet collection
	list_accounts = ['JRaj_Music','AMAs', 'AppleMusic',
					 'CBCNews','YahooNews','CBSNews',
					 'BBCSport','sportingnews','BeInspired_UK',
					 'etnow','enews','KEEMSTAR',
					 'SPACEdotcom', 'PopSci', 'technology']
	
	#num of tweets collected
	tweet_count = 1

	# Creation of the actual interface, using authentication
	twitter_api = oauth_login()

	#for each account, grab 1200 tweets, and write out to it's own file
	for account in list_accounts:
		user_tweets = get_all_user_tweets(account, twitter_api)
		tweet_count = write_out(user_tweets, tweet_count)

	#write number of tweets collected to stats file
	f = open('CLASS_TEST_stat.txt', 'w')
	f.write('TEST tweet count: '+str(tweet_count)+'\n')
	f.close()
	

if __name__ == '__main__':
   main()
