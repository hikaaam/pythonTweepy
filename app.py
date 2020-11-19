import eel
#untuk install ketik "pip install eel"
#penting!!! untuk mennggunakan library eel harus memeliki browser google chrome yg sudah terinstall
import re 
import tweepy 
#untuk install ketik "pip install tweepy"
from tweepy import OAuthHandler 
from textblob import TextBlob 
#untuk install ketik "pip install textblob"
import time
eel.init('web') 
#memanggil folder web

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
	
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = '2dxpi0MQO9yzlD9BjSzcRByQy'
		consumer_secret = 'Ez4OqZ1fo92NOqJIUA2c40snAqvAVYLkt8XH3GxlIDdoFKooos'
		access_token = '1146591160208510976-L2npI5gTPETJZCgIjcQ6a2niDTDV96'
		access_token_secret = 'YOfSiR1BsvWtoNFxSBNwMERI6jfzt2xQh300qQnqs6TJc'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		#function untuk membersihkan tweet
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
			#function untuk membuat sentiment analisis menggunakan textblob dari hasil cari tweepy
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			#jika polarity sentiment nya melebihi 0 maka positive
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			#jika polarity sentiment nya mendekati 0 maka neutral
			return 'neutral'
		else: 
			#jika polarity sentiment nya kurannd dari 0 maka negrative
			return 'negative'

	def get_tweets(self, query, count = 10): 
		#function untuk mencari kata di twitter menggunakan tweepy
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

@eel.expose
def my_python_method(param1):
    print(param1)
@eel.expose
def main(param1):
    # creating object of TwitterClient Class 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = param1, count = 400)
	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	# percentage of positive tweets 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	ptper = round(100*len(ptweets)/len(tweets),0)
	ntper = round(100*len(ntweets)/len(tweets),0)
	nnper = round((100 *(len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)),0)
	panjang = len(tweets)
	persen = [ptper,ntper,nnper,panjang]
	nettweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral'] 
	# percentage of neutral tweets 
	print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets)) /len(tweets)))    
	# printing first 5 positive tweets 
	print("\n\nPositive tweets:") 
	# for tweet in ptweets[:10]: 

	#     print(tweet['text']) 
	# # printing first 5 negative tweets 
	# print("\n\nNegative tweets:") 
	# for tweet in ntweets[:10]: 
	#     print(tweet['text'])

	return ptweets,ntweets,persen,nettweets; 


@eel.expose
def getTime():
	#memanggil function request dari javascript
    print(str)
    return time.strftime('%c')


eel.start('main.html', block=False) # Don't block on this call
#memanggil resource javascript di main.html yang terletak di folder web
#jangan lupa lihat folder web untuk menangkap request dari python server

while True:
    eel.sleep(1.0) # Must use eel.sleep()
	#melakukan polling server ke javascript terus menerus