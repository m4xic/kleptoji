import dotenv
import os
import re
import random
import traceback
import requests
import discord

dotenv.load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print("Kleptoji is ready!")

@client.event
async def on_message(ctx):
    if not ctx.content.startswith('steal'):
        return
    emojis = ctx.content.split('steal ')[-1]
    status_message = list("Stealing emojis... 👤💰 ")
    base_length = len(status_message)
    msg = await ctx.channel.send(''.join(status_message))
    animated_emojis = re.findall(r'<a:(.+?):(\d+)>', emojis)
    still_emojis = re.findall(r'<:(.+?):(\d+)>', emojis)
    emojis_to_upload = []

    status_message += [":white_circle:"] * (len(animated_emojis) + len(still_emojis))
    await msg.edit(content=''.join(status_message))

    for animated_emoji in animated_emojis:
        emojis_to_upload.append((animated_emoji[0], f"https://cdn.discordapp.com/emojis/{animated_emoji[1]}.gif"))
    for still_emoji in still_emojis:
        emojis_to_upload.append((still_emoji[0], f"https://cdn.discordapp.com/emojis/{still_emoji[1]}.png"))

    success = 0
    for i in range(len(emojis_to_upload)):
        await msg.edit(content=''.join(status_message))
        try:
            response = requests.get(emojis_to_upload[i][1])
        except Exception:
            traceback.print_exc()
            status_message[base_length + i] = "🔴"
            continue

        try:
            await ctx.guild.create_custom_emoji(name=emojis_to_upload[i][0], image=response.content)
            success += 1
            status_message[base_length + i] = "🟢"
        except Exception:
            traceback.print_exc()
            status_message[base_length + i] = "🔴"
            continue
    await msg.edit(content=''.join(status_message))

    await ctx.channel.send(f"{random.choice(['Et voilà!', 'Job done!', 'All done!'])} {success}/{len(emojis_to_upload)} emojis stolen. 💰")


client.run(os.getenv('KLEPTOJI_KEY'))