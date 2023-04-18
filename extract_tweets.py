import tweepy
from tweepy import Client
from decouple import config

api_key = config('api_key')
api_key_secret= config('api_key_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def extract_tweets(keyword, date_since, date_until, num_tweets):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en", since_id=date_since, until=date_until, tweet_mode='extended').items(num_tweets)
    tweet_cont, tweet_rt, tweet_fav = [], [], []
    for tweet in tweets:
        try:
            tweet_cont.append(tweet.retweeted_status.full_text)
            tweet_rt.append(tweet.retweeted_status.retweet_count)
            tweet_fav.append(tweet.retweeted_status.favorite_count)
        except AttributeError:
            tweet_fav.append(tweet.favorite_count)

    data = {
        'tweet_content': tweet_cont,
        'retweet_count': tweet_rt,
        'favorite_count': tweet_fav
    }
    return data

if __name__ == '__main__':
    keyword = 'bitcoin'
    date_since = '2020-01-01'
    date_until = '2020-01-02'
    num_tweets = 100
    data = extract_tweets(keyword, date_since, date_until, num_tweets)
    print(data)