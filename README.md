# assistant4discord

<p>
<a href=https://www.python.org/downloads/release/python-370/><img alt=Python 3.7 src=https://img.shields.io/badge/python-3.7-blue.svg></a>
<a href="https://github.com/Rapptz/discord.py/"><img alt="discord.py" src="https://img.shields.io/badge/discord-py-blue.svg"></a>
<a href="https://github.com/mongodb/motor"><img alt="mongodb motor" src="https://img.shields.io/badge/mongodb-motor-green.svg"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Contents
- [Overview](#overview)
- [Features](#features)
- [Default commands](#default-commands)
    - [bot info and help](#info-and-help)
    - [set reminders](#reminders)
    - [set timers](#timers)
    - [check for changes in a website](#website-comparrsion)
    - [take notes](#notes)
    - [text to latex](#latex)
    - [set mods](#mods)
    - [vector model](#vector-model)
- [Setup](#setup)
    - [local](#local)
    - [cloud](#cloud)
- [Making custom commands](#making-custom-commands)

## Overview
Assistant4discord (a4d for short) was originally intended to be a reminder bot but the project gradually 
evolved to be a framework for writing persistent time dependent bot commands. It's a self hosted bot meant for smaller servers or individual use. 
A4d uses MongoDB (NoSQL database) as data storage which allows the bot to retain data on shutdown or on server restart. 
Additionally it offers input to command matching using 
[word embeddings](https://medium.com/explore-artificial-intelligence/word2vec-a-baby-step-in-deep-learning-but-a-giant-leap-towards-natural-language-processing-40fe4e8602ba).


## Features
- using discord.py rewrite
- object orientated framework for writting commands easily
- persistent storage with MongoDB
- simple text user interface for discord
- bot response can be sent to same channel or to user directly
- mod support for commands
- runs on [Heroku](https://www.heroku.com) with [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- fully asynchronous using [aiohttp](https://aiohttp.readthedocs.io/en/stable/), 
                           [Motor](https://github.com/mongodb/motor) and 
                           [Python 3.7 asyncio](https://docs.python.org/3/library/asyncio.html)
- uses natural language processing for user input recognition 
([word2vec](https://radimrehurek.com/gensim/models/word2vec.html) or 
[term frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf))

## Default commands

### Info and help
Display basic bot information.
_Example_:
```
command: @assistant info
output:  name: @assistant
         owner: Thund3rz#5416
         description: 
         public bot: True
         github: https://github.com/NightThunder/assistant4discord
         -------------------------------
         type help for commands info

command: @assistant help
output:  My commands: NoteIt, NotesTxt, RemoveNote, ShowNotes, ShowMods, RemoveTimer, ShowTimers, TimeIt, TextToLatex,
         Ping, MostSimilarWords, Word2WordSim, WordNum, RemoveWebsite, ShowWebsites, WebsiteComparison, AppInfo, 
         RemindMe, RemoveReminder, ShowReminders, Help 
         Type help <command> for more info!
```

### Reminders
Set reminder for yourself, received by dm if command on server (default option). Format for dates and time of day:
**on** day/month/year **at** hour/minute/second. Format for just time: hour/minute/second. Also
accepts names of days, tomorrow and day(s). Use with keyword **every** to repeat reminder. 
See docs in a4d/nlp_tasks/find_times.py for more info and examples.  
_Example:_ 
```
input:   remember this
command: @assistant reminder tomorrow at 12
output:  reminder: remember this
         set for: 28.09.2019 @ 12:00:00

input:   remind me
command: @assistant reminder 30 min
ouput:   reminder: remind me
         set for: 27.09.2019 @ 12:29:12

command: @assistant show reminders
output:  0 - reminder: remember this
         set for: 28.09.2019 @ 12:00:00
         -----------------------------------
         1 - reminder: remind me
         set for: 27.09.2019 @ 12:29:12

command: @assistant remove reminder 1
output:  Removed items with index 1

command: @assistant show reminders:
ouput:   0 - reminder: remember this
         set for: 28.09.2019 @ 12:00:00
         
input:   remind me this every day
command: @assistant reminder every day at 8:15
output:  reminder: remind me this every day
         set every 1 day
         next reminder on 28.09.2019 @ 08:15:00
```

### Timers
Time any command that doesn't initially use time and doesn't require any input.  
_Example:_
```
command: ping
output: 126 ms

command: @assistant time ping every 10 sec
output:  command: Ping
         set every 10 sec
         next run on 27.09.2019 @ 22:08:50

output:  119 ms
output:  151 ms

command: @assistant show timers
output:  0 - command: Ping
         set every 10 sec
         next run on 27.09.2019 @ 22:09:10
```

### Website comparrsion
Compares website text and detects changes using python's difflib. Intended for simple websites
(like those 90s style websites that college professors have).  
_Example:_
```
input:   https://www.reddit.com/r/Python/new/.json?limit=1
command: @assistant check every 120 sec
output:  0 - https://www.reddit.com/r/Python/new/.json?limit=1
         check set every 2 min
         next check on 28.09.2019 @ 18:10:35

(after 120 sec)
output:  https://www.reddit.com/r/Python/new/.json?limit=1
         - "subreddit_subscribers": 426463, "created_utc": 1569686430.0,
         ?                               ^
         + "subreddit_subscribers": 426462, "created_utc": 1569686430.0,
         ?                               ^

(after another 120 sec)
output: Websites ['https://www.reddit.com/r/Python/new/.json?limit=1'] checked, no difference found.
```
Note that this is just an example and that checking Reddit shouldn't be done like this.

### Notes
Make a note out of a message. Same as reminder but without time.  
_Example:_
```
input:   this is a note
command: @assistant note
output:  noted on 28.09.2019 @ 18:46:20
         this a note

command: @assistant notes to text
output:  <all your notes in a .txt file>
```

### Latex
Returns rendered latex image. Using https://www.codecogs.com/latex/eqneditor.php .  
_Example:_
```
command: @assistant latex <latex notation>
output:  <rendered latex in .png>
```
[Example output](https://i.imgur.com/fuOaKKE.png)  
[Produced png](https://cdn.discordapp.com/attachments/599894710546595840/622461665111441428/latex_img.png)

### Mods
Make user a mod. Commands can be set so only mod or owner can use them.  
_Example:_
```
input:   assistant#4819
command: @assistant mod
output:  bot mod: assistant#4819

command: @assistant show mods
output:  0 - bot mod: Thund3rz#5416
         -----------------------------
         1 - bot mod: assistant#4819
```
By default there are no mod commands only add mod and remove mod are owner only.

### Vector model
Display information about vector model. Works with w2v only. Uses Gensim library.  
_Example:_
```
command: similarity python, discord
output:  0.280426

command: most similar discord
output:  whatsapp: 0.71 irc: 0.71 teamspeak: 0.67 skype: 0.66 ...
```
Small word2vec model made with Reddit can be found [here](https://github.com/NightThunder/RAT/releases). 

## Setup

### Local

1. have python3 working
2. download assistant4discord zip and extract it to a folder
3. make python [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
(recommended) and pip install everything in requirements.txt (pip3 install -r requirements.txt)
4. get your discord bot token from [here](https://discordapp.com/developers/applications/)
5. install MongoDB, see [documentation](https://docs.mongodb.com/manual/administration/install-community/)

   if on Ubuntu and the documentation way doesn't work you can try:  
   `sudo apt-get update`  
   `sudo apt-get install mongodb`  
   `sudo service mongodb status`  
   `sudo service mongodb start`  
   `sudo service mongodb stop`  

6. configure environment variables in run_assistant.py

    - set MONGODB_TOKEN = "mongodb://localhost:27017/"
    - set DISCORD_TOKEN = <your discord token from step 3>
    
    Note: if you intend to share your code it is good practice to configure environment variables
    in your IDE. If you use PyCharm go to Run->Edit Configurations->Chose assistant.py->click Environment variables on 
    right hand side->set all your tokens->apply and close

7. chose method

    - tf, doesn't require any further setup
    - w2v, you can download my model from [here](https://github.com/NightThunder/RAT/releases) and
      extract it to a4d/data/models

8. run run_assistant.py, invite your bot to a server and that's it!
    
video tutorial for steps 1, 4 and 8: [How to Create a Discord Bot With Python](https://youtu.be/xdg39s4HSJQ)

### Cloud (recommended)

1. download assistant4discord zip and extract it to a folder
2. get your discord bot token from [here](https://discordapp.com/developers/applications/)
3. setup [MongoDB atlas](https://www.mongodb.com/cloud/atlas) 

    - make an account and setup your cluster, [tutorial](https://youtu.be/_d8CBOtadRA)

## Making custom commands
