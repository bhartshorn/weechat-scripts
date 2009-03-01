#!/bin/env python
#
# HilightBuffer, version .1, for weechat version 0.2.7 or later
#
#  Listens for hilights and sends them to a hilight buffer.
#
# Usage:
#
#   Simply load the script, and all hilights in all channels will be sent to a single hilight buffer.
#
# Configuration:
#
#   None needed so far.
#
# Requirements:
#
#   No requirements so far.
#
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                    Version 2, December 2004
#
# Copyright (C) 2004 Sam Hocevar
#  14 rue de Plaisance, 75014 Paris, France
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#
# Changelog:
#
# Version 0.5, 28 Feb, 2009
#  Commented out the import of pynotify - it was causing troubles, so visual notification will not work for now. Added channel name for hilights and "privmsg -- " in front of privmsgs.
#  Everything still works as it should
#
# Version 0.4, 23 Feb, 2009
#   Changed the way the script gets settings, so it actually gets settings real-time. It no longer just loads them on registration. 
#
# Version 0.3, 20 Feb, 2009
#   All works as expected. Added testing popup and sound notification. Also added settings, which was a pain, but I think it works. Actually changed the version number.
#
# Version 0.2, 03 Feb, 2009
#   Prints both private massages and hilights to core buffer. Hilights are in an acceptable format for now, though I will need to get the buffer they came from soon.
#   Private messages works, but give full hostname and lots of other info. Added seperate function to handle splitting and formatting them. (hilightBufferAddPriv)
#   All formatting is done for privmsgs, and a little for hilights also. Still need to add channel/buffer hilight came from.
#
# Version 0.1, 02 Feb, 2009
#   Initial work is started - succesfully prints test string to root buffer
#   Prints every message in every channel to core buffer, unluding full hostname.

import weechat
#try:
#    import pynotify
#    if pynotify.init("hilightbuffer"):
#        weechat.prnt( "", "pynotify was found and properly initialised. Popup notification avaliable." )
#    else:
#        weechat.prnt( "", "There was a problem initializing the pynotify module" )
#except:
#    weechat.prnt( "", "You don't seem to have pynotify installed" )

# Register with weechat
weechat.register( "hilightbuffer", "Brandon Hartshorn", "0.5", "WTFPL", "Listens for hilights on all your channels and writes them to a common hilight buffer", "", "" )

# script options
settings = {
	"buffer_out"			: "hilight",
	"show_hilights"			: "on",
	"show_priv_msg"			: "on",
	"notification_popup"		: "off",
	"notification_sound"		: "off",
	"notification_sound_cmd"	: "None",
}

for option, default_value in settings.iteritems():
	if weechat.config_get_plugin(option) == "":
		weechat.config_set_plugin(option, default_value)

# Make new buffer for hilights if needed
if weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out') ) == "":
    weechat.buffer_new( weechat.config_get_plugin('buffer_out'), "", "" )
    buffername = weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out') )
else: 
    buffername = weechat.buffer_search( "python", weechat.config_get_plugin('buffer_out') )


# Hook privmsg/hilights
weechat.hook_print("", "", "", 1, "hilightBuffer_AddHi")
weechat.hook_signal("weechat_pv", "hilightBuffer_AddPriv")

# Functions
def hilightBuffer_Popup( type, message ):
    """Shows a libnotify/pynotify popup notification for a privmsg/hilight. Still buggy as of 0.4 Feb 23"""
    popup = pynotify.Notification( type, message )
    popup.show()
    return weechat.WEECHAT_RC_OK

def hilightBuffer_AddHi( bufferp, time, tagsn, displayed, ishilight, prefix, message ):
    """Adds hilighted text to hilight buffer"""
    if ishilight == "1" and weechat.config_get_plugin('show_hilights') == "on":
        buffer = weechat.buffer_get_string(bufferp, "name").rsplit(".", 1)[1]
        weechat.prnt( buffername, buffer + " -- " + prefix + "\t"  + message )
        if weechat.config_get_plugin('notification_popup') == "on":
            hilightBuffer_Popup( "Hilight", message )
    return weechat.WEECHAT_RC_OK

def hilightBuffer_AddPriv( signal, message ):
    """Formats and adds private messages to hilight buffer"""
    if weechat.config_get_plugin('show_priv_msg') == "on":
        weechat.prnt( buffername, "privmsg -- " + message )
        if weechat.config_get_plugin('notification_popup') == "on":
            hilightBuffer_Popup( "Privmsg", message )
    return weechat.WEECHAT_RC_OK
