# MusicMatcherBot

A music recommendation Discord bot for a uni project.

## Installation

First, clone the repository:

```
$ git clone https://github.com/Suguivy/MusicMatcherBot.git
```

Then create a virtual enviroment. This is very useful for the next step to install all the required packages locally.

```
$ python3 -m venv mmbot-venv
$ source mmbot-venv/bin/activate
```

Make sure you have your `pip3` updated:

```
$ pip3 install --upgrade pip
```

Now install all the required `pip3` packages:

```
$ pip3 install youtube-search-python discord.py python-dotenv youtube_dl
```

Create a new file called `.env` and put the following text in it, replacing `<your discord bot token> with your Discord bot token:

```
DISCORD_TOKEN=<your discord bot token>
```

Finally, run the bot:

```
$ python main.py
```