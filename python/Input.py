#!/usr/bin/env python

#   This is Protein ORIGAMI, a program for the creation of 3D peptide paper models
#   Copyright (C) 2018 Sabine Reisser (sreisser@sissa.it)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License V3 as published by
#   the Free Software Foundation, 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
		ACY (R-CO, acyl), None; default: NH3
	-cter c-terminal modification: COO (COO-), NHE (NH2, amidated), 
		LIP (NH-R, lipidated), None; default: COO
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
"-o" : "^\w[\/\s\w\-]*$",
"-c" : "^[1|3]$",
"-cl" : "^color$|^bw$",
"-pH" : "^le7$|^ge8$",
"-pitch" : "^[0-9]{1,3}$",
"-s" : "^[A-Za-z\s]+$",
"-b" : "^[0-9]+$",
"-sh" : "^[0-9]+$",
"-nter" : "^NH3$|^FOR$|^ACY$|^None$$",
"-cter" : "^COO$|^NHE$|^LIP$|^None$",
"-mesh" : "^vert|horiz$",
"-map" : "[\w:,]+", # non-usual amino-acids
"-cmap" : "[\w:,]+", # colors for non-usual amino acids
"-chmap" : "[\w:,]+", # colors for non-usual amino acids
"-repres" : "^helix_origami$|^helical_wheel$|^helical_mesh_vert$|^helical_mesh_horiz$|^beta_sheet$|^beta_sheet_origami$|^random_coil$|^random_coil_origami$",
"-r" : "[0-9]+"
}

	# default input values
input = {
"-pitch" : 100.,
"-pH" : "le7",
"-c" : 3,
"-cl" : "color",
"-b" : 1,
"-sh" : 0,
"-nter" : "NH3",
"-cter" : "COO",
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
		print_info("protein_ORIGAMI")
		sys.exit()

	for key, arg in enumerate(arguments):
		if arg in re_input.keys():
			try: 
				value = sys.argv[key+1].strip()
			except IndexError:
				print_info("protein_ORIGAMI")
				print "Invalid input for %s" % arg
				sys.exit()
			else:
				if not re.match(re_input[arg], value.decode('UTF-8'), re.UNICODE):
					print_info("protein_ORIGAMI")
					print
					print "Invalid input for %s: %s" % (arg, value)
					sys.exit()
				else:
					input[arg] = value
		if arg in ["-nter", "-cter"] and input[arg] == "None":
			input[arg] = "" 
		if arg == "-h":
			print_info("protein_ORIGAMI")
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
		print_info("protein_ORIGAMI")
		sys.exit("Please provide a name with -n NAME.")
	if not "-s" in input:	
		print_info("protein_ORIGAMI")
		sys.exit("Please provide a sequence with -s SEQUENCEONELETTERCODE.")

	# set output name
	if not "-o" in input:
		input["-o"] = "_".join(input["-n"].split() + [input["-repres"]])


	return input
	# end input handling


