#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.2.0
#                                |  
#
# @ octopg/__init__.py => Run this file to start OctoPG!


print("  ___     _       ___  ___ _ ")
print(" / _ \ __| |_ ___| _ \/ __| |")
print("| (_) / _|  _/ _ \  _/ (_ |_|")
print(" \___/\__|\__\___/_|  \___(_)")
print("")



"""
--------------------------------------------

             LOADING PROCESS

--------------------------------------------
"""


print("==== LOADING START ====")
print("- Starting octopg...") # Loads pygame as the game octopg
import pygame as pg

print("- Initializing octopg...") # Init pygame & mixers
pg.mixer.pre_init(44100)
pg.init()
pg.mixer.set_num_channels(30)

print("- Opening window...") # Opens the window using the graphics helper
import octopg.graphics
octopg.graphics.init()

print("- Setting loading screen...") # Load splash-art
loading_assets = [
	pg.image.load("assets/sprites/octopg_logo_small.png").convert()
]

# Reset screen
octopg.graphics.reset()

# Set the splash art
octopg.graphics.screen.blit(loading_assets[0], [112, 103])

# Update screen
octopg.graphics.flip()


print("- Loading external libraries...") # Load all used modules in the memory to avoid freezes ingame when fetching the modules
# Generic
import time, random, math, numpy, sys, json, os, webbrowser, copy

# OctoPG resources
import octopg.res # Get the resource list of the main menu


print("- Loading external files...") # Load all OctoPG modules
import octopg.util           # Load utilities
import octopg.data           # Load octopg data system
import octopg.color          # Load color listing
import octopg.events         # Load event system
import octopg.font           # Load font octopg
import octopg.settings       # Load settings pages
import octopg.debug          # Load debug utilities
import octopg.version        # Load version infos

# Init all modules
octopg.data.init()
octopg.events.init()
octopg.font.init()
octopg.debug.init()
octopg.settings.init()

# Init module configurations
octopg.graphics.apply_config(octopg.data.d['config']['graphics'])
octopg.events.apply_config(octopg.data.d['config']['controls'])

print("==== LOADING DONE ====")