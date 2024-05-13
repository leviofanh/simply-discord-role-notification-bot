import discord
from discord.ext import commands
import sqlite3

intents = discord.Intents.all()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='//?', intents=intents)


def create_table():
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (server_id INTEGER PRIMARY KEY, message TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS excluded_roles
                 (server_id INTEGER, role_id INTEGER, PRIMARY KEY (server_id, role_id))''')
    conn.commit()
    conn.close()


create_table()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command(aliases=['setmsg'])
@commands.has_permissions(administrator=True)
async def setmessage(ctx, *, message):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO settings (server_id, message) VALUES (?, ?)''', (ctx.guild.id, message))
    conn.commit()
    conn.close()
    await ctx.send('Message are set.')


@bot.command(aliases=['exrole'])
@commands.has_permissions(administrator=True)
async def excluderole(ctx, role: discord.Role):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO excluded_roles (server_id, role_id) VALUES (?, ?)''', (ctx.guild.id, role.id))
    conn.commit()
    conn.close()
    await ctx.send(f'Role {role.name} has been added to the exclusion list.')


@bot.command(aliases=['unexrole'])
@commands.has_permissions(administrator=True)
async def unexcluderole(ctx, role: discord.Role):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute('''DELETE FROM excluded_roles WHERE server_id = ? AND role_id = ?''', (ctx.guild.id, role.id))
    conn.commit()
    conn.close()
    await ctx.send(f'Role {role.name} has been removed from the exclusion list.')


@bot.event
async def on_member_update(before, after):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute('''SELECT message FROM settings WHERE server_id = ?''', (after.guild.id,))
    result = c.fetchone()

    c.execute('''SELECT role_id FROM excluded_roles WHERE server_id = ?''', (after.guild.id,))
    excluded_roles = [role[0] for role in c.fetchall()]

    conn.close()

    if result:
        message = result[0]
        roles_added = [role for role in after.roles if role not in before.roles and role.id not in excluded_roles]

        for role in roles_added:
            user = after.mention
            role_name = role.name
            server_name = after.guild.name
            formatted_message = message.format(USER=user, ROLE=role_name, SERVER=server_name)
            await after.send(formatted_message)


api_key = open('key.txt', 'r').read()
bot.run(api_key)
