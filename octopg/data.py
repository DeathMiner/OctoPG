#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.1.0
#                                |  
#
# @ octopg/data.py => Handles multiple data files

import json
import os

files = {}

d = {}


def init():
	load_file("config", "data/config.json")

def load_file(name, path):
	global files, d

	print("- Loading '"+name+"' data file")
	print("  => "+path)

	if name not in files:
		files[name] = path

		if os.path.exists(path):
			with open(path, "r") as f:
				d[name] = json.loads(f.read())

			print("Done.")
		else:
			print("File not found.")
	else:
		print("File already loaded.")

def close_file(name):
	global files, d

	print("- Saving '"+name+"' data file")
	print("  => "+files[name])

	if name in files:
		with open(files[name], "w") as f:
			f.write(json.dumps(d[name], sort_keys=True, indent=4))
		del d[name]
		del files[name]

		print("Done.")
	else:
		print("File not loaded.")

def close_all():
	to_close = [name for name in files]
	for name in to_close:
		close_file(name)
		
# TODO:
# default config files if file is deleted