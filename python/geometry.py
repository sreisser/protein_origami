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

def add_scissors(svgfile, start, rotation):
	svgfile.write('''
  <path
     d="m %.5f, %.5f c -0.45391,-0.1152 -0.63359,-0.2001 -0.97097,-0.4548 -0.9213,-0.6953 -1.26795,-2.1263 -0.83927,-3.4644 0.40838,-1.2746 1.50237,-2.3285 2.66897,-2.5709 0.46725,-0.098 1.23718,-0.042 1.59655,0.1152 l 0.28392,0.1232 0.91294,-1.5973 0.91295,-1.5972 -1.25119,-2.4859 c -0.68815,-1.3674 -1.64559,-3.246 -2.1276,-4.1748 -0.75741,-1.4596 -0.87964,-1.734 -0.9003,-2.0207 -0.0293,-0.4073 0.13327,-0.9596 0.40931,-1.3899 l 0.19534,-0.3045 0.10031,0.1687 c 0.0552,0.093 1.12915,1.9668 2.38648,4.1647 1.25732,2.1976 2.30238,3.9958 2.32234,3.9958 0.02,0 1.065,-1.7982 2.32234,-3.9958 1.25732,-2.1979 2.33124,-4.0719 2.38645,-4.1647 l 0.10048,-0.1687 0.19535,0.3045 c 0.27622,0.4306 0.43869,0.9826 0.40911,1.3899 -0.0208,0.2875 -0.14912,0.5732 -0.96113,2.1412 -0.51538,0.9953 -1.47247,2.8743 -2.1269,4.1759 l -1.18986,2.3661 0.91245,1.5962 0.91242,1.5965 0.28393,-0.1232 c 0.35936,-0.1568 1.1293,-0.2115 1.59655,-0.1152 1.16659,0.2424 2.26058,1.2963 2.66896,2.5709 0.43042,1.3435 0.0824,2.7687 -0.84768,3.4707 -1.47472,1.1136 -3.71077,0.3387 -4.63388,-1.6055 -0.20906,-0.4403 -0.30559,-0.8004 -0.52538,-1.9602 -0.16735,-0.8829 -0.41616,-1.7249 -0.71364,-2.4149 -0.23352,-0.5416 -0.7009,-1.3246 -0.79072,-1.3246 -0.0785,0 -0.47864,0.6407 -0.70213,1.1244 -0.31219,0.6756 -0.59509,1.5902 -0.77321,2.4994 -0.3232,1.6497 -0.45045,2.0233 -0.91592,2.6888 -0.78402,1.1213 -2.17948,1.7293 -3.30737,1.4411 z m 1.08264,-1.5861 c 0.42413,-0.1505 0.94874,-0.6539 1.18834,-1.1407 0.36125,-0.7338 0.29866,-1.6716 -0.136,-2.0373 -0.51231,-0.431 -1.26528,-0.2726 -1.9017,0.4003 -0.4714,0.4986 -0.68634,1.0171 -0.68231,1.6463 0.006,0.9629 0.65503,1.4422 1.53166,1.1314 z m 10.15419,0.021 c 0.64919,-0.3377 0.8067,-1.3731 0.34478,-2.2658 -0.18332,-0.3544 -0.7348,-0.8829 -1.07278,-1.0284 -0.60489,-0.2602 -1.11028,-0.1472 -1.41646,0.3155 -0.15168,0.2294 -0.16561,0.299 -0.16561,0.829 0,0.5316 0.016,0.611 0.19709,0.9787 0.44832,0.9105 1.49695,1.4915 2.11298,1.171 z"
     id="path2987"
     style="fill:#000000" transform="rotate(%d, %.5f, %.5f)"/>
''' % (start[0]-5.80928, start[1], rotation, start[0], start[1]))

scale = 35.0/38
circle_radius = 38 * scale
term_circle_radius = 33 * scale
term_font_size_l = 22 * scale 
term_font_size_s = 20 * scale 
term_font_size_sup = 16 * scale
dy_nr = 6 * scale
dx_nr1= 1 * scale # ending in a e t
dx_nr2= 0 # else
font_weight = 'bold'
font_color = 'black'
font_size_info = 20

gm_n_termini = {
	'NH3' : { 'font-size' :  term_font_size_s, 
		'font-size_sub' : term_font_size_sup, 
		'font-size_sup' : term_font_size_sup,
		'dy1': -0 * scale,
		'dy2': -12 * scale,
		'dy3': 20 * scale,
		'dy4': 5 * scale, 
		'dx': -9 * scale}, 
	'ACE' : { 'font-size' : 16 * scale, 
		'font-size_sub' : 12 * scale, 
		'dy1': -2 * scale,
		'dy2': 6 * scale,
		'dy3': -6 * scale}, 
	'FOR' : { 'font-size' : term_font_size_s, 
		'dy': -0 * scale,
		}, 
	'ACY' : { 'font-size' : term_font_size_s, 
		'dy': -0 * scale
		}
} 

gm_c_termini = {
	'COO' : { 'font-size' :  term_font_size_s, 
		'dy1': 0 * scale,
		'dy2': -12 * scale,
		'font-size_sup' : term_font_size_s},
	'NME' : { 'font-size' :  16 * scale, 
		'font-size_sub' : 12 * scale,
		'dy1': -4 * scale,
		'dy2': 6 * scale}, 
	'NHE' : { 'font-size' :  term_font_size_s, 
		'font-size_sub' : term_font_size_sup, 
		'dy1': -2 * scale,
		'dy2': 5 * scale},
	'LIP' : { 'font-size' :  term_font_size_s,
		'dy': -0 * scale
		}
} 


