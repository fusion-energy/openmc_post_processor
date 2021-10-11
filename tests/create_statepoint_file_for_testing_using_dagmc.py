# This minimal example makes a 3D volume and exports the shape to a stp file
# A surrounding volume called a graveyard is needed for neutronics simulations

import openmc
import openmc_dagmc_wrapper as odw
import openmc_plasma_source as ops
import paramak
from stl_to_h5m import stl_to_h5m

my_shape = paramak.ExtrudeStraightShape(
    points=[(1, 1), (1, 200), (600, 200), (600, 1)],
    distance=180,
)

my_shape.export_stl("steel.stl")

# This script converts the CAD stl files generated into h5m files that can be
# used in DAGMC enabled codes. h5m files created in this way are imprinted,
# merged, faceted and ready for use in OpenMC. One of the key aspects of this
# is the assignment of materials to the volumes present in the CAD files.

stl_to_h5m(
    files_with_tags=[("steel.stl", "mat1")],
    h5m_filename="dagmc.h5m",
)

# makes use of the previously created neutronics geometry (h5m file) and assigns
# actual materials to the material tags. Sets simulation intensity and specifies
# the neutronics results to record (know as tallies).

geometry = odw.Geometry(
    h5m_filename="dagmc.h5m",
)

materials = odw.Materials(
    h5m_filename="dagmc.h5m", correspondence_dict={"mat1": "eurofer"}
)

tally1 = odw.CellTally(
    tally_type="flux",
    target=1,
)

tally2 = odw.CellTally(
    tally_type="neutron_spectra",
    target=1,
)

tally3 = odw.CellTally(
    tally_type="TBR",
    target=1,
)

tally4 = odw.CellTally(
    tally_type="heating",
    target=1,
)

tally5 = odw.CellTally(
    tally_type="neutron_effective_dose",
    target=1,
)

tally6 = odw.CellTally(
    tally_type="photon_effective_dose",
    target=1,
)

tally7 = odw.CellTally(
    tally_type="neutron_fast_flux",
    target=1,
)

tally8 = odw.CellTally(
    tally_type="photon_fast_flux",
    target=1,
)

tally9 = odw.CellTally(
    tally_type="neutron_spectra",
    target=1,
)

tally10 = odw.CellTally(
    tally_type="photon_spectra",
    target=1,
)

tally11 = odw.CellTally(
    tally_type="(n,total)",
    target=1,
)

tallies = openmc.Tallies(
    [
        tally1,
        tally2,
        tally3,
        tally4,
        tally5,
        tally6,
        tally7,
        tally8,
        tally9,
        tally10,
        tally11,
    ]
)

settings = odw.FusionSettings()
settings.batches = 2
settings.particles = 1000
# assigns a ring source of DT energy neutrons to the source using the
# openmc_plasma_source package
settings.source = ops.FusionPointSource()


my_model = openmc.Model(
    materials=materials, geometry=geometry, settings=settings, tallies=tallies
)
statepoint_file = my_model.run()
