import fortio
import numpy as np

hexahedra = None
prisms = None
pyramids = None
tetrahedra = None
quads = None
triangles = None
vertices = None
quad_surfaces = None
triangle_surfaces = None

def load_mesh(file):
    global hexahedra, prisms, pyramids, tetrahedra, quads, triangles, vertices, quad_surfaces, triangle_surfaces  # Naughty global variables

    root_group = file["FS:Mesh"]

    # Load vertices
    vertices_group = root_group.get("UnstructuredCells/Datasets/Coordinates/Values")
    # num_vertices = len(vertices_group)
    vertices = vertices_group[:, :]
    # print("Vertices", vertices.shape)
    # print(vertices)

    # Load hexahedra
    hexahedra_group = root_group.get("UnstructuredCells/Hexa8/Cell2Node")
    # hexahedra_cad_group = root_group.get(
    #     "UnstructuredCells/Hexa8/CellAttributes/CADGroupID"
    # )
    # num_hexahedra = len(hexahedra_group)
    hexahedra = hexahedra_group[:, :]
    hexahedra += 1
    # hexahedra_cad = hexahedra_cad_group[:]
    # print("Hexahedra", num_hexahedra)
    # print(hexahedra)
    # print(hexahedra_cad)

    # Load prisms
    prisms_group = root_group.get("UnstructuredCells/Prism6/Cell2Node")
    # prisms_cad_group = root_group.get(
    #     "UnstructuredCells/Prism6/CellAttributes/CADGroupID"
    # )
    # num_prisms = len(prisms_group)
    prisms = prisms_group[:, :]
    prisms += 1
    # prisms_cad = prisms_cad_group[:]
    # print("Prisms", num_prisms)
    # print(prisms)
    # print(prisms_cad)

    # Load pyramids
    pyramids_group = root_group.get("UnstructuredCells/Pyra5/Cell2Node")
    # pyramids_cad_group = root_group.get(
    #     "UnstructuredCells/Pyra5/CellAttributes/CADGroupID"
    # )
    # num_pyramids = len(pyramids_group)
    pyramids = pyramids_group[:, :]
    pyramids += 1
    # pyramids_cad = pyramids_cad_group[:]
    # print("Pyramids", num_pyramids)
    # print(pyramids)
    # print(pyramids_cad)

    # Load tetrahedra
    tetrahedra_group = root_group.get("UnstructuredCells/Tetra4/Cell2Node")
    # tetrahedra_cad_group = root_group.get(
    #     "UnstructuredCells/Tetra4/CellAttributes/CADGroupID"
    # )
    # num_tetrahedra = len(tetrahedra_group)
    tetrahedra = tetrahedra_group[:, :]
    tetrahedra += 1
    # tetrahedra_cad = tetrahedra_cad_group[:]
    # print("Tetrahedra", num_tetrahedra)
    # print(tetrahedra)
    # print(tetrahedra_cad)

    # Load quads
    quads_group = root_group.get("UnstructuredCells/Quad4/Cell2Node")
    quads_cad_group = root_group.get(
        "UnstructuredCells/Quad4/CellAttributes/CADGroupID"
    )
    # num_quads = len(quads_group)
    quads = quads_group[:, :]
    quads += 1
    quad_surfaces = quads_cad_group[:]
    # print("Quads", num_quads)
    # print(quads)
    # print(quad_surfaces)

    # Load triangles
    triangles_group = root_group.get("UnstructuredCells/Tri3/Cell2Node")
    triangles_cad_group = root_group.get(
        "UnstructuredCells/Tri3/CellAttributes/CADGroupID"
    )
    # num_triangles = len(triangles_group)
    triangles = triangles_group[:, :]
    triangles += 1
    triangle_surfaces = triangles_cad_group[:]
    # print("Triangles", num_triangles)
    # print(triangles)
    # print(triangle_surfaces)


def write_mesh(filename):
    global hexahedra, prisms, pyramids, tetrahedra, quads, triangles, vertices, quad_surfaces, triangle_surfaces  # Naughty global variables

    # Construct Flite arrays
    numElements = len(hexahedra) + len(prisms) + len(pyramids) + len(tetrahedra)
    numFaces = len(triangles) + len(quads)
    header = np.array(
        [
            numElements,
            len(vertices),
            numFaces,
            len(hexahedra),
            len(prisms),
            len(pyramids),
            len(tetrahedra),
            len(quads),
            len(triangles),
        ],
        dtype=np.int32,
    )
    # print(header)
    # print(header.shape)
    # print(np.asarray(header))

    # Add the extra columns for triangles and quads
    quad_surfaces = quad_surfaces[
        :, np.newaxis
    ]  # Turn the 1D surface array into a 2D (n,1) array
    combined_quads = np.hstack(
        (quads, quad_surfaces, quad_surfaces)
    )  # Join them all together (n,4) + (n,1) + (n,1) = (n,6)

    triangle_parents = np.zeros(
        (len(triangles), 1), dtype=np.int32
    )  # Create a vector of zeros - Make sure the data type is an integer*4
    triangle_surfaces = triangle_surfaces[
        :, np.newaxis
    ]  # Turn the 1D surface array into a 2D (n,1) array
    combined_triangles = np.hstack(
        (triangles, triangle_parents, triangle_surfaces)
    )  # Join them all together (n,3) + (n,1) + (n,1) = (n,5)

    # Vectorise the arrays for Flite
    flite_hexahedra = hexahedra.transpose()
    flite_prisms = prisms.transpose()
    flite_pyramids = pyramids.transpose()
    flite_tetrahedra = tetrahedra.transpose()
    flite_vertices = vertices.transpose()
    flite_triangles = combined_triangles.transpose()
    flite_quads = combined_quads.transpose()

    # Bug in the fortio library - cannot create file when one isn't there already so we quickly create one
    f = open(filename, "w")
    f.close()

    with fortio.FortranFile(filename, mode="w") as f:
        f.write_record(header)
        f.write_record(flite_hexahedra)
        f.write_record(flite_prisms)
        f.write_record(flite_pyramids)
        f.write_record(flite_tetrahedra)
        f.write_record(flite_vertices)
        f.write_record(flite_quads)
        f.write_record(flite_triangles)
