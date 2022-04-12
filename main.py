import os
import discord
from discord import Member
from discord.utils import get
from webserver import keep_alive
import random
import asyncio
import time

from discord.ext import commands, tasks

token = os.environ['token']
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())
client.remove_command("help")
	
@client.event
async def on_ready():
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" $help"))


@client.command()
async def status(ctx):
    em = discord.Embed(title="Dark Alley Bot is online!", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def help(ctx):
    em = discord.Embed(title="Help", description="Find the docs at https://github.com/sam-march/Dark-Alley-discord-Bot/wiki\nIf you find a bug with this bot, please create an error on the GitHub Repository (https://github.com/sam-march/Dark-Alley-discord-Bot/issues)", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def docs(ctx):
    em = discord.Embed(title="Docs", description="Find the docs at https://github.com/sam-march/Dark-Alley-discord-Bot/wiki\nIf you find a bug with this bot, please create an error on the GitHub Repository (https://github.com/sam-march/Dark-Alley-discord-Bot/issues)", colour=discord.Colour.purple())
    #em.set_footer(text=f"Time Occured: {curr_time}")
    await ctx.reply(embed=em, mention_author=False)

@client.command()
async def hello(ctx):
	bot = client.get_user(955534616683507772)
	dev = client.get_user(723569355710922802)
	member = ctx.author
	file = discord.File("499.png")
	
	em = discord.Embed(title="👋",description=f"Hello there {member.mention}, I'm {bot.mention}, here to keep you safe in the Dark Alley discord Server\nI was programmed by {dev.mention}", colour=discord.Colour.purple())
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
	em = discord.Embed(title="Github Source Code", description=f"Find the source code for this bot, written by {dev.mention} at https://github.com/sam-march/Dark-Alley-discord-Bot", colour=discord.Colour.purple())
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
	em = discord.Embed(title="Timestamp Generator", description=f"We all know how hard discord timestamps are to write, so follow this handy link to quickly create them without the faff\nhttps://bchaing.github.io/discord-timestamp/", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def invite(ctx):
	dev = client.get_user(723569355710922802)
	em = discord.Embed(title="Invite Bot", description=f"Unfortunately, you can't invite the bot, but if you want, DM {dev.mention}, as if he's free, he may make you a bot.", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)
@client.command()
async def rules(ctx):
	judge = discord.utils.get(ctx.guild.roles, id=912537782654754850)
	em = discord.Embed(title="Server Rules", description=f"**discord TOS & Community Guidelines:**\nhttps://discordapp.com/terms\nhttps://discordapp.com/guidelines\n\n**Server Rules:**\n\nBe nice or leave!\n1.1. No homophobia, personal attacks, offensive language, harassment, witch hunting, sexism, racism, hate speech, religious/political discussion, or other disruptive behavior.\n1.2. Also applies to voice chats. Disruptive behavior in voice includes voice changers, soundboards, extremely loud noises, etc.\n1.3. Do not impersonate anyone — including admins, mods, or anyone else\n1.4. Do not act as if you are able to carry out staff actions if you're not part of the staff team.\n\n2. No offensive or otherwise inappropriate nicknames or profile pictures\n2.1. This includes blank or invisible names and excessive use of noisy or unusual Unicode characters\n\n3. Don't spam\n3.1. Includes excessive amounts of messages, emojis, capital letters, pings/mentions, etc.\n\n4. NSFW content is NOT allowed\n4.1. NSFW = Not Safe For Work, i.e. porn, gore, suggestive content, etc.\n\n5. English, please\n5.1. Keep all discussion in text channels and general voice channels in English\n\n6. No scam links, URL shorteners, IP grabbers, etc.\n\n7. Listen to the server staff\n7.1. If a moderator tells you to stop doing something, stop it\n7.2. Don't argue about mod decisions in chat. If you'd like to discuss or dispute a decision, please message a @Judge.\n\n**In addition to these rules, the moderation team reserves the right to remove messages and users from the server that are detrimental to the discussion and community. Since this is the first page you are seeing, ignorance of the rules does not excuse breaking them.**", colour=discord.Colour.purple())
	await ctx.reply(embed=em, mention_author=False)

@client.command()
@commands.has_role(905700432687538196)
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
@commands.has_role(905700432687538196)
async def clear_amount(ctx, *, amount=1):
	amount = amount +2
	
	try:
		await ctx.channel.purge(limit=amount)
		em = discord.Embed(title="🗑️ | Purged Message(s)", description=f"{ctx.author} just cleared {amount-2} message(s) in {ctx.channel.mention}", colour=discord.Colour.purple())
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)
		
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Purge Messages Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await ctx.send(embed=em)

@client.command()
@commands.has_role(905700432687538196)
async def clear_all(ctx):

	try:
		await ctx.channel.purge()
		em = discord.Embed(title="📨 | Purged Messages", description=f"{ctx.author} just cleared all messages in {ctx.channel.mention}", colour=discord.Colour.purple())
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)
		
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Purge Messages Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await ctx.send(embed=em)

@client.command()
@commands.has_role(905700432687538196)
async def kick(ctx, member: discord.Member, *, reason):
	try:
		await member.send(f"> You have been kicked from the Dark Alley server. The reason is listed below:```{reason}```")
		await member.kick(reason=reason)
		mod_member = ctx.author
		em = discord.Embed(title="👟 | User kicked", description=f"{ctx.author.mention} kicked {member.mention} from the server\n\nReason:```{reason}```", colour=discord.Colour.purple())
		em.set_footer(text="Message Sent: True")
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)
	except:
		await member.kick(reason=reason)
		mod_member = ctx.author
		em = discord.Embed(title="👟 | User kicked", description=f"{ctx.author.mention} kicked {member.mention} from the server\n\nReason:```{reason}```", colour=discord.Colour.purple())
		em.set_footer(text="Message Sent: False")
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)

@client.command()
@commands.has_role(911803484288999424) 
async def ban(ctx, member: discord.Member, *, reason):
	try:
		await member.send(f"> You have been banned from the Dark Alley server. The reason is listed below:```{reason}```")
		await member.kick(reason=reason)
		mod_member = ctx.author
		em = discord.Embed(title="🔨 | User banned", description=f"{ctx.author.mention} banned {member.mention} from the server\n\nReason:```{reason}```", colour=discord.Colour.purple())
		em.set_footer(text="Message Sent: True")
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)
	except:
		await member.kick(reason=reason)
		mod_member = ctx.author
		em = discord.Embed(title="🔨 | User banned", description=f"{ctx.author.mention} banned {member.mention} from the server\n\nReason:```{reason}```", colour=discord.Colour.purple())
		em.set_footer(text="Message Sent: False")
		mod_logs = client.get_channel(956218604251144272)
		await mod_logs.send(embed=em)

@client.command()
@commands.has_role(911803484288999424)
async def unban(ctx, *, member):
	try:
	    banned_users = await ctx.guild.bans()
	    member_name, member_disc = member.split('#')
	    for banned_entry in banned_users:
	        user = banned_entry.user
	        if (user.name, user.discriminator) == (member_name, member_disc):
	            await ctx.guild.unban(user)
	            await member.send(
	                "> You have been unbanned from the Dark Alley discord Server. You may now send messages and use voice chat!"
	            )
	            await ctx.send(member.mention + " has been unbanned")
	            return
	    await ctx.send(member.mention + " was not found")
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Unban User Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await ctx.reply(embed=em)

@client.command()
async def rps(ctx, choice=None):
	if choice==None:
		await ctx.reply("> You need to enter either `rock`, `paper` or `scissors` to play! Try again.", mention_author=False)
	else:
		bot_choice = random.randint(1,3)
		if bot_choice == 1:
			bot_choice = "rock"
		elif bot_choice == 2:
			bot_choice = "paper"
		elif bot_choice == 3:
			bot_choice = "scissors"
		else:
			await ctx.reply("> Oops, I messed up. Please try again", mention_author=False)
		choice = choice.lower()
		if choice == "rock":
			if bot_choice == "scissors":
				await ctx.reply("> You win, I chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> I win, I chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> Nobody won, we both chose rock (🪨)", mention_author=False)
		elif choice == "paper":
			if bot_choice == "scissors":
				await ctx.reply("> I win, I chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> Nobody won, we both chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> You win, I chose rock (🪨)", mention_author=False)
		elif choice == "scissors":
			if bot_choice == "scissors":
				await ctx.reply("> Nobody won, we both chose scissors (✂️)", mention_author=False)
			elif bot_choice == "paper":
				await ctx.reply("> You win, I chose paper (📄)", mention_author=False)
			elif bot_choice == "rock":
				await ctx.reply("> I win, I chose rock (🪨)", mention_author=False)
		else:
			await ctx.reply(f"> {choice}, really? You didn't enter `rock`, `paper` or `scissors`. Do you know how to play?", mention_author=False)


@client.command(aliases = ['gg'])
async def guessing_game(ctx):
	bot_number= random.randint(1,100)
	bot_number2 = random.randint(1,100)
	if bot_number > bot_number2:
		answer = "⬆️"
	elif bot_number < bot_number2:
		answer = "⬇️"
	elif bot_number == bot_number2:
		answer = "🤑"
	else:
		await ctx.reply(f">>> Oops, I messed up, please try again", mention_author=False)
	msg = await ctx.reply(f">>> Your number is `{bot_number2}`. Do you think that the number is higher (⬆️), lower (⬇️), or the same as `{bot_number2}` (🤑)?", mention_author=False)
	await msg.add_reaction("⬆️")
	await msg.add_reaction("⬇️")
	await msg.add_reaction("🤑")
	def check(reaction, user):
		return user == ctx.message.author and str(reaction.emoji) in ['⬆️', '⬇️', '🤑']
	try:
		reaction, user = await client.wait_for('reaction_add', timeout=10, check=check)
		if reaction.emoji == '⬆️':
			if answer == '⬆️':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
				await msg.clear_reactions()
			elif answer == '🤑':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()
			elif answer == '⬇️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
				await msg.clear_reactions()
		elif reaction.emoji == '⬇️':
			if answer == '⬆️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()
			elif answer == '🤑':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()			
			elif answer == '⬇️':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
				await msg.clear_reactions()
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
				await msg.clear_reactions()
		elif reaction.emoji == '🤑':
			if answer == '⬆️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()
			elif answer == '🤑':
				await msg.edit(content=f"> Correct, how did you get that? The number I chose was {bot_number}")
				await msg.clear_reactions()
			elif answer == '⬇️':
				await msg.edit(content=f"> Wrong, good try. The number I chose was {bot_number}")
				await msg.clear_reactions()
			else:
				await msg.edit(content="Oops, I messed up. Please try again")
				await msg.clear_reactions()
		else:
			await msg.edit(content="Oops, I messed up. Please try again")
	except asyncio.TimeoutError:
		await msg.edit(content="Timed out")
		await msg.clear_reactions()




keep_alive()
client.run(token)
