#!/bin/bash

ln -s python/main.py protein_ORIGAMI
chmod +x protein_ORIGAMI

echo -e "\n\nexport PATH=$PWD:\$PATH" >> ~/.bashrc

echo -e "Added current directory to your path variable.\nPlease run '. ~/.bashrc'."
echo "Then start program with 'protein_ORIGAMI'"
