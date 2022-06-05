import discord
from discord.ext import commands
import json

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

class Character(commands.Cog):
  def __init__(self, bot):
    self.bot=bot
    self.name="Character"
  
  @commands.command(
    name="upload",
    brief="Upload json character.",
    description="Upload a character made in JSON at https://hala-1.marleyakins.repl.co/",
    usage="<json>"
  )
  async def _upload(self, ctx, *, json):
    with open(f"{ctx.author.id}.json", 'w') as f:
      f.write(json)

    await ctx.reply("Character uploaded.")

  @commands.command(
    name="get",
    brief="Get character info.",
    description="Gets information on a character from json.",
    usage="<attribute> <member: discord.Member>"
  )
  async def _get(self, ctx, attribute, member: discord.Member = None):
    if member == None:
      member = ctx.author
    
    try:
      with open(f"{member.id}.json", 'r') as f:
        obj = recursive_object_builder(json.load(f))
        if "." in attribute:
          attr = attribute.split(".")
          x = obj
          for item in attr:
            x = getattr(x, item)

          return await ctx.reply(x)

        await ctx.reply(getattr(obj, attribute) if str(getattr(obj, attribute)) != "" else "None.")
            
        
    except FileNotFoundError:
      await ctx.reply("Member does not have character uploaded")

    except AttributeError:
      await ctx.reply("That is not a valid attribute")

  @commands.command(
    name="equipment",
    brief="Add or remove equipment.",
    description = "Add or remove equipment.",
    usage = "<add or remove> <item>"
  )
  async def _equipment(self, ctx, choice, *, item):
    try:
      with open(f"{ctx.author.id}.json", 'r') as f:
        obj = recursive_object_builder(json.load(f))
        equipment = getattr(getattr(obj, "inventory"), "equipment")

        array = equipment.split(", ")
        eqt = []
        index = 0

        for ite in array:
          eqt.append(ite.upper())
          if ite.upper() == item.upper():
            if index == len(array)-1:
              continue
            else:
              item = item + ", "

          index += 1

        if choice.lower() == "remove":
          if item.upper() not in eqt:
            return await ctx.reply("You do not have this item.")

          else:
            eqt.remove(item.upper())

          new = ""
          for ite in eqt:
            new += ite.lower().capitalize() + ", "
          with open(f"{ctx.author.id}.json", 'r+') as f:
            do = json.load(f)
            do['inventory']['equipment'] = new
          with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

          await ctx.reply("Item removed from inventory.")

        if choice.lower() == "add":
          equipment += ", " + item
          with open(f"{ctx.author.id}.json", 'r+') as f:
              do = json.load(f)
              do['inventory']['equipment'] = equipment
          with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

          await ctx.reply("Item added to inventory.")
 
    except FileNotFoundError:
      await ctx.reply("Member does not have character uploaded") 

  @commands.command(
    name="gold",
    brief="Add or remove gold",
    description="Add or remove gold from your character.",
    usage = "<add or remove> <amonunt>"
  )
  async def _gold(self, ctx, choice, amount: int):
    if choice.lower() == "add":
      with open(f"{ctx.author.id}.json", 'r+') as f:
              do = json.load(f)
              do['inventory']['gold'] = str(int(do['inventory']['gold']) + amount)
      with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

      await ctx.reply("Gold added.")

    if choice.lower == "remove":
      with open(f"{ctx.author.id}.json", 'r+') as f:
              do = json.load(f)
              do['inventory']['gold'] = str(int(do['inventory']['gold']) - amount)
      with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

      await ctx.reply("Gold removed.")

  @commands.command(
    name="exp",
    brief="Add or remove exp",
    description="Add or remove exp from your character.",
    usage = "<add or remove> <amonunt>"
  )
  async def _exp(self, ctx, choice, amount: int):
    if choice.lower() == "add":
      with open(f"{ctx.author.id}.json", 'r+') as f:
              do = json.load(f)
              do['experience'] = str(int(do['experience']) + amount)
      with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

      await ctx.reply("Experience added.")

    if choice.lower == "remove":
      with open(f"{ctx.author.id}.json", 'r+') as f:
              do = json.load(f)
              do['experience'] = str(int(do['experience']) - amount)
      with open(f"{ctx.author.id}.json", "wt") as fp:
            json.dump(do, fp)

      await ctx.reply("Experience removed.")

def setup(bot):
  bot.add_cog(Character(bot))