# Starship_Crafting.py
import discord
from discord.ext import commands

from .Starship_Classes import STARSHIP_CLASSES

class Starship_Crafting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



async def setup(bot: commands.Bot):
    await bot.add_cog(Starship_Crafting(bot))