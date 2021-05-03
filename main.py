import praw
import json
from random import choice
from praw.reddit import Subreddit
from time import sleep, time
import discord
from discord.ext import tasks, commands
#from discord_webhook import DiscordWebhook
#from datetime import datetime


#--------------- DATA ---------------
#bot
#webhookLink = "https://discord.com/api/webhooks/838743675093385257/V1JDQLZMPH966g3mmBmlqHfJraSAjmsw0xZ6OWLnG7DPyPUs4FHHlrU7EL1L2wekeLid"
#"""devoirs"""
webhookLink = "https://discord.com/api/webhooks/838747699448512552/8Nl27cQCctRSbCRcHPpprJv7pr8ZYYpPqLrLTNAbQfu8kAiny3f_vrHztuuH_SN-98y2"

#timer = 1800
last_time=0
infos = {}
with open("infosPorn.json", "r") as f:
    infos = json.load(f)
#print(infos["subreddits"])


#-------------- CLIENTS ---------------

reddit = praw.Reddit(
    client_id = infos["client_id"],
    client_secret = infos["client_secret"],
    user_agent = infos["user_agent"],
    password = infos["password"],
    username = infos["username"],
)
reddit.read_only = True

#client = commands.Bot(command_prefix="<")
client = discord.Client()


subreddits = []
for subreddit1 in infos["subreddits"]:
    subreddits.append(reddit.subreddit(subreddit1))


#-------------- FUNCTIONS --------------

def postPorn():
    done = False
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
            #webhook = DiscordWebhook(webhookLink, content = post.title+" from "+tempSubreddit.title+"\n"+post.url+" \nlink :<"+post.shortlink+">")
            #webhook.execute()
            print()
            return (post.title+" from "+tempSubreddit.title+"\n"+post.url+" \nlink :<"+post.shortlink+">")
        else:
            print("pas original")
            done = False


#--------------- DISCORD EVENTS ---------------

@client.event
async def on_message(message):
    global last_time
    if message.content.find("<porn") == 0:
        if not message.channel.is_nsfw():
            await message.channel.send("You must be in a nsfw channel to use this command")
        elif time()-last_time >= 5:
            await message.channel.send(postPorn())
            last_time = time()
        else:
            await message.channel.send("Calm down dude, wait {}s to ask for another post".format(5-time()-last_time))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.change_presence(status="😏")

client.run(infos["token"])
