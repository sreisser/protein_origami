#!/usr/bin/python

import sys, re, math, AA_Data as aa
from Input import *
from geometry import *




def  write_head(svgfile, page_width, page_height, key, n_aa):
	svgfile.write('''<?xml version="1.0" encoding="UTF-8" standalone="no"?> 
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" 
  "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg width="%d" height="%d" xmlns="http://www.w3.org/2000/svg"
  xmlns:xlink="http://www.w3.org/1999/xlink">
''' % (page_width, page_height))

# vertical
	if (n_aa - key) >= 9:
		line_1 = line_2 = line_length
	elif (n_aa - key ) <= 4:
		line_1 = y_interval * (n_aa - key -1)
		line_2 = 0
	elif (n_aa - key) == 5:
		line_1 = line_length
		line_2 = 0
	else:
		line_1 = line_length
		line_2 = y_interval * (n_aa-key-5)
	for i in xrange(0,3):
		x1 = vert_line_l[0][0] + i * x_interval
		y1 = vert_line_l[0][1]
		x2 = x1
		y2 = y1 + line_1
		svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
	''' % (x1, y1-circle_radius, x2, y2+circle_radius, other_colors['grey']))

	for j in xrange(4,7):
		x1 = vert_line_l[0][0] + j * x_interval
		y1 = vert_line_l[0][1]
		x2 = x1
		y2 = y1 + line_2
		if line_2 != 0:
			svgfile.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
	''' % (x1, y1-circle_radius, x2, y2+circle_radius, other_colors['grey']))
	svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M%5.3f %5.3f l0 %5.3f " />
</g>''' % (vert_line_l[0][0] + 3 * x_interval, vert_line_l[0][1]-circle_radius, line_length+2*circle_radius+2*term_circle_radius))
	if (n_aa - key > 5):
		svgfile.write('''<g fill="none" stroke="black" stroke-width="1">
    <path stroke-dasharray="5,5" d="M%5.3f %5.3f l%5.3f 0" />
</g>''' % (vert_line_l[0][0] + 3 * x_interval, vert_line_l[0][1]-circle_radius,x_interval*4))



def write_tail(svgfile, info):
	if info == 'yes':
		write_info(svgfile)
	add_scissors(svgfile, [vert_line_l[0][0] + 3 * x_interval,1025.2399], 0)
	svgfile.write('</svg>')
	svgfile.close()

def write_info(svgfile):
	svgfile.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%dpx; text-align:center; text-anchor:left; font-family:Liberation Sans">
	''' % (130, page_height-70, 'black', 'normal', font_size_info))
	svgfile.write('''       <tspan >
			Name:
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
			Sequence:
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
			Charge:
		</tspan>
	</text>
	''' % (130, page_height-45, 130, page_height-20))

	svgfile.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%dpx; text-align:center; text-anchor:left; font-family:Liberation Sans">
	''' % (280, page_height-70, 'black', 'normal', font_size_info))
	svgfile.write('''       <tspan >
	%s
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
	%s
		</tspan>
		<tspan x="%5.3f" y="%5.3f">
	%s
		</tspan>
		<tspan x="%5.3f" y="%5.3f"><![CDATA[
	pH: %s]]>
		</tspan>

	</text>
	''' % (name, 280, page_height-45, sequence, 280, page_height-20, charge, 400, page_height-20, pH_string))

def draw_dummy_circle(file, side):
	if side == 'left':
		cx1 = vert_line_l[0][0]
		cy1 = vert_line_l[0][1] + line_length
		cx2 = vert_line_l[0][0] + 2*x_interval
		cy2 = cy1
	elif side == 'right':
		cx1 = vert_line_l[0][0] + 4*x_interval
		cy1 = vert_line_l[0][1] + line_length
		cx2 = vert_line_l[0][0] + 6*x_interval
		cy2 = cy1
	file.write('''<circle cx="%5.3f" cy="%5.3f" r="%d" stroke="black" stroke-width="2" fill="%s" />
	''' % (cx1, cy1, circle_radius, 'white'))
	file.write('''<circle cx="%5.3f" cy="%5.3f" r="%d" stroke="black" stroke-width="2" fill="%s" />
	''' % (cx2, cy2, circle_radius, 'white'))




def draw_amino_acid(file, letter, nr, key, n_aa, term):
	p1 = {}
	p2 = {}
	if (key % 8) < 4 or (key+1 == n_aa and (n_aa % 8) == 5) :
		p1['cx'] = vert_line_l[0][0]
		p1['cy'] = vert_line_l[0][1] + (key % 8)*y_interval
		p2['cx'] = vert_line_l[0][0] + 2*x_interval
		p2['cy'] = p1['cy']
	else:
		p1['cx'] = vert_line_l[0][0] + 4*x_interval
		p1['cy'] = vert_line_l[0][1] + (key % 4)*y_interval
		p2['cx'] = vert_line_l[0][0] + 6*x_interval
		p2['cy'] = p1['cy']


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
	if term in aa.n_term_map.keys():
		p1['cy'] = p1['cy'] - circle_radius - term_circle_radius
		p2['cy'] = p1['cy']
	elif  term in aa.c_term_map.keys():
		p1['cy'] = p1['cy'] + circle_radius + term_circle_radius
		p2['cy'] = p1['cy'] 
	if letters == 3:
		print_name = aa.name_map[letter.upper()]
		if print_name[-1] in ["a", "e", "t"]:
			dx_nr = dx_nr1
		else:
			dx_nr = dx_nr2
	else:
		print_name = letter.upper()
		dx_nr = 0
	if fill_color in ('dblue', 'red'):
		i_font_color = 'white'
	else:
		i_font_color = font_color

	if "random_coil" not in repres:
		if (key % 2) == 0:
			p1['fill_color'] = aa.colors[fill_color]
			p2['fill_color'] = other_colors['grey']
			p1['i_font_color'] = i_font_color
			p2['i_font_color'] = font_color
		else:
			p2['fill_color'] = aa.colors[fill_color]
			p1['fill_color'] = other_colors['grey']
			p2['i_font_color'] = i_font_color
			p1['i_font_color'] = font_color
	else:
		p1['fill_color'] = aa.colors[fill_color]
		p2['fill_color'] = p1['fill_color']
		p1['i_font_color'] = i_font_color
		p2['i_font_color'] = i_font_color

	params = [p1, p2]
        if term == '':
                if (key % 2) == 0:
                        file.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
                ''' % (p2['cx']-x_interval, p2['cy'], p2['cx']+x_interval, p2['cy'], other_colors['grey']))
                else:
                        file.write('''<line x1="%5.3f" y1="%5.3f" x2="%5.3f" y2="%5.3f" style="stroke:%s; stroke-width:2px;" />
                ''' % (p1['cx']-x_interval, p1['cy'], p1['cx']+x_interval, p1['cy'], other_colors['grey']))


	for p in params:
		file.write('''<circle cx="%5.3f" cy="%5.3f" r="%d" stroke="black" stroke-width="2" fill="%s" />
		''' % (p['cx'], p['cy'], i_circle_radius, p['fill_color']))
		file.write('''<text x="%5.3f" y="%5.3f" style="fill:%s; font-weight:%s; font-size:%.1fpx; text-anchor:middle; font-family:Liberation Sans">''' % (p['cx'], p['cy']+circle_radius/5.0,  p['i_font_color'], font_weight, font_size))

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
				file.write(''' <tspan dy="%dpx" style="font-size:%dpx">D</tspan>
		''' % (-term_font_size_sup, font_size_sup))
				file.write('''	<tspan dy="%dpx" >''' % term_font_size_sup)
			else:
				file.write('''	<tspan  > ''')
			file.write(''' %s </tspan>
		<tspan dy="%.1fpx" dx="%.1fpx" style="font-size:%.1fpx">%d</tspan>
		</text>
		''' % (print_name, dy_nr, dx_nr, font_size_sup, nr))





def draw(r):
	global repres, svgfile, vert_line_l, vert_line_r, res_per_turn, slope, page_height, page_width, line_length
	global x_interval, y_interval #, circle_radius, term_circle_radius
	repres = r
	font_size_info = 20
	page_height = 1051
	page_width = 744
	slope = (630.0, -160.0)
	circle_radius = 38
	term_circle_radius = circle_radius-6
	vert_line_l = [(100, 120), (100, 930)]
	vert_line_r = [(630, 120), (630, 930)]
	line_length = vert_line_l[1][1]-vert_line_l[0][1]
	distance_lines = vert_line_r[0][0]-vert_line_l[0][0]
	x_interval = distance_lines/6
	y_interval = line_length/4
	first_res_y = page_height - (page_height + slope[1]*5)/2 - circle_radius
	slope = (630.0, -160.0)
	start_skew_line = (60.0, first_res_y)

	res_per_turn = 3.6

	if not re.match("^.*\.svg$", input["-o"]):
		filename_base = input["-o"]
	else:
		filename_base = re.match("^(.*\).svg$", input["-o"]).group(1)

	turn = ""
	old_turn = ""
	n_aa = len(sequence_list)
	page = 0
	for key, letter in enumerate(sequence_list):
		nr = key + start_index
		if key % 8 == 0:
			max_res_per_page = 8
			if key != 0:
				old_svgfile = svgfile
			page += 1
			svgfile = open("%s_%d.svg" % (filename_base, page), "w")
			write_head(svgfile, page_width, page_height, key, n_aa)


		draw_amino_acid(svgfile, letter, nr, key, n_aa, '' )
		if (key+1) % 4 == 0 and not (n_aa-key < 3):
			if (key+1) % 8 == 0:
				draw_dummy_circle(svgfile, 'right')
			else:
				draw_dummy_circle(svgfile, 'left')

		if input["-nter"]  != "" and key == 0:
			draw_amino_acid(svgfile, letter, nr, key, n_aa, input["-nter"]) 
		if input["-cter"]  != "" and (key+1) == n_aa:
			draw_amino_acid(svgfile, letter, nr, key, n_aa, input["-cter"])

		if (key+1) % 8 == 0 or key+1 == n_aa:
			write_tail(svgfile, '')


