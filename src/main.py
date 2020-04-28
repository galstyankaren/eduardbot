import random
import re

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

PROJECT_FOLDER = os.getcwd()

load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))

TOKEN = os.getenv("TOKEN")

SRC_PATH = "./res/"

CHANNEL_LIST = ['Лужа', 'ТВ Х*Й', 'Х*Й ТВ', 'ТВ Б**ДЬ',
                'ЦКТЗ ТВ', 'Russia Yesterday', 'НТВ Минус', 'Золотой дождь']

FLAC_REGEX = r".\s+([^()]+)\.flac$"

ffmpeg_options = {
    'options': '-vn'
}


class Eduard(commands.Cog):
    song_list = []

    def __init__(self, bot):
        self.bot = bot
        self.song_list = os.listdir(SRC_PATH)

    @commands.command()
    async def sing(self, ctx):

        count = len(self.song_list)

        if count == 0:
            # Reset the song list
            self.song_list = os.listdir(SRC_PATH)

        choice_index = random.choice(range(count))
        choice = self.song_list[choice_index]

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{SRC_PATH}{choice}"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        random_channel = random.choice(CHANNEL_LIST)
        # Filter out the name of the song from the flac files
        song_name = re.findall(FLAC_REGEX, choice, re.MULTILINE)

        # Remove the song from the list, so it's not gonna repeat again (unless the playlist is exhausted)
        del self.song_list[choice_index]

        await bot.change_presence(activity=discord.Game(name=song_name[0]))
        await ctx.send(f"<<{song_name[0]}>> на телеканале {random_channel}")

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

    @sing.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


bot = commands.Bot(command_prefix=commands.when_mentioned_or("eduard."),
                   description='Discord bot that plays random Эдуард Суровый songs.')


@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')


# @bot.listen()
# async def on_message(message):
#     if message.author.id == bot.user.id:
#         return
#     if 'Эдуард' in message.content:
#         random_command = bot.get_command("sing")
#         await message.channel.invoke(random_command)


bot.add_cog(Eduard(bot))
bot.run(TOKEN)
