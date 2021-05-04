import praw
import json
from random import choice
from time import time
import discord
from discord.ext import tasks, commands
#from discord_webhook import DiscordWebhook


fileJson = "infosPorn.json"
infos = {}
serverTime = {}
with open(fileJson, "r") as f:
    infos = json.load(f)
isNSFW = infos["isNSFW"]
prefix = infos["prefix"]


#-------------- CLIENTS ---------------

reddit = praw.Reddit(
    check_for_async=False,
    client_id = infos["client_id"],
    client_secret = infos["client_secret"],
    user_agent = infos["user_agent"],
    password = infos["password"],
    username = infos["username"],
)
reddit.read_only = True

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
        #listPosts = tempSubreddit.hot(limit=20)    #WIP
        #post = choice(listPosts)                   #Serait cool mais marche pas
        if post == None:
            print("erreur aucun post trouvé dans r/"+tempSubreddit.diaplay_name)
            done = False
        elif any(site in post.url for site in infos["banlist"]):
            print("site de merde")
            done = False
        elif post.is_original_content or not post.stickied:
            #print(post.title)
            print(post.shortlink)
            #print(post.url)
            print()
            return ([post.title,tempSubreddit.display_name,post.url,post.shortlink])
        else:
            print("pas original")
            done = False

def saveJson():
    with open(fileJson, "w") as f:
        json.dump(infos, f)

#--------------- DISCORD EVENTS ---------------

@client.event
async def on_message(message):
    if message.content.find(prefix) == 0:
        if message.guild.id not in serverTime.keys():
            serverTime[message.guild.id] = 0

        if message.content.find(prefix+" add") == 0:
            if len(message.content[10:]) != 0:
                infos["subreddits"].append(message.content[len(prefix)+5:])
                saveJson()
                await message.add_reaction("✅")
            else:
                await message.add_reaction("❌")
        elif message.content.find(prefix+" remove") == 0:
            try:
                infos["subreddits"].remove(message.content[len(prefix)+8:])
                saveJson()
                await message.add_reaction("✅")
            except ValueError:
                await message.add_reaction("❌")
        if message.content.find(prefix+" ban") == 0:
            if len(message.content[10:]) != 0:
                infos["banlist"].append(message.content[len(prefix)+5:])
                saveJson()
                await message.add_reaction("✅")
            else:
                await message.add_reaction("❌")
        elif message.content.find(prefix+" unban") == 0:
            try:
                infos["banlist"].remove(message.content[len(prefix)+7:])
                saveJson()
                await message.add_reaction("✅")
            except ValueError:
                await message.add_reaction("❌")  

        elif not message.channel.is_nsfw() and isNSFW:
            await message.channel.send("You must be in a nsfw channel to use this command")
        elif time()-serverTime[message.guild.id] >= 5:
            post = postPorn()
            embed=discord.Embed(title=post[0],url=post[3], color=0xe32400)
            embed.add_field(name="r/"+post[1], value="\u200b", inline=True)
            embed.set_image(url=post[2])
            await message.channel.send(embed=embed)
            #await message.channel.send(postPorn())
            serverTime[message.guild.id] = time()
        else:
            await message.channel.send("Calm down dude, wait {}s to ask for another post".format(int(5-(time()-serverTime[message.guild.id]))))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.change_presence(status="😏")

client.run(infos["token"])
