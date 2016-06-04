import sys
import discord
import asyncio
import requests
import datetime
import random
import sqlite3
import cakebot_config
import cakebot_help

client = discord.Client()
conn = sqlite3.connect('cakebot.db')
c = conn.cursor()

invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=66186303'
normal_invite = 'https://discordapp.com/oauth2/authorize?client_id=178312661233172480&scope=bot&permissions=67356673'

def parse_command_args(command):
    splitted = command.split(' ')
    return splitted

def is_integer(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def select_repl(char):
    try:
        weight = 8
        key = int(random.random() * (len(cakebot_config.repl_dict[char]) + weight))
        if key < weight + 1: return cakebot_config.repl_dict[char][0] # Below weight, key equals 0 (key for first/default character)
        else: return cakebot_config.repl_dict[char][key - weight]
    except KeyError: # Return original char if char not found in dict
        return char

def return_troll(url):
    prefix = ''
    if 'https://' in url: prefix = 'https://'
    elif 'http://' in url: prefix = 'http://'
    return prefix + ''.join([select_repl(x) for x in url[len(prefix):]])

def find_permissions(perms, word):
    if perms:
        for perm in perms:
            if word == perm:
                return True
    return False

# @client.event
# async def on_server_join(server):
#     pass
#     channels = client.get_all_channels()
#     for channel in channels:
#         if str(channel.type) == 'text':
#             await client.send_message(channel, 'Hi everyone!')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # channels = client.get_all_channels()
    # for channel in channels:
    #     if str(channel.type) == 'text':
    #         await client.send_message(channel, 'Hi everyone! I\'m online now!')

@client.event
async def on_message(message):
    content = message.content
    if content.startswith('!hello'):
        await client.send_message(message.channel, 'Hello {}!'.format(message.author.mention))
    if content.startswith('!bye'):
        if str(message.author.id) == '139345807944974336':
            await client.send_message(message.channel, 'Logging out, bye!')
            sys.exit()
        else:
            await client.send_message(message.channel, 'I\'m not going anywhere!')
    elif content.startswith('!permissions'):
        args = parse_command_args(content)
        user = message.author
        server_id = message.server.id;
        if message.mentions:
            user = message.mentions[0] # Find id of first mentioned user

        #await client.send_message(message.channel, 'Detected: {} with id {}'.format(user, user.id))

        c.execute("SELECT permissions FROM permissions WHERE user_id = ? AND server_id = ?", (user.id, server_id))
        found = c.fetchone()
        if len(args) == 2:
            if found:
                await client.send_message(message.channel, 'Permissions for {}: {}'.format(user, found))
            else:
                await client.send_message(message.channel, 'There are no set permissions for: {}'.format(user))

        elif str(message.author.id) == '139345807944974336' and len(args) > 2:
            if found:
                current_perms = found[0]
                new_perms = current_perms + ',' + ','.join(args[2:])
                c.execute("UPDATE permissions SET permissions = ? WHERE user_id = ? AND server_id = ?", (new_perms, user.id, server_id))
                await client.send_message(message.channel, 'Added permissions: `{}` to {}'.format(','.join(args[2:]), user))
                conn.commit()
            else:
                c.execute("INSERT INTO permissions (user_id, server_id, permissions) VALUES (?, ?, ?)", (user.id, server_id, ','.join(args[2:])))
                await client.send_message(message.channel, 'Added permissions: `{}` to {}'.format(','.join(args[2:]), user))
                conn.commit()
        else:
            pass
    elif content.startswith('!musicprefix'):
        args = parse_command_args(content)
        #await client.send_message(message.channel, 'Server: {}'.format(message.server.id))
        server_id = message.server.id

        c.execute("SELECT permissions FROM permissions WHERE user_id = ? AND server_id = ?", (message.author.id, message.server.id))
        found = c.fetchone()

        can_manage_server = message.channel.permissions_for(message.author).manage_server
        has_musicprefix_perm = find_permissions(found, 'musicprefix')

        if len(args) == 1:
            c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
            found = c.fetchone()
            if found:
                tmp = await client.send_message(message.channel, 'Current music prefix for this server is: `{}`'.format(found[0]))
                await(asyncio.sleep(5))
                await client.delete_message(tmp)
            else:
                tmp = await client.send_message(message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
                await(asyncio.sleep(5))
                await client.delete_message(tmp)
        else:
            # tmp = await client.send_message(message.channel, 'Can update music prefix: {}'.format(can_manage_server))#.can_manage_server(message.author)))
            if can_manage_server or has_musicprefix_perm:
                prefix = ' '.join(args[1:])

                c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
                found = c.fetchone()
                if found:
                    c.execute("UPDATE music_prefix SET prefix = ? WHERE server_id = ?", (prefix, server_id))
                    conn.commit()
                    await client.send_message(message.channel, 'Updated music prefix for this server to: `{}`'.format(prefix))
                else:
                    c.execute("INSERT INTO music_prefix(server_id, prefix) VALUES (?, ?)", (server_id, prefix))
                    conn.commit()
                    await client.send_message(message.channel, 'Set music prefix for this server to: `{}`'.format(prefix))
            else:
                tmp = await client.send_message(message.channel, 'You don\'t have the permissions to do that! Message a moderator to change it.')
                await(asyncio.sleep(5))
                await client.delete_message(tmp)

    elif content.startswith('!invite'):
        await client.send_message(message.channel, 'Add me to your server! Click here: {}!'.format(normal_invite))
    elif content.startswith('!timedcats'):
        if str(message.author.id) == '139345807944974336':
            times = 5
            duration_str = 'm'

            args = parse_command_args(content)

            if len(args) > 1:
                arg_times = args[1]
                if is_integer(arg_times):
                    if int(arg_times) <= 60:
                        times = int(arg_times)

                if len(args) > 2:
                    arg_duration = args[2]
                    if arg_duration in cakebot_config.time_map:
                        duration_str = arg_duration

            unit_time = cakebot_config.time_map[duration_str][0]
            duration_time = unit_time * times

            unit_duration_str = cakebot_config.time_map[duration_str][1]
            long_duration_str = cakebot_config.time_map[duration_str][2]

            if times == 1:
                long_duration_str = unit_duration_str

            sending_msg = 'Sending cats every {} for {} {}!'.format(unit_duration_str, times, long_duration_str)
            await client.send_message(message.channel, sending_msg)

            loop = asyncio.get_event_loop()
            end_time = loop.time() + duration_time

            await asyncio.sleep(5)
            while True:
                cat_url = requests.get('http://random.cat/meow').json()['file']
                await client.send_message(message.channel, cat_url)
                if (loop.time() + unit_time) >= end_time:
                    break
                await(asyncio.sleep(unit_time))
            await client.send_message(message.channel, 'Finished sending cats!')
        else:
            await client.send_message(message.channel, 'Only leagueofcake can send cats right now, sorry :(')
    elif content.startswith('!find'):
        args = parse_command_args(content)
        found = False

        if len(args) > 1:
            keyword = args[1]
            user_id = None
            if message.raw_mentions:
                user_id = message.raw_mentions[0] # Find id of first mentioned user

            async for log in client.logs_from(message.channel, limit=500):
                if keyword.lower() in log.content.lower() and log.id != message.id and log.author != client.user:
                    if user_id == None or log.author.id == user_id:
                        try:
                            timestamp = log.timestamp.strftime('%H:%M, %d/%m/%Y')
                            await client.send_message(message.channel, '{} said at {}:\n```{}```'.format(log.author, timestamp, log.clean_content))
                            found = True
                        except:
                            print('Untranslatable message')
                        break # terminate after finding first message
            if not found:
                not_found = await client.send_message(message.channel, 'Couldn\'t find message!')
                await asyncio.sleep(5)
                await client.delete_message(not_found)
        else:
            await client.send_message(message.channel, 'Not enough arguments! Expecting 1')
    elif content.startswith('!trollurl'):
        args = parse_command_args(content)
        url = args[1]
        await client.send_message(message.channel, return_troll(url))
        await client.delete_message(message)
    elif content.startswith('!google'):
        args = parse_command_args(content)
        words = args[1:]
        url = 'https://www.google.com/#q=' + '+'.join(words)
        await client.send_message(message.channel, url)
    elif content.startswith('!redirect'):
        args = parse_command_args(content)
        room = message.channel_mentions[0]
        tmp = await client.send_message(room, '`{}` redirected:'.format(message.author))
        tmp = await client.send_message(room, ' '.join(args[2:]))
        #await asyncio.sleep(3)
        await client.delete_message(message)
    elif content.startswith('!play'): # Play song by title
        args = parse_command_args(content)
        if args[0] == '!play':
            song_name = ' '.join(args[1:])
            s = '%{}%'.format(song_name.lower())
            c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (s, s))
            found = c.fetchmany(size=13)

            if len(found) == 1:
                server_id = message.server.id
                c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
                prefix = c.fetchone()
                if prefix:
                    prefix = prefix[0]
                    confirm = await client.send_message(message.channel, "{} {}".format(prefix, found[0][4]))
                    await client.send_message(message.channel, "{} queued: {}".format(message.author, found[0][1]))
                    await(asyncio.sleep(3))
                    await client.delete_message(confirm)
                else:
                    tmp = await client.send_message(message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
                    await(asyncio.sleep(5))
                    await client.delete_message(tmp)
            elif len(found) > 1:
                results = "\nFound multiple matches: (limited to 13). Use ``!playid <id>``\n```"
                s = '%{}%'.format(song_name.lower())
                c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(alias) LIKE ?", (s, s))
                found = c.fetchmany(size=13)
                results += '{} {} {} {} {}'.format('ID'.ljust(4, ' '), 'Name'.ljust(45, ' '), 'Artist'.ljust(25, ' '), 'Album'.ljust(35, ' '), 'Alias'.ljust(20, ' '))
                if found:
                    for song in found:
                        id, name, artist, album, alias = song[0], song[1], song[2], song[3], song[5]
                        id = str(id).ljust(4, ' ')
                        name = name[:45].ljust(45, ' ')
                        artist = str(artist)[:25].ljust(25, ' ')
                        album = str(album)[:35].ljust(35, ' ')
                        alias = str(alias)[:20].ljust(20, ' ')

                        formatted = "{} {} {} {} {}".format(id, name, artist, album, alias)
                        results += '\n' + formatted
                    tmp = await client.send_message(message.channel, results + '```')
                    await(asyncio.sleep(8))
                    await client.delete_message(tmp)
            else:
                await client.send_message(message.channel, "Couldn't find that song!")
        else:
            if content.startswith('!playalbum'):
                album_name = ' '.join(args[1:])
                c.execute("SELECT * FROM songs WHERE LOWER(album) LIKE ?", ('%{}%'.format(album_name.lower()),))
            elif content.startswith('!playid'):
                id = args[1]
                c.execute("SELECT * FROM songs WHERE id LIKE ?", (id,))

            found = c.fetchmany(size=15)
            server_id = message.server.id

            if found:
                for song in found:
                    #await client.send_message(message.channel, found)
                    # Find music_prefix in db
                    c.execute("SELECT prefix FROM music_prefix WHERE server_id = ?", (server_id, ))
                    prefix = c.fetchone()
                    if prefix:
                        prefix = prefix[0]
                        confirm = await client.send_message(message.channel, "{} {}".format(prefix, song[4]))
                        await client.send_message(message.channel, "{} queued: {}".format(message.author, song[1]))
                        await(asyncio.sleep(3))
                        await client.delete_message(confirm)
                    else:
                        tmp = await client.send_message(message.channel, 'No prefix is configured for this server. Add one with `!musicprefix <prefix>`')
                        await(asyncio.sleep(5))
                        await client.delete_message(tmp)
            else:
                await client.send_message(message.channel, "Couldn't find that song!")

    elif content.startswith('!reqsong'):
        await client.send_message(message.channel, '\nFill this in and PM leagueofcake: <http://goo.gl/forms/LesR4R9oXUalDRLz2>\nOr this (multiple songs): <http://puu.sh/pdITq/61897089c8.csv>')
    elif content.startswith('!search'):
        args = parse_command_args(content)
        search_str = ' '.join(args[1:])
        s = '%{}%'.format(search_str.lower())
        c.execute("SELECT * FROM songs WHERE LOWER(name) LIKE ? OR LOWER(album) LIKE ? OR LOWER(artist) LIKE ? OR LOWER(alias) LIKE ?", (s, s, s, s))
        found = c.fetchmany(size=13)
        results = '\nSongs found (limited to 13):\n```'
        results += '{} {} {} {} {}'.format('ID'.ljust(4, ' '), 'Name'.ljust(45, ' '), 'Artist'.ljust(25, ' '), 'Album'.ljust(35, ' '), 'Alias'.ljust(20, ' '))
        if found:
            for song in found:
                id, name, artist, album, alias = song[0], song[1], song[2], song[3], song[5]
                id = str(id).ljust(4, ' ')
                name = name[:45].ljust(45, ' ')
                artist = str(artist)[:25].ljust(25, ' ')
                album = str(album)[:35].ljust(35, ' ')
                alias = str(alias)[:20].ljust(20, ' ')

                formatted = "{} {} {} {} {}".format(id, name, artist, album, alias)
                results += '\n' + formatted
            tmp = await client.send_message(message.channel, results + '```')
            await(asyncio.sleep(8))
            await client.delete_message(tmp)
        else:
            await client.send_message(message.channel, "Couldn't find any songs!")
    elif content.startswith('!help'):
        args = parse_command_args(content)
        if len(args) > 1: # specific command
            command = args[1]
            try:
                entry = cakebot_help.get_entry(command)
                tmp = await client.send_message(message.channel, cakebot_help.get_entry(command))
            except KeyError:
                tmp = await client.send_message(message.channel, 'Command not found! Do ``!help`` for the command list.')
        else: # command list summary
            tmp = await client.send_message(message.channel, cakebot_help.generate_summary())

        # Delete message after 5 seconds
        await(asyncio.sleep(10))
        await client.delete_message(tmp)
    # elif content.startswith('!'):
        # tmp = await client.send_message(message.channel, 'Unknown command! Type !help for commands')
        # await(asyncio.sleep(5))
        # await client.delete_message(tmp)

client.run(cakebot_config.token)
