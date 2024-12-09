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
    hexahedra_group = root_group.get("UnstructuredCells/Hexa27/Cell2Node")
    # hexahedra_cad_group = root_group.get(
    #     "UnstructuredCells/Hexa27/CellAttributes/CADGroupID"
    # )
    # num_hexahedra = len(hexahedra_group)
    hexahedra = hexahedra_group[:, :]
    hexahedra += 1
    # hexahedra_cad = hexahedra_cad_group[:]
    # print("Hexahedra", num_hexahedra)
    # print(hexahedra)
    # print(hexahedra_cad)

    # Load prisms
    prisms_group = root_group.get("UnstructuredCells/Prism18/Cell2Node")
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
    pyramids_group = root_group.get("UnstructuredCells/Pyra14/Cell2Node")
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
    tetrahedra_group = root_group.get("UnstructuredCells/Tetra10/Cell2Node")
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
    quads_group = root_group.get("UnstructuredCells/Quad9/Cell2Node")
    quads_cad_group = root_group.get(
        "UnstructuredCells/Quad9/CellAttributes/CADGroupID"
    )
    # num_quads = len(quads_group)
    quads = quads_group[:, :]
    quads += 1
    quad_surfaces = quads_cad_group[:]
    # print("Quads", num_quads)
    # print(quads)
    # print(quad_surfaces)

    # Load triangles
    triangles_group = root_group.get("UnstructuredCells/Tri6/Cell2Node")
    triangles_cad_group = root_group.get(
        "UnstructuredCells/Tri6/CellAttributes/CADGroupID"
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

    f = open(filename, "w")
    line = "HEX {num_hex} PRI {num_prisms} PYR {num_pyrs} TET {num_tets} QUAD {num_quads} TRI {num_tris} VERT {num_nodes}"
    fline = line.format(
        num_hex=len(hexahedra),
        num_prisms=len(prisms),
        num_pyrs=len(pyramids),
        num_tets=len(tetrahedra),
        num_quads=len(quads),
        num_tris=len(triangles),
        num_nodes=len(vertices),
    )
    f.write(fline + "\n")

    # Add the extra columns for triangles and quads
    quad_surfaces = quad_surfaces[
        :, np.newaxis
    ]  # Turn the 1D surface array into a 2D (n,1) array
    combined_quads = np.hstack(
        (quads, quad_surfaces, quad_surfaces)
    )  # Join them all together (n,9) + (n,1) + (n,1) = (n,11)

    triangle_parents = np.zeros(
        (len(triangles), 1), dtype=np.int32
    )  # Create a vector of zeros - Make sure the data type is an integer*4
    triangle_surfaces = triangle_surfaces[
        :, np.newaxis
    ]  # Turn the 1D surface array into a 2D (n,1) array
    combined_triangles = np.hstack(
        (triangles, triangle_parents, triangle_surfaces)
    )  # Join them all together (n,6) + (n,1) + (n,1) = (n,8)

    write_table(f, "Hexahedra", hexahedra)
    write_table(f, "Prisms", prisms)
    write_table(f, "Pyramids", pyramids)
    write_table(f, "Tetrahedra", tetrahedra)
    write_table(f, "Quads", combined_quads)
    write_table(f, "Triangles", combined_triangles)
    write_table(f, "Vertices", vertices)

    f.close()


def write_table(f, label, table):
    print("Writing ", label, len(table))
    f.write(f"{label} {str(len(table))}\n")
    for row_num, row in enumerate(table, 1):
        line = str(row_num) + " "
        line += " ".join( [str(i) for i in row] ) + "\n"
        f.write(line)
        # for i in row:
        #     line += " " + str(i)
        # f.write(line + "\n")
