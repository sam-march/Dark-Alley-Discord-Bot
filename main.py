import os
import discord
from discord import Member
from discord.utils import get
from webserver import keep_alive
import random
import asyncio
import time
import youtube_dl
import pafy
from random import choice
from discord.ext import commands, tasks




token = os.environ['token']
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}

        self.setup()

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")

        if ctx.voice_client is None:
            return await ctx.send("I must be in a voice channel to play a song.")

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")
			
            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")

    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.red())
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.dark_gold())
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**80% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.blue())
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 15 seconds.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(15) # 15 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.79: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 80% of the members to skip.**", colour=discord.Colour.red())

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")
        
        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")


@client.event
async def on_ready():
	print("Bot is online and ready to serve!")
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f" $help"))
	await client.add_cog(Player(client))


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
	                "> You have been unbanned from the Dark Alley Discord Server. You may now send messages and use voice chat!"
	            )
	            await ctx.send(member.mention + " has been unbanned")
	            return
	    await ctx.send(member.mention + " was not found")
	except:
		dev = client.get_user(723569355710922802)
		em = discord.Embed(title=f"❌ | Unban User Failed", description=f"The bot encountered an error when executing this command. This may be due to you, or the bot, not having the correct permissions. Please contact a superior or {dev.mention}", colour=discord.Colour.purple())
		await ctx.reply(embed=em)






keep_alive()
client.run(token)