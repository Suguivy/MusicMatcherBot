# MusicMatcherBot

A music recommendation Discord bot for a uni project.

## Installation

First, clone the repository:

```
git clone https://github.com/Suguivy/MusicMatcherBot.git
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
pip3 install youtube-search-python discord.py python-dotenv youtube_dl
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
