# This program requires 3 modules to be installed.
# These are named in 'requirements.txt'
# To install these, simply run the following command:
#
#    pip install -r requirements.txt
# (For Linux, you may need to use 'pip3' instead of 'pip')
#

import h5py

from display_tree import display_tree
from flite_mesh import load_mesh, write_mesh

h5_filename = input("Please enter the H5 filename (with extension): ")
print("Loading '" + h5_filename + "'")

mesh_file = h5py.File(h5_filename, "r")

display_tree(mesh_file)

load_mesh(mesh_file)

mesh_file.close()

flite_filename = input("Please enter the FLITE mesh filename (with extension): ")
print("Saving to '" + flite_filename + "'")

write_mesh(flite_filename)
