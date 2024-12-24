import discord
import json
import re

# SETTINGS and PREFABS

# fetch options from file
with open('config.json', 'r') as f:
    data = json.load(f)
    token = data['token']
    mode = data['mode']
    testbotlogchannel = data['testbotlogchannel']
    testhackerrole = data['testhackerrole']
    testserver = data['testserver']
    prodbotlogchannel = data['prodbotlogchannel']
    prodhackerrole = data['prodhackerrole']
    prodserver = data['prodserver']
    bugcrowdlogourl = data['bugcrowdlogourl']

# legalembed=discord.Embed(title="Bugcrowd is for legal hacking!", description="This Discord server is for hackers who get permission when targeting companies. If you are looking to hire a hacker to attack a target for you, unless you have that target's explicit consent, we can't help you.")
# legalembed.set_thumbnail(url=bugcrowdlogourl)
# legalembed.add_field(name="No, just becuase your account was hacked doesn't make it legal to \"hack back\".", value="To hack your account, we would have to hack the company your account is on (i.e. Instagram, Google, etc), and they didn't give consent! Hacking those companies without consent is illegal.", inline=False)
# legalembed.add_field(name="No, we cannot recover your crypto.", value="Anyone claiming to be able to is a scammer.", inline=False)
# legalembed.add_field(name="No, we will not find the location or name of a person, even if they are doing something wrong.", value="That is just stalking. Two wrongs don't make a right.", inline=True)

legalembed=discord.Embed(title="Bugcrowd is for legal hacking!", color=0xed7123)
legalembed.set_thumbnail(url=bugcrowdlogourl)
legalembed.add_field(name="", value="Do not request or discuss illegal hacking. Hacking violates not only the server rules, but the law. If you are trying to get an account recovered, contact that platform's support. This is your final warning, next time is a ban.", inline=False)

# initialize the bot client
client = discord.Bot(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

def logToChannel(message):
    guildtosend = 0
    if mode == "test":
        guildtosend = testbotlogchannel
    elif mode == "prod":
        guildtosend = prodbotlogchannel
    return client.get_channel(guildtosend).send(message)
        

class firstView(discord.ui.View): # buttons on the initial embed
    @discord.ui.button(label="A hacker", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

    @discord.ui.button(label="Looking for hackers", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):

        embed=discord.Embed(title="Sounds good!", description="Keep answering the questions to get started.", color=0xed722e)
        embed.set_thumbnail(url=bugcrowdlogourl)
        embed.add_field(name="Answer this question:", value="I am...", inline=False)
        
        await interaction.response.send_message(embed=embed, view=secondView(), ephemeral=True)
    
    @discord.ui.button(label="Something Else", row=2, style=discord.ButtonStyle.secondary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message('Here are some more options:', view=extraFirstView(), ephemeral=True)

class extraFirstView(discord.ui.View): # buttons on the "Something Else" embed
    @discord.ui.button(label="A hacker", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

    @discord.ui.button(label="Looking for hackers", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):

        embed=discord.Embed(title="Sounds good!", description="Keep answering the questions to get started.", color=0xed722e)
        embed.set_thumbnail(url=bugcrowdlogourl)
        embed.add_field(name="Answer this question:", value="I am...", inline=False)
        
        await interaction.response.send_message(embed=embed, view=secondView(), ephemeral=True)

    @discord.ui.button(label="Learning to hack", row=2, style=discord.ButtonStyle.secondary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

    @discord.ui.button(label="Curious about the industry", row=2, style=discord.ButtonStyle.secondary)
    async def fourth_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

    @discord.ui.button(label="Looking for collaborators", row=2, style=discord.ButtonStyle.secondary)
    async def fifth_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

    @discord.ui.button(label="VDP/BBP Target representative", row=2, style=discord.ButtonStyle.secondary)
    async def sixth_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome!', ephemeral=True)

class secondView(discord.ui.View): # buttons on the "I am looking for a hacker" embed
    @discord.ui.button(label="A person", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        legalembed.set_footer(text="If you aren't here to ask for illegal hacking, press the gray button.")
        await interaction.response.send_message(embed=legalembed, view=skidView(), ephemeral=True)
        await logToChannel(f"User {interaction.user} selected they are a person looking for a hacker in the screener.")
    
    @discord.ui.button(label="A company", row=1, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        embed=discord.Embed(title="#1 Crowdsourced Cybersecurity Platform | Bugcrowd", url="https://www.bugcrowd.com", description="Bugcrowd offers a platform that combines data, technology, human intelligence, and remediation workflows to secure your digital innovation. You can collaborate with a global community of trusted researchers, configure pen tests, and access vulnerability reports from the public.", color=0xed722e)
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
        await interaction.response.send_message('I solemnly swear that I am not asking anyone to do anything illegal, as explained above.', view=swearView(), ephemeral=True)

class swearView(discord.ui.View): # buttons on the "I solemnly swear" embed
    @discord.ui.button(label="I swear", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome to the Bugcrowd Discord!', ephemeral=True)

    @discord.ui.button(label="I don't swear", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message('Sorry, but you must swear to join the Bugcrowd Discord.', ephemeral=True)

@client.event # when a message is sent in chat
async def on_message(message):
    if message.author == client.user: # filter bot's own messages
        return

    if message.content.startswith('$createembed'): # create an embed

        # check if ok to send
        if (message.guild.id != testserver and mode == "test") or (message.guild.id != prodserver and mode == "prod"):
            return

        if message.author.guild_permissions.kick_members:
            embed=discord.Embed(title="Welcome to the Bugcrowd Discord!", description="Bugcrowd's online hacker community. Hacking discussion, collaboration, networking, giveaways, and pizza parties.", color=0xed722e)
            embed.set_thumbnail(url=bugcrowdlogourl)
            embed.add_field(name="Answer this question:", value="I am...", inline=False)
            await message.channel.send(embed=embed, view=firstView(timeout=None))
        else:
            await message.channel.send("You must be an administrator to use this command.")
            await logToChannel(f"User {message.author} tried to use the $createembed command without permission.")

    # TODO check for skids dynacmically

# SLASH COMMANDS

# @client.command(description="Sends the bot's latency.")
# async def ping(ctx):
#     await ctx.respond(f"Pong! Latency is {client.latency}")

# legal warning with reply
@client.message_command(name="Legal Reminder")
async def legalreply(ctx, message: discord.Message):

    if (message.guild.id != testserver and mode == "test") or (message.guild.id != prodserver and mode == "prod"):
        return

    # if not ctx.author.permissions_in(message.channel).send_messages:
    if not message.channel.permissions_for(ctx.author).send_messages:
        await ctx.respond("You don't have permission to send messages in that channel.")
        return
    legalembed.set_footer(text="Anyone offering to hack without permission is a scammer.")
    await ctx.respond(f'<@{message.author.id}>',embed=legalembed, view=None, ephemeral=False)

# run the bot
client.run(token)
