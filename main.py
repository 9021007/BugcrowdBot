import discord
from discord.ext import tasks
import json
import re
import platform
import psutil
import datetime
import pg8000.native
from cannedresponses import *
from verificationui import *

# SETTINGS and PREFABS

# fetch options from file
with open('config.json', 'r') as f:
    data = json.load(f)
    token = data['token']
    mode = data['mode']
    testbotlogchannel = int(data['testbotlogchannel'])
    testhackerrole = int(data['testhackerrole'])
    testserver = int(data['testserver'])
    testcrowdstream = int(data['testcrowdstream'])
    prodbotlogchannel = int(data['prodbotlogchannel'])
    prodhackerrole = int(data['prodhackerrole'])
    prodserver = int(data['prodserver'])
    prodcrowdstream = int(data['prodcrowdstream'])
    bugcrowdlogourl = data['bugcrowdlogourl']
    embedcolor = int(data['embedcolor'][1:], 16)
    db_db=data['db_db']
    db_user=data['db_user']
    crowdstreamurl = data['crowdstreamurl']
    pemojis= data['pemojis']

if mode == "test":
    hackerrole = testhackerrole
    botlogchannel = testbotlogchannel
    server = testserver
    crowdstream = testcrowdstream
elif mode == "prod":
    hackerrole = prodhackerrole
    botlogchannel = prodbotlogchannel
    server = prodserver
    crowdstream = prodcrowdstream
else:
    print("Invalid mode in config.json. Please enter 'test' or 'prod'.")
    exit()

# connect to the database
try:
    con = pg8000.native.Connection(database=db_db, user=db_user)
    print(con.run("SELECT * FROM leaderboard LIMIT 1"))
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()

starttime = datetime.datetime.now()

# initialize the bot client
client = discord.Bot(intents=discord.Intents.all(), persistent_views_added = False)

@tasks.loop(minutes=1)
async def crowdStreamCheck():
    try:
        async with client.http._HTTPClient__session.get(crowdstreamurl) as response:
            if response.status == 200:
                data = await response.json()
                latestCsUUID = con.run("SELECT latest_crowdstream FROM data")[0][0]
                print(f"Latest Crowdstream UUID in DB: {latestCsUUID}")
                if (data['results'][0]['id'] != str(latestCsUUID)):
                    con.run("UPDATE data SET latest_crowdstream = :latest_crowdstream", latest_crowdstream=data['results'][0]['id'])
                    cschannel = client.get_channel(crowdstream)
                    thiscsitem = data['results'][0]
                    if cschannel is not None:
                        embed = discord.Embed(title=thiscsitem['submission_state_text'], color=embedcolor)
                        embed.set_thumbnail(url=thiscsitem['logo_url'])
                        # if researcher username key exists
                        if 'researcher_username' in thiscsitem:
                            embed.add_field(name="Researcher", value=f"[{thiscsitem['researcher_username']}](https://bugcrowd.com{thiscsitem['researcher_profile_path']})", inline=False)
                        else:
                            embed.add_field(name="Researcher", value="Private User", inline=False)
                        embed.add_field(name="Engagement", value=f"[{thiscsitem['engagement_name']}](https://bugcrowd.com{thiscsitem['engagement_path']})", inline=False)
                        if 'amount' in thiscsitem:
                            embed.add_field(name="Reward", value=thiscsitem['amount'], inline=False)
                        embed.add_field(name="Priority", value=f"<:p{thiscsitem['priority']}:{pemojis[thiscsitem['priority']-1]}>", inline=False)
                        embed.set_footer(text=thiscsitem['submission_state_date_text'])
                        # add button to bottom, called "View CrowdStream"
                        view = discord.ui.View()
                        view.add_item(discord.ui.Button(label="View CrowdStream", url="https://bugcrowd.com/crowdstream"))
                        if 'disclosure_report_url' in thiscsitem:
                            view.add_item(discord.ui.Button(label="View Disclosure Report", url=f"https://bugcrowd.com{thiscsitem['disclosure_report_url']}"))
                        await cschannel.send(embed=embed, view=view)
                    else:
                        print("Crowdstream channel not found.")
                    
            else:
                print(f"Error fetching crowdstream data: {response.status}")
    except Exception as e:
        print(f"Exception in crowdStreamCheck: {e}")
    


@client.event
async def on_ready():
    client.add_view(firstView())
    client.persistent_views_added = True
    print(f'We have logged in as {client.user}')
    # run crowdStreamCheck every 10 minutes
    crowdStreamCheck.start()





@client.event # when a message is sent in chat
async def on_message(message):
    if message.author == client.user: # filter bot's own messages
        return

    if message.guild is None: # filter DMs
        return
    
    if message.guild.id != server:
        return

    if message.content.startswith('$createembed'): # create an embed

        if message.author.guild_permissions.kick_members:
            embed=discord.Embed(title="Welcome to the Bugcrowd Discord!", description="Bugcrowd's online hacker community. Hacking discussion, collaboration, networking, giveaways, and pizza parties.", color=embedcolor)
            embed.set_thumbnail(url=bugcrowdlogourl)
            embed.add_field(name="Answer this question:", value="I am...", inline=False)
            await message.channel.send(embed=embed, view=firstView())
        else:
            await message.channel.send("You must be an administrator to use this command.")
            await logToChannel(f"User {message.author} tried to use the $createembed command without permission.")

    if re.search(r'(?:i have a question|(?:hey )?can (?:some|any)(?:one |body )help(?: me)?(?: out)?|i need help|(?:some|any)(?:one|body) (?:online|available|here))(?: please)?', message.content, re.IGNORECASE):
        # if message count less than 15
        if con.run("SELECT count FROM leaderboard WHERE user_id = :user_id", user_id=message.author.id):
            await message.reply(embed=dontasktoaskembed, mention_author=True)

    # increment the leaderboard, cols are ['user_id', 'count']
    if message.guild.id == server:
        con.run("INSERT INTO leaderboard (user_id, count) VALUES (:user_id, 1) ON CONFLICT (user_id) DO UPDATE SET count = leaderboard.count + 1", user_id=message.author.id)


    
    # TODO check for skids dynacmically

# SLASH COMMANDS

@client.command(description="Bot info and status check")
async def ping(ctx):
    uptime = datetime.datetime.now() - starttime
    embed=discord.Embed(title="Bugcrowd Bot", description="A bot for the Bugcrowd Discord server.", color=embedcolor)
    embed.set_thumbnail(url=bugcrowdlogourl)
    embed.add_field(name="Status", value="Online", inline=True)
    embed.add_field(name="Mode", value=mode, inline=True)
    embed.add_field(name="Latency", value=f"{client.latency * 1000:.2f}ms", inline=True)
    embed.add_field(name="Python Version", value=platform.python_version(), inline=True)
    embed.add_field(name="Discord.py", value=discord.__version__, inline=True)
    embed.add_field(name="Server", value=platform.system() + " " + platform.release(), inline=True)
    embed.add_field(name="CPU", value=platform.processor(), inline=True)
    embed.add_field(name="Memory", value=f"{psutil.virtual_memory().percent}%", inline=True)
    embed.add_field(name="Uptime", value=f'{uptime.days} days, {uptime.seconds//3600} hours, {(uptime.seconds//60)%60} minutes', inline=True)
    await ctx.respond(embed=embed)

@client.command(description="View the message leaderboard")
async def leaderboard(ctx):
    # fetch the leaderboard from the database
    leaderboard = con.run("SELECT user_id, count FROM leaderboard ORDER BY count DESC LIMIT 10")
    yourcount = con.run("SELECT count FROM leaderboard WHERE user_id = :user_id", user_id=ctx.author.id)
    
    embed = discord.Embed(title="Leaderboard", description="Top 10 users by message count", color=embedcolor)
    embed.set_thumbnail(url=bugcrowdlogourl)
    place = 1
    for row in leaderboard:
        embed.add_field(name=f"", value=f'`{place}` - <@{row[0]}> - **{row[1]}** Messages\n', inline=False)
        place += 1

    if yourcount:
        yourcount = yourcount[0][0]
        embed.add_field(name=f"---- Your Count ----", value=yourcount, inline=False)

    await ctx.respond(embed=embed)

# accept message author id
class CannedResponseView(discord.ui.View):
    def __init__(self, targetid):
        super().__init__(timeout=None)
        self.targetid = targetid

    @discord.ui.select(placeholder="Select a canned response", options=[
        discord.SelectOption(label="Legal Reply", value="legal_reply"),
        discord.SelectOption(label="The Beginner's Guide", value="beginners_guide"),
        discord.SelectOption(label="Items Needed", value="items_needed"),
        discord.SelectOption(label="Don't Ask to Ask", value="dont_ask_to_ask"),
        discord.SelectOption(label="Hacking Back an Account", value="hacking_back")
    ])
    async def select_callback(self, select, interaction):
        tosend = None
        if select.values[0] == "legal_reply":
            tosend = legalembed
            tosend.set_footer(text="ANYONE offering to hack without permission is trying to SCAM YOU, ignore any DMs from people claiming to be able to do so.")
        elif select.values[0] == "beginners_guide":
            tosend = beginnersguideembed
        elif select.values[0] == "items_needed":
            tosend = itemsneededembed
        elif select.values[0] == "dont_ask_to_ask":
            tosend = dontasktoaskembed
        elif select.values[0] == "hacking_back":
            tosend = hackingbackembed
        await interaction.response.send_message(f'<@{self.targetid}>', embed=tosend, ephemeral=False)


    


 

@client.message_command(name="Canned Responses")
async def cannedresponses(ctx, message: discord.Message):
    # dropdown menu with options
    if message.guild.id != server:
        return
    if not message.channel.permissions_for(ctx.author).send_messages:
        await ctx.respond("You don't have permission to send messages in that channel.")
        return
    embed = discord.Embed(title="Canned Responses", description="A list of canned responses for common questions.", color=embedcolor)
    embed.set_thumbnail(url=bugcrowdlogourl)
    embed.add_field(name="Select a response:", value="Use the dropdown menu below to select a canned response.", inline=False)
    view = CannedResponseView(targetid=message.author.id)
    await ctx.respond(embed=embed, view=view, ephemeral=True)

# run the bot
client.run(token)
