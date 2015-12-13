#   ___     _       ___  ___ _   |  
#  / _ \ __| |_ ___| _ \/ __| |  |  Create 8-bit-like games!
# | (_) / _|  _/ _ \  _/ (_ |_|  |  Author: Death_Miner
#  \___/\__|\__\___/_|  \___(_)  |  Version: 0.4.0
#                                |  
#
# @ octopg/data.py => Handles multiple data files

# We use the JSON format for all data files.
import json
import os

# Current opened files list
files = {}

# Current data of files
d = {}

"""
init()
Loads the required files for the octopg engine

@return void
"""
def init():

	# We load the main config file
	load_file("config", "data/config.json", "data/config.default.json")


"""
load_file()
Loads a data file and decodes it

@param name         (str) The name to use for this file
@param path         (str) Path of the data file
@param default_path (str) Path of the default data file
@return void
"""
def load_file(name, path, default_path = None):
	global files, d

	# Do some debug for the developers
	print("- Loading '"+name+"' data file")
	print("  => "+path)


	# Load only the file once
	if name not in files:

		# Get the path of the default file
		if default_path == None:

			# Generate the path of the default data file.
			# It should be (original basename)/(original filename).default.(original extension)
			default_file = os.path.basename(path).split(".")
			default_file.insert(-1, "default")
			default_path = os.path.dirname(path) + "/" + ".".join(default_file)
		

		# Check if the config file exists
		if os.path.exists(path):

			# Open this file
			with open(path, "r") as f:

				# Decode the JSON file and add it to the data list
				d[name] = json.loads(f.read())

				# Add the file we want to load to the file list
				files[name] = path

			# Debug
			print("Done.")


		# The file doesn't exists, try to open a default config file
		elif os.path.exists(default_path):

			# Open this file
			with open(default_path, "r") as f:

				# Decode the JSON file and add it to the data list
				d[name] = json.loads(f.read())

				# Add the file we want to load to the file list
				files[name] = path

			# Debug
			print("Done.")
		

		# We didn't find any file... Shame!
		else:
			print("File not found.")


	# Show this when file already loaded
	else:
		print("File already loaded.")


"""
save_file()
Saves a data file

@param name (str) The name of the data file
@return void
"""
def save_file(name):
	global files, d

	# Do some debug for the developers
	print("- Saving '"+name+"' data file")
	print("  => "+files[name])


	# Check first is file was loaded
	if name in files:

		# Open the file and write the new JSON encoded data
		with open(files[name], "w") as f:
			f.write(json.dumps(d[name], sort_keys=True, indent=4))

		# Debug
		print("Done.")


	# The file is not loaded, we can't save it obviously
	else:
		print("File not loaded.")


"""
close_file()
Saves a data file and close it (removes it from the list)

@param name (str) The name of the data file
@return void
"""
def close_file(name):
	global files, d

	# Do some debug for the developers
	print("- Closing '"+name+"' data file")


	# Check first is file was loaded
	if name in files:

		# Save the file
		save_file(name)

		# Delete the data & file from memory
		del d[name]
		del files[name]

		# Debug
		print("Done.")


	# The file is not loaded, we can't close it obviously
	else:
		print("File not loaded.")


"""
close_all()
Closes all the opened data files

@return void
"""
def close_all():
	# list of files to close
	to_close = [name for name in files]

	# Close them all
	for name in to_close:
		close_file(name)