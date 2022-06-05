import discord
from discord.ext import commands

from replit import db

def get_prefix(bot, message):
    if str(message.guild.id) in db:
      prefix = db[str(message.guild.id)]
    else:
      prefix = '?'
    return prefix
  
class Hala(commands.Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args,
                     command_prefix = get_prefix,
                     **kwargs)