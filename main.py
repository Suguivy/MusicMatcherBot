from youtubesearchpython.__future__ import VideosSearch
from discord.ext import commands, tasks
from dotenv import load_dotenv
import discord
import os
import youtube_dl
import asyncio
import MusicRecommender as mr

"""
Most of the code comes from https://python.land/build-discord-bot-in-python-that-plays-music
"""

from YTDLSource import YTDLSource

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

queue = []

recommender = mr.MusicRecommender()
recommender.load_all_from_csv('recommender_data/spotify_songs.csv', 'recommender_data/dataset', 'recommender_data/matrix.npy')

def readable_queue():
    if len(queue) == 0:
        return "The queue is empty."
    else:
        return '\n'.join([f'{i} - _{v["title"]}_' for i, v in enumerate(queue)])

def id_to_url(id):
    return f"https://youtube.com/watch?v={id}"

async def id_to_video(id):
    result = await VideosSearch(video_title, limit = number_of_results).next()
    return result['result'][0]

async def search_by_title(title, num_of_results=1):
    result = await VideosSearch(title, limit = num_of_results).next()
    return result['result'][0]
async def play(ctx):
    pass

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='showqueue', aliases=['q'])
async def _showqueue(ctx):
    await ctx.send(readable_queue())

@bot.command(name='create', aliases=['c'])
async def _create(ctx, title, count=1):
    similar = recommender.similar_by_exact_title(title, count)
    similar_search_titles = [f'{song_title} {song_artist}' for song_title, song_artist in similar]
    results = [await search_by_title(title) for title in similar_search_titles]
    for video in results:
        queue.append(video)

@bot.command(name='play', aliases=['p'])
async def _play(ctx):
    while len(queue) > 0:
        server = ctx.message.guild
        voice_channel = server.voice_client
        if not (voice_channel and voice_channel.is_connected()):
            await ctx.send('I\'m not connected to a voice channel, but I will connect to your current voice channel.')
            await join(ctx)
            server = ctx.message.guild
            voice_channel = server.voice_client
        video = queue.pop(0)
        async with ctx.typing():
            filename = await YTDLSource.from_url(id_to_url(video['id']), loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=filename))
        await ctx.send(f'**Playing:** {video["title"]}')
        while voice_channel.is_playing():
            await asyncio.sleep(.1)
    await ctx.send("The queue is empty.")

@bot.group(name='join', aliases=['j'])
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
        await channel.connect()

@bot.command(name='leave', alisases=['l'])
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='pause', aliases=['pp'])
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

@bot.command(name='resume', aliases=['r'], help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("I wasn't playing anything before this. Use `!play` or `!p`")

@bot.command(name='stop', aliases=['s'])
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

if __name__ == "__main__" :
    bot.run(TOKEN)
