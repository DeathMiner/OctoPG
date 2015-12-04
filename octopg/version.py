#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.2.0
#                                |  
#
# @ octopg/version.py => Version of this octopg!

octopg_ver = "0.2.0"
octopg_vernum = (0, 2, 0)

def vernum_to_ver(vernum):
	return ".".join(map(str, vernum))

import pygame
import pygame.version

pg_ver = pygame.version.ver
pg_vernum = pygame.version.vernum

sdl_vernum = pygame.get_sdl_version()
sdl_ver = vernum_to_ver(sdl_vernum)