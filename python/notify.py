# Author: lavaramano <lavaramano AT gmail DOT com>
# Improved by: BaSh - <bash.lnx AT gmail DOT com>
# Ported to Weechat 0.2.7 by: Sharn - <sharntehnub AT gmail DOT com)
# This Plugin Calls the libnotify bindings via python when somebody says your nickname, sends you a query, etc.
# To make it work, you may need to download: python-notify (and libnotify - libgtk) 
# Requires Weechat 0.2.7
# Released under GNU GPL v2

import weechat, pynotify, string

WEECHAT_ICON = "/usr/share/pixmaps/weechat.xpm"

weechat.register("weenotify", "lavaramano", "0.0.1.6", "GPL", "weenotify: A real time notification system for weechat", "", "")

# script options
settings = {
    "show_hilights"             : "on",
    "show_priv_msg"             : "on",
    "debug"                     : "off",
}

# Init everything
for option, default_value in settings.items():
    if weechat.config_get_plugin(option) == "":
        weechat.config_set_plugin(option, default_value)

# Hook privmsg/hilights
weechat.hook_print("", "", "", 1, "weenAddHi")
weechat.hook_signal("weechat_pv", "weenAddPriv")

# Functions
def weenAddHi( bufferp, uber_empty, tagsn, isdisplayed, ishilight, prefix, message ):
    """Sends highlighted message to be printed on notification"""
    if ishilight == "1" and weechat.config_get_plugin('show_hilights') == "on":
        window = WeeNotification()
        if not weechat.buffer_get_string(bufferp, "short_name"):
            buffer = weechat.buffer_get_string(bufferp, "name")
        else:
            buffer = weechat.buffer_get_string(bufferp, "short_name")

        window.show_notification(buffer , "<b>"+prefix+"</b>: "+message)
        if weechat.config_get_plugin('debug') == "on":
            print prefix

    return weechat.WEECHAT_RC_OK

def weenAddPriv( signal, message ):
    """Sends private message to be printed on notification"""
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

# vim: ai ts=4 sts=4 et sw=4
