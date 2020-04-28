# EduardBot
Discord bot that plays random Эдуард Суровый songs. 
The only thing that can make your jokes sound decent in comparison.

# Usage

Connect to a voice channel.Write the command bellow to play a random song
```eduard.sing```
To stop the bot
```eduard.stop```

# Installation 

## Add to channel

TODO: Add the discord bot link

## Prerequisites
To host the bot locally , you will need:
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/#install-pipenv-today): 2018.11.26 >
* Python 3.6 
* [discord.py](https://discordpy.readthedocs.io/en/latest/intro.html#prerequisites)
* A Discord developer account / bot application for the TOKEN
* Download the songs from [this](https://t.me/eduqard_surovy) telegram channel and put them into the res directory 
## Installing

1. Clone the repository 
```git clone https://github.com/galstyankaren/eduardbot.git```
2. Init pipenv from inside the project
```cd eduardbot && pipenv shell```
3. Create a .env file in the project root and add your Discord bot token
```TOKEN=<YOUR_DISCORD_TOKEN>```
4. Thats it! Now run the bot script 
```cd src && python main.py```

# TODO list

* Add an option to play X ammount of random songs
* Add a command to play Eduards intro riff
* Spaghetti cleanup 
* Dockerize the bot

