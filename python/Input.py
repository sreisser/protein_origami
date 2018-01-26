#!/usr/bin/python

import string, sys, re, math, locale
import AA_Data as aa

def print_info(program):
	print """This is Protein ORIGAMI v1.0 .

Please cite: Protein ORIGAMI - a program for the creation of 3D peptide paper models, S. Rei\{ss}er, S. Prock, H. Heinzmann, A. S. Ulrich. Submitted (2018)

Options:
	-n name of your peptide
	-s amino acid sequence in one-letter code, 
		capitals letters: L-form, small letters: D-form
	-nter n-terminal modification: NH3 (NH3+), FOR (HCO, formyl), 
		ACY (R-CO, acyl), default: None
	-cter c-terminal modification: COO (COO-), NHE (NH2, amidated), 
		LIP (NH-R, lipidated), default: None
	-repres representation (helix_origami (default), helical_wheel, 
		helical_mesh_vert, helical_mesh_horiz, beta_sheet, random_coil)
	-pitch Helix pitch in degrees (default: 100)
	-pH pH values (le7 (<= 7; default) or ge8 (>= 8))
	-c one- or three-letter code for output, possible values: 1 (default), 3
	-cl amino acids in color or in white: color (default), bw
	-b begin numbering with index (integer, default: 1)
	-sh shift geometry by N positions (integer, default: 0)
	-h this info
example: %s -n TisB -c 3 -s \"MNLVDIAILILKLIVAALQLLDAVLKYLK\"
""" % program



# begin input handling

re_input = {
"-n" : "^\w[\s\w\-]*$",
"-c" : "^[1|3]$",
"-cl" : "^[a-z]{2,5}$",
"-pH" : "^le7|ge8$",
"-pitch" : "^[0-9]{1,3}$",
"-s" : "^[A-Za-z\s]+$",
"-b" : "^[0-9]+$",
"-sh" : "^[0-9]+$",
"-r" : "^[0-9]+$",
"-o" : "^[\/\w]+$",
"-nter" : "^N|ACE|FOR|ACY|None$",
"-cter" : "^C|NME|NHE|LIP|None$",
"-mesh" : "^vert|horiz$",
"-map" : "[\w:,]+", # non-usual amino-acids
"-cmap" : "[\w:,]+", # colors for non-usual amino acids
"-chmap" : "[\w:,]+", # colors for non-usual amino acids
"-rc" : "yes", # random coil representation
"-repres" : "[\w]+"
}

	# default input values
input = {
"-pitch" : 100.,
"-pH" : "le7",
"-c" : 1,
"-cl" : "color",
"-b" : 1,
"-sh" : 0,
"-nter" : "",
"-cter" : "",
"-map" : {},
"-cmap" : {},
"-chmap" : {},
"-rc" : 0,
"-repres" : "helix_origami"
}

name = "" 
letters = int(input["-c"])
color = input["-cl"]
sequence = "" 
pH = input["-pH"]
pitch = float(input["-pitch"])
pH_string = ">= 8"
charge = '0'
start_index = int(input["-b"])
init_shift = int(input["-sh"])
write_mass = "yes"

def check_input(arguments):
	if len(arguments) < 2:
		print_info(sys.argv[0])
		sys.exit()

	for key, arg in enumerate(arguments):
		if arg in re_input.keys():
			try: 
				value = sys.argv[key+1].strip()
			except IndexError:
				print "Invalid input for %s" % arg
				sys.exit()
			else:
				if not re.match(re_input[arg], value.decode('UTF-8'), re.UNICODE):
					print "Invalid input for %s: %s" % (arg, value)
					sys.exit()
				else:
					input[arg] = value
		if  arg == "-h":
			print_info(sys.argv[0])
			sys.exit()
		if arg == "-map":
			aa_map = string.split(input["-map"], ',')
			new_name_map = {}
			for i, val in enumerate(aa_map):
				if val != "":
					entry = string.split(val, ":")
					new_name_map[entry[0]] = entry[1]
			input["-map"] = new_name_map
		if arg == "-cmap":
			aa_cmap = string.split(input["-cmap"], ',')
			new_color_map = {}
			new_charge_map = {}
			for i, val in enumerate(aa_cmap):
				if val != "":
					entry = string.split(val, ":")
					new_color_map[entry[0]] = entry[1]
					if  entry[1] == "dark-blue":
						new_charge_map[entry[0]] = 1
					if  entry[1] == "red":
						new_charge_map[entry[0]] = -1
			input["-cmap"] = new_color_map
			input["-chmap"] = new_charge_map

	if not "-n" in input:	
		sys.exit("Please provide a name with -n NAME.\nSee help with '%s -h'" % sys.argv[0])
	if not "-s" in input:	
		sys.exit("Please provide a sequence with -s SEQUENCEONELETTERCODE.\nSee help with '%s -h'" % sys.argv[0])

	# set output name
	if not "-o" in input:
		input["-o"] = "_".join(input["-n"].split() + [input["-repres"]])


	return input
	# end input handling


