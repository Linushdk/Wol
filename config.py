import discord
import os
import pymongo
from dotenv import load_dotenv

### FARBEN ###
TRANPARENT = discord.Color.from_rgb(47, 49, 54)
KEKS_ORANGE = 0xffa500
RED = 0xff0000
GREEN = 0x00ff00


### DATABASE ###
load_dotenv()
MONGO_CLIENT = pymongo.MongoClient(os.getenv('MONGO_URITESTWOLKENLOS'))

DB = MONGO_CLIENT.wolkenlos