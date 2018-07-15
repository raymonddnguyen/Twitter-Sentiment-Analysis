import time
import tweepy
from json import loads
from tweepy.streaming import StreamListener
 
class saveTweepyTweets(StreamListener):
    """
    A handler object for Twitter's stream data. Allows users to specify a certain time limit, 
    number of tweets and whether to grab retweets or not.

    Keyword Arguments:

    time_limit -- Time limit in seconds stream will listen. (default 60)
    num_of_tweets -- Number of tweets grabbed. (default 20)
    save_file -- File tweets are saved to. (default twitter_stream_data.json)
    retweets -- Boolean to grab retweets or not (default False)
    filter_set -- Set of filter words to remove tweets
    """
    def __init__(self, time_limit=60, num_of_tweets=20, save_file='twitter_stream_data.json', retweets=False, filter_set=None):
        self.__start_time = time.time()
        self.__limit = time_limit
        self.__tweet_count = 0
        self.__num_of_tweets = num_of_tweets
        self.__save_file = open(save_file, 'w')
        self.__retweets = retweets
        self.__filter_set = filter_set
        super(saveTweepyTweets, self).__init__()

    def on_data(self, data):
        try:
            if (time.time() - self.__start_time) < self.__limit and self.__tweet_count < self.__num_of_tweets:
                tweet = loads(data)
                tokens = tweet['text'].split()
                no_filtered_words = True
                for token in tokens:
                    if token.lower() in self.__filter_set:
                        print('Filtering...')
                        no_filtered_words = False
                        break
                
                if no_filtered_words:
                    if not tweet['retweeted'] and 'RT @' not in tweet['text'] and not self.__retweets:
                        print("Getting tweet #{}...".format(self.__tweet_count + 1))
                        self.__save_file.write(data) 
                        self.__tweet_count += 1
                    elif self.__retweets:
                        print("Getting tweet #{}...".format(self.__tweet_count + 1))
                        self.__save_file.write(data) 
                        self.__tweet_count += 1
                return True
            else:
                print('Completed collection of tweets.')
                self.__save_file.close()
                return False
        except BaseException as e: 
            print("Failed: ", str(e)) 
            return False

    def on_error(self, status): 
        if status == 420:
            return False