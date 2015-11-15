#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.1.0
#                                |  
#
# @ octopg/graphics.py => The graphical octopg overlay used by OctoPG

import pygame as pg
import octopg.color as color
import octopg.debug
import octopg.version
import copy

# All possibles resolutions
RESOLUTIONS = {
	"4/3":[
		[640, 480],   # VGA (NTSC)
		[720, 576],   # VGA (PAL)
		[800, 600],   # SVGA
		[1024, 768],  # XGA
		[1152, 864],  # XGA+
		[1280, 960]   # (no name)
	],
	"5/3":[
		[1280, 1024]  # SXGA
	],
	"16/9":[
		[1176, 664],  # (no name)
		[1280, 720],  # HD 720
		[1360, 768],  # (no name)
		[1366, 768],  # (no name)
		[1440, 576],  # (no name)
		[1600, 900],  # (no name)
		[1768, 992],  # (no name)
		[1920, 1080], # HD 1080
		[2560, 1440], # WQHD
		[2715, 1527], # (no name)
		[3840, 2160]  # UHD-1 (4K)
	],
	"16/10":[
		[720, 480],   # (no name)
		[1280, 768],  # (no name)
		[1280, 800],  # WXGA
		[1600, 1024], # (no name)
		[1680, 1050]  # WSXGA+
	]
}

# Current & default display config
current_config = {
	"aspect_ratio": "4/3",
	"resolution": [640, 480],
	"fullscreen": False,
	"post_effects": 0,
	"tv": False,
	"fps_blocker": 0
}


# NES Screen size
screen_size = [256, 240]

# Info about current display
display_info = False

# Screen & window surfaces
screen = False
window = False

# Current window size
window_size = False

# Screen size & pos on window
screen_resized = False
screen_pos = False

# TV data if TV mode activated
tv = {}

# FPS blocker
fps_clock = False

def init():
	global display_info, RESOLUTIONS, screen, fps

	# Get info about current display
	display_info = pg.display.Info()

	# Delete all resolutions higher than current screen to avoid errors (We do not support DSR)
	aspect_ratios = [key for key in RESOLUTIONS.keys()]
	for key in aspect_ratios:
		RESOLUTIONS[key] = [val for val in RESOLUTIONS[key] if not val[0] > display_info.current_w or not val[1] > display_info.current_h]

		# Delete aspect ratio if no resolutions available
		if len(RESOLUTIONS[key]) == 0:
			del RESOLUTIONS[key]

	# Create screen surface
	screen = pg.Surface(screen_size)

	# Set FPS blocker
	fps = pg.time.Clock()

	# Open first window with current params (splash window)
	open_window()

	# Hide mouse
	pg.mouse.set_visible(False)

	# Set window title
	set_title("OctoPG! "+octopg.version.octopg_ver)

def open_window():
	global window_size, window, screen_resized, screen_pos, tv

	# Check if resolution selected in config exists (if can be used)
	if current_config['aspect_ratio'] in RESOLUTIONS:
		if current_config['resolution'] in RESOLUTIONS[current_config['aspect_ratio']]:

			# Set current window size
			window_size = current_config['resolution']

			# Set window params (fullscreen or not)
			window_flags = pg.HWSURFACE | pg.DOUBLEBUF
			if current_config['fullscreen']:
				window_flags = pg.HWSURFACE | pg.DOUBLEBUF | pg.FULLSCREEN

			# Open window
			window = pg.display.set_mode(window_size, window_flags)

			# Calculate ratio between NES screen & window
			ratio = window_size[1]/screen_size[1]

			# Calculate screen size & pos on window
			screen_resized = [int(screen_size[0]*ratio), window_size[1]]
			screen_pos = [int(window_size[0]/2-screen_resized[0]/2), 0]

			# TVmode pos & size calculation
			if current_config['tv']:
				frame = pg.image.load("assets/sprites/tv.png").convert_alpha()
				pixels = pg.image.load("assets/sprites/scanlines.png").convert()
				pixels.set_alpha(25)
	
				tv['size'] = [int(328*ratio), int(288*ratio)]
				tv['position'] = [screen_pos[0]-int(36*ratio), screen_pos[1]-int(24*ratio)]
				tv['frame'] = pg.transform.scale(frame, tv['size'])
				tv['pixels'] = pg.transform.scale(pixels, tv['size'])

			# Reset screen & flip for first frame
			reset()
			flip()

def set_title(title):
	pg.display.set_caption(title)

def flip():
	global fps

	# Blit screen at his current pos & size (No sampling while resizing to keep pixels)
	window.blit(pg.transform.scale(screen, screen_resized), screen_pos)

	# Post effects
	if current_config['post_effects'] > 0:
		pass

	# TV Mode
	if current_config['tv']:
		window.blit(tv['pixels'], tv['position'])
		window.blit(tv['frame'], tv['position'])

	# Debug
	if octopg.debug.on:
		octopg.debug.draw(window)

	# Update screen
	pg.display.flip()

	# FPS Blocker
	fps.tick(current_config['fps_blocker'])

def reset():
	window.fill([10, 10, 10])
	screen.fill(color.n1)

def apply_config(conf):
	global current_config

	current_config = copy.deepcopy(conf)

	open_window()

# TODO:
# post effects
# non-buggy fullscreen