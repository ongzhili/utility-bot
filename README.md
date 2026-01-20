# task-manager-bot

## About

Just a simple discord bot project to replicate functions that we want (from other bots), as well as some new ideas, and compiling it into a single bot.

## Installation

This bot uses the discord.py library, and ossapi (wrapper for osu!API)

To install dependencies:
```
pip install discord
pip install ossapi
pip install firebase_admin
```

## Running:

Requires:

`token.txt` with your bot's token

`python main.py`

## PLANNED FEATURES (Feel free to add)

### TODO feat/split-money
- [ ] Implement input system for money to local vars
- [ ] Implement max-flow algorithm
- [ ] Functioning money-transfer logic
- [ ] Migrate local vars to database

### Main functions
- [x] CRUD for tasks
- [x] Send a reminder during set time
- [x] Tools - coinflip, roll dice (XdY, X<=10, Y=4,6,8,10,12,20)
- [ ] Backend db
- [ ] Splitwise-like functionality

### Far goals
- [ ] play with osu api (i need to check this apparently there is a rate limit)
- [ ] CTF api
- [ ] linkedin/job api maybe?
- [ ] news api (game news, tech news etc.)