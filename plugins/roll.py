import discord, json
from discord.ext import commands
from d20 import roll as diceroll

def recursive_object_builder(d):
    """Returns a dictionary as an object class.
    Parameters:
      d: dict - The dictionary whose keys and values will become an object.
    """
    if isinstance(d, list):
        d = [recursive_object_builder(x) for x in d]

    if not isinstance(d, dict):
        return d

    class Obj:
        pass

    obj = Obj()

    for o in d:
        obj.__dict__[o] = recursive_object_builder(d[o])

    return obj

class Rolling(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Rolling"

  @commands.command(
    name="roll",
    aliases=['dice', 'r'],
    brief="Rolls a dice using RPG format",
    description="Rolls a dice using the traditional RPG format. A guide can be found at https://en.wikipedia.org/wiki/Dice_notation",
    usage="<roll>"
    )
  async def _roll(self, ctx, roll=None):
    if roll == None:
      await ctx.send("You must provide a roll.")
      return
    rolls = diceroll(roll)
    rolls = str(rolls).replace('`', '')
    embed = discord.Embed(description=f"```{rolls}```", color=discord.Colour.dark_purple()).set_author(name=f"Roll Results - {ctx.message.author.display_name}")
    await ctx.reply(embed=embed)

  @commands.command(
    name="roll-initiative",
    aliases = ['ri'],
    brief="Rolls for initiative",
    description = "Rolls for initiative",
    usage=""
  )
  async def _rollinit(self, ctx):
      with open(f"{ctx.author.id}.json", 'r') as f:
        obj = recursive_object_builder(json.load(f))
        bonus = getattr(obj, "initiative")

        if bonus.startswith("0"):
          bonus = "+" + bonus

      roll = diceroll("1d20" + bonus)
      embed = discord.Embed(description=f"```{roll}```", color=discord.Colour.dark_purple()).set_author(name=f"Initiative Roll Results - {ctx.message.author.display_name}")
      await ctx.reply(embed=embed)
  
  @commands.command(
    name="roll-proficiency",
    aliases = ['rp', 'rollprof'],
    brief="Rolls a proficiency check",
    description = "Rolls a proficiency check based on a given proficiency.",
    usage="<proficiency>"
  )
  async def _rollprof(self, ctx, proficiency):
      with open(f"{ctx.author.id}.json", 'r') as f:
        obj = recursive_object_builder(json.load(f))
        bonus = getattr(getattr(obj, "proficiencies"), proficiency)

        if bonus.startswith("0"):
          bonus = "+" + bonus

      roll = diceroll("1d20" + bonus)
      embed = discord.Embed(description=f"```{roll}```", color=discord.Colour.dark_purple()).set_author(name=f"Proficiency Roll Results - {ctx.message.author.display_name}")
      await ctx.reply(embed=embed)
      
      
        

  @commands.command(
    name="stats",
    aliases=['stat', 'rs'],
    brief="Rolls basic stat rolls.",
    description="Rolls 6 4d6kh3 to fit traditional D&D 5e stat rolls.",
    usage=""
    )
  async def _stat(self, ctx,):
    embed = discord.Embed(description=f"```Stat Rolls```", color=discord.Colour.dark_purple()).set_author(name=f"Stat Roll Results - {ctx.message.author.display_name}")
    n = 6
    while n > 0:
      roll = diceroll('4d6kh3')
      rolls = str(roll).replace('`', '')
      embed.add_field(name=f"Stat - {roll.total}", value=f"{rolls}", inline=False)
      n = n-1
    await ctx.reply(embed=embed)

def setup(bot):
  bot.add_cog(Rolling(bot))