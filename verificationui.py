import discord
import json
from cannedresponses import *

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
with open('rules.txt', 'r') as f:
    rules = f.read()
if mode == "test":
    hackerrole = testhackerrole
    botlogchannel = testbotlogchannel
    server = testserver
elif mode == "prod":
    hackerrole = prodhackerrole
    botlogchannel = prodbotlogchannel
    server = prodserver

def logToChannel(message, client=None):
    return client.get_channel(botlogchannel).send(message)

async def allowIn(interaction):
    await interaction.response.send_message(rules, view=rulesView(), ephemeral=True)
    

class rulesView(discord.ui.View): # buttons on the "I solemnly swear" embed
    @discord.ui.button(label="I agree", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_message('Welcome to the Bugcrowd Discord!', ephemeral=True)
        await logToChannel(f"User {interaction.user} agreed to the rules in the screener.", client=interaction.client)
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
        await logToChannel(f"User {interaction.user} selected they are learning to hack in the screener.", client=interaction.client)
        await allowIn(interaction)

    @discord.ui.button(label="Curious about the industry", row=2, style=discord.ButtonStyle.secondary)
    async def fourth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are curious about the industry in the screener.", client=interaction.client)
        await allowIn(interaction)

    @discord.ui.button(label="Looking for collaborators", row=2, style=discord.ButtonStyle.secondary)
    async def fifth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are looking for collaborators in the screener.", client=interaction.client)
        await allowIn(interaction)

    @discord.ui.button(label="VDP/BBP Target representative", row=2, style=discord.ButtonStyle.secondary)
    async def sixth_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they are a VDP/BBP Target representative in the screener.", client=interaction.client)
        await allowIn(interaction)

class secondView(discord.ui.View): # buttons on the "I am looking for a hacker" embed
    @discord.ui.button(label="A person", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        legalembed.set_footer(text="If you aren't here to ask for illegal hacking, press the gray button.")
        await interaction.response.send_message(embed=legalembed, view=skidView(), ephemeral=True)
        await logToChannel(f"User {interaction.user} selected they are a person looking for a hacker in the screener.", client=interaction.client)
    
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
        await logToChannel(f"User {interaction.user} was kicked for selecting they are a skid in the screener.", client=interaction.client)
    
    @discord.ui.button(label="Stay", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} arrived at the 'I solemnly swear' embed in the screener.", client=interaction.client)
        await interaction.response.send_message('# I solemnly swear that...\n\n### 🚫 - I am not asking for someone to recover an account\n\n### 🚫 - I am not asking someone to track down an alledged scammer\n\n### 🚫 - I am not asking someone to stalk my ex\n\n## __Understood?__\n-# If you don\'t listen, you will be banned. The moderators can see that you have read this message.', view=swearView(), ephemeral=True)

class swearView(discord.ui.View): # buttons on the "I solemnly swear" embed
    @discord.ui.button(label="I swear", row=0, style=discord.ButtonStyle.secondary)
    async def first_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they swear in the screener.", client=interaction.client)
        await allowIn(interaction)

    @discord.ui.button(label="I don't swear", row=0, style=discord.ButtonStyle.secondary)
    async def second_button_callback(self, button, interaction):
        await logToChannel(f"User {interaction.user} selected they don't swear in the screener.", client=interaction.client)
        await interaction.response.send_message('Sorry, but you must swear to join the Bugcrowd Discord.', ephemeral=True)