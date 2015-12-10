#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.3.0
#                                |  
#
# @ octopg/events.py => This file catches events like buttons presses

import pygame as pg
import sys
import octopg.data as data
import copy

# Virtual controller events
CNTLR_KEYDOWN = 2000
CNTLR_KEYUP = 2001

# Xbox360 controller event
X360_CNTRL_DOWN = 2026
X360_CNTRL_UP = 2027

# Buttons IDs for testing
# Global buttons, for both p1 and p2
BTN_LEFT = 2002
BTN_UP = 2003
BTN_DOWN = 2004
BTN_RIGHT = 2005
BTN_SELECT = 2006
BTN_START = 2007
BTN_B = 2008
BTN_A = 2009

# P1 Buttons
P1_BTN_LEFT = 2010
P1_BTN_UP = 2011
P1_BTN_DOWN = 2012
P1_BTN_RIGHT = 2013
P1_BTN_SELECT = 2014
P1_BTN_START = 2015
P1_BTN_B = 2016
P1_BTN_A = 2017

# P2 Buttons
P2_BTN_LEFT = 2018
P2_BTN_UP = 2019
P2_BTN_DOWN = 2020
P2_BTN_RIGHT = 2021
P2_BTN_SELECT = 2022
P2_BTN_START = 2023
P2_BTN_B = 2024
P2_BTN_A = 2025

# Current configuration & default
CONFIG = {
	"p1": {
		"controller": -1,
		"keyboard": {
			"left": pg.K_a,
			"up": pg.K_w,
			"down": pg.K_s,
			"right": pg.K_d,
			"select": pg.K_g,
			"start": pg.K_h,
			"b": pg.K_k,
			"a": pg.K_SEMICOLON
		},
		"joystick": {
			"left": -1,
			"up": -1,
			"down": -1,
			"right": -1,
			"select": -1,
			"start": -1,
			"b": -1,
			"a": -1
		}
	},
	"p2": {
		"controller": -1,
		"keyboard": {
			"left": -1,
			"up": -1,
			"down": -1,
			"right": -1,
			"select": -1,
			"start": -1,
			"b": -1,
			"a": -1
		},
		"joystick": {
			"left": -1,
			"up": -1,
			"down": -1,
			"right": -1,
			"select": -1,
			"start": -1,
			"b": -1,
			"a": -1
		}
	}
}

BTN_STATES = {
	'PRESSED':{
		P1_BTN_LEFT: False,
		P1_BTN_UP: False,
		P1_BTN_DOWN: False,
		P1_BTN_RIGHT: False,
		P1_BTN_SELECT: False,
		P1_BTN_START: False,
		P1_BTN_B: False,
		P1_BTN_A: False,
		P2_BTN_LEFT: False,
		P2_BTN_UP: False,
		P2_BTN_DOWN: False,
		P2_BTN_RIGHT: False,
		P2_BTN_SELECT: False,
		P2_BTN_START: False,
		P2_BTN_B: False,
		P2_BTN_A: False
	}
}

x360_cntrl_requirements = {
	"axes": 5,
	"buttons": 10,
	"hats": 1
}

x360_cntrl_map_reverse = {
	"button":{
		0: "a",
		1: "b",
		2: "x",
		3: "y",
		4: "lb",
		5: "rb",
		6: "back",
		7: "start",
		8: "lstick_btn",
		9: "rstick_btn"
	},
	"axis":{
		0: {
			-1: "lstick_left",
			0: "NONE",
			1: "lstick_right",
			"current": "NONE"
		},
		1: {
			-1: "lstick_up",
			0: "NONE",
			1: "lstick_down",
			"current": "NONE"
		},
		2: {
			-1: "rt",
			0: "NONE",
			1: "lt",
			"current": "NONE"
		},
		3: {
			-1: "rstick_up",
			0: "NONE",
			1: "rstick_down",
			"current": "NONE"
		},
		4: {
			-1: "rstick_left",
			0: "NONE",
			1: "rstick_right",
			"current": "NONE"
		}
	},
	"hat":{
		0: {
			0: {
				-1: "dpad_left",
				0: "NONE",
				1: "dpad_right",
				"current": "NONE"
			},
			1: {
				-1: "dpad_down",
				0: "NONE",
				1: "dpad_up",
				"current": "NONE"
			}
		}
	}
}

event_list = []

# joys = Joys that can be used
# joysticks = Current detected joysticks and their instances
joys = []
joysticks = []



def init():
	global joysticks, joys
	pg.joystick.init()
	joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]
	joys = []

	print("- "+str(len(joysticks))+" controllers found.")

	for index, joy in enumerate(joysticks):
		name = joy.get_name();

		print("  => "+name)

		joy.init()

		# Save joy only if it is a legit x360 controller
		if joy.get_numaxes() == 5 and joy.get_numbuttons() == 10 and joy.get_numhats() == 1:
			joys.append({
					'name': name,
					'id': index
				})


def update():
	for event in pg.event.get():
		event_list.append(event)

		if event.type == pg.QUIT:
			close()

		elif event.type == pg.KEYDOWN:

			# Button pressed
			if (event.key == CONFIG['p1']['keyboard']['up'] or 
			   event.key == CONFIG['p1']['keyboard']['left'] or 
			   event.key == CONFIG['p1']['keyboard']['down'] or 
			   event.key == CONFIG['p1']['keyboard']['right'] or 
			   event.key == CONFIG['p1']['keyboard']['select'] or 
			   event.key == CONFIG['p1']['keyboard']['start'] or 
			   event.key == CONFIG['p1']['keyboard']['b'] or 
			   event.key == CONFIG['p1']['keyboard']['a'] or 
			   event.key == CONFIG['p2']['keyboard']['up'] or 
			   event.key == CONFIG['p2']['keyboard']['left'] or 
			   event.key == CONFIG['p2']['keyboard']['down'] or 
			   event.key == CONFIG['p2']['keyboard']['right'] or 
			   event.key == CONFIG['p2']['keyboard']['select'] or 
			   event.key == CONFIG['p2']['keyboard']['start'] or 
			   event.key == CONFIG['p2']['keyboard']['b'] or 
			   event.key == CONFIG['p2']['keyboard']['a']):

				# Get pressed btn [player_btn, global_btn]
				btn = get_used_button_from_key(event.key)

				# Create a new event
				new_event = pg.event.Event(CNTLR_KEYDOWN, {
					'source': event,
					'btn_global': btn[1],
					'btn': btn[0]
				})

				# Save the event
				event_list.append(new_event)

				# Set btn pressed state
				BTN_STATES['PRESSED'][btn[0]] = True

		elif event.type == pg.KEYUP:
			if (event.key == CONFIG['p1']['keyboard']['up'] or 
			   event.key == CONFIG['p1']['keyboard']['left'] or 
			   event.key == CONFIG['p1']['keyboard']['down'] or 
			   event.key == CONFIG['p1']['keyboard']['right'] or 
			   event.key == CONFIG['p1']['keyboard']['select'] or 
			   event.key == CONFIG['p1']['keyboard']['start'] or 
			   event.key == CONFIG['p1']['keyboard']['b'] or 
			   event.key == CONFIG['p1']['keyboard']['a'] or 
			   event.key == CONFIG['p2']['keyboard']['up'] or 
			   event.key == CONFIG['p2']['keyboard']['left'] or 
			   event.key == CONFIG['p2']['keyboard']['down'] or 
			   event.key == CONFIG['p2']['keyboard']['right'] or 
			   event.key == CONFIG['p2']['keyboard']['select'] or 
			   event.key == CONFIG['p2']['keyboard']['start'] or 
			   event.key == CONFIG['p2']['keyboard']['b'] or 
			   event.key == CONFIG['p2']['keyboard']['a']):

				# Get pressed btn [player_btn, global_btn]
				btn = get_used_button_from_key(event.key)

				# Create a new event
				new_event = pg.event.Event(CNTLR_KEYUP, {
					'source': event,
					'btn_global': btn[1],
					'btn': btn[0]
				})

				# Save the event
				event_list.append(new_event)

				# Remove btn pressed state
				BTN_STATES['PRESSED'][btn[0]] = False

		elif event.type == pg.JOYAXISMOTION:

			# Listen only to registered controllers to avoid duplicates
			if event.joy == CONFIG['p1']['controller'] or event.joy == CONFIG['p2']['controller']:

				# Skip float values, 0.5 sensibility
				true_value = 0
				if event.value < -0.5:
					true_value = -1
				elif event.value > 0.5:
					true_value = 1

				# Get current button and last button according to map
				button = x360_cntrl_map_reverse['axis'][event.axis][true_value]
				last_button = x360_cntrl_map_reverse['axis'][event.axis]['current']

				# Trigger event if only the last button wasn't the same
				if last_button != button and last_button != "NONE":
					trigger_joy_up_event(last_button, event)

				# Skip NONE shitload of events
				if button != "NONE":
					trigger_joy_down_event(button, event)

				# Save current button
				x360_cntrl_map_reverse['axis'][event.axis]['current'] = button

		elif event.type == pg.JOYHATMOTION:

			# Listen only to registered controllers to avoid duplicates
			if event.joy == CONFIG['p1']['controller'] or event.joy == CONFIG['p2']['controller']:

				# For both axes of the hat
				for i in range(2):

					# Get current button and last button according to map
					button = x360_cntrl_map_reverse['hat'][event.hat][i][event.value[i]]
					last_button = x360_cntrl_map_reverse['hat'][event.hat][i]['current']
	
					# Trigger event if only the last button wasn't the same
					if last_button != button and last_button != "NONE":
						trigger_joy_up_event(last_button, event)
	
					# Skip NONE shitload of events
					if button != "NONE":
						trigger_joy_down_event(button, event)
	
					# Save current button
					x360_cntrl_map_reverse['hat'][event.hat][i]['current'] = button

		elif event.type == pg.JOYBUTTONUP:

			# Listen only to registered controllers to avoid duplicates
			if event.joy == CONFIG['p1']['controller'] or event.joy == CONFIG['p2']['controller']:
				button = x360_cntrl_map_reverse['button'][event.button]

				trigger_joy_up_event(button, event)

		elif event.type == pg.JOYBUTTONDOWN:

			# Listen only to registered controllers to avoid duplicates
			if event.joy == CONFIG['p1']['controller'] or event.joy == CONFIG['p2']['controller']:
				button = x360_cntrl_map_reverse['button'][event.button]

				trigger_joy_down_event(button, event)



def retrieve_events():
	global event_list
	old_event_list = event_list
	event_list = []
	return old_event_list

def close():
	print("==== CLOSING SEQUENCE ====")
	print("- Saving data...")
	data.close_all()

	# Troll easter egg xD
	"""pg.cdrom.init()
	cd = pg.cdrom.CD(0)
	cd.init()
	cd.eject()"""

	print("- Closing...")
	pg.quit()

	print("Done.")
	sys.exit(0)

def apply_config(conf):
	global CONFIG

	CONFIG = copy.deepcopy(conf)

	CONFIG['p1']['controller'] = -1
	CONFIG['p2']['controller'] = -1

	# Select controllers to use
	selected_joys = [] # Avoid controller duplicates
	for joy in joys:

		if joy['id'] == conf['p1']['controller'] and joy['id'] not in selected_joys:
			CONFIG['p1']['controller'] = joy['id']
			selected_joys.append(joy['id'])

		elif joy['id'] == conf['p2']['controller'] and joy['id'] not in selected_joys:
			CONFIG['p2']['controller'] = joy['id']
			selected_joys.append(joy['id'])


def get_used_button_from_key(key):
	# Returns [LOCAL BUTTON, GLOBAL BUTTON]
	
	if key == CONFIG['p1']['keyboard']['up']:
		return [P1_BTN_UP, BTN_UP]

	elif key == CONFIG['p1']['keyboard']['down']:
		return [P1_BTN_DOWN, BTN_DOWN]

	elif key == CONFIG['p1']['keyboard']['left']:
		return [P1_BTN_LEFT, BTN_LEFT]

	elif key == CONFIG['p1']['keyboard']['right']:
		return [P1_BTN_RIGHT, BTN_RIGHT]

	elif key == CONFIG['p1']['keyboard']['select']:
		return [P1_BTN_SELECT, BTN_SELECT]

	elif key == CONFIG['p1']['keyboard']['start']:
		return [P1_BTN_START, BTN_START]

	elif key == CONFIG['p1']['keyboard']['a']:
		return [P1_BTN_A, BTN_A]

	elif key == CONFIG['p1']['keyboard']['b']:
		return [P1_BTN_B, BTN_B]


	elif key == CONFIG['p2']['keyboard']['up']:
		return [P2_BTN_UP, BTN_UP]

	elif key == CONFIG['p2']['keyboard']['down']:
		return [P2_BTN_DOWN, BTN_DOWN]

	elif key == CONFIG['p2']['keyboard']['left']:
		return [P2_BTN_LEFT, BTN_LEFT]

	elif key == CONFIG['p2']['keyboard']['right']:
		return [P2_BTN_RIGHT, BTN_RIGHT]

	elif key == CONFIG['p2']['keyboard']['select']:
		return [P2_BTN_SELECT, BTN_SELECT]

	elif key == CONFIG['p2']['keyboard']['start']:
		return [P2_BTN_START, BTN_START]

	elif key == CONFIG['p2']['keyboard']['a']:
		return [P2_BTN_A, BTN_A]

	elif key == CONFIG['p2']['keyboard']['b']:
		return [P2_BTN_B, BTN_B]


	else:
		return [-1, -1]

def get_used_button_from_joy(button, joy):
	# Returns [LOCAL BUTTON, GLOBAL BUTTON]
	
	if button == CONFIG['p1']['joystick']['up'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_UP, BTN_UP]

	elif button == CONFIG['p1']['joystick']['down'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_DOWN, BTN_DOWN]

	elif button == CONFIG['p1']['joystick']['left'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_LEFT, BTN_LEFT]

	elif button == CONFIG['p1']['joystick']['right'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_RIGHT, BTN_RIGHT]

	elif button == CONFIG['p1']['joystick']['select'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_SELECT, BTN_SELECT]

	elif button == CONFIG['p1']['joystick']['start'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_START, BTN_START]

	elif button == CONFIG['p1']['joystick']['a'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_A, BTN_A]

	elif button == CONFIG['p1']['joystick']['b'] and joy == CONFIG['p1']['controller']:
		return [P1_BTN_B, BTN_B]


	elif button == CONFIG['p2']['joystick']['up'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_UP, BTN_UP]

	elif button == CONFIG['p2']['joystick']['down'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_DOWN, BTN_DOWN]

	elif button == CONFIG['p2']['joystick']['left'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_LEFT, BTN_LEFT]

	elif button == CONFIG['p2']['joystick']['right'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_RIGHT, BTN_RIGHT]

	elif button == CONFIG['p2']['joystick']['select'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_SELECT, BTN_SELECT]

	elif button == CONFIG['p2']['joystick']['start'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_START, BTN_START]

	elif button == CONFIG['p2']['joystick']['a'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_A, BTN_A]

	elif button == CONFIG['p2']['joystick']['b'] and joy == CONFIG['p2']['controller']:
		return [P2_BTN_B, BTN_B]


	else:
		return [-1, -1]

def trigger_joy_up_event(button, event):
	# Get pressed btn [player_btn, global_btn]
	btn = get_used_button_from_joy(button, event.joy)


	# Create x360_cntrl event
	new_event = pg.event.Event(X360_CNTRL_UP, {
		'source': event,
		'button': button
	})

	# Save the event
	event_list.append(new_event)


	# Create virtual controller event
	new_event = pg.event.Event(CNTLR_KEYUP, {
		'source': event,
		'btn_global': btn[1],
		'btn': btn[0]
	})

	# Save the event
	event_list.append(new_event)

	# Add btn pressed state
	BTN_STATES['PRESSED'][btn[0]] = True

def trigger_joy_down_event(button, event):
	# Get pressed btn [player_btn, global_btn]
	btn = get_used_button_from_joy(button, event.joy)


	# Create x360_cntrl event
	new_event = pg.event.Event(X360_CNTRL_DOWN, {
		'source': event,
		'button': button,
		'joy': event.joy
	})

	# Save the event
	event_list.append(new_event)


	# Create virtual controller event
	new_event = pg.event.Event(CNTLR_KEYDOWN, {
		'source': event,
		'btn_global': btn[1],
		'btn': btn[0]
	})

	# Save the event
	event_list.append(new_event)

	# Add btn pressed state
	BTN_STATES['PRESSED'][btn[0]] = True

# TODO:
# cleaner code
# comments
