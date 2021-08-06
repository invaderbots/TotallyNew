import discord
from discord.ext import commands
import os 
import sys
from dotenv import load_dotenv

def logError(content):
	print(content)

intents = discord.Intents.all()
intents.members = True
load_dotenv()
config = os.environ
client = commands.Bot(command_prefix=config.get('PREFIX'), intents=intents)
clientMemberConverter = commands.MemberConverter()
clientTextChannelConverter = commands.TextChannelConverter()
clientVoiceChannelConverter = commands.VoiceChannelConverter()

@client.event
async def on_ready():
	print('Bot is ready')

@client.command()
async def ready(ctx):
	await ctx.send('yeah !')

@client.command(
	name = 'kick',
	description = 'Kicks the specified user with the reason if specified',
	usage = f'{client.command_prefix}kick [member] <reason>',
	aliases = []
)
async def kick(ctx, member=None, *, reason='No reason provided'):

	if ctx.author.bot:
		return

	if (ctx.author.permissions_in(ctx.channel).kick_members!=True):
		await ctx.send(embed=discord.Embed(title='Kick Error',description='You do not have permissions to kick members',color=0xFFFF00))
		return

	if member == None:
		await ctx.send(embed=discord.Embed(title='Kick Error',description='You need to specify a valid member to kick them',color=0xFFFF00))
		return
	else:
		try:
			member = await clientMemberConverter.convert(ctx, member)
		except commands.MemberNotFound:
			await ctx.send(embed=discord.Embed(title='Kick Error',description='You need to specifiy a valid member to kick them',color=0xFFFF00))
			return

	if (ctx.me.permissions_in(ctx.channel).kick_members==True):

		if ctx.author.top_role > member.top_role:

			if ctx.me.top_role > member.top_role:

				await member.kick(reason=reason)

				kickEmbed = discord.Embed(title='Kick',description=f'{member.mention} was kicked',color=0x00FFFF)
				kickEmbed.set_footer(text=reason)

			else:

				kickEmbed = discord.Embed(title='Kick Error',description='I cannot kick members with higher authority than mine',color=0xFFFF00)

				await ctx.send(embed=kickEmbed)
		else:

			if (ctx.guild.owner == ctx.author):

				if (ctx.me.top_role > member.top_role):

					await member.kick(reason=reason)
					kickEmbed = discord.Embed(title='Kick',description=f'{member.mention} was kicked',color=0x00FFFF)
					kickEmbed.set_footer(text=reason)

				else:

					kickEmbed = discord.Embed(title='Kick',description='I cannot kick members with higher authority than mine',color=0xFFFF00)

				await ctx.send(embed=kickEmbed)


@client.command(
	name = 'ban',
	description = 'Bans the specified member with the reason if specified',
	usage = f'{client.command_prefix}ban [member] <reason>',
	alises = []
)
async def ban(ctx, member=None, *, reason='No reason provided'):

	if ctx.author.bot:
		return

	if (ctx.author.permissions_in(ctx.channel).ban_members!=True):

		if (ctx.author == ctx.guild.owner):
			if ctx.me.top_role > member.top_role:
				await member.kick(reason=reason)
				kickEmbed = discord.Embed(
					title = 'Kick',
					description = f'{member.mention} was kicked\n\nReason `{reason}`',
					color=0x00FFFF
				)
			else:
				kickEmbed = discord.Embed(
					title = 'Kick Error',
					description = 'I cannot kick members with higher authority than mine',
					color = 0xFF0000
				)
			await ctx.send(embed=kickEmbed)

		else:
			
			await ctx.send(
				embed=discord.Embed(
					title = 'Ban Error',
					description = 'You do not have permissions to ban members',
					color = 0xFF0000
					)
			)
			return

	if member == None:
		await ctx.send(
			embed=discord.Embed(
				title='Ban Error',
				description='You need to specify a valid user to ban',
				color = 0xFF0000
			)
		)
		return
	else:
		try:
			member = await clientMemberConverter.convert(ctx, member)
		except commands.MemberNotFound:
			await ctx.send(
				embed=discord.Embed(
				title = 'Ban Error',
				description = 'You need to specify a valid user to ban',
				color = 0xFF0000
				)
			)
			return
	if (ctx.me.permissions_in(ctx.channel).ban_members==True):
		if  ctx.author.top_role > member.top_role:
			if ctx.me.top_role > member.top_role:
				await member.ban(reason=reason)
				banEmbed = discord.Embed(
					title = 'Ban',
					description = f'{member.mention} was banned\n\nReason `{reason}`',
					color=0x00FFFF
				)
			else:
				banEmbed = discord.Embed(
					title = 'Ban Error',
					description = 'I cannot ban members with higher authority than mine',
					color = 0xFF0000
				)
		else:
			banEmbed = discord.Embed(
				title = 'Ban Error',
				description = 'You cannot ban members with higher authority than yours',
				color = 0xFFFF00)
	else:
		banEmbed = discord.Embed(
			title = 'Ban Error',
			description = 'I do not have permissions to ban members',
			color = 0xFF0000)
		banEmbed.set_footer(text='Ban Members permission missing')
	await ctx.send(embed=banEmbed)

@client.event
async def on_command_error(ctx, error):
	if isinstance(ctx, commands.CommandInvokeError):
		error = error.original
	await ctx.send(
		title = 'Error',
		description = error.capitalize(),
		color = 0xFF0000
	)


client.run(config.get('TOKEN'))