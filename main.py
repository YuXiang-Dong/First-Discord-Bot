import random
import json
from discord.ext import commands, tasks
from itertools  import cycle
import requests
import os
import discord


description = ''' Help command Discription '''
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=".",                   description=description,intents=intents)  # discord bot initialization

def get_prefix(client, message):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)
  return prefixes[str(message.guild.id)]



@bot.event
async def on_guild_join(guild):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  prefixes[str(guild.id)] - '.'

  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
  with open('prefixes.json','r') as f:
    prefixes = json.load(f)

  prefixes.pop[str(guild.id)]

  with open('prefixes.json','w') as f:
    json.dump(prefixes, f, indent=4)

status = cycle(["Uno", "TLOU 2", "Shark Doooo"])


@bot.event
async def on_ready():
  change_status.start()
  await bot.change_presence(status = discord.Status.idle)
  print("Bot is ready")
  
@tasks.loop(seconds = 10)
async def change_status():
  await bot.change_presence(activity = discord.Game(next(status)))

@bot.event
async def on_member_join(member):
  print(f"{member} has joined the server.")

@bot.event 
async def on_member_remove(member):
  print(f"{member} has left the server.")

@bot.command()
async def smash(ctx):
  await ctx.send(f"You are my senpai and I will serve you UwU! I will be at your home in {round(bot.latency*1000)} milliseconds")

@bot.command(aliases = ["senpai","test"])
async def Senpai(ctx, *, question):
  responses = ["It is certain.",
  "It is decidedly so.",
  "Without a doubt.",
  "Yes - definitely.",
  "You may rely on it.",
  "As I see it, yes.",
  "Most likely.",
  "Outlook good.",
  "Yes.",
  "Signs point to yes.",
  "Reply hazy, try again.",
  "Ask again later.",
  "Better not tell you now.",
  "Cannot predict now.",
  "Concentrate and ask again.",
  "Don't count on it.",
  "My reply is no.",
  "My sources say no.",
  "Outlook not so good.",
  "Very doubtful."]

  await ctx.send(f"Answer= {random.choice(responses)}")

@bot.command()  
async def kick(ctx, member:discord.Member, *, reason = None):
  await member.kick(reason = reason)

@bot.command()
async def ban(ctx, member:discord.Member, *, reason = None):
  await member.ban(reason = reason)
  await ctx.send(f"Banned {member.mention}")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Invaild command.")

def is_me(m):
    return m.author == bot.user
  
@bot.command()
@commands.check(is_me)
async def example(ctx):
  await ctx.send(f"Hi I'm {ctx.author}")

@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
  await ctx.channel.purge(limit=amount+1)

@clear.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please specify the amount of messages you want to delete.")

@bot.command()
async def unban(ctx, *, member):
  banned_user = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")

  for banned_entry in banned_user:
    user = banned_entry.user
    if(user.name, user.member_discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"Unbanned {user.mention}. Welcome back")
      return
      
#check token
bot.run('SECRET') 
