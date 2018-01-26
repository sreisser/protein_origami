# Protein ORIGAMI - a program for the creation of 3D peptide paper models

Protein ORIGAMI (http://ibg.kit.edu/protein_origami) is a browser-based web application that allows the user to create straightforward 3D paper models of folded peptides for research, teaching and presentations. An amino acid sequence can be turned into alpha-helices,beta-strands and random coils that can be printed out and folded into properly scaled models, with a colour code denoting the biophysical characteristics of each amino acid residue (hydrophobicity, charge, etc.). These models provide an intuitive visual and tactile understanding of peptide interactions with other partners, such as helix-helix assembly, oligomerization, membrane binding, or pore formation. Helices can also be displayed as a helical wheel or helical mesh in 2D graphics, to be used in publications or presentations. The highly versatile programme Protein ORIGAMI is also suited to create less conventional helices with arbitrary pitch (e.g. 3_10-helix, π-helix, or left-handed helices). Non-canonical amino acids, labels and different terminal modifications can be defined and displayed at will, and different protonation states can be shown. 

The python code which generates the figures in SVG format can be downloaded here and installed locally on a PC. The figures can then be viewed and/or converted to PDF or PNG using a SVG editing program, we recommend inkscape (inkscape.org).

For bugs, questions or comments contact Sabine at sabine dot reisser (guesswhat) gmail dot com.

##INSTALLATION

1) Use git: 

		git clone https://github.com/sabinereisser/protein_origami

		cd protein_origami	

   or
   Download https://github.com/sabinereisser/protein_origami/archive/master.zip	

   		unzip protein_origami-master.zip

		cd protein_origami-master

2) Run install script	

		bash install.sh

		. ~/.bashrc
3) Run program

		protein_ORIGAMI	


##CONVERSION WITH INKSCAPE

SVG files can be converted to PDF or PNG 
- via the graphical interface: 

	File -> Save as (Select PDF; always for 3D paper models)

	File -> Export PNG Image 
- via the command line:

	for 3D paper models, convert to PDF (seperately for each *_1.svg *_2.svg etc.):

		inkscape  name_1.svg  -A name_1.pdf

	for PNG format

		inkscape  name.svg  -e name.png -D -b white -d 300

		-d is the option for dpi, if you want higher quality, increase
