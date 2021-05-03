import praw
import json
from random import choice
from praw.reddit import Subreddit
from time import sleep
from prawcore import requestor
import requests

done = False
infos = {}
with open("infos.json", "r") as f:
    infos = json.load(f)


reddit = praw.Reddit(
    client_id = infos["client_id"],
    client_secret = infos["client_secret"],
    user_agent = infos["user_agent"],
    password = infos["password"],
    username = infos["username"],
)
reddit.read_only = True

#print(reddit.user.me())

subreddits = []
for subreddit in infos["subreddits"]:
    subreddits.append(reddit.subreddit(subreddit))




while not done:
    tempSubreddit = choice(subreddits)
    #tempSubreddit.get_top_from_day(limit=1)
    post = tempSubreddit.random()
    if post.is_original_content or not post.stickied:
        print(post.title)
        print(post.shortlink)
        print(post.url)
        #resp = requests.get(url=post.url)
        #print(resp.json['data']['children'][0]['data']['url'])
        done = True
    else:
        print("pas original")
        done = False
sleep(3600)
done = False

