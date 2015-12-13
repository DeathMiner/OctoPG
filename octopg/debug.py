#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.3.0
#                                |  
#
# @ octopg/debug.py => All about debugging

import octopg.data
import octopg.graphics
import pygame as pg
import octopg.version

on = False

font = False

def init():
	global on, font

	if octopg.data.d['config']['debug']:
		on = True

		print("- Debugging activated")

		font = pg.font.Font(None, 16)


		print("- Checking for updates...")

		update = octopg.version.check_updates()

		if update != False:
			print("\007") # Bell char
			print("")
			print("=============================")
			print("    NEW UPDATE AVAILABLE:    ")
			print("=============================")
			print(update['name']) # Show update name
			print("")
			print(update['body']) # Show update changelog
			print("=============================")
			print("Download link: "+update['html_url']) # Show update url
			print("=============================")
			print("")
			print("")
		else:
			print("No new updates.")


def draw(surface):

	right_str = ""
	left_str = ""
	separator = " | "

	# Show joystick count
	right_str += "Joys: "+str(len(octopg.events.joys))
	right_str += separator

	# Show graphical infos
	right_str += "Window: "+str(octopg.graphics.current_config['resolution'][0])+"x"+str(octopg.graphics.current_config['resolution'][1])

	if octopg.graphics.current_config['fullscreen']:
		right_str += ",F"

	if octopg.graphics.current_config['post_effects'] > 0:
		right_str += ",E["+str(octopg.graphics.current_config['post_effects'])+"]"

	if octopg.graphics.current_config['tv']:
		right_str += ",TV"

	right_str += separator

	# Set fps
	left_str += "FPS: "+str(int(octopg.graphics.fps.get_fps()))

	if octopg.graphics.current_config['fps_blocker'] > 0:
		left_str += " ["+str(octopg.graphics.current_config['fps_blocker'])+" blocked]"

	#right_str += separator

	# Versions
	right_str += "OctoPG "+octopg.version.octopg_ver+separator
	right_str += "PyGame "+octopg.version.pg_ver+separator
	right_str += "SDL "+octopg.version.sdl_ver


	# Draw right
	text = font.render(right_str, True, [0, 255, 0])
	text_size = text.get_size()
	surface.blit(text, [octopg.graphics.window_size[0]-text_size[0]-5 , octopg.graphics.window_size[1]-text_size[1]-5])

	# Draw left
	text = font.render(left_str, True, [0, 255, 0])
	text_size = text.get_size()
	surface.blit(text, [5 , octopg.graphics.window_size[1]-text_size[1]-5])

# TODO:
# better debug messages?
# debug window?