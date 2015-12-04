#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.2.0
#                                |  
#
# @ octopg/util.py => Some useful utilities obviously!

import pygame as pg
import numpy as np

class Object(object):
	pass

def set_per_pixel_alpha(surf, amount):
	# Get access to the alpha band of the image.
	pixels_alpha = pg.surfarray.pixels_alpha(surf)
	# Do a floating point multiply, by alpha 100, on each alpha value.
	# Then truncate the values (convert to integer) and copy back into the surface.
	pixels_alpha[...] = (pixels_alpha * (255-amount)).astype(np.uint8)
	# Unlock the surface.
	del pixels_alpha
		

def text_render(text, color, background=False):
	texts = text.split("\n")
	surfs = []
	ws = []
	h = 0

	for txt in texts:
		size = default_font.size(txt)
		ws.append(size[0])
		h = size[1]
		if not background:
			surfs.append(default_font.render(txt, False, color))
		else:
			surfs.append(default_font.render(txt, False, color, background))

	surf = pg.Surface([max(ws), len(surfs)*h])

	for i in range(0, len(surfs)):
		surf.blit(surfs[i], [0, i*h])

	return surf

# Fake "rect", but following [left, right, width, height]
def gen_sprite(image, rect):
	surf = pg.Surface([rect[2], rect[3]])
	surf.fill([0, 255, 0])
	surf.set_colorkey([0, 255, 0])
	surf.blit(image, [-rect[0], -rect[1]])
	return surf

# TODO:
# documentation
# cleaner code
# documentation