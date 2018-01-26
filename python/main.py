#!/usr/bin/env python

import sys, re, math, AA_Data as aa
import Input
from geometry import *
import origami, beta_sheet, helical_wheel



if __name__ == "__main__": 
	input = Input.check_input(sys.argv)
	aa.name_map.update(input["-map"])
	aa.color_map.update(input["-cmap"])
	repres = input["-repres"]
	r_origami = ['helix_origami', 'helical_mesh_vert', 'helical_mesh_horiz']
	r_strand = ['beta_sheet_origami', 'random_coil_origami', 'beta_sheet', 'random_coil']
	if repres in r_origami:
		mod_object = origami
	elif repres in r_strand:
		mod_object = beta_sheet
	elif repres == "helical_wheel":
		mod_object = helical_wheel
	mod_object.name = input["-n"]
	mod_object.letters = int(input["-c"])
	mod_object.color = input["-cl"]
	mod_object.sequence = input["-s"] 
	mod_object.pH = input["-pH"]
	mod_object.pitch = float(input["-pitch"])
	if mod_object.pH == "ge8":
		mod_object.pH_string = ">= 8"
		aa.color_map.update(aa.basic_colors)
		aa.charge_map.update(aa.basic_charges)
	else:
		mod_object.pH_string = "<= 7"
	mod_object.charge = 0
	mod_object.start_index = int(input["-b"])
	mod_object.init_shift = int(input["-sh"])
	mod_object.write_charge = True
	mod_object.write_mass = True
	if input["-map"] != "":
		mod_object.write_mass = False
	mod_object.sequence_list = []
	for letter in mod_object.sequence:
		if re.match("^[a-z]$", letter):
			print "D amino acid: %s" % letter
		if letter in aa.name_map.keys() or letter.upper() in aa.name_map.keys():
			mod_object.sequence_list.append(letter)
		elif re.match("[A-Za-z]", letter):
			mod_object.sequence_list.append(letter)
			if mod_object.color == "color":
				if letter.upper() not in aa.color_map.keys():
					aa_color = ""
					while aa_color not in aa.colors.keys():
						question = "What color do you want for %s? [" % letter
						for c in aa.colors:
							question += " %s" % c
						question += "]"
						aa_color = raw_input(question)
					aa.color_map[letter.upper()] = aa_color
			if mod_object.letters == 3:
				three_letter = ""
				while three_letter not in aa.name_map and not re.match('^[A-Za-z]{3}$', three_letter):
					question = "What three-letter-code do you want for %s? " % letter
					three_letter = raw_input(question)
				aa.name_map[letter.upper()] = three_letter

	mod_object.mass = 0.0
	for key, letter in enumerate(mod_object.sequence_list):
		if mod_object.color == "color" and letter.upper() not in aa.charge_map:
			if aa.color_map[letter.upper()] == "dark-blue":
				aa.charge_map.update({letter.upper(): 1})
			elif aa.color_map[letter.upper()] == "red":
				aa.charge_map.update({letter.upper(): -1})
			else:
				aa.charge_map.update({letter.upper(): 0})

		try: charge_i = aa.charge_map[letter.upper()]
		except:
			print "missing ", letter.upper() 
			mod_object.write_charge = False
			pass
		else:
			mod_object.charge += charge_i
		if mod_object.write_mass:
			mod_object.mass += aa.mass_map[letter.upper()]
	if input['-nter'] != "":		
		mod_object.charge += aa.charge_map[input['-nter']]
	if input['-cter'] != "":		
		mod_object.charge += aa.charge_map[input['-cter']]

	if mod_object.write_mass == True:
		if input['-nter'] != '':
			mod_object.mass += aa.mass_map[input['-nter']]
		if input['-cter'] != '':
			mod_object.mass += aa.mass_map[input['-cter']]

	if mod_object.letters == 1:
		mod_object.font_size = 30 * scale
	else:
		mod_object.font_size = 25.0 * scale
	mod_object.font_size_sup = mod_object.font_size - 10.0 * scale
	mod_object.other_colors = {
	"grey" : "#9c9c9c",
	"black" : "#ffffff"
	}
	mod_object.draw(repres)

