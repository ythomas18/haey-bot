import aiohttp
import discord
from discord.ext import tasks, commands
import random
import praw
from dotenv import load_dotenv
import os

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='/')

load_dotenv()

DISCROD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
API_KEY = os.getenv('WEATHER_API_KEY')

reponses_quoi = [
    "ok QUOICOUBEH",
    "feur",
    "QUOICOUBAKA UwU",
]

reponses_ratio = [
    "gros flop rions :joy_cat:",
    "ok flopito :call_me:",
    "pas nécessaire le ratio enfin bref..",
]

reddit = praw.Reddit(client_id='eqwU7ifSx8ha6vNzmomR5w', client_secret='668cQolPM9cdit6wAzCy1xwAL17uRw',
                     user_agent='haey/0.1 by trankiste (yanntho97@gmail.com)')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.event
async def on_message(message):
    if 'quoi' in message.content and bot.user.id != message.author.id:
        print("quoi détecté !")
        reponse = random.choice(reponses_quoi)
        await message.channel.send(f"{message.author.mention} {reponse}")

    elif 'ratio' in message.content and bot.user.id != message.author.id:
        print("ratio détecté !")
        reponse = random.choice(reponses_ratio)
        await message.channel.send(f"{message.author.mention} {reponse}")
    await bot.process_commands(message)

@bot.command()
async def meteo(ctx, ville):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://dataservice.accuweather.com/locations/v1/cities/search?apikey={API_KEY}&q={ville}") as response:
            data = await response.json()
            location_key = data[0]["Key"]
            city_name = data[0]["LocalizedName"]
        async with session.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={API_KEY}&details=true") as response:
            data = await response.json()
            temperature = data[0]["Temperature"]["Metric"]["Value"]
            weather_text = data[0]["WeatherText"]
            wind_speed = data[0]["Wind"]["Speed"]["Metric"]["Value"]
            wind_direction = data[0]["Wind"]["Direction"]["Localized"]
            humidity = data[0]["RelativeHumidity"]
    await ctx.send(f"```Météo actuelle pour {city_name}:\n🌡️Température: {temperature}°C\n🌤️Conditions: {weather_text}\n🌬️Vitesse du vent: {wind_speed} km/h\n🧭Direction du vent: {wind_direction}\n💧Humidité: {humidity}%```")



@bot.command()
async def hello(ctx):
    await ctx.send(ctx.author.mention + " hello!")

def get_subreddit_posts():
    subreddit = reddit.subreddit('HighschoolDxD')
    posts = subreddit.hot(limit=5) # Récupère les 5 derniers posts
    return posts

@tasks.loop(hours=24)
async def post_subreddit_posts():

    channel = bot.get_channel(1084085506272399370) # ID du canal où vous voulez que les messages soient publiés
    posts = get_subreddit_posts()
    for post in posts:
        await channel.send(post.title + '\n' + post.url)

@bot.command()
async def start(ctx):
    post_subreddit_posts.start()
    await ctx.send('Bot lancé!')

# Commande pour arrêter la tâche planifiée
@bot.command()
async def stop(ctx):
    post_subreddit_posts.stop()
    await ctx.send('Bot arreté !')


bot.run(DISCROD_TOKEN)
