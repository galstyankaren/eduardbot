import random
import re
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

PROJECT_FOLDER = os.getcwd()

load_dotenv(os.path.join(PROJECT_FOLDER, '.env'))
ffmpeg_options = {
    'options': '-vn'
}

TOKEN = os.getenv("TOKEN")
SRC_PATH = "./res/"
SONG_LIST = os.listdir(SRC_PATH)

CHANNEL_LIST = ['Лужа', 'ТВ Х*Й', 'Х*Й ТВ', 'ТВ Б**ДЬ',
                'ЦКТЗ ТВ', 'Russia Yesterday', 'НТВ Минус', 'Золотой дождь']
FLAC_REGEX = r".\s+([^()]+)\.flac$"



class Eduard(commands.Cog):

    queue = []

    def __init__(self, bot):
        global SONG_LIST
        self.bot = bot
        self.queue = [i for i in SONG_LIST]

    async def play_local(self,ctx,choice):
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(f"{SRC_PATH}{choice}"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        random_channel = random.choice(CHANNEL_LIST)
        # Filter out the name of the song from the flac files
        song_name = re.findall(FLAC_REGEX, choice, re.MULTILINE)
        await bot.change_presence(activity=discord.Game(name=song_name[0]))
        await ctx.send(f"<<{song_name[0]}>> на телеканале {random_channel}")

    @commands.command()
    async def play(self, ctx,*, query=None):
        global SONG_LIST
        count = len(self.queue)
        if count == 0:
            # Reset the song list
            self.queue = [i for i in SONG_LIST]
        try:
            choice_index = int(query) if query else random.choice(range(count))
            choice = SONG_LIST[choice_index] if query else self.queue[choice_index]
        except ValueError:
            print('Choice is not a number')

        await self.play_local(ctx,choice)

        # Remove the song from the list, so it's not gonna repeat again (unless the playlist is exhausted)
        del self.queue[choice_index]


    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()


    @commands.command()
    async def list(self, ctx):
        global SONG_LIST
        temp_list = [(i,song) for i,song in enumerate(SONG_LIST)]
        await ctx.channel.send(f"{temp_list}")


    @play.before_invoke
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
#         play_command = bot.get_command("playy")
#         await message.channel.invoke(play_command)


bot.add_cog(Eduard(bot))
bot.run(TOKEN)
