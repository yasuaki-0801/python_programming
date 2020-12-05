import tweepy
import os


auth = tweepy.OAuthHandler(os.environ['tw_consumer_key'], consumer_secret=os.environ['tw_consumer_secret'])
auth.set_access_token(os.environ['tw_token'], os.environ['tw_token_secret'])
api=tweepy.API(auth)

q_list=["#資産運用","#プログラミング初心者","#programming","#pythonprogramming"]
count=30#取得するツイート数
for q in q_list:
    print("Now:QUERY-->>{}".format(q))
    search_results=api.search(q=q,count=count)#ツイートのデータであるstatusオブジェクトを取得
    for status in search_results:
        tweet_id=status.id#ツイートidにアクセス
        try:
            api.create_favorite(tweet_id)#ファボ
        except:
            pass