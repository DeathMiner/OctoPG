#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.3.0
#                                |  
#
# @ octopg/settings.py => Fully featured settings for OctoPG games!

import pygame as pg
import octopg.res
import octopg.graphics as g
import octopg.events as e
import octopg.font as font
import octopg.data as data
import octopg.version
import webbrowser
import time

i = octopg.res.load_images({
	"left": "assets/sprites/small_arrow_left.png",
	"right": "assets/sprites/small_arrow_right.png",
	"key_alert": "assets/sprites/key_alert.png",
	"joy_alert": "assets/sprites/joy_alert.png",
	"x360_cntrl_buttons": "assets/sprites/x360_cntrl_buttons.png"
})

s = octopg.res.load_sounds({
	"move": "assets/sounds/ui_move.ogg",
	"select": "assets/sounds/ui_select.ogg",
	"back": "assets/sounds/ui_back.ogg"
})

# Sprite definitions for the x360 buttons icons
x360_cntrl_buttons = {
	"a": [0, 0, 11, 11],
	"b": [11, 0, 11, 11],
	"back": [22, 0, 11, 11],
	"dpad_down": [33, 0, 22, 11],
	"dpad_left": [55, 0, 22, 11],
	"dpad_right": [0, 11, 22, 11],
	"dpad_up": [22, 11, 22, 11],
	"lb": [44, 11, 19, 11],
	"lstick_btn": [0, 22, 33, 11],
	"lstick_down": [33, 22, 33, 11],
	"lstick_left": [0, 33, 33, 11],
	"lstick_right": [33, 33, 33, 11],
	"lstick_up": [0, 44, 33, 11],
	"lt": [33, 44, 19, 11],
	"rb": [52, 44, 19, 11],
	"rstick_btn": [0, 55, 33, 11],
	"rstick_down": [33, 55, 33, 11],
	"rstick_left": [0, 66, 33, 11],
	"rstick_right": [33, 66, 33, 11],
	"rstick_up": [77, 0, 33, 11],
	"rt": [63, 11, 19, 11],
	"start": [82, 11, 11, 11],
	"x": [93, 11, 11, 11],
	"y": [66, 22, 11, 11]
}

CURRENT = {
	'part': 'MAIN',
	'item': 0
}

def graphics_on_open():
	global options

	# Get all selectors
	for item in options['GRAPHICS']['items']:
		if item['type'] == "selector":

			# populate values if needed
			if item['key'] == "resolution":

				# Delete old resolutions
				item['values'] = []

				# Load available resolutions for current aspect ratio
				for resolution in g.RESOLUTIONS[g.current_config['aspect_ratio']]:
					item['values'].append({
						'name':str(resolution[0])+"x"+str(resolution[1]),
						'value':resolution
					})

			# Get selected value in configuration
			for index, value in enumerate(item['values']):
				if value['value'] == g.current_config[item['key']]:
					item['selected'] = index

					break
			else:
				item['selected'] = 0

def graphics_ar_on_change(new_value):
	global options

	# Get all selectors
	for item in options['GRAPHICS']['items']:
		if item['type'] == "selector" and item['key'] == "resolution":

			# Delete old resolutions
			item['values'] = []

			# Load available resolutions for current aspect ratio
			for resolution in g.RESOLUTIONS[new_value]:
				item['values'].append({
					'name':str(resolution[0])+"x"+str(resolution[1]),
					'value':resolution
				})

			# Get selected value in configuration
			for index, value in enumerate(item['values']):
				if value['value'] == g.current_config[item['key']]:
					item['selected'] = index
	
					break
			else:
				item['selected'] = 0

def graphics_apply_config():
	global options

	new_config = g.current_config

	# Get values of all items
	for item in options['GRAPHICS']['items']:
		if item['type'] == "selector":
			new_config[item['key']] = item['values'][item['selected']]['value']

	# Save config
	data.d['config']['graphics'] = new_config
	g.apply_config(new_config)


def misc_website():
	webbrowser.open("https://github.com/DeathMiner/OctoPG")

def select_key(player, button):
	# Show key alert
	g.screen.blit(i['key_alert'], [12, 73])

	# Show title with button name
	f = font.render("Set "+button+" button", [255, 255, 255], [0, 0, 0])
	f_size = f.get_size()
	g.screen.blit(f, [g.screen_size[0]/2-f_size[0]/2, 80])

	# Update screen
	g.flip()

	# Some vars for timer
	start_time = time.time()
	total = 5
	diff = 0

	# Wait 5 secs, while listenning to events
	while diff <= total:

		# Show timer
		f = font.render(str(total-int(diff))+" seconds left", [255, 255, 255], [0, 0, 0])
		f_size = f.get_size()
		g.screen.blit(f, [g.screen_size[0]/2-f_size[0]/2, 124])

		# Update screen
		g.flip()

		# Calculate timer difference
		diff = (time.time() - start_time)

		# Get all events
		e.update()
		for event in e.retrieve_events():

			# A key was pressed, save it !
			if event.type == pg.KEYDOWN:

				# Stop loop
				diff = total+1

				# Save key number in data
				data.d['config']['controls']['p'+player]['keyboard'][button] = event.key
				print("CONFIG: New "+button+" key for p"+player+": "+str(event.key))

				# Apply config in event module
				e.apply_config(data.d['config']['controls'])

def select_joy(player, button):
	# Show key alert
	g.screen.blit(i['joy_alert'], [12, 73])

	# Show title with button name
	f = font.render("Set "+button+" button", [255, 255, 255], [0, 0, 0])
	f_size = f.get_size()
	g.screen.blit(f, [g.screen_size[0]/2-f_size[0]/2, 80])

	# Update screen
	g.flip()

	# Some vars for timer
	start_time = time.time()
	total = 5
	diff = 0

	# Wait 5 secs, while listenning to events
	while diff <= total:

		# Show timer
		f = font.render(str(total-int(diff))+" seconds left", [255, 255, 255], [0, 0, 0])
		f_size = f.get_size()
		g.screen.blit(f, [g.screen_size[0]/2-f_size[0]/2, 124])

		# Update screen
		g.flip()

		# Calculate timer difference
		diff = (time.time() - start_time)

		# Get all events
		e.update()
		for event in e.retrieve_events():

			# A key was pressed, save it !
			if event.type == e.X360_CNTRL_DOWN and event.joy == e.CONFIG['p'+player]['controller']:
				print(event.joy, e.CONFIG['p'+player]['controller'])

				# Stop loop
				diff = total+1

				# Save key number in data
				data.d['config']['controls']['p'+player]['joystick'][button] = event.button
				print("CONFIG: New "+button+" joy for p"+player+": "+event.button)

				# Apply config in event module
				e.apply_config(data.d['config']['controls'])

def open_p1_settings():
	open_player_settings("1")

def open_p2_settings():
	open_player_settings("2")

def open_player_settings(player):
	items = [
		{
			'name':'Keyboard-Only',
			'value': -1
		}
	]
	selected = 0

	oposite_player = "2"
	if player == "2":
		oposite_player = "1"

	for joy in e.joys:

		if joy['id'] != e.CONFIG['p'+oposite_player]['controller']:
			items.append({
				'name': joy['name'],
				'value': joy['id']
			})

			if joy['id'] == e.CONFIG['p'+player]['controller']:
				selected = len(items)-1

	for item in options['P'+player+'_CONTROLS']['items']:
		if item['type'] == "selector":
			item['values'] = items
			item['selected'] = selected

			break

def p1_controller_selector_on_change(value):
	controller_selector_on_change("1", value)

def p2_controller_selector_on_change(value):
	controller_selector_on_change("2", value)

def controller_selector_on_change(player, value):

	if value != e.CONFIG['p'+player]['controller']:
		data.d['config']['controls']['p'+player]['controller'] = value

		e.apply_config(data.d['config']['controls'])

		print("Setting "+str(value)+" controller for p"+player+"...")


options = {
	'MAIN': {
		'back': False,
		"title": "Settings!",
		'items': [
			{
				'type': 'link',
				'name': 'Player 1 Settings',
				'goto': 'P1_CONTROLS'
			},
			{
				'type': 'link',
				'name': 'Player 2 Settings',
				'goto': 'P2_CONTROLS'
			},
			{
				'type': 'link',
				'name': 'Video settings',
				'goto': 'GRAPHICS'
			},
			{
				'type': 'link',
				'name': 'Audio settings',
				'goto': 'SOUNDS'
			},
			{
				'type': 'link',
				'name': 'Other',
				'goto': 'MISC'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': '#CLOSE#'
			}
		]
	},
	'P1_CONTROLS':{
		'back': "MAIN",
		"title": "Player 1 Settings",
		"on_open": open_p1_settings,
		'items': [
			{
				"type": "text",
				"name": "Choose controller:"
			},
			{
				'type': 'selector',
				'name': '',
				'values': [], # Generated after controller initialization
				'selected': 0,
				'on_change': p1_controller_selector_on_change
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Configure keyboard',
				'goto': 'P1_KEYS'
			},
			{
				'type': 'link',
				'name': 'Configure controller',
				'goto': 'P1_JOYS'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'MAIN'
			}
		]
	},
	'P1_KEYS': {
		'back': "P1_CONTROLS",
		"title": "Player 1 Keyboard",
		'items': [
			{
				'type': 'keyselector',
				'button': 'left',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'right',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'up',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'down',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'select',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'start',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'a',
				'player': '1'
			},
			{
				'type': 'keyselector',
				'button': 'b',
				'player': '1'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'P1_CONTROLS'
			}
		]
	},
	'P1_JOYS': {
		'back': "P1_CONTROLS",
		"title": "Player 1 Controller",
		"items": [
			{
				'type': 'joyselector',
				'button': 'left',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'right',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'up',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'down',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'select',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'start',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'a',
				'player': '1'
			},
			{
				'type': 'joyselector',
				'button': 'b',
				'player': '1'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'P1_CONTROLS'
			}
		]
	},
	'P2_CONTROLS':{
		'back': "MAIN",
		"title": "Player 2 Settings",
		"on_open": open_p2_settings,
		'items': [
			{
				"type": "text",
				"name": "Choose controller:"
			},
			{
				'type': 'selector',
				'name': '',
				'values': [], # Generated after controller initialization
				'selected': 0,
				'on_change': p2_controller_selector_on_change
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Configure keyboard',
				'goto': 'P2_KEYS'
			},
			{
				'type': 'link',
				'name': 'Configure controller',
				'goto': 'P2_JOYS'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'MAIN'
			}
		]
	},
	'P2_KEYS': {
		'back': "P2_CONTROLS",
		"title": "Player 2 Keyboard",
		'items': [
			{
				'type': 'keyselector',
				'button': 'left',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'right',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'up',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'down',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'select',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'start',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'a',
				'player': '2'
			},
			{
				'type': 'keyselector',
				'button': 'b',
				'player': '2'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'P2_CONTROLS'
			}
		]
	},
	"P2_JOYS":{
		'back': "P2_CONTROLS",
		"title": "Player 2 Controller",
		"items": [
			{
				'type': 'joyselector',
				'button': 'left',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'right',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'up',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'down',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'select',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'start',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'a',
				'player': '2'
			},
			{
				'type': 'joyselector',
				'button': 'b',
				'player': '2'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'P2_CONTROLS'
			}
		]
	},
	'GRAPHICS': {
		'back': "MAIN",
		"title": "Video Settings",
		"on_open": graphics_on_open,
		'items': [
			{
				'type': 'selector',
				'name': 'Aspect ratio',
				'values': [], # Generated at start
				'selected': 0,
				'key': 'aspect_ratio',
				'on_change': graphics_ar_on_change
			},
			{
				'type': 'selector',
				'name': 'Resolution',
				'values': [], # Generated depending on the current selected aspect_ratio
				'selected': 0,
				'key': 'resolution'
			},
			{
				'type': 'selector',
				'name': 'Fullscreen',
				'values': [
					{
						'name':'Disabled',
						'value': False
					},
					{
						'name':'Enabled',
						'value': True
					}
				],
				'selected': 0,
				'key': 'fullscreen'
			},
			{
				'type': 'selector',
				'name': 'Effects',
				'values': [
					{
						'name':'Disabled',
						'value':0
					},
					{
						'name':'Low',
						'value':1
					},
					{
						'name':'Medium',
						'value':2
					},
					{
						'name':'High',
						'value':3
					}
				],
				'selected': 0,
				'key': 'post_effects'
			},
			{
				'type': 'selector',
				'name': 'TV Mode',
				'values': [
					{
						'name':'Disabled',
						'value':False
					},
					{
						'name':'Enabled',
						'value':True
					}
				],
				'selected': 0,
				'key': 'tv'
			},
			{
				'type': 'selector',
				'name': 'FPS Blocker',
				'values': [
					{
						'name':'Disabled',
						'value':0
					},
					{
						'name':'30 FPS',
						'value':30
					},
					{
						'name':'60 FPS',
						'value':60
					},
					{
						'name':'120 FPS',
						'value':120
					}
				],
				'selected': 0,
				'key': 'fps_blocker'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'button',
				'name': 'Apply',
				'function': graphics_apply_config
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'MAIN'
			}
		]
	},
	'SOUNDS': {
		'back': "MAIN",
		"title": "Audio Settings",
		'items': [
			{
				"type":"text",
				"name": "OctoPG has no Audio settings."
			},
			{
				"type":"text",
				"name": "to add custom audio"
			},
			{
				"type":"text",
				"name": "settings to your game,"
			},
			{
				"type":"text",
				"name": "Please create a custom OctoPG!"
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'MAIN'
			}
		]
	},
	'MISC': {
		'back': "MAIN",
		"title": "About OctoPG!",
		'items': [
			{
				'type': 'text',
				'name': 'Version: '+octopg.version.octopg_ver
			},
			{
				'type': 'text',
				'name': 'By: Death_Miner'
			},
			{
				'type': 'text',
				'name': 'License: MIT'
			},
			{
				'type': 'separator'
			},
			{
				'type': 'button',
				'name': 'Official website',
				'function': misc_website
			},
			{
				'type': 'separator'
			},
			{
				'type': 'link',
				'name': 'Back',
				'goto': 'MAIN'
			}
		]
	}
}

keynames = {
	pg.K_BACKSPACE: "BACKSPACE",
	pg.K_TAB: "TAB",
	pg.K_CLEAR: "CLEAR",
	pg.K_RETURN: "RETURN",
	pg.K_PAUSE: "PAUSE",
	pg.K_ESCAPE: "ESCAPE",
	pg.K_SPACE: "SPACE",
	pg.K_EXCLAIM: "EXCLAIM",
	pg.K_QUOTEDBL: "QUOTEDBL",
	pg.K_HASH: "HASH",
	pg.K_DOLLAR: "DOLLAR",
	pg.K_AMPERSAND: "AMPERSAND",
	pg.K_QUOTE: "QUOTE",
	pg.K_LEFTPAREN: "LEFTPAREN",
	pg.K_RIGHTPAREN: "RIGHTPAREN",
	pg.K_ASTERISK: "ASTERISK",
	pg.K_PLUS: "PLUS",
	pg.K_COMMA: "COMMA",
	pg.K_MINUS: "MINUS",
	pg.K_PERIOD: "PERIOD",
	pg.K_SLASH: "SLASH",
	pg.K_0: "0",
	pg.K_1: "1",
	pg.K_2: "2",
	pg.K_3: "3",
	pg.K_4: "4",
	pg.K_5: "5",
	pg.K_6: "6",
	pg.K_7: "7",
	pg.K_8: "8",
	pg.K_9: "9",
	pg.K_COLON: "COLON",
	pg.K_SEMICOLON: "SEMICOLON",
	pg.K_LESS: "LESS",
	pg.K_EQUALS: "EQUALS",
	pg.K_GREATER: "GREATER",
	pg.K_QUESTION: "QUESTION",
	pg.K_AT: "AT",
	pg.K_LEFTBRACKET: "LEFTBRACKET",
	pg.K_BACKSLASH: "BACKSLASH",
	pg.K_RIGHTBRACKET: "RIGHTBRACKET",
	pg.K_CARET: "CARET",
	pg.K_UNDERSCORE: "UNDERSCORE",
	pg.K_BACKQUOTE: "BACKQUOTE",
	pg.K_a: "a",
	pg.K_b: "b",
	pg.K_c: "c",
	pg.K_d: "d",
	pg.K_e: "e",
	pg.K_f: "f",
	pg.K_g: "g",
	pg.K_h: "h",
	pg.K_i: "i",
	pg.K_j: "j",
	pg.K_k: "k",
	pg.K_l: "l",
	pg.K_m: "m",
	pg.K_n: "n",
	pg.K_o: "o",
	pg.K_p: "p",
	pg.K_q: "q",
	pg.K_r: "r",
	pg.K_s: "s",
	pg.K_t: "t",
	pg.K_u: "u",
	pg.K_v: "v",
	pg.K_w: "w",
	pg.K_x: "x",
	pg.K_y: "y",
	pg.K_z: "z",
	pg.K_DELETE: "DELETE",
	pg.K_KP0: "KP0",
	pg.K_KP1: "KP1",
	pg.K_KP2: "KP2",
	pg.K_KP3: "KP3",
	pg.K_KP4: "KP4",
	pg.K_KP5: "KP5",
	pg.K_KP6: "KP6",
	pg.K_KP7: "KP7",
	pg.K_KP8: "KP8",
	pg.K_KP9: "KP9",
	pg.K_KP_PERIOD: "KP_PERIOD",
	pg.K_KP_DIVIDE: "KP_DIVIDE",
	pg.K_KP_MULTIPLY: "KP_MULTIPLY",
	pg.K_KP_MINUS: "KP_MINUS",
	pg.K_KP_PLUS: "KP_PLUS",
	pg.K_KP_ENTER: "KP_ENTER",
	pg.K_KP_EQUALS: "KP_EQUALS",
	pg.K_UP: "UP",
	pg.K_DOWN: "DOWN",
	pg.K_RIGHT: "RIGHT",
	pg.K_LEFT: "LEFT",
	pg.K_INSERT: "INSERT",
	pg.K_HOME: "HOME",
	pg.K_END: "END",
	pg.K_PAGEUP: "PAGEUP",
	pg.K_PAGEDOWN: "PAGEDOWN",
	pg.K_F1: "F1",
	pg.K_F2: "F2",
	pg.K_F3: "F3",
	pg.K_F4: "F4",
	pg.K_F5: "F5",
	pg.K_F6: "F6",
	pg.K_F7: "F7",
	pg.K_F8: "F8",
	pg.K_F9: "F9",
	pg.K_F10: "F10",
	pg.K_F11: "F11",
	pg.K_F12: "F12",
	pg.K_F13: "F13",
	pg.K_F14: "F14",
	pg.K_F15: "F15",
	pg.K_NUMLOCK: "NUMLOCK",
	pg.K_CAPSLOCK: "CAPSLOCK",
	pg.K_SCROLLOCK: "SCROLLOCK",
	pg.K_RSHIFT: "RSHIFT",
	pg.K_LSHIFT: "LSHIFT",
	pg.K_RCTRL: "RCTRL",
	pg.K_LCTRL: "LCTRL",
	pg.K_RALT: "RALT",
	pg.K_LALT: "LALT",
	pg.K_RMETA: "RMETA",
	pg.K_LMETA: "LMETA",
	pg.K_LSUPER: "LSUPER",
	pg.K_RSUPER: "RSUPER",
	pg.K_MODE: "MODE",
	pg.K_HELP: "HELP",
	pg.K_PRINT: "PRINT",
	pg.K_SYSREQ: "SYSREQ",
	pg.K_BREAK: "BREAK",
	pg.K_MENU: "MENU",
	pg.K_POWER: "POWER",
	pg.K_EURO: "EURO"
}

arrow_pos = 1 # Menu arrow pos

def init():

	# List all aspect ratios
	for key in g.RESOLUTIONS.keys():
		options['GRAPHICS']['items'][0]['values'].append({
			'name':key,
			'value':key
		})

		if key == g.current_config['aspect_ratio']:
			options['GRAPHICS']['items'][0]['selected'] = len(options['GRAPHICS']['items'][0]['values'])-1

def loop(onclose):
	global CURRENT, options, keynames, arrow_pos

	# Useful vars
	current_part = options[CURRENT['part']]
	current_item = current_part['items'][CURRENT['item']]

	# Encountered keys for matching duplicates
	encountered_keys = []

	# skip item if item is separator or text (useful for default selected seps)
	while current_item['type'] == "separator" or current_item['type'] == "text":
		CURRENT['item'] += 1
		if CURRENT['item'] >= len(current_part['items']):
			CURRENT['item'] = 0

		current_item = current_part['items'][CURRENT['item']]



	# Event
	for event in e.retrieve_events():

		# Controller button
		if event.type == e.CNTLR_KEYDOWN:

			# B goes back
			if event.btn_global == e.BTN_B:
				if current_part['back'] != False:
					CURRENT['part'] = current_part['back']

					# Do part init if needed
					if 'on_open' in options[CURRENT['part']]:
						options[CURRENT['part']]['on_open']()

					# Get part (updated by init)
					current_part = options[CURRENT['part']]
				else:
					CURRENT['part'] = "MAIN"
					onclose()
				CURRENT['item'] = 0

				s['back'].play()

			# Select next option
			elif event.btn_global == e.BTN_DOWN:

				# Start scroll + avoid separators
				done_1_time = False
				while current_item['type'] == "separator" or current_item['type'] == "text" or not done_1_time:

					# Set we done scroll 1 time
					done_1_time = True

					# Update current selected item
					CURRENT['item'] += 1
					if CURRENT['item'] >= len(current_part['items']):
						CURRENT['item'] = 0
					current_item = current_part['items'][CURRENT['item']]

				# Reset arrow animation :D
				arrow_pos = 0

				s['move'].play()

			# Select prev option
			elif event.btn_global == e.BTN_UP:

				# Start scroll + avoid separators
				done_1_time = False
				while current_item['type'] == "separator" or current_item['type'] == "text" or not done_1_time:

					# Set we done scroll 1 time
					done_1_time = True

					# Update current selected item
					CURRENT['item'] -= 1
					if CURRENT['item'] < 0:
						CURRENT['item'] = len(current_part['items'])-1
					current_item = current_part['items'][CURRENT['item']]

				# Reset arrow animation :D
				arrow_pos = 0

				s['move'].play()

			# Current option selected
			elif event.btn_global == e.BTN_A:
				if current_item['type'] == "link":
					old_back = current_part['back']

					if current_item['goto'] == "#CLOSE#":
						CURRENT['part'] = "MAIN"
						onclose()
					else:
						CURRENT['part'] = current_item['goto']

						# Do part init if needed
						if 'on_open' in options[CURRENT['part']]:
							options[CURRENT['part']]['on_open']()

						# Get part (updated by init)
						current_part = options[CURRENT['part']]

					CURRENT['item'] = 0

					if old_back == CURRENT['part']:
						s['back'].play()
					else:
						s['select'].play()

				elif current_item['type'] == "button":
					current_item['function']()

					s['select'].play()

				elif current_item['type'] == "keyselector":

					s['select'].play()
					select_key(current_item['player'], current_item['button'])

					s['select'].play()

				elif current_item['type'] == "joyselector":

					s['select'].play()
					select_joy(current_item['player'], current_item['button'])

					s['select'].play()

			# Left value on selectors
			elif event.btn_global == e.BTN_LEFT:
				if current_item['type'] == "selector":
					# Update current selected item
					current_item['selected'] -= 1
					if current_item['selected'] < 0:
						current_item['selected'] = len(current_item['values'])-1

					# Do on_change event if needed
					if 'on_change' in current_item:
						current_item['on_change'](current_item['values'][current_item['selected']]['value'])

					s['move'].play()

			# Right value on selectors
			elif event.btn_global == e.BTN_RIGHT:
				if current_item['type'] == "selector":
					# Update current selected item
					current_item['selected'] += 1
					if current_item['selected'] >= len(current_item['values']):
						current_item['selected'] = 0

					# Do on_change event if needed
					if 'on_change' in current_item:
						current_item['on_change'](current_item['values'][current_item['selected']]['value'])

					s['move'].play()


	# Show current page title centered
	title = font.render(current_part['title'], [255, 255, 255], [0, 0, 0])
	g.screen.blit(title, [g.screen_size[0]/2-title.get_size()[0]/2, 8])

	# Offsets
	offset = 39
	margin = 9

	# Iterating through all items
	for index, item in enumerate(current_part['items']):

		# Link = goes to a new page
		if item['type'] == "link" or item['type'] == "button" or item['type'] == "text":

			# Link name
			f = font.render(item['name'], [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [236-f_size[0], offset])

			# Arrow
			if CURRENT['item'] == index:
				g.screen.blit(i['right'], [int(241+5*arrow_pos), offset+3])

			# Set next item position
			offset += f_size[1]+margin

		# A blank separator
		elif item['type'] == "separator":

			# Draw a little line
			f = font.render("-", [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [236-f_size[0], offset])

			# Set next item position
			offset += f_size[1]+margin

		# Used to selct a key
		# This item is on the left with a label
		elif item['type'] == "keyselector":
			# BTN NAME
			f = font.render(item['button'], [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [16, offset])

			# KEY NAME
			key = e.CONFIG['p'+item['player']]['keyboard'][item['button']]
			if key in keynames:
				name = keynames[key]
			else:
				name = "[?]"

			# Set background
			background = [0, 0, 0]
			if key in encountered_keys:
				background = [255, 0, 0]
			else:
				encountered_keys.append(key)

			f = font.render(name, [255, 255, 255], background)
			f_size = f.get_size()
			g.screen.blit(f, [236-f_size[0], offset])

			# Cursor
			if CURRENT['item'] == index:
				g.screen.blit(i['right'], [int(241+5*arrow_pos), offset+3])

			offset += f_size[1]+margin

		# Joystick key selector
		# On the right, next to keyselector items
		elif item['type'] == "joyselector":
			# BTN NAME
			f = font.render(item['button'], [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [16, offset])

			# KEY NAME
			name = e.CONFIG['p'+item['player']]['joystick'][item['button']]
			if name in x360_cntrl_buttons:
				sprite = octopg.util.crop_surf(i['x360_cntrl_buttons'], x360_cntrl_buttons[name])
				pos = [236-x360_cntrl_buttons[name][2], offset]
			else:
				sprite = font.render("[?]", [255, 255, 255], [0, 0, 0])
				f_size = sprite.get_size()
				pos = [236-f_size[0], offset]

			g.screen.blit(sprite, pos)

			# Cursor
			if CURRENT['item'] == index:
				g.screen.blit(i['right'], [int(241+5*arrow_pos), offset+3])

			offset += f_size[1]+margin

		# A selector = choose in a set of values
		elif item['type'] == "selector":
			f = font.render(item['name'], [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [16, offset])

			f = font.render(item['values'][item['selected']]['name'], [255, 255, 255], [0, 0, 0])
			f_size = f.get_size()
			g.screen.blit(f, [236-f_size[0], offset])

			if CURRENT['item'] == index:
				g.screen.blit(i['right'], [int(241+5*arrow_pos), offset+3])
				g.screen.blit(i['left'], [int(226-f_size[0]-5*arrow_pos), offset+3])

			offset += f_size[1]+margin

		# Arrow animationl
		if CURRENT['item'] == index:
			arrow_pos += 0.02
			if arrow_pos >= 1:
				arrow_pos = 0

# TODO:
# commenting
# cleaning up code
# mark duplicates in keyboard/controller configuration
# a better ui?
# customizable?
# disallow controller configuration when no controller selected