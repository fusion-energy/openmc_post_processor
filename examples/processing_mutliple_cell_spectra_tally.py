import openmc_post_processor as opp
from spectrum_plotter import plot_spectrum  # a convenient plotting package

# loads in the statepoint file containing tallies
statepoint = opp.StatePoint(filepath="statepoint.2.h5")

results = {}
for tally_name in ["2_neutron_spectra", "3_neutron_spectra"]:

    # gets one tally from the available tallies
    my_tally = statepoint.get_tally(name=tally_name)

    # returns the tally with normalisation per pulse
    result = statepoint.process_tally(
        tally=my_tally,
        required_units=["MeV", "centimeter / pulse"],
        source_strength=1.3e6,
    )
    results[tally_name] = result


# plots a graph of the results
plot_spectrum(
    spectrum=results,
    x_label="Energy [MeV]",
    y_label="neutron flux [centimeter / second]",
    x_scale="log",
    y_scale="log",
    # trim_zeros=False,
    filename="combine_spectra_plot.png",
)
