import discord
import json

with open('config.json', 'r') as f:
    data = json.load(f)
    bugcrowdlogourl = data['bugcrowdlogourl']
    embedcolor = int(data['embedcolor'][1:], 16)






# Legal Reply
legalembed=discord.Embed(title="Bugcrowd is for legal hacking!", color=embedcolor)
legalembed.set_thumbnail(url=bugcrowdlogourl)
legalembed.add_field(name="", value="Do not request or discuss illegal hacking. Hacking violates not only the server rules, but the law. If you are trying to get an account recovered, contact that platform's support.", inline=False)


# The Beginner's Guide
beginnersguideembed = discord.Embed(title="The Beginner's Guide", description="The freshly-canned response to \"Where the hell do I start?!\"", color=embedcolor)
beginnersguideembed.set_thumbnail(url=bugcrowdlogourl)
beginnersguideembed.add_field(name="We have a list of resources just for this exact thing! ", value="Click here: https://discord.com/channels/319555028341882885/575438624397590539/1364496033626984489", inline=False)


# Items Needed
itemsneededembed = discord.Embed(title="Items Needed", description="", color=embedcolor)
itemsneededembed.set_thumbnail(url=bugcrowdlogourl)
itemsneededembed.add_field(name="You will need:", value="One (1) Computer", inline=False)
itemsneededembed.add_field(name="FAQ: Does it need to be fast?", value="No.", inline=False)
itemsneededembed.add_field(name="But it's a computer from 2008!", value="Any computer new enough to run Linux will work just fine.", inline=False)
itemsneededembed.add_field(name="Can it be a Chromebook?", value="A Chromebook is not a computer, unless you [put Linux on it](https://geekflare.com/dev/install-linux-on-chromebook/).", inline=False)
itemsneededembed.add_field(name="Can it be a phone?", value="No Patrick, a phone is not a computer either.", inline=False)
itemsneededembed.add_field(name="But Tony Stark was able to build this in a cave! With a box of scraps!", value="And you can build a computer in a cave with a box of scraps. Don't use a phone.", inline=False)
itemsneededembed.add_field(name="What Linux distribution should I use?", value="Use something basic, like [Linux Mint](https://linuxmint.com/), [Ubuntu](https://ubuntu.com/desktop), [Debian](https://www.debian.org/), or [Zorin](https://zorin.com/os/). Avoid pentesting-specific distributions, especially when learning. Selecting and installing tools on your own gives you a greater level of experience with each one.", inline=False)


# Don't Ask to Ask
dontasktoaskembed = discord.Embed(title="Don't ask to ask", description="If you have a question, just ask it.", color=embedcolor)
dontasktoaskembed.set_thumbnail(url=bugcrowdlogourl)
dontasktoaskembed.add_field(name="Don't ask 'can somebody help me?'", value="__Just ask your question.__", inline=False)
dontasktoaskembed.add_field(name="Don't say 'I have a question'", value="*Just ask your question.*", inline=False)
dontasktoaskembed.add_field(name="Don't say 'I need help'", value="**Just ask your question.**", inline=False)
dontasktoaskembed.add_field(name="Don't say 'Can I ask a question?'", value="***Just ask your question.***", inline=False)
dontasktoaskembed.add_field(name="Don't say 'Can someone DM me?'", value="***__Just ask your question.__***\n-# Also, moving to DMs makes you more vulnerable to getting scammed!", inline=False)


# "Hacking Back" an Account
hackingbackembed = discord.Embed(title="\'Hacking back\' an account is illegal", description="", color=embedcolor)
hackingbackembed.set_thumbnail(url=bugcrowdlogourl)
hackingbackembed.add_field(name="Consider this:", value="If you have a paperwork issue with the bank, is a robbery legal? Of course no  t, and neither is breaking into an app or service because you forgot your password.", inline=False)
hackingbackembed.add_field(name="If you are trying to recover an account, contact that platform's support.", value="Tried that already and it didn't work? Try again. We certainly can't help you.", inline=False)
hackingbackembed.add_field(name="Instagram Suport", value="[Website](https://www.instagram.com/hacked/)", inline=True)
hackingbackembed.add_field(name="Snapchat Support", value="[Website](https://help.snapchat.com/hc/en-us/requests/new)", inline=True)
hackingbackembed.add_field(name="Roblox Support", value="[Website](https://en.help.roblox.com/hc/en-us/articles/203313390)", inline=True)
hackingbackembed.add_field(name="Facebook Support", value="[Website](https://www.facebook.com/hacked)", inline=True)
hackingbackembed.add_field(name="Discord Support", value="[Website](https://support.discord.com/hc/en-us/articles/24160905919511)", inline=True)
hackingbackembed.add_field(name="Google (Gmail) Support", value="[Website](https://support.google.com/accounts/answer/6294825)", inline=True)


# How long to find a bug?
howlongembed = discord.Embed(title="How long does it take to find a bug?", description="As with all great answers, \'it depends\"", color=embedcolor)
howlongembed.set_thumbnail(url=bugcrowdlogourl)
howlongembed.add_field(name="If you're just starting out, it can take a while to find your first bug.", value="", inline=False)