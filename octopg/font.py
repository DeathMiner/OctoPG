#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.1.0
#                                |  
#
# @ octopg/font.py => Font utilities

import pygame as pg

default_font = False

def init():
	global default_font

	# Load font
	#default_font = freetype.Font("assets/emulogic.ttf", size=6) Can't use freetype
	default_font = pg.font.Font("assets/emulogic.ttf", 8) # SIZE: photo=6 pg=8 | POS: photo=[+0, +0] pg=[-1, -2]


def render(text, color, background=False, alternateFont=False):
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

# TODO:
# font from sprite?