import os
import discord

from core import Hala

bot = Hala(
  case_insensitive=True,
  strip_after_whitespace=True,
  description="A discord D&D bot.",
  intents=discord.Intents.all(),
  help_command=None
)

extensions = [
  'plugins.help',
  'plugins.misc',
  'plugins.roll',
  'plugins.characters'
]

@bot.event
async def on_ready():
  print("bot is online")

if __name__ == '__main__':
  for cog in extensions:
    bot.load_extension(cog)

bot.run(os.getenv("TOKEN"))