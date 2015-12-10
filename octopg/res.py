#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.3.0
#                                |  
#
# @ octopg/res.py => Helpers used for loading ressources

import os, json
import pygame as pg

def load_images(images):
	print("==== IMAGE LOADING ===")

	total = len(images)
	print(str(total)+" images to load!")
	progress = 0
	result = {}

	for key, value in images.items():

		# Load selected image using alpha
		result[key] = pg.image.load(value).convert_alpha()

		# Update progress
		progress += 1
		print("Progress: "+str(progress)+"/"+str(total)+" | "+value)

	print("==== IMAGE LOADING FINISHED ===")

	return result

def load_sounds(sounds):
	print("==== SOUND LOADING ===")

	total = len(sounds)
	print(str(total)+" sounds to load!")
	progress = 0
	result = {}

	for key, value in sounds.items():

		# Load selected sound using alpha
		result[key] = pg.mixer.Sound(value)

		# Update progress
		progress += 1
		print("Progress: "+str(progress)+"/"+str(total)+" | "+value)

	print("==== SOUND LOADING FINISHED ===")

	return result