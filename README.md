# A simple reader for CFD Meshes from Airbus

This is a simple Python code to read CFD mesh formats from Airbus using the HDF format. Both linear meshes and quadratic meshes can be read.

These codes were designed to be used by colleagues with little Python experience so they have been kept simple on purpose.

They rely on a few Python modules listed in `requirements.txt`.

To get started, we need to create the Python environment:

- Open a terrminal window (Linux) / Command Prompt (Windows).
- Run `python -m venv venv` to create a virtual environment for this code (This step only needs to be done once)
- Run `source ./venv/bin/activate` (Linux) or `.\venv\Scripts\activate` (Windows) to activate the virtual environment
- Run `pip install -r requirements.txt` to install the modules required for this code. (This step only needs to be done once).

The codes are then ready to run.

The reader for linear meshes is used by running `python xrf_flite_reader.py`. This reads the mesh, displays the tree structure of the HDF file and then writes it out in a format called FLITE. This is a simple unformatted, binary format used by the FLITE suite of tools developed in Swansea University. However, it coud be easily converted to write in a format of your own.

The reader for quadratic meshes is used by running `python xrf_higher-order_reader.py`. This reads the mesh, displays the tree structure of the HDF fileand then writes it out in a simple textual format.
