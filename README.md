# Mafia Bot

Mafia bot for the Starmen.net community.

## Dependencies
* [Python 3.9.4](https://www.python.org/) and up
* Bash or other Unix-like shell (see [cmder](https://cmder.net/) for Windows)

## Setup

### 1. Grab your Discord ID

Activate `Developer Mode` in Discord. This setting can be found from the `Advanced` tab inside of `User settings`. Once activated, right-click your name inside of a chat and select `Copy ID`. Keep this for later.

### 2. Create a Bot.

Use the [developers](https://discord.com/developers/applications) portal to create an Application. You may then select the `Bot` tab and create a Bot.

### 3. Generate an Authentication token

Inside of the `Bot` tab, generate a token. Please understand that this token should be a closely guarded secret. In this context equivalent to holding a password. Do not share this token with anyone you do not wish to have access to the bot, and be careful not accidentally package it with any other projects.

### Setup the local environment

From terminal run

> bash setup.sh

When the setup is finished, navigate into the `conf` folder and edit the `bot_config.json` file to include tha authentication token for your Discord bot and your Discord ID.


## Usage Guide

This package needs two processes: one is the Discord client (your bot) and the other is a game server. It is preferable to run each inside separate terminals or screens where possible. In one terminal run

> bash run_server.sh

and in another

> bash run_client.sh

The processes communicate with each other over local websocket connections, although it is possible to configure the bot to communicate over a network. A more thorough guide is forthcoming.


## Misc.

KingSpore is mafia