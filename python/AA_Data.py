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


import sys, re, math


# data definitions
name_map = {"A":"Ala", "C":"Cys", "D":"Asp", "E":"Glu", "F":"Phe", "G":"Gly", "H":"His", "I":"Ile", "K":"Lys", "L":"Leu", "M": "Met", "N":"Asn", "O":"Orn", "P":"Pro", "Q":"Gln", "R":"Arg", "S":"Ser", "T":"Thr", "V":"Val", "W":"Trp", "Y":"Tyr"}

charge_map = {
"D" : -1,
"E" : -1,
"R" : 1,
"K" : 1,
"H" : 1,
"A": 0, 
"C": 0, 
"F": 0, 
"G": 0, 
"I": 0, 
"L": 0, 
"M":  0, 
"N": 0, 
"O": 1,
"P": 0, 
"Q": 0, 
"S": 0, 
"T": 0, 
"V": 0, 
"W": 0, 
"Y": 0
}
charge_map_term = {
"NH3": 1,
"COO": -1,
"FOR": 0,
"ACY": 0,
"LIP": 0,
"ACE": 0,
"NHE" : 0,
"NME": 0,
}

charge_map.update(charge_map_term)

basic_charges = {
"H": 0,
"NH3": 0
}

color_map = {
"A":"yellow", 
"C":"green", 
"D":"red", 
"E":"red", 
"F":"yellow", 
"G":"green", 
"H":"dark-blue", 
"I":"yellow", 
"K":"dark-blue", 
"L":"yellow", 
"M": "yellow", 
"N":"light-blue", 
"O": "dark-blue",
"P":"green", 
"Q":"light-blue", 
"R":"dark-blue", 
"S":"light-blue", 
"T":"light-blue", 
"V":"yellow", 
"W":"yellow", 
"Y":"yellow"
}

n_term_map = {
"NH3": "dark-blue",
"FOR": "yellow",
"ACY": "yellow",
"ACE": "yellow",
}

c_term_map = {
"LIP": "yellow",
"NHE" : "yellow",
"COO" : "red",
"NME": "yellow"
}

basic_colors = {
"NH3": "yellow",
"H": "light-blue"
}
color_map.update(n_term_map)
color_map.update(c_term_map)
	

mass_map = {
"A": 71.07,
"C": 103.14,
"E": 129.11,
"D": 115.08,
"G": 57.05,
"F": 147.17,
"I": 113.16,
"H": 137.14,
"K": 128.17,
"M": 131.19,
"L": 113.15,
"O": 99.12,
"N": 114.10,
"Q": 128.13,
"P": 97.11,
"S": 87.07,
"R": 156.18,
"T": 101.10,
"W": 186.21,
"V": 99.13,
"Y": 163.17,
# n-termini
"NH3": 2.02,
"ACE": 43.04 ,
# c-termini
"NHE" : 16.02,
"COO" : 16.00,
"NME": 30.05
}



colors = { 
"yellow": "#fffa00",
"green" : "#00d436",
"red" : "#ff0000",
"dark-blue" : "#0023ae",
"light-blue" : "#00d9ff",
"white" : "#ffffff"
}

