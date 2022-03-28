import os
import discord
from discord import Member
from discord.utils import get
from webserver import keep_alive
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
async def ping(ctx):
	before = time.monotonic()
	em = discord.Embed(title="Latency Test", description=f"**Please Hold ... Working**", colour=discord.Colour.purple())
	msg = await ctx.reply(embed=em, mention_author = False)
	ping = (time.monotonic() - before) * 1000
	em = discord.Embed(title="Ping", description=f"Latency: `{ping}ms`", colour=discord.Colour.purple())
	await msg.edit(embed=em)

@client.command()
async def github(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Github Source Code", description=f"Find the source code for this bot, written by {dev.mention} at https://github.com/sam-march/Dark-Alley-Discord-Bot", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def version(ctx):
	em = discord.Embed(title="Versions", description="Python:\n`3.8.12`\ndiscord.py:\n`Development Version`" ,colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)

@client.command()
async def dev(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="About Developer", description=f"This bot was developed by {dev.mention}. If you wish to get in contact, do DM him", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def about(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="About Bot", description=f"I was developed by {dev.mention}, and I joined on the <t:1647964800:d>", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def timestamp(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Timestamp Generator", description=f"We all know how hard Discord timestamps are to write, so follow this handy link to quickly create them without the faff\nhttps://bchaing.github.io/discord-timestamp/", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def invite(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Invite Bot", description=f"Unfortunately, you can't invite the bot, but if you want, DM {dev.mention}, as if he's free, he may make you a bot.", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def rules(ctx):
	judge = discord.utils.get(ctx.guild.roles, id=912537782654754850)
	em = discord.Embed(title="Server Rules", description=f"**Discord TOS & Community Guidelines:**\nhttps://discordapp.com/terms\nhttps://discordapp.com/guidelines\n\n**Server Rules:**\n\nBe nice or leave!\n1.1. No homophobia, personal attacks, offensive language, harassment, witch hunting, sexism, racism, hate speech, religious/political discussion, or other disruptive behavior.\n1.2. Also applies to voice chats. Disruptive behavior in voice includes voice changers, soundboards, extremely loud noises, etc.\n1.3. Do not impersonate anyone — including admins, mods, or anyone else\n1.4. Do not act as if you are able to carry out staff actions if you're not part of the staff team.\n\n2. No offensive or otherwise inappropriate nicknames or profile pictures\n2.1. This includes blank or invisible names and excessive use of noisy or unusual Unicode characters\n\n3. Don't spam\n3.1. Includes excessive amounts of messages, emojis, capital letters, pings/mentions, etc.\n\n4. NSFW content is NOT allowed\n4.1. NSFW = Not Safe For Work, i.e. porn, gore, suggestive content, etc.\n\n5. English, please\n5.1. Keep all discussion in text channels and general voice channels in English\n\n6. No scam links, URL shorteners, IP grabbers, etc.\n\n7. Listen to the server staff\n7.1. If a moderator tells you to stop doing something, stop it\n7.2. Don't argue about mod decisions in chat. If you'd like to discuss or dispute a decision, please message a @Judge.\n\n**In addition to these rules, the moderation team reserves the right to remove messages and users from the server that are detrimental to the discussion and community. Since this is the first page you are seeing, ignorance of the rules does not excuse breaking them.**", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)

@client.command()
@commands.has_role(911806935072931871)
async def message(ctx, member: discord.Member, *, message):
	em = discord.Embed(title="Message Sending", description=f"Bot is sending message ... Please Wait", colour=discord.Colour.purple())
	alert=await ctx.reply(embed=em, mention_author=False)
	try:
		await member.send(f"> You have been sent a message from {ctx.author} (Moderator)\n```{message}```")
		em = discord.Embed(title="📨 | Message Sent", description=f"Your message has been sent to {member.mention}", colour=discord.Colour.purple())
		await alert.edit(embed=em)
		em = discord.Embed(title="📨 | Message Sent", description=f"A message was sent to {member.mention} by {ctx.author.mention}.\n\nContents:```{message}```", colour=discord.Colour.purple())
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)
	except:
		em = discord.Embed(title="❌ | Message Send Error", description=f"The message to {member} failed to send. This may because you don't share a common server with the recipient, or their DMs are closed.\nIf you think there is a problem, please contact an admin", colour=discord.Colour.purple())
		await alert.edit(embed=em)

@client.command()
async def update(ctx, *, message):
	em = discord.Embed(title="Update Sending", description=f"Bot is sending update ... Please Wait", colour=discord.Colour.purple())
	alert=await ctx.reply(embed=em, mention_author=False)
	if ctx.author.id == 723569355710922802:
		try:
			updates_channel = client.get_channel(956218810967416832)
			em = discord.Embed(title="🔔 | Bot Update", description=f"{message}", colour=discord.Colour.purple())
			await updates_channel.send(embed=em)
			em = discord.Embed(title="🔔 | Update Sent", description=f"The update sent", colour=discord.Colour.purple())
			await alert.edit(embed=em)
		except:
			em = discord.Embed(title="❌ | Update Send Error", description=f"The update to failed to send. Please check bot permissions in #bot-updates", colour=discord.Colour.purple())
			await alert.edit(embed=em)
	else:
		em = discord.Embed(title="❌ | Update Send Error", description=f"You don't have the permssions to send bot updates", colour=discord.Colour.purple())
		await alert.edit(embed=em)
		
	
@client.command()
#@commands.has_role(911806935072931871)
async def clear_amount(ctx, *, amount=1):
	amount = amount +2
	em = discord.Embed(title=f"🗑️ | Purging Message(s)", description=f"Bot purging {amount-2} message(s) ... Please wait", colour=discord.Colour.purple())
	message=await ctx.reply(embed=em, mention_author=False)
	try:
		await ctx.channel.purge(limit=amount)
		em = discord.Embed(title=f"🗑️ | Purged Message(s)", description=f"Bot purged {amount-2} messages(s) successfully", colour=discord.Colour.purple())
		await message.edit(embed=em)
		embed = discord.Embed(title="📨 | Purged Messages", description=f"{ctx.author} just cleared {amount} message(s) in {ctx.channel.mention}", colour=discord.Colour.purple())
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=embed)
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Purge Messages Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await message.edit(embed=em)

@client.command()
#@commands.has_role(911806935072931871)
async def clear_all(ctx, *, amount=1):
	amount = amount +2
	em = discord.Embed(title=f"🗑️ | Purging all messages", description=f"Bot purging all messages ... Please wait", colour=discord.Colour.purple())
	message=await ctx.reply(embed=em, mention_author=False)
	try:
		await ctx.channel.purge()
		em = discord.Embed(title=f"🗑️ | Purged all messages", description=f"Bot purged all messages", colour=discord.Colour.purple())
		await message.edit(embed=em)
		embed = discord.Embed(title="📨 | Purged Messages", description=f"{ctx.author} just cleared all messages in {ctx.channel}", colour=discord.Colour.purple())
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=embed)
		
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Purge Messages Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await message.edit(embed=em)
	


keep_alive()
client.run(token)