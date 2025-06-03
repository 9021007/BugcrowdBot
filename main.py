import discord
import json
import re
import platform
import psutil
import datetime
import pg8000.native

# SETTINGS and PREFABS

# fetch options from file
with open('config.json', 'r') as f:
    data = json.load(f)
    token = data['token']
    mode = data['mode']
    testbotlogchannel = int(data['testbotlogchannel'])
    testhackerrole = int(data['testhackerrole'])
    testserver = int(data['testserver'])
    prodbotlogchannel = int(data['prodbotlogchannel'])
    prodhackerrole = int(data['prodhackerrole'])
    prodserver = int(data['prodserver'])
    bugcrowdlogourl = data['bugcrowdlogourl']
    embedcolor = int(data['embedcolor'][1:], 16)
    db_db=data['db_db']
    db_user=data['db_user']

if mode == "test":
    hackerrole = testhackerrole
    botlogchannel = testbotlogchannel
    server = testserver
elif mode == "prod":
    hackerrole = prodhackerrole
    botlogchannel = prodbotlogchannel
    server = prodserver
else:
    print("Invalid mode in config.json. Please enter 'test' or 'prod'.")
    exit()

with open('rules.txt', 'r') as f:
    rules = f.read()

# connect to the database
try:
    con = pg8000.native.Connection(database=db_db, user=db_user)
    print(con.run("SELECT * FROM leaderboard LIMIT 1"))
except Exception as e:
    print(f"Error connecting to the database: {e}")
    exit()


legalembed=discord.Embed(title="Bugcrowd is for legal hacking!", color=embedcolor)
legalembed.set_thumbnail(url=bugcrowdlogourl)
legalembed.add_field(name="", value="Do not request or discuss illegal hacking. Hacking violates not only the server rules, but the law. If you are trying to get an account recovered, contact that platform's support.", inline=False)

starttime = datetime.datetime.now()

# initialize the bot client
client = discord.Bot(intents=discord.Intents.all(), persistent_views_added = False)

@client.event
async def on_ready():
    client.add_view(firstView())
    client.persistent_views_added = True
    print(f'We have logged in as {client.user}')

def logToChannel(message):
    return client.get_channel(botlogchannel).send(message)

async def allowIn(interaction):
    await interaction.response.send_message(rules, view=rulesView(), ephemeral=True)
    

class rulesView(discord.ui.View): # buttons on the "I solemnly swear" embed
    @discord.ui.button(label="I agree", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome to the Bugcrowd Discord!', ephemeral=True)
        await logToChannel(f"User {interaction.user} agreed to the rules in the screener.")
        await interaction.user.add_roles(discord.Object(hackerrole))

    @discord.ui.button(label="I don't agree", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message('You must agree to the rules to join the Bugcrowd Discord.', ephemeral=True)
        

class firstView(discord.ui.View): # buttons on the initial embed
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="A hacker", row=0, style=discord.ButtonStyle.primary, custom_id="hacker_button")
    async def first_button_callback(self, button, interaction):
        # await interaction.response.send_message('Welcome!', ephemeral=True)
        await allowIn(interaction)

    @discord.ui.button(label="Looking for hackers", row=1, style=discord.ButtonStyle.primary, custom_id="looking_for_hackers_button")
    async def second_button_callback(self, button, interaction):

        embed=discord.Embed(title="Sounds good!", description="Keep answering the questions to get started.", color=embedcolor)
        embed.set_thumbnail(url=bugcrowdlogourl)
        embed.add_field(name="Answer this question:", value="I am...", inline=False)
        
        await interaction.response.send_message(embed=embed, view=secondView(), ephemeral=True)
    
    @discord.ui.button(label="Something Else", row=2, style=discord.ButtonStyle.secondary, custom_id="something_else_button")
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message('Here are some more options:', view=extraFirstView(), ephemeral=True)

class extraFirstView(discord.ui.View): # buttons on the "Something Else" embed
    @discord.ui.button(label="A hacker", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        # await interaction.response.send_message('Welcome!', ephemeral=True)
        await allowIn(interaction)

    @discord.ui.button(label="Looking for hackers", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):

        embed=discord.Embed(title="Sounds good!", description="Keep answering the questions to get started.", color=embedcolor)
        embed.set_thumbnail(url=bugcrowdlogourl)
        embed.add_field(name="Answer this question:", value="I am...", inline=False)
        
        await interaction.response.send_message(embed=embed, view=secondView(), ephemeral=True)

    @discord.ui.button(label="Learning to hack", row=2, style=discord.ButtonStyle.secondary)
    async def third_button_callback(self, button, interaction):
        logToChannel(f"User {interaction.user} selected they are learning to hack in the screener.")
        await allowIn(interaction)

    @discord.ui.button(label="Curious about the industry", row=2, style=discord.ButtonStyle.secondary)
    async def fourth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are curious about the industry in the screener.")
        await allowIn(interaction)

    @discord.ui.button(label="Looking for collaborators", row=2, style=discord.ButtonStyle.secondary)
    async def fifth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are looking for collaborators in the screener.")
        await allowIn(interaction)

    @discord.ui.button(label="VDP/BBP Target representative", row=2, style=discord.ButtonStyle.secondary)
    async def sixth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are a VDP/BBP Target representative in the screener.")
        await allowIn(interaction)

class secondView(discord.ui.View): # buttons on the "I am looking for a hacker" embed
    @discord.ui.button(label="A person", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        legalembed.set_footer(text="If you aren't here to ask for illegal hacking, press the gray button.")
        await interaction.response.send_message(embed=legalembed, view=skidView(), ephemeral=True)
        await logToChannel(f"User {interaction.user} selected they are a person looking for a hacker in the screener.")
    
    @discord.ui.button(label="A company", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        embed=discord.Embed(title="#1 Crowdsourced Cybersecurity Platform | Bugcrowd", url="https://www.bugcrowd.com", description="Bugcrowd offers a platform that combines data, technology, human intelligence, and remediation workflows to secure your digital innovation. You can collaborate with a global community of trusted researchers, configure pen tests, and access vulnerability reports from the public.", color=embedcolor)
        embed.set_thumbnail(url=bugcrowdlogourl)
        embed.add_field(name="To get started with joining Bugcrowd, head to the website!", value="", inline=True)
        await interaction.response.send_message(embed=embed, view=companyLinkView(), ephemeral=True)

class companyLinkView(discord.ui.View): # button on the "I am looking for a hacker" > "I am a company" embed
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Learn More", url="https://www.bugcrowd.com"))

class skidView(discord.ui.View): # buttons on the "I am looking for a hacker" > "I am a person" embed
    @discord.ui.button(label="Leave Server", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Goodbye!', ephemeral=True)
        await interaction.user.kick(reason="User selected they are a skid.")
        await logToChannel(f"User {interaction.user} was kicked for selecting they are a skid in the screener.")
    
    @discord.ui.button(label="Stay", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} arrived at the 'I solemnly swear' embed in the screener.")
        await interaction.response.send_message('# I solemnly swear that...\n\n### 🚫 - I am not asking for someone to recover an account\n\n### 🚫 - I am not asking someone to track down an alledged scammer\n\n### 🚫 - I am not asking someone to stalk my ex\n\n## __Understood?__\n-# If you don\'t listen, you will be banned. The moderators can see that you have read this message.', view=swearView(), ephemeral=True)

class swearView(discord.ui.View): # buttons on the "I solemnly swear" embed
    @discord.ui.button(label="I swear", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they swear in the screener.")
        await allowIn(interaction)

    @discord.ui.button(label="I don't swear", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they don't swear in the screener.")
        await interaction.response.send_message('Sorry, but you must swear to join the Bugcrowd Discord.', ephemeral=True)

@client.event # when a message is sent in chat
async def on_message(message):
    if message.author == client.user: # filter bot's own messages
        return

    if message.content.startswith('$createembed'): # create an embed

        # check if ok to send
        if message.guild.id != server:
            return

        if message.author.guild_permissions.kick_members:
            embed=discord.Embed(title="Welcome to the Bugcrowd Discord!", description="Bugcrowd's online hacker community. Hacking discussion, collaboration, networking, giveaways, and pizza parties.", color=embedcolor)
            embed.set_thumbnail(url=bugcrowdlogourl)
            embed.add_field(name="Answer this question:", value="I am...", inline=False)
            await message.channel.send(embed=embed, view=firstView())
        else:
            await message.channel.send("You must be an administrator to use this command.")
            await logToChannel(f"User {message.author} tried to use the $createembed command without permission.")

    # increment the leaderboard, cols are ['user_id', 'count']
    con.run("INSERT INTO leaderboard (user_id, count) VALUES (:user_id, 1) ON CONFLICT (user_id) DO UPDATE SET count = leaderboard.count + 1", user_id=message.author.id)


    
    # TODO check for skids dynacmically

# SLASH COMMANDS

@client.command(description="Bot info and status check")
async def ping(ctx):
    uptime = datetime.datetime.now() - starttimex
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

    for row in leaderboard:

        try:
            thisuser = await client.fetch_user(row[0])
        except discord.NotFound:
            thisuser = f"User {row[0]} (not found)"
        except discord.HTTPException:
            thisuser = f"User {row[0]} (not found)"
        embed.add_field(name=thisuser, value=row[1], inline=False)

    if yourcount:
        yourcount = yourcount[0][0]
        embed.add_field(name=f"---- Your Count ----", value=yourcount, inline=False)

    await ctx.respond(embed=embed)

# legal warning with reply
@client.message_command(name="Legal Reminder")
async def legalreply(ctx, message: discord.Message):

    if message.guild.id != server:
        return

    # if not ctx.author.permissions_in(message.channel).send_messages:
    if not message.channel.permissions_for(ctx.author).send_messages:
        await ctx.respond("You don't have permission to send messages in that channel.")
        return
    legalembed.set_footer(text="ANYONE offering to hack without permission is trying to SCAM YOU, ignore any DMs from people claiming to be able to do so.")
    await ctx.respond(f'<@{message.author.id}>',embed=legalembed, view=None, ephemeral=False)

# run the bot
client.run(token)
