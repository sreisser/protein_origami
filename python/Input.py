#!/usr/bin/python

import string, sys, re, math, locale
import AA_Data as aa

def print_info(program):
	print """This is Protein ORIGAMI.

Please cite: Protein ORIGAMI - a program for the creation of 3D peptide paper models, S. Rei\{ss}er, S. Prock, H. Heinzmann, A. S. Ulrich. Submitted (2018)

Options:
\t-n name of your peptide
\t-c one- or three-letter code for output, possible values: 1, 3 (default: 1)
\t-repres representation (helical_wheel, helix_origami, helical_mesh_vert, helical_mesh_horiz, beta_sheet, random_coil)
\t-cl amino acids in color or in white (color vs. bw)
\t-pitch Helix pitch (default: 100)
\t-ph pH values (le7(<= 7) or ge8(>= 8)) (default: <= 7)
\t-s sequence in one-letter code, L - amino acids in capitals, D - amino acids in small letters
\t-b begin with index (integer)
\t-sh shift geometry by N positions (integer)
\t-nter n-terminal modification (NH3+, CH3-CO)
\t-cter c-terminal modification (COO-, NH-CH3, NH2)
\t-mesh output complete sequence on one page, vertically or horizontally (vert, horiz)
\t-o output filename (no spaces, no umlauts)
\t-h this info
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
"-rc" : 0
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
	#		print "MAP: %s" % aa_map
			new_name_map = {}
			for i, val in enumerate(aa_map):
				if val != "":
	#				print "---%s---" % val
					entry = string.split(val, ":")
	#				print "ENTRY: %s" % entry
					new_name_map[entry[0]] = entry[1]
			input["-map"] = new_name_map
		if arg == "-cmap":
			aa_cmap = string.split(input["-cmap"], ',')
			new_color_map = {}
			new_charge_map = {}
			for i, val in enumerate(aa_cmap):
				if val != "":
	#				print "---%s---" % val
					entry = string.split(val, ":")
	#				print "ENTRY: %s" % entry
					new_color_map[entry[0]] = entry[1]
					if  entry[1] == "dblue":
						new_charge_map[entry[0]] = 1
					if  entry[1] == "red":
						new_charge_map[entry[0]] = -1
			input["-cmap"] = new_color_map
			input["-chmap"] = new_charge_map

#	print input
	for o in ("-n", "-s"):
		try:
			input[o]
		except KeyError:
			print "Input %s is obligatory!" % o
			sys.exit()


	return input
	# end input handling


