import praw
import json
from random import choice
from praw.reddit import Subreddit
from time import sleep
from prawcore import requestor
import requests
from discord_webhook import DiscordWebhook

#bot
#webhookLink = "https://discord.com/api/webhooks/838743675093385257/V1JDQLZMPH966g3mmBmlqHfJraSAjmsw0xZ6OWLnG7DPyPUs4FHHlrU7EL1L2wekeLid"
#"""devoirs"""
webhookLink = "https://discord.com/api/webhooks/838747699448512552/8Nl27cQCctRSbCRcHPpprJv7pr8ZYYpPqLrLTNAbQfu8kAiny3f_vrHztuuH_SN-98y2"

timer = 1800
done = False
infos = {}
with open("infosPorn.json", "r") as f:
    infos = json.load(f)
#print(infos["subreddits"])

reddit = praw.Reddit(
    client_id = infos["client_id"],
    client_secret = infos["client_secret"],
    user_agent = infos["user_agent"],
    password = infos["password"],
    username = infos["username"],
)
reddit.read_only = True


subreddits = []
for subreddit1 in infos["subreddits"]:
    subreddits.append(reddit.subreddit(subreddit1))


while 1:
    while not done:
        tempSubreddit = choice(subreddits)
        post = tempSubreddit.random()
        if post == None:
            print("erreur aucun post trouvé dans "+tempSubreddit.title)
            done = False
        elif "redgifs.com" in post.url:
            print("redgif de merde fais chier")
            done = False
        elif post.is_original_content or not post.stickied:
            print(post.title)
            print(post.shortlink)
            print(post.url)
            webhook = DiscordWebhook(webhookLink, content = post.title+" from "+tempSubreddit.title+"\n"+post.url+" \nlink :<"+post.shortlink+">")
            webhook.execute()
            print()
            done = True
        else:
            print("pas original")
            done = False
    sleep(timer)
    done = False
