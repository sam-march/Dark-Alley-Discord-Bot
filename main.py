import os
import discord
from discord import Member

from discord.utils import get
import random
import asyncio
import time
from discord.ext import commands

token = os.environ['token']
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
client.remove_command("help")





@client.event
async def on_ready():
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" all online members"))
	
@client.command()
async def status(ctx):
    em = discord.Embed(title="Dark Alley Bot is online!", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def hello(ctx):
	bot = client.get_user(955534616683507772)
	dev = client.get_user(723569355710922802)
	member = ctx.author
	file = discord.File("499.png")
	
	em = discord.Embed(title="👋",description=f"Hello there {member.mention}, I'm {bot.mention}, here to keep you safe in the Dark Alley Discord Server\nI was programmed by {dev.mention}", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
	em.set_image(url="attachment://499.png")
	await ctx.reply(embed=em, mention_author=False, file=file)

@client.command()
@commands.has_role(935538300570185740)
async def setup(ctx):
	msg = await ctx.reply("> Setting Up Bot | Please wait", mention_author=False)
	msg = msg.id
	try:
		guild = client.get_guild(905684366620000287)
		await guild.create_category("Bot Moderation")
		 # <-- insert yor guild id here
		mod_logs = await ctx.guild.create_text_channel("mod logs", category="Bot Moderation")
		bot_updates = await ctx.guild.create_text_channel("bot updates", category="Bot Moderation")
        
	except Exception as errors:
		await ctx.reply(f"> ❌ | Bot Error: {errors}", mention_author=False)

@client.commands()
async def ping(ctx):
	em = discord.Embed(title="Latency Test", description=f"**Please Hold ... Working**", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author = False)
	before = time.monotonic()
	em = discord.Embed(title="Ping", description=f"**")

client.run(token)