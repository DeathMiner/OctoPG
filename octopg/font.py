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


"""
RasterFont

Renders text from raster font sprites
"""
class RasterFont():

	"""
	RasterFont.__init__()

	RasterFont constructor

	@param sprite      (str) Path to the sprite font image (should include all ASCII & ASCII-extended chars)
	@param chr_w       (int) The width of a character
	@param chr_h       (int) The height of a character
	@param chr_offset  (int) Space between characters on the sprite
	@param chr_spacing (int) Space between characters in rendered text

	@return (void)
	"""
	def __init__(self, sprite, chr_w, chr_h, chr_offset, chr_spacing):

		# Load sprite image
		self.sprite = pg.image.load(sprite).convert_alpha()

		# Get the sprite size
		self.sprite_size = self.sprite.get_size()

		# Save the parameters
		self.chr_w = chr_w
		self.chr_h = chr_h
		self.chr_offset = chr_offset
		self.chr_spacing = chr_spacing

		# Calculate the amount of cells on each line of the sprite
		self.per_line = ( self.sprite_size[0]-self.chr_offset ) / (self.chr_w+self.chr_offset)

	"""
	RasterFont.render()

	Renders the given text on a surface

	@param text             (str)  The text to render
	@param color            (list) [DEFAULT = white] The color of the font
	@param background_color (list) [DEFAULT = None] The color of the background, if no color the background will be transparent

	@return (pygame.Surface)
	"""
	def render(self, text, color = [255, 255, 255], background_color = None):

		# Create surface by calculating the width & height according to char count
		surf = pg.Surface([len(text)*(self.chr_w+self.chr_spacing), self.chr_h])

		# Set the background color if provided
		if background_color != None:
			surf.fill(background_color)


		# Used to track current progress
		count = 0

		# For all chars
		for char in text:

			# Try to get the ASCII code of the char
			try:
				number = ord(char)
			except:
				number = 0

			# Create a letter Surface to crop the sprite
			letter = pg.Surface([self.chr_w, self.chr_h])

			# The ASCII code is found
			if number != 0:

				# Get the cell x (skip control chars 0->32)
				x = number - 33

				# Calculate the cell y according to amount of cells on a line
				y = (x - (x % self.per_line)) / self.per_line

				# Recalculate the cell x
				x = x % self.per_line


				# Crop the sprite at the calculated positions from cell x, y
				letter.blit(self.sprite, [-self.chr_offset-x*(self.chr_w+self.chr_offset), -self.chr_offset-y*(self.chr_h+self.chr_offset)])
			
			# The ASCII code is not found, set a blank char
			else:
				letter.fill(color)

			# Add letter to main surface
			surf.blit(letter, [count*(self.chr_w+self.chr_spacing), 0])

			# Update progress
			count += 1

		# Give back the rendered text
		return surf

# TODO:
# Cleaner code