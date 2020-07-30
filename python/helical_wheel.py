#!/usr/bin/env python3

#   This is Protein ORIGAMI, a program for the creation of 3D peptide paper models
#   Copyright (C) 2020 Sabine Reisser (sabine.reisser@mdc-berlin.de)

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License V3 as published by
#   the Free Software Foundation, 
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, re, math, AA_Data as aa
import numpy as np
from  Input import *
from geometry import *



# functions 
def calc_circle(start_skew_line, shift, slope, pos):
	row = math.floor(pos/res_per_turn)
	cx = start_skew_line[0] + shift*slope[0]/res_per_turn
	cy = start_skew_line[1] + shift*slope[1]/res_per_turn + slope[1]*row
	return cx, cy

def calc_circle_sec(start_skew_line, shift, slope, pos):
	row = math.floor(pos/res_per_turn)
	cx = start_skew_line[0] + slope[0]
	cy = start_skew_line[1] + shift*slope[1]/res_per_turn + slope[1]*row
	return cx, cy

def rotation_matrix(axis,theta):
	axis = axis/math.sqrt(np.dot(axis,axis))
	a = math.cos(theta/2)
	b,c,d = -axis*math.sin(theta/2)
	return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
			[2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
			[2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])


def draw(r):
	global font_size, font_size_sup, circle_radius, dy_nr
	repres = r
	if re.match("^[a-zG\s]+$", sequence):
		helix = "left"
	else:
		helix = "right"

	page_width = 744.0
	page_height = 1051.0
	n=1
	while (360*n)%pitch != 0:
		n += 1
	res_per_turn = 360.0/pitch
	max_res_per_wheel = n*360.0/pitch 
	angle = pitch/180*math.pi
	angles = []

	if helix == "left":
		angle = -angle

	factor = 1.0 - math.floor(len(sequence_list)/18.01)*0.12
	font_size *= factor
	font_size_sup *= factor
	font_shift = factor * 8
	circle_radius *= factor 
	dy_nr *= factor
	inner_line_length = factor * page_width/4.3
	outer_line_length = inner_line_length + 1.1*circle_radius
	outer_line_length_2 =  outer_line_length + 2.1*circle_radius
	wheel_center = np.array([page_width/2, page_height/2, 0 ])
	nearest_neighbor = 13.0 # degrees

	shift = "no"
	p0 = wheel_center - np.array([0, inner_line_length, 0])
	p1 = p0
	c0 = wheel_center - np.array([0, outer_line_length, 0])
	c1 = c0

	a = np.array([1,0,0])
	axis = np.array([0,0,1])

	if not re.match("^.*\.svg$", input["-o"]):
		svgfile = open(input["-o"]+'.svg', "w")
	else:
		svgfile = open(input["-o"], "w")


	svgfile.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?> 
	<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" 
	  "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
	<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg"
	  xmlns:xlink="http://www.w3.org/1999/xlink">
	''' % (page_width, page_height))


	for key, letter in enumerate(sequence_list):
		nr = key + start_index
		if letters == 3:
			print_name = aa.name_map[letter.upper()]
			if print_name[-1] in ["a", "e", "t"]:
				dx_nr = dx_nr1
			else:
				dx_nr = dx_nr2
		else:
			print_name = letter.upper()
			dx_nr = 0


		angle_i = ( (key+init_shift) * angle)%(2*math.pi)
		# lines
		if key + 1 != len(sequence_list) and key < max_res_per_wheel:
			p2 =  np.dot(rotation_matrix(axis, -angle), p1-wheel_center) + wheel_center
			svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:1px;" />
			''' % (p1[0], p1[1], p2[0], p2[1], other_colors['grey']));
			p1 = p2

		# circles
		for a in angles:
			if np.abs(angle_i - a) <= nearest_neighbor/180.0*math.pi:
				shift = "yes"
				# after first shift, there is more space
				if nearest_neighbor > 4:
					nearest_neighbor -= 3
				continue

		if shift == "yes":
			length = np.linalg.norm(c1-wheel_center)
			c0 = wheel_center +  (length+2.2*circle_radius)*(c0-wheel_center)/length
			shift = "no"
			angles = []
		angles.append(angle_i)

		if input['-cl'] == 'bw':
			fill_color = "white"
		else:
			fill_color = aa.color_map[letter.upper()]
		c2 =  np.dot(rotation_matrix(axis, -angle_i), c0-wheel_center) + wheel_center
		svgfile.write('''<circle cx="%5.3f" cy="%5.3f" r="%d" stroke="black" stroke-width="2" fill="%s" />
	''' % (c2[0], c2[1], circle_radius, aa.colors[fill_color]))

		# names
		if fill_color in ('dark-blue', 'red'):
			i_font_color = 'white'
		else:
			i_font_color = font_color
		svgfile.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%dpx; text-align:center; text-anchor:middle; font-family:Liberation Sans">''' % (c2[0], c2[1]+circle_radius/5., i_font_color, font_weight, font_size))
		if re.match("^[a-z](?<!g)$", letter):
			svgfile.write(''' <tspan dy="%dpx" style="font-size:%dpx">D</tspan>
	''' % (-font_size_sup,font_size_sup))
			svgfile.write('''	<tspan dy="%dpx" >''' % font_size_sup)
		else:
			svgfile.write('''	<tspan  > ''')
		svgfile.write('''

		%s
		</tspan>
	<tspan dy="%.1fpx" dx="%.1fpx" style="font-size:%.1fpx">%d</tspan>
	</text>
	''' % (print_name, dy_nr, dx_nr, font_size_sup, nr))
		c1 = c2


	svgfile.write('</svg>')
	svgfile.close()


