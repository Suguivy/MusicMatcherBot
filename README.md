# MusicMatcherBot

A music recommendation Discord bot for a uni project.

## Installation

First, clone the repository:

```
git clone https://github.com/Suguivy/MusicMatcherBot.git
cd MusicMatcherBot
```

Then create a virtual enviroment. This is very useful for the next step to install all the required packages locally.

```
python3 -m venv mmbot-venv
source mmbot-venv/bin/activate
```

Make sure you have your `pip3` updated:

```
pip3 install --upgrade pip
```

Now install all the required `pip3` packages:

```
pip3 install youtube-search-python discord.py python-dotenv youtube_dl pandas scikit-learn pynacl
```

Download the dataset the bot uses:
```
mkdir recommender_data
curl https://gitlab.com/bollafa/data-music/-/raw/main/tcc_ceds_music.csv -o recommender_data/tcc_ceds_music.csv
```

Create a new file called `.env` and put the following text in it, replacing `<your discord bot token>` with your Discord bot token:

```
DISCORD_TOKEN=<your discord bot token>
```

Finally, run the bot:

```
python main.py
```

## Usage

The bot has a queue of songs. You must first to add songs to the queue before playing them.

The bot is controlled by commands. These commands are:
- `!join`, `!j`: tells the bot to join the audio channel.
- `!leave`, `!l`: tells the bot to leave the audio channel.
- `!create <title> [<count>=5]`, `!c`: searches and adds to the queue the specified song and some recommendations based on the given `<title>`. It will add as many songs as the `<count>` value (5 if ommited).
- `!showqueue`, `!q`: shows the current queue.
- `!play`, `!p`: plays in order the songs of the queue, removing it from the queue.
- `!pause`, `!pp`: if a song is playing, it pauses the reproduction.
- `!resume`, `!r`: if a song is paused, it resumes the reproduction.
- `!next`, `!n`: if a song is playing, it stops it and plays the next song.
- `!stop`, `!s`: it stops the reproduction of all songs in the queue.

## Usage example

Make sure your bot is in your Discord server. Join an audio channel and type `!j` to make the bot join the channel too.

Next, tell the bot to add to the playing queue some songs based on a song you want. For example, if you want similar songs to the song "I Believe" by Frankie Laine, type `!c "i believe"`. You need to write the exact title of the song as it is as its name in the dataset.

The bot will add the corresponding songs on the queue. Each songs is based on the first video of a YT search, searching by the title and the author. You can tell the bot to show the queue with `!q` (if the bot added songs to the queue recently, you may need to wait some seconds to see the actual queue).

To start playing the songs type `!p`. You can control the reproduction with `!pp` (pause), `!r` (resume), `!n` (next song) or `!s` (stop).
