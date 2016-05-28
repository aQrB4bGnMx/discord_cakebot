class help_entry():
    def __init__(self, command, description, usage):
        self.command = command
        self.description = description
        self.usage = usage
        self.short_description = description.split('\n')[0]
    def get_entry(self):
        formatted = '\n' \
                    '**Command:** ``' + self.command + '``\n\n' \
                    '**Description**\n' + self.description + '\n\n' \
                    '**Usage**\n```' + self.usage + '```'
        return formatted

hello_desc = 'cakebot says hello!'
hello_usage = '!hello'
hello_help = help_entry('!hello', hello_desc, hello_usage)

timedcats_desc = 'Sends random cat images in timed intervals :3'
timedcats_usage = '!timedcats <number> <interval>\n' \
                  '<interval> - m (minute) or h (hour)\n\n' \
                  'Example: !timedcats 3 m - send random cat images each minute for 3 minutes\n' \
                  'Default is 5 m'
timedcats_help = help_entry('!timedcats', timedcats_desc, timedcats_usage)

find_desc = 'Searches the last 500 messages in current channel for a message containing a keyword'
find_usage = '!find <keyword> <user mention>\n' \
             '<user mention> - optional, Example:  @leagueofcake\n' \
             'Returns a message with the author of found message and timestamp.\n\n' \
             'Example: !find fruit @leagueofcake\n (user specified)' \
             'Example: !find fruit (user not specified)'
find_help = help_entry('!find', find_desc, find_usage)

redirect_desc = 'Redirects a message to another channel.'
redirect_usage = '!redirect <channel> <message>\n\n' \
                 '<channel> - Must be in #form Example:  #main\n\n' \
                 'Example: !redirect #alt Hi guys, from the main channel! - redirects message to #alt with message'
redirect_help = help_entry('!redirect', redirect_desc, redirect_usage)

play_desc = 'Queues music\n' \
            'Variants: for more info do !help <variant>\n' \
            '!play      - Queues a song by name or alias' \
            '!playid    - Queues a song by id\n' \
            '!playalbum - Queues all the songs in an album'
play_usage = '!play <keyword/title/alias>\n' \
             'Not case sensitive. If multiple matches are found, cakebot will display 15 possible matches and prompt the user to !playid <id>\n\n' \
             'Example: !play snow (will have multiple matches)\n' \
             'Example: !play sound of silence (exact match, plays song)\n' \
             'Example: !play haifuriop (exact match for alias)'
play_help = help_entry('!play', play_desc, play_usage)

playid_desc = 'Queues music by id\n' \
              'Variant of !play: to see other variants do !help play'
playid_usage = '!playid <id>\n' \
               '<id> - number, can be found with !search <keyword>\n\n' \
               'Example: !play 315'
playid_help = help_entry('!playid', playid_desc, playid_usage)

playalbum_desc = 'Queues an entire album\n' \
                 'Variant of !play: to see other variants do !help play'
playalbum_usage = '!playalbum <name/keyword>\n' \
                  '<name> - Not case sensitive\n\n' \
                  'Example: !play snow halation'
playalbum_help = help_entry('!playalbum', playalbum_desc, playalbum_usage)

reqsong_desc = 'Sends link to a form for requesting songs to be added to the database.'
reqsong_usage = '!reqsong'
reqsong_help = help_entry('!reqsong', reqsong_desc, reqsong_usage)

search_desc = 'Searches the song database for a keyword'
search_usage = '!search <keyword>\n' \
               '<keyword> - Alias/song/artist/album name. Not case sensitive.\n\n' \
               'Example: !search snow\n' \
               'Returns up to 15 results.'
search_help = help_entry('!search', search_desc, search_usage)

google_desc = 'Generates a Google search link for a keyword. For lazy people like me.'
google_usage = '!google <keyword>\n'
google_help = help_entry('!google', google_desc, google_usage)

trollurl_desc = 'Replaces characters in a URL to make a similar looking one'
trollurl_usage = '!trollurl <url>\n'
trollurl_help = help_entry('!trollurl', trollurl_desc, trollurl_usage)

invite_desc = 'Generates a link to invite cakebot to your server'
invite_usage = '!invite\n'
invite_help = help_entry('!invite', invite_desc, invite_usage)

help_desc = 'Displays this message.'
help_usage = '!help'
help_help = help_entry('!help', help_desc, help_usage)

help_dict = {
                'hello':     hello_help,
                'timedcats': timedcats_help,
                'find':      find_help,
                'redirect':  redirect_help,
                'play':      play_help,
                'playid':    playid_help,
                'playalbum': playalbum_help,
                'reqsong':   reqsong_help,
                'search':    search_help,
                'google':    google_help,
                'trollurl':  trollurl_help,
                'invite':    invite_help,
            }

# Interface functions
def get_entry(name):
    return help_dict[name].get_entry()

def generate_summary():
    sorted_keys = sorted(help_dict)
    head = '\nCommand summary. For more information do ``!help <command>`` e.g. ``!help timedcats``\n'
    summary = head
    summary += '```'
    for command in sorted_keys:
        summary += help_dict[command].command.ljust(12, ' ')
        summary += help_dict[command].short_description + '\n'
    summary += '```'
    return summary
