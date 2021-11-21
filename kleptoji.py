import dotenv
import discord
import os
from discord_slash import SlashCommand # Importing the newly installed library.
from discord_slash.utils.manage_commands import create_option
import re
import random
import requests

dotenv.load_dotenv()

client = discord.Client(intents=discord.Intents.none())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

@client.event
async def on_ready():
    print("Kleptoji is ready!")

#guild_ids = [894965656607391764]

@slash.slash(name="steal",
             description="Steal custom emojis from another server.",
             options=[
               create_option(
                 name="emojis",
                 description="The list of emojis to steal.",
                 option_type=3,
                 required=True
               )
             ])
async def _steal(ctx, emojis: str):
    status_message = list("Stealing emojis... 👤💰 ")
    base_length = len(status_message)
    msg = await ctx.send(''.join(status_message))
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
            status_message[base_length + i] = "🔴"
            continue

        try:
            await ctx.guild.create_custom_emoji(name=emojis_to_upload[i][0], image=response.content)
            success += 1
            status_message[base_length + i] = "🟢"
        except Exception:
            status_message[base_length + i] = "🔴"
            continue
    await msg.edit(content=''.join(status_message))

    await ctx.send(f"{random.choice(['Et voilà!', 'Job done!', 'All done!'])} {success}/{len(emojis_to_upload)} emojis stolen. 💰")


client.run(os.environ.get('KLEPTOJI_KEY'))