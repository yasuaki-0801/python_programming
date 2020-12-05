import feedparser
from datetime import datetime
import twitter
import pandas as pd
import os

def post_tweet(language):
    if language == "ja":
       RSS_URL = "https://yasu-investing.com/feed/"
    else:
       RSS_URL = "https://yasu-investing.com/en/feed/"
    wordpress = feedparser.parse(RSS_URL)
    auth = twitter.OAuth(consumer_key=os.environ['tw_consumer_key'],
                     consumer_secret=os.environ['tw_consumer_secret'],
                     token=os.environ['tw_token'],
                     token_secret=os.environ['tw_token_secret'])

    data_bloglist = r'\temp\bloglist.csv'
    df = pd.read_csv(data_bloglist,encoding = "shift-jis", index_col=1)
    t = twitter.Twitter(auth=auth)

    for entry in wordpress.entries:
  
      published = entry.published.replace(",","").replace(" +0000","")
      objDate = datetime.strptime(published,'%a %d %b %Y %H:%M:%S')
  
      strtag = ""
      for tag in entry.tags:
          strtag = strtag + " #"+tag.term
      if language == "ja":
          strTweet = "ブログの新着記事です\nタイトル：{0}\nURL：{1}\n投稿日：{2}\n#情シス #Python {3}".format(entry.title,entry.link,str(objDate),strtag)
      else:
          strTweet = "New article\nTitle：{0}\nURL：{1}\nPosted Date：{2}\n#Python {3}".format(entry.title,entry.link,str(objDate),strtag)

      blog_list = df[df["url"] == entry.link]
      if blog_list.empty:
           df=df.append({'url' : entry.link , 'title':entry.title} , ignore_index=True)
           t.statuses.update(status=strTweet)
           print(strTweet)
           df.to_csv(data_bloglist,encoding = "shift-jis",index=False)
if __name__ == '__main__':
    post_tweet('ja')
    post_tweet('en')

