import discord
from discord.ext import commands
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


intents = discord.Intents.all()
intents.guilds = True
intents.members = True

PREFIX = config['bot']['BOT_PREFIX']
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

DATABASE_URL = 'sqlite:///config.db'
DEFAULT_MESSAGE = config['bot']['DEFAULT_MESSAGE']
STATUS = config['bot']['STATUS']

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


class Settings(Base):
    __tablename__ = 'settings'
    server_id = Column(Integer, primary_key=True)
    message = Column(Text, default=DEFAULT_MESSAGE)


class ExcludedRole(Base):
    __tablename__ = 'excluded_roles'
    server_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)


class RoleMessage(Base):
    __tablename__ = 'role_messages'
    server_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, primary_key=True)
    message = Column(Text)


Base.metadata.create_all(engine)

setmessage_aliases = config['commands_aliases']['setmessage']
excluderole_aliases = config['commands_aliases']['excluderole']
unexcluderole_aliases = config['commands_aliases']['unexcluderole']
setrolemessage_aliases = config['commands_aliases']['setrolemessage']


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name=STATUS))


@bot.command(aliases=(setmessage_aliases, ))
@commands.has_permissions(administrator=True)
async def setmessage(ctx, *, message):
    settings = session.query(Settings).filter_by(server_id=ctx.guild.id).first()
    if settings:
        settings.message = message
    else:
        settings = Settings(server_id=ctx.guild.id, message=message)
        session.add(settings)
    session.commit()
    await ctx.send('Message has been set.')


@bot.command(aliases=(excluderole_aliases, ))
@commands.has_permissions(administrator=True)
async def excluderole(ctx, role: discord.Role):
    excluded_role = session.query(ExcludedRole).filter_by(server_id=ctx.guild.id, role_id=role.id).first()
    if not excluded_role:
        excluded_role = ExcludedRole(server_id=ctx.guild.id, role_id=role.id)
        session.add(excluded_role)
        session.commit()
        await ctx.send(f'Role {role.name} has been added to the exclusion list.')


@bot.command(aliases=(unexcluderole_aliases, ))
@commands.has_permissions(administrator=True)
async def unexcluderole(ctx, role: discord.Role):
    session.query(ExcludedRole).filter_by(server_id=ctx.guild.id, role_id=role.id).delete()
    session.commit()
    await ctx.send(f'Role {role.name} has been removed from the exclusion list.')


@bot.command(aliases=(setrolemessage_aliases, ))
@commands.has_permissions(administrator=True)
async def setrolemessage(ctx, role: discord.Role, *, message):
    role_message = session.query(RoleMessage).filter_by(server_id=ctx.guild.id, role_id=role.id).first()
    if role_message:
        role_message.message = message
    else:
        role_message = RoleMessage(server_id=ctx.guild.id, role_id=role.id, message=message)
        session.add(role_message)
    session.commit()
    await ctx.send(f'Custom message for role {role.name} has been set.')


@bot.event
async def on_member_update(before, after):
    settings = session.query(Settings).filter_by(server_id=after.guild.id).first()
    default_message = settings.message if settings else DEFAULT_MESSAGE

    excluded_roles = session.query(ExcludedRole.role_id).filter_by(server_id=after.guild.id).all()
    excluded_roles = [role_id for role_id, in excluded_roles]

    roles_added = [role for role in after.roles if role not in before.roles and role.id not in excluded_roles]

    for role in roles_added:
        role_message = session.query(RoleMessage).filter_by(server_id=after.guild.id, role_id=role.id).first()
        message = role_message.message if role_message else default_message

        user = after.mention
        role_name = role.name
        server_name = after.guild.name
        formatted_message = message.format(USER=user, ROLE=role_name, SERVER=server_name)
        await after.send(formatted_message)


if config['api']['USE_ENV'].lower() == 'yes':
    ENV = config['api']['ENV_NAME']
    api_key = (os.environ[ENV])

if config['api']['USE_ENV'].lower() == 'no':
    PATH = config['api']['API_KEY_PATH']
    api_key = open(PATH, 'r').read()


bot.run(api_key)
