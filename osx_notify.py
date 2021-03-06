# https://github.com/sindresorhus/weechat-notification-center
# Requires `pip install pync`

import os
import weechat
from pync import Notifier
from time import sleep, strftime, localtime

SCRIPT_NAME = 'osx_notify'
SCRIPT_AUTHOR = 'Sindre Sorhus <sindresorhus@gmail.com>'
SCRIPT_VERSION = '1.2.1'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'Pass highlights and private messages to the OS X 10.8+ Notification Center'
WEECHAT_ICON = os.path.expanduser('~/.weechat/weechat.png')

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE, SCRIPT_DESC, '', '')

DEFAULT_OPTIONS = {
	'show_highlights': 'on',
	'show_private_message': 'on',
	'show_message_text': 'on',
	'sound': 'off',
	'sound_name': 'Pong',
}

for key, val in DEFAULT_OPTIONS.items():
	if not weechat.config_is_set_plugin(key):
		weechat.config_set_plugin(key, val)

weechat.hook_print('', 'irc_privmsg', '', 1, 'notify', '')

def notify(data, buffer, date, tags, displayed, highlight, prefix, message):
	# ignore if it's yourself
	own_nick = weechat.buffer_get_string(buffer, 'localvar_nick')
	if prefix == own_nick or prefix == ('@%s' % own_nick):
		return weechat.WEECHAT_RC_OK

	# passing `None` or `''` still plays the default sound so we pass a lambda instead
	sound = weechat.config_get_plugin('sound_name') if weechat.config_get_plugin('sound') == 'on' else lambda:_
	channel = weechat.buffer_get_string(buffer, 'localvar_channel')
        currentTime = strftime("%H:%M:%S", localtime())
	#If show highlights are on, and this is one of our weechat configured hightlights...
	if weechat.config_get_plugin('show_highlights') == 'on' and int(highlight):
		if weechat.config_get_plugin('show_message_text') == 'on':
                        #notify us of the message, and what channel with a sound
			Notifier.notify(message, title='%s %s' % (prefix, channel), sound=sound, appIcon=WEECHAT_ICON)
		else:
                        #Else, notify us of what channel and who it wat
			Notifier.notify('In %s by %s' % (channel, prefix), title='Highlighted Message', sound=sound, appIcon=WEECHAT_ICON)
        #Else if highlights are on, and this is an important channel...
	elif weechat.config_get_plugin('show_highlights') == 'on' and channel == "#importantchannel":
                #get the channel name and notify us without displaying channel name
		channel = weechat.buffer_get_string(buffer, 'localvar_channel')
		Notifier.notify("Message in important channel", sound=sound, appIcon=WEECHAT_ICON)
	#Private Message Block
	elif weechat.config_get_plugin('show_private_message') == 'on' and 'notify_private' in tags:
#		if weechat.config_get_plugin('show_message_text') == 'on':
#			Notifier.notify(message, title='%s [private]' % prefix, sound=sound, appIcon=WEECHAT_ICON)
#		else:
# Showing the time annoyingly causes new notifications for every PM. If a notification is identical to the last one in content,
# it won't open an additional one. Gonna have to take time out for now.
#                concatenatePMMessage = 'From %s at '+str(currentTime)
                concatenatePMMessage = 'From %s'
		Notifier.notify(concatenatePMMessage % prefix, title='Private Message', sound=sound, appIcon=WEECHAT_ICON)
	return weechat.WEECHAT_RC_OK
