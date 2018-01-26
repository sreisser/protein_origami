#!/usr/bin/python

import sys, re, math, AA_Data as aa
import numpy as np
from Input import *
from geometry import *

def write_head(svgfile):
	svgfile.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?> 
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" 
  "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink">
''' % (page_width, page_height))

# vertical lines
	if not "mesh" in repres:
		svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
	''' % (vert_line_l[0][0], vert_line_l[0][1], vert_line_l[1][0], vert_line_l[1][1], other_colors['grey']))

def write_cut_first_page(svgfile, height):
	if height > 0:	
		svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M %5.3f %5.3f l%5.3f %5.3f l%5.3f %5.3f " />
</g>''' % (0, height, vert_line_r[0][0], 0 , 0 , page_height ))
		add_scissors(svgfile, [40, height], 90)
	else:
		svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M %5.3f %5.3f l%5.3f %5.3f " />
</g>''' % (vert_line_r[0][0], 0 , 0 , page_height ))
		add_scissors(svgfile, [vert_line_r[0][0], 20], 180)

def write_cut_middle_page(svgfile):
	svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M %5.3f %5.3f l%5.3f %5.3f l%5.3f %5.3f" />
</g>''' % (vert_line_r[0][0], 0 , 0 , first_res_y, -vert_line_r[0][0], 0 ))
	add_scissors(svgfile, [vert_line_r[0][0], 20], 180)

def write_cut_last_page(svgfile, height):
	svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M %5.3f %5.3f l%5.3f %5.3f l%5.3f %5.3f l%5.3f %5.3f" />
</g>''' % (0, height,  vert_line_r[0][0], 0 ,  0 , first_res_y-height, -vert_line_r[0][0], 0))
	if height < 0:
		add_scissors(svgfile, [vert_line_r[0][0], 20], 180)
	else:
		add_scissors(svgfile, [40, height], 90)
		
		

def write_tail(svgfile, info):
	if info == 'yes':
		write_info(svgfile)

	svgfile.write('</svg>')
	svgfile.close()

def write_info(svgfile):
	svgfile.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%.1fpx; text-align:center; text-anchor:left; font-family:Liberation Sans">
	''' % (130, page_height-70+shift_info, 'black', 'normal', font_size_info))
	svgfile.write('''       <tspan >
			Name:
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
			Sequence:
		</tspan>
	''' % (130, page_height-45+shift_info))
	if write_charge:
		svgfile.write('''	<tspan x="%5.3f" y="%5.3f">
			Charge:
		</tspan>
	''' % (130, page_height-20+shift_info))
	svgfile.write('''</text>
	''')

	svgfile.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%.1fpx; text-align:center; text-anchor:left; font-family:Liberation Sans">
	''' % (280, page_height-70+shift_info, 'black', 'normal', font_size_info))
	svgfile.write('''       <tspan >
	%s
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
	%s
		</tspan>
	''' % (name, 280, page_height-45+shift_info, sequence))
	if write_charge:
		svgfile.write('''	<tspan x="%5.3f" y="%5.3f">
	%s
		</tspan>
	''' % (280, page_height-20+shift_info, charge))
		pH_x = 350
	else:
		pH_x = 280
	svgfile.write('''	<tspan x="%5.3f" y="%5.3f"><![CDATA[
	pH: %s]]>
		</tspan>
	''' % (pH_x, page_height-20+shift_info, pH_string))
	if write_mass:
		svgfile.write('''       
		<tspan x="%5.3f" y="%5.3f">
	Mass: %s au
		</tspan>
		''' % (450, page_height-20+shift_info, mass))
	svgfile.write('''   
	</text>
	''') 


def draw_amino_acid(file, cx, cy, letter, nr, term):
	if term != '':
		i_circle_radius = term_circle_radius
		if input['-cl'] == 'bw':
			fill_color = "white"
		else:
			fill_color = aa.color_map[term]
	else:
		i_circle_radius = circle_radius
		if input['-cl'] == 'bw':
			fill_color = "white"
		else:
			fill_color = aa.color_map[letter.upper()]
	if letters == 3:
		print_name = aa.name_map[letter.upper()]
		if print_name[-1] in ["a", "e", "t"]:
			dx_nr = dx_nr1
		else:
			dx_nr = dx_nr2
	else:
		print_name = letter.upper()
		dx_nr = 0
	if fill_color in ('dark-blue', 'red'):
		i_font_color = 'white'
	else:
		i_font_color = font_color
#	print "fill_vor %s color : %s" % (color, i_font_color)
	for key, x in enumerate(cx):
		file.write('''<circle cx="%5.3f" cy="%5.3f" r="%.1f" stroke="black" stroke-width="2" fill="%s" />
	''' % (x, cy, i_circle_radius, aa.colors[fill_color]))
		if mesh == 'horiz':
			rotate = 'transform="rotate(-90, %5.3f, %5.3f)"' % (x, cy)
		else:
			rotate = ''
		file.write('''<text x="%5.3f" y="%5.3f" %s style="fill:%s; font-weight:%s; font-size:%.1fpx; text-align:center; text-anchor:middle; font-family:Liberation Sans">''' % (x, cy + circle_radius/5.0, rotate , i_font_color, font_weight, font_size))

# N-terminal modifications
		if term == 'NH3':
			if pH == "ge8":
				file.write('<tspan style="font-size:%.1fpx" dy="%.1f">NH</tspan>\n' % (gm_n_termini['NH3']['font-size'], gm_n_termini['NH3']['dy1']))
				file.write(' <tspan style="font-size:%.1fpx" dy="%.1fpx" >2</tspan>\n</text>\n' % (gm_n_termini['NH3']['font-size_sub'], gm_n_termini['NH3']['dy4']))
			else:
				file.write('<tspan dy="%.1fpx" style="font-size:%.1fpx">NH</tspan>\n' % (gm_n_termini['NH3']['dy1'], gm_n_termini['NH3']['font-size']))
				file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx">+</tspan>\n' % (gm_n_termini['NH3']['font-size_sup'], gm_n_termini['NH3']['dy2']))
 				file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx" dx="%.1fpx" >3</tspan>\n</text>\n' % (gm_n_termini['NH3']['font-size_sub'], gm_n_termini['NH3']['dy3'], gm_n_termini['NH3']['dx']))
		elif term == 'ACE':
			file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx">CH</tspan>\n' % (gm_n_termini['ACE']['font-size'], gm_n_termini['ACE']['dy1'])) 
			file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx">3</tspan>\n' % (gm_n_termini['ACE']['font-size_sub'], gm_n_termini['ACE']['dy2']))
			file.write('<tspan  dy="%.1f" style="font-size:%.1fpx">-CO</tspan>\n</text>\n' % (gm_n_termini['ACE']['dy3'], gm_n_termini['ACE']['font-size']))
		elif term == 'FOR':
			file.write('<tspan style="font-size:%.1fpx" dy="%.1f">HCO</tspan>\n</text>\n' % (gm_n_termini['FOR']['font-size'], gm_n_termini['FOR']['dy'] ))
		elif term == 'ACY':
			file.write('<tspan style="font-size:%.1fpx" dy="%.1f">R-CO</tspan>\n</text>\n' % (gm_n_termini['ACY']['font-size'], gm_n_termini['ACY']['dy']  ))

# C-terminal modifications
		elif term == 'COO':
			file.write('<tspan dy="%.1f" style="font-size:%.1fpx">COO</tspan>\n' % (gm_c_termini['COO']['dy1'], gm_c_termini['COO']['font-size']))
			file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx">-</tspan>\n</text>' % (gm_c_termini['COO']['font-size_sup'], gm_c_termini['COO']['dy2']))
		elif term == 'NME':
			file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx">NH-CH</tspan>\n' % (gm_c_termini['NME']['font-size'], gm_c_termini['NME']['dy1']))
			file.write('<tspan style="font-size:%.1fpx" dy="%.1f">3</tspan>\n</text>' % ( gm_c_termini['NME']['font-size_sub'], gm_c_termini['NME']['dy2']))
		elif term == 'NHE':
			file.write('<tspan style="font-size:%.1fpx" dy="%.1f">NH</tspan>\n' % (gm_c_termini['NHE']['font-size'], gm_c_termini['NHE']['dy1']))
 			file.write('<tspan style="font-size:%.1fpx" dy="%.1fpx" >2</tspan>\n</text>\n' % (gm_c_termini['NHE']['font-size_sub'], gm_c_termini['NHE']['dy2']))
		elif term == 'LIP':
			file.write('<tspan dy="%.1f" style="font-size:%.1fpx">NH-R</tspan>\n </text>\n' % (gm_c_termini['LIP']['dy'], gm_c_termini['LIP']['font-size']))


# normal residues
		else:
			if re.match("^[a-z](?<!g)$", letter):
				file.write(''' <tspan dy="%.1fpx" style="font-size:%.1fpx">D</tspan>
		''' % (-term_font_size_sup, font_size_sup))
				file.write('''	<tspan dy="%.1fpx" >''' % term_font_size_sup)
			else:
				file.write('''	<tspan  > ''')
			file.write('''
	%s
	</tspan>
	<tspan dy="%.1fpx" dx="%.1fpx" style="font-size:%.1fpx">%d</tspan>
	</text>
	''' % (print_name, dy_nr, dx_nr, font_size_sup, nr))

def draw_skew_line(turn, key, svgfile, page):
	if init_shift == 0 or turn > 0 or page > 1:
		x1 = start_skew_line[0]
		y1 = start_skew_line[1] + turn*slope[1]
	else:
		first_shift = (init_shift*pitch % 360.0)/pitch
		x1 = start_skew_line[0] + slope[0]*first_shift/res_per_turn
		y1 = start_skew_line[1] + (turn+ first_shift/res_per_turn)*slope[1]
	if math.floor((n_aa-1  + init_shift)/res_per_turn) == math.floor((key + init_shift)/res_per_turn):
		last_shift = ((n_aa-1+init_shift)*pitch % 360.0)/pitch	
	#	print last_shift
		x2 = start_skew_line[0] + slope[0]*last_shift/res_per_turn
		y2 = start_skew_line[1] + (turn+ last_shift/res_per_turn)*slope[1]
	else:
		x2 = start_skew_line[0] + slope[0]
		y2 = start_skew_line[1] + (turn+1)*slope[1]
	svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
''' % (x1, y1, x2, y2, other_colors['grey']))

def draw_skew_lines(init_shift, pitch, n_aa, svgfile, page, n_turns, n_pages, cterm):
	x = (n_aa-1 + float(init_shift) % res_per_turn)  / res_per_turn
	max_row = math.floor(x) % n_turns
	if np.abs(math.ceil(x) - x) < 1e-6:
		max_row = math.ceil(x) % n_turns
		if max_row == 0 and not cterm:
			max_row = n_turns
			
	for turn in range(n_turns):
		if init_shift == 0 or turn > 0 or page > 1:
			x1 = start_skew_line[0]
			y1 = start_skew_line[1] + turn*slope[1]
		else:
			first_shift = (init_shift*pitch % 360.0)/pitch
			x1 = start_skew_line[0] + slope[0]*first_shift/res_per_turn
			y1 = start_skew_line[1] + (turn+ first_shift/res_per_turn)*slope[1]
		if page == n_pages and turn == max_row:
			last_shift = ((n_aa-1+init_shift)*pitch % 360.0)/pitch	
		#	print last_shift
			x2 = start_skew_line[0] + slope[0]*last_shift/res_per_turn
			y2 = start_skew_line[1] + (turn+ last_shift/res_per_turn)*slope[1]
		else:
			x2 = start_skew_line[0] + slope[0]
			y2 = start_skew_line[1] + (turn+1)*slope[1]
		svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
''' % (x1, y1, x2, y2, other_colors['grey']))
		if page == n_pages and turn == int(max_row):
			break

def draw(r):
	global repres, svgfile, vert_line_l, vert_line_r, res_per_turn, slope, page_height, page_width
	global shift_info, first_res_y, mesh, start_skew_line, n_aa
	repres = r
	page_height = 1051
	page_width = 744
	slope = (630.0, -160.0)
	vert_line_r = [(690, 22), (690, 1030)]
	first_res_y = page_height - (page_height + slope[1]*5)/2 - circle_radius
	start_skew_line = (60.0, first_res_y)
	vert_line_l = [(60, 22), (60, 1030)]
	res_per_turn = 360.0/pitch
	if not re.match("^.*\.svg$", input["-o"]):
		filename_base = input["-o"]
	else:
		filename_base = input["-o"][:-4]

	if re.match("^[a-zG\s]+$", sequence):
		slope = (-630.0, -160.0)
		start_skew_line = (690.0, first_res_y)

	if "mesh" in repres:
		shift_info = 100
		if "vert" in repres: 	mesh = "vert"
		elif "horiz" in repres: mesh = "horiz"
	else:
		shift_info = 0
		mesh = ""

	max_pos_per_page = int(math.floor(1800.0/pitch)) 
	if input["-cter"]  != "":
		cterm = True
	else:
		cterm = False

	n_aa = len(sequence_list)
	
	if n_aa > max_pos_per_page or (n_aa == max_pos_per_page and cterm):
		if "mesh" in repres:
			multi_page = 'no'
			n_pages = 1
		else:
			multi_page = 'yes'
			n_pages = math.ceil(float(n_aa-1+(init_shift%res_per_turn))/max_pos_per_page)
			if ( n_aa+(init_shift%res_per_turn)) % max_pos_per_page == 1. and cterm:
				n_pages += 1
	else:
		multi_page = 'no'
		n_pages = 1

	page = 1
	if multi_page == 'no':
		svgfile = open(filename_base+'.svg', "w")
		write_head(svgfile)
		max_pos_per_page = 100
		n_rows = 100
	else:
		svgfile = open("%s_%d.svg" % (filename_base, page), "w")
		write_head(svgfile)
		n_rows = 5
	draw_skew_lines(init_shift, pitch, n_aa, svgfile, page, n_rows, n_pages, cterm)
	

	shift = 0
	for key, letter in enumerate(sequence_list):
		nr = key + start_index
		old_shift = shift
		shift = ( (key+init_shift) *pitch % 360.0)/pitch
		x = (key + float(init_shift) % res_per_turn)  / res_per_turn
		row = math.floor(x) % n_rows
		if np.abs(math.ceil(x) - x) < 1e-6:
			row = math.ceil(x) % n_rows
	
		cx = []
		cx.append(start_skew_line[0] + shift*slope[0]/res_per_turn)
		cy = start_skew_line[1] + shift*slope[1]/res_per_turn + slope[1]*row

		if mesh == '':
		# if last circle overlapped with horizontal cutting edge of this page, add last circle on current page	
			cy_last = start_skew_line[1] + old_shift*slope[1]/res_per_turn + slope[1]*(row-1)
			if key > 0 and row == 0 and 0 < cy_last - first_res_y < circle_radius:
				cx_last = []
				cx_last.append(start_skew_line[0] + old_shift*slope[0]/res_per_turn)
				if vert_line_r[0][0] - cx_last[0] < circle_radius and mesh == '':
					cx_last.append(cx_last[0] - vert_line_r[0][0] + vert_line_l[0][0])
				elif cx_last[0] - vert_line_l[0][0] < circle_radius and mesh == '':
					cx_last.append(cx_last[0] + vert_line_r[0][0] - vert_line_l[0][0])
				cy_last += slope[1] * row 
				draw_amino_acid(svgfile, cx_last, cy_last, sequence_list[key-1], nr-1, '')



		# if circle overlapping with cutting edge, add same circle on opposite side
			if vert_line_r[0][0] - cx[0] < circle_radius:
				cx.append(cx[0] - vert_line_r[0][0] + vert_line_l[0][0])
			elif cx[0] - vert_line_l[0][0] < circle_radius:
				cx.append(cx[0] + vert_line_r[0][0] - vert_line_l[0][0])

		draw_amino_acid(svgfile, cx, cy, letter, nr, '')
 

	# page break, if next res is first one to go on next page	
		if (multi_page == 'yes' and 0 <= pitch*(key+1+(init_shift%res_per_turn))%1800.0 < pitch 
			and (0 < key+1 < n_aa)): # or (key+1 == n_aa and cterm))):

		# if next circle overlaps with horizontal cutting edge of next page, add same circle on current page	
			shift_next = ((key+1+init_shift) * pitch % 360.0)/pitch
			x = (key + 1 + float(init_shift) % res_per_turn)  / res_per_turn
			row_next = math.floor(x) % n_rows
			if np.abs(math.ceil(x) - x) < 1e-6:
				row_next = math.ceil(x) % n_rows
			cy = start_skew_line[1] + shift_next*slope[1]/res_per_turn + slope[1]*row_next
			if first_res_y - cy < circle_radius:
				cx = []
				cx.append(start_skew_line[0] + shift_next*slope[0]/res_per_turn)
				if vert_line_r[0][0] - cx[0] < circle_radius and mesh == '':
					cx.append(cx[0] - vert_line_r[0][0] + vert_line_l[0][0])
				elif cx[0] - vert_line_l[0][0] < circle_radius and mesh == '':
					cx.append(cx[0] + vert_line_r[0][0] - vert_line_l[0][0])
				cy += slope[1] * (row + 1)
				draw_amino_acid(svgfile, cx, cy, sequence_list[key+1], nr+1, '')

			if page == 1:
				write_cut_first_page(svgfile, 0)
				write_tail(svgfile, 'yes')
			elif page < n_pages:
				write_cut_middle_page(svgfile)
				write_tail(svgfile, 'no')
			if page < n_pages:
				page += 1
				svgfile = open("%s_%d.svg" % (filename_base, page), "w")
				write_head(svgfile)
				draw_skew_lines(init_shift, pitch, n_aa, svgfile, page, n_rows, n_pages, cterm)


		if input["-nter"]  != "" and key == 0:
			cy +=  (circle_radius + term_circle_radius)
			draw_amino_acid(svgfile, cx, cy, letter, nr, input["-nter"]) 
		elif cterm and (key+1) == n_aa:
			dist_cut = term_circle_radius + 40
			cy -=  (circle_radius + term_circle_radius)
			draw_amino_acid(svgfile, cx, cy, letter, nr, input["-cter"])
		else:
			dist_cut = circle_radius + 40
		if key+1 == n_aa or (multi_page == "yes" and key+2 == n_aa and pitch*(key+1+init_shift%res_per_turn)%1800.0 == 0 and not cterm):
			if multi_page == 'no':
				info = 'yes'
				if not "mesh" in repres:
					write_cut_first_page(svgfile, cy - dist_cut)
			else:
				info = 'no'
				write_cut_last_page(svgfile, cy - dist_cut)
			write_tail(svgfile, info)
			break


