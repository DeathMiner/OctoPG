#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.3.0
#                                |  
#
# @ octopg/version.py => Version of this octopg!

octopg_ver = "0.3.0"
octopg_vernum = (0, 3, 0)

def vernum_to_ver(vernum):
	return ".".join(map(str, vernum))

import pygame
import pygame.version

pg_ver = pygame.version.ver
pg_vernum = pygame.version.vernum

sdl_vernum = pygame.get_sdl_version()
sdl_ver = vernum_to_ver(sdl_vernum)



import urllib.request as url
import json
from operator import itemgetter

"""
check_updates()

Check if an update is available for the OctoPG library

@return (bool|dict) False when there is no update, the release info when the update is available
"""
def check_updates():

    # We check the github API for recent OctoPG releases
    # Create request with these headers
    headers = {
        "User-Agent": "OctoPG-Updater",
        "Accept": "application/vnd.github.v3+json"
    }
    request = url.Request("https://api.github.com/repos/DeathMiner/OctoPG/releases", None, headers)

    # Avoid errors from stopping program
    try:

        # Start request
        with url.urlopen(request, None, 10) as r:
            
            # Get the response, decode it, json parse it and sort it by desc id! *pfeww*
            releases = sorted(json.loads(r.read().decode("utf-8")), key = itemgetter("id"), reverse = True) 
            
            # Get the release vernum [eg: "v3.2.5" to (3, 2, 5)]
            # Remove the "v", split it by "." and convert numbers to int, then convert map to tuple
            release_vernum = tuple(map(int, releases[0]['tag_name'][1:].split(".")))
            
            # Compare release vernum with current vernum
            if release_vernum > octopg_vernum:
                return releases[0]
            else:
                return False
    except:
        return False