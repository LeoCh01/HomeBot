import asyncio
import os
import discord
import datetime
from discord.ext import commands
from replit import db

BCOL = 0xFF73EF


def guild_owner_only():

  async def predicate(ctx):
    if ctx.author == ctx.guild.owner:
      return True
    await ctx.send('only owners can use this command')
    return False

  return commands.check(predicate)


def run_bot():
  client = commands.Bot(command_prefix='?',
                        intents=discord.Intents.all(),
                        help_command=None)

  @client.event
  async def on_ready():
    print("Bot online...")

  @client.event
  async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send('Invalid Command')

  @client.command()
  async def ping(ctx):
    """
    Latency
    """
    await ctx.send(f'{round(client.latency * 1000)}ms')

  @client.command(aliases=['rm'])
  @guild_owner_only()
  async def remove(ctx, amount=2):
    """
    Remove messages
    """
    await ctx.channel.purge(limit=amount)

  @client.command(aliases=['t'])
  async def timer(ctx, num=10):
    """
    Countdown
    """
    num_real = int(num)
    num_conv = datetime.timedelta(seconds=num_real)
    msg = await ctx.send(
      embed=discord.Embed(title=f'Timer: {num_conv}', color=BCOL))

    while num_real > 0:
      await asyncio.sleep(1)
      num_real -= 1
      num_conv = datetime.timedelta(seconds=num_real)
      await msg.edit(
        embed=discord.Embed(title=f'Timer: {num_conv}', color=BCOL))

    timerVar = discord.Embed(title='Time\'s up!', color=BCOL)
    await msg.edit(embed=timerVar)
    await ctx.send(f'<@{ctx.message.author.id}> Time\'s up!')

  # run
  client.run(os.environ['TOKEN'])
