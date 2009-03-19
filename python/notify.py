# Author: lavaramano <lavaramano AT gmail DOT com>
# Improved by: BaSh - <bash.lnx AT gmail DOT com>
# This Plugin Calls the libnotify bindings via python when somebody says your nickname, sends you a query, etc.
# To make it work, you may need to download: python-notify (and libnotify - libgtk) 
# TODO: set on/off the notification popup. 
# Released under GNU GPL v2

import weechat, pynotify, string

WEECHAT_ICON = "/usr/share/pixmaps/weechat.xpm"

weechat.register("wee-n", "lavaramano", "0.0.1.6", "GPL", "wee-n!: A real time notification system for weechat", "", "")

# script options
settings = {
    "show_hilights"             : "on",
    "show_priv_msg"             : "on",
    "debug"                     : "off",
}

# Init everythin
for option, default_value in settings.items():
    if weechat.config_get_plugin(option) == "":
        weechat.config_set_plugin(option, default_value)

if weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out')) == "":
    weechat.buffer_new( weechat.config_get_plugin('buffer_out'), "", "" )
    bufferpointer = weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out'))
else:
    bufferpointer = weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out'))

# Hook privmsg/hilights
weechat.hook_print("", "", "", 0, "weenAddHi")
weechat.hook_signal("weechat_pv", "weenAddPriv")

# Functions
def weenAddHi( bufferp, uber_empty, tagsn, isdisplayed, ishilight, prefix, message ):
    """Adds hilighted text to hilight buffer"""
    if ishilight == "1" and weechat.config_get_plugin('show_hilights') == "on":
        window = WeeNotification()
        if not weechat.buffer_get_string(bufferp, "short_name"):
            buffer = weechat.buffer_get_string(bufferp, "name")
        else:
            buffer = weechat.buffer_get_string(bufferp, "short_name")

	    window.show_notification(buffer , "<b>"+prefix+"</b>: "+message)
    return weechat.WEECHAT_RC_OK

def weenAddPriv( signal, message ):
    """Formats and adds private messages to hilight buffer"""
    if weechat.config_get_plugin('show_priv_msg') == "on":
        window = WeeNotification()
        window.show_notification("Private message: ",  message)
    return weechat.WEECHAT_RC_OK

class WeeNotification:
    def show_notification(self,chan,message):
        pynotify.init("wee-notifier")
        wn = pynotify.Notification(chan, message, WEECHAT_ICON)
        wn.set_urgency(pynotify.URGENCY_NORMAL)
        #wn.set_timeout(pynotify.EXPIRES_NEVER)
        wn.show()
    def message_irc(self,message):
        string = ''
        msg = message.split(":")
        for i in range(len(msg)):
            if i > 0:
                string += msg[i]+' '
        return string

def handle_message(server, args):
    window         = WeeNotification()
    string         = args.split('!')
    nick           = string[0].replace(':','')
    nick_say       = string[1].split("PRIVMSG")
    nickname	   = weechat.get_info("nick")
    current_server = weechat.get_info("server")
    current_chan   = weechat.get_info("channel")
    away		   = weechat.get_info("away")
    chan           = nick_say[1].split(":")[0].strip()
    message        = window.message_irc(nick_say[1])
    if (away == '1'):
        if (nickname == chan):
            window.show_notification("Private message by "+ nick, message)
        elif (nickname) in message:
            if "ACTION" in message:
                window.show_notification("<i>"+message.replace('ACTION','')+"</i>" ,"<b>"+ nick +" ("+chan+")</b>")
                weechat.prnt(message)
            else:
                window.show_notification(chan +" on "+ server, "<b>"+nick+"</b>: "+message)
    return weechat.PLUGIN_RC_OK

# vim: ai ts=4 sts=4 et sw=4
