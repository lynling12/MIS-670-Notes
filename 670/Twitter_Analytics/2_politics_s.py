# If you're collecting tweets with very popular keywords (e.g., clinton, trump), use the following script.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

save_file = open('politics.json', 'a')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        if isinstance(data, dict):
            # An attempt to cut down on non English tweets.
            if data['user']['lang'] != 'en':
                return


        print data
        save_file.write(str(data))
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

while True:
	try:
		stream = Stream(auth, l)
		#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby', '#bigdata'
		stream.filter(track=['trump', 'hillary'])
	except: 
		continue