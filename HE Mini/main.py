import os
import json
import random
import time
import asyncio
from datetime import datetime, timezone
from collections import Counter
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def setup_hook():
	for filename in ["Starship_Classes", "Asteroids", "Starship_Fleets", "Visual_Interface"]:
		await bot.load_extension(f"Gameplay.{filename}")

@bot.group(name='group_name', invoke_without_command=True)
async def group_name(ctx):
	"""Command group template."""
	if ctx.invoked_subcommand is None:
		message = await ctx.send('Please specify a subcommand.')

@group_name.command(name='command_name')
async def command_name(ctx):
	"""Command template."""
	message = await ctx.send('Command executed.')
	await message.delete(delay=20)

@bot.command(name="Register_UI")
async def UI(ctx):
	"""Create the category used to hold player instance channels."""
	category_name = 'Instances'
	category = discord.utils.get(ctx.guild.categories, name=category_name)

	if category is None:
		category = await ctx.guild.create_category(category_name)
		message = await ctx.send(f'Created the **{category.name}** category.')
		await message.delete(delay=20)
	else:
		message = await ctx.send(f'The **{category.name}** category already exists.')
		await message.delete(delay=20)

    

@bot.group(name='Instance', invoke_without_command=True)
async def instance(ctx):
	"""Instance Grouping: This Command group is used to manage player instances and Server Load"""
	if ctx.invoked_subcommand is None:
		await ctx.send(
			'Create\n'
			'Delete\n'
			'Load\n'
			'Save'
		)

@instance.command(name='create')
async def create_instance(ctx):
	"""Create a new player instance."""
	message = await ctx.send('Creating instance...')
	await message.delete(delay=20)

	USER_ID = str(ctx.author.id)
	channel_name = f"instance-{USER_ID}"
	channel = discord.utils.get(ctx.guild.channels, name=channel_name)

	if channel is None:
		channel = await ctx.guild.create_text_channel(
			channel_name,
			category=discord.utils.get(ctx.guild.categories, name='Instances')
		)
		await channel.set_permissions(ctx.guild.default_role, read_messages=False)
	else:
		message = await ctx.send(f'Instance channel **{channel_name}** already exists.')
		await message.delete(delay=20)

	# Administrators retain access, while the author is granted access to the channel.
	await channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

@instance.command(name='delete')
async def delete_instance(ctx):
    """Delete an existing player instance."""
    message = await ctx.send('Deleting instance...')
    await message.delete(delay=20)

    USER_ID = str(ctx.author.id)
    channel_name = f"instance-{USER_ID}"
    channel = discord.utils.get(ctx.guild.channels, name=channel_name)

    if channel is not None:
        await channel.delete(delay=20)
    else:
        message = await ctx.send(f'Instance channel **{channel_name}** does not exist.')
        await message.delete(delay=20)

class SaveData:
	def __init__(self, filename, changes_filename="User_Changes.json"):
		self.filename = filename
		self.changes_filename = changes_filename
		try:
			with open(filename, "r", encoding="utf-8") as file:
				self.data = json.load(file)
		except (FileNotFoundError, json.JSONDecodeError):
			self.data = {}

		try:
			with open(changes_filename, "r", encoding="utf-8") as file:
				self.changes = json.load(file)
		except (FileNotFoundError, json.JSONDecodeError):
			self.changes = []

	def get_user(self, user_id):
		"""Return one user's saved data, creating defaults if needed."""
		user_id = str(user_id)
		user = self.data.setdefault(
			user_id,
			{"balance": 4000, "access_codes": []},
		)
		user.setdefault("balance", 4000)
		user.setdefault("access_codes", [])
		return user

	def set_balance(self, user_id, balance):
		user_id = str(user_id)
		user = self.get_user(user_id)
		old_balance = user["balance"]
		if old_balance == balance:
			return

		user["balance"] = balance
		self.log_change(user_id, "balance", old_balance, balance)
		self.save()

	def add_access_code(self, user_id, access_code):
		user_id = str(user_id)
		user = self.get_user(user_id)
		if access_code in user["access_codes"]:
			return

		old_codes = user["access_codes"].copy()
		user["access_codes"].append(access_code)
		self.log_change(
			user_id,
			"access_codes",
			old_codes,
			user["access_codes"].copy(),
		)
		self.save()

	def log_change(self, user_id, field, old_value, new_value):
		"""Record one change in the separate audit file."""
		self.changes.append(
			{
				"timestamp": datetime.now(timezone.utc).isoformat(),
				"user_id": str(user_id),
				"field": field,
				"old_value": old_value,
				"new_value": new_value,
			}
		)
		with open(self.changes_filename, "w", encoding="utf-8") as file:
			json.dump(self.changes, file, indent=4)

	def save(self):
		with open(self.filename, "w", encoding="utf-8") as file:
			json.dump(self.data, file, indent=4)

user_data = SaveData("User_Data.json", "User_Changes.json")

@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.id}')

@bot.event
async def on_disconnect():
	print(f'Logged out as {bot.user.id}')
	send_category = discord.utils.get(bot.guilds[0].categories, name='Instances')
	if send_category:
		message = await send_category.send(f'Instance Stopped')
		await message.delete(delay=20)
	else:
		print('No "Instances" category found.')

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await bot.close()  # Closes the bot connection cleanly
        

bot.run('')