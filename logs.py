import discord
from discord.ext import commands
import datetime

client = discord.Client()
client = commands.Bot(command_prefix = '!')
client.remove_command('help')

@client.event
async def on_ready():
	print('Bot are working - LOGS')
	global LogsChannel
	LogsChannel = client.get_channel(LOGSCHANNELIDHERE!)


@client.event
async def on_member_join(member):
	await LogsChannel.send(embed=MemberEmbed("Has joined the server", member, member.mention, 0x7289da, True, "Total users:", totalmembers(), "Account create on: ", "{}".format(member.created_at.strftime("%d/%m/%Y %H:%M")), None, None))
	

@client.event
async def on_member_update(before, after):
	async for entry in LogsChannel.guild.audit_logs(limit=1):
		creator = entry.user
		if len(before.roles) < len(after.roles):
			new_role = next(role for role in after.roles if role not in before.roles)
			await LogsChannel.send(embed=MemberEmbed("Update Member", after, "{} role applied to {}".format(new_role.mention, after.mention), 0x7289da, False, "Updated by:", creator.mention, None, None, None, None))
		elif len(before.roles) > len(after.roles):
			new_role = next(role for role in before.roles if role not in after.roles)
			await LogsChannel.send(embed=MemberEmbed("Update Member", after, "{} role removed of {}".format(new_role.mention, after.mention), 0x7289da, False, "Updated by:", creator.mention, None, None, None, None))
		elif before.nick != after.nick:
			if after.nick == None:
				await LogsChannel.send(embed=MemberEmbed("Update Member", after, "`{}` has renamed to {}".format(before.nick, after.mention), 0x7289da, False, "Updated by:", creator.mention, None, None, None, None))
			elif before.nick == None:
				await LogsChannel.send(embed=MemberEmbed("Update Member", after, "{} has renamed to `{}`".format(before, after.nick), 0x7289da, False, "Updated by:", creator.mention, None, None, None, None))
			else:
				await LogsChannel.send(embed=MemberEmbed("Update Member", after, "`{}` has renamed to `{}`".format(before.nick, after.nick), 0x7289da, False, "Updated by:", creator.mention, None, None, None, None))

@client.event
async def on_member_remove(member):
	await LogsChannel.send(embed=MemberEmbed("Has left the server", member, member.mention, 0x7289da, True, "Total users:", totalmembers(), None, None, None, None))


@client.event
async def on_message(message):
	restric = client.get_channel(NEWS/WELCOMECHANNELHERE!)
	if not message.author.bot:
		if not message.channel == restric:
			if str(message.content[0]) != "!":
				await LogsChannel.send(embed=MessageEmbed("Sent Message", message, 0x4caf50, "Message:", "[Click to see message]({})".format(message.jump_url), "Channel:", "<#{}>".format(message.channel.id), None, None))

@client.event
async def on_message_edit(before, after):
	if not before.author.bot:
		before.content = "`Message:`\n{} \n\n`Edited Message:`\n {}".format(before.content, after.content)
		await LogsChannel.send(embed=MessageEmbed("Edited Message", before, 0xffc107, "Message:", "[Click to see message]({})".format(before.jump_url), "Channel:", "<#{}>".format(before.channel.id), None, None))

@client.event
async def on_message_delete(message):
	if not message.author.bot:
		await LogsChannel.send(embed=MessageEmbed("Deleted Message", message, 0xff4747, "Channel:", "<#{}>".format(message.channel.id), None, None, None, None))
		

@client.event
async def on_guild_role_create(role):
	async for entry in LogsChannel.guild.audit_logs(limit=1):
		creator = entry.user
		await LogsChannel.send(embed=GuildEmbed("Created Role", creator, "{} has created `{}`".format(creator.mention, role.name), 0x7289da, None, None, None, None, None, None))

@client.event
async def on_guild_role_update(before, after):
	async for entry in LogsChannel.guild.audit_logs(limit=1):
		creator = entry.user
		if before.name != after.name:
			await LogsChannel.send(embed=GuildEmbed("Updated Role", creator, "{} has renamed `{}` to `{}`".format(creator.mention, before.name, after.name), 0x7289da, None, None, None, None, None, None))


@client.event
async def on_guild_role_delete(role):
	async for entry in LogsChannel.guild.audit_logs(limit=1):
		creator = entry.user
		await LogsChannel.send(embed=GuildEmbed("Deleted Role", creator, "{} has deleted `{}`".format(creator.mention, role.name), 0x7289da, None, None, None, None, None, None))


@client.event
async def on_guild_channel_create(channel):
		async for entry in LogsChannel.guild.audit_logs(limit=1):
			creator = entry.user
			await LogsChannel.send(embed=GuildEmbed("Created {} channel".format(channel.type), creator, "{} has created `{}`".format(creator.mention, channel.name), 0x7289da, None, None, None, None, None, None))

@client.event
async def on_guild_channel_update(before, after):
		async for entry in LogsChannel.guild.audit_logs(limit=1):
			creator = entry.user
			if before.name != after.name:
				print(after.type)
				print(before.type)
				if str(after.type) == 'category':
					await LogsChannel.send(embed=GuildEmbed("Updated category", creator, "{} has renamed `{}` to `{}`".format(creator.mention, before.name, after.name), 0x7289da, None, None, None, None, None, None))
				else:
					await LogsChannel.send(embed=GuildEmbed("Updated {} channel".format(before.type), creator, "{} has renamed `{}` to `{}`".format(creator.mention, before.name, after.name), 0x7289da, None, None, None, None, None, None))

			elif before.category != after.category:
				await LogsChannel.send(embed=GuildEmbed("Updated {} channel".format(before.type), creator, "{} has moved `{}` to category `{}`".format(creator.mention, before.name, after.category), 0x7289da, None, None, None, None, None, None))

@client.event
async def on_guild_channel_delete(channel):
		async for entry in LogsChannel.guild.audit_logs(limit=1):
			creator = entry.user
			await LogsChannel.send(embed=GuildEmbed("Deleted {} channel".format(channel.type), creator, "{} has deleted `{}`".format(creator.mention, channel.name), 0x7289da, None, None, None, None, None, None))


@client.event
async def on_voice_state_update(member, before, after):
	async for entry in LogsChannel.guild.audit_logs(limit=1):
		creator = entry.user
		if before.channel is None and after.channel is not None:
			await LogsChannel.send(embed=GuildEmbed("Voice State Update", member, "{} has joined to `{}`".format(creator.mention, after.channel), 0x4caf50, None, None, None, None, None, None))
		if after.channel is None and before.channel is not None:
			await LogsChannel.send(embed=GuildEmbed("Voice State Update", member, "{} has left to `{}`".format(creator.mention, before.channel), 0xff4747, None, None, None, None, None, None))
		if before.channel != after.channel and before.channel is not None and after.channel is not None:
			await LogsChannel.send(embed=GuildEmbed("Voice State Update", member, "{} has moved of `{}` to `{}`".format(creator.mention, before.channel, after.channel), 0xffc107, None, None, None, None, None, None))



def GuildEmbed(title, guild, description, color, field_title1, field_value1, field_title2, field_value2, field_title3, field_value3):
	title = "{} ({}) - {}".format(guild, guild.id, title)
	content = "{}".format(description)
	embed = discord.Embed(description=content, color=color, timestamp=datetime.datetime.utcnow())
	embed.set_author(name=title, icon_url=guild.avatar_url)
	if field_title1 != None and field_value1 != None:
		embed.add_field(name=field_title1, value=field_value1, inline=True)
	if field_title2 != None and field_value2 != None:
		embed.add_field(name=field_title2, value=field_value2, inline=True)
	if field_title3 != None and field_value3 != None:
		embed.add_field(name=field_title3, value=field_value3, inline=True)
	return embed

def MemberEmbed(title, member, description, color, thumbnail, field_title1, field_value1, field_title2, field_value2, field_title3, field_value3):
	title = "{} ({}) - {}".format(member, member.id, title)
	content = "{}".format(description)
	embed = discord.Embed(description=content, color=color, timestamp=datetime.datetime.utcnow())
	embed.set_author(name=title, icon_url=member.avatar_url)
	if thumbnail:
		embed.set_thumbnail(url=member.avatar_url)
	if field_title1 != None and field_value1 != None:
		embed.add_field(name=field_title1, value=field_value1, inline=True)
	if field_title2 != None and field_value2 != None:
		embed.add_field(name=field_title2, value=field_value2, inline=True)
	if field_title3 != None and field_value3 != None:
		embed.add_field(name=field_title3, value=field_value3, inline=True)
	return embed

def MessageEmbed(title, message, color, field_title1, field_value1, field_title2, field_value2, field_title3, field_value3):
	title = "{} ({}) - {}".format(message.author, message.author.id, title)
	content = "{}".format(message.content)
	embed = discord.Embed(description=content, color=color, timestamp=datetime.datetime.utcnow())
	embed.set_author(name=title, icon_url=message.author.avatar_url)
	if field_title1 != None and field_value1 != None:
		embed.add_field(name=field_title1, value=field_value1, inline=True)
	if field_title2 != None and field_value2 != None:
		embed.add_field(name=field_title2, value=field_value2, inline=True)
	if field_title3 != None and field_value3 != None:
		embed.add_field(name=field_title3, value=field_value3, inline=True)
	return embed

def totalmembers():
	for guild in client.guilds:
		x = guild.member_count
	return x

client.run(TOKEN!)