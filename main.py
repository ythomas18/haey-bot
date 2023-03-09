import discord
from discord.ext import commands
import icalendar

intents = discord.Intents.default()
intents.members = True  # permet de récupérer les membres du serveur

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def agenda(ctx):
    # Ouverture du fichier iCal statique
    with open('ADECal.ics', 'rb') as f:
        cal = icalendar.Calendar.from_ical(f.read())

    # Parcours des événements dans le calendrier
    for event in cal.walk('vevent'):
        # Récupération des informations de l'événement
        summary = event.get('summary')
        start = event.get('dtstart').dt
        end = event.get('dtend').dt
        location = event.get('location')

        # Affichage des informations de l'événement
        await ctx.send(f"{summary} ({location}) du {start.strftime('%d/%m/%Y %H:%M')} au {end.strftime('%d/%m/%Y %H:%M')}")

@bot.event
async def on_message(message):
    if message.content.lower().endswith('quoi'):
        await message.channel.send(message.author.mention + "feur")

@bot.event
async def xavier(message):
    if message.author.discriminator == 'Baka_a_toi':
        await message.channel.send("Xavier qu'a écouter !")

bot.run('MTA3NjIyMDQzMTQzNjA5MTQ3Mg.Gx2aus.T4PSbV2amTvO5sx93h89JQughSRxU3reMObRV8')
