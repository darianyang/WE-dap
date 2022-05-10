"""
Eventually incorporate into tests.

TODO: add styles for 1 col, 2 col, and poster figures.
TODO: how to allow for evolution and 1D plots of second pcoord dimension.
"""
from h5_pdist import *
from h5_plot import *

# formatting
plt.style.use("default.mplstyle")

# TODO: auto ignore auxy when using 1d
data_options = {"h5" : "data/west_c2.h5",
                #"h5" : "data/multi_2kod.h5",
                #"h5" : "data/2kod_v03.02.h5",
                #"h5" : "data/p53.h5",
                #"Xname" : "1_75_39_c2",
                #"Xname" : "dihedral_3",
                #"Yname" : "dihedral_4",
                #"Xname" : "pcoord",
                #"Yname" : "pcoord",
                #"Xindex" : 1,
                #"Yindex" : 0,            # TODO: maybe can set this more automatically?
                #"Yname" : "angle_3pt",
                #"Yname" : "RoG",
                #"Yname" : "XTAL_REF_RMS_Heavy",
                #"Xname" : "rog",
                #"Yname" : "rms_bb_nmr",
                #"Yname" : "rms_heavy_xtal",
                #"Yname" : "rms_m1_xtal",
                #"Xname" : "M1_E175_phi",
                #"Yname" : "M1_E175_psi",
                "data_type" : "evolution",
                "weighted" : False,
                #"p_min" : 15,
                #"p_max" : 20,
                "p_units" : "kcal",
                #"first_iter" : 100,
                #"last_iter" : 400, 
                #"bins" : 100, # note bins affects contour quality
                #"plot_mode" : "contour",
                #"cmap" : "gnuplot_r",
                "plot_mode" : "hist2d",
                #"plot_mode" : "line",
                #"data_smoothing_level" : 0.4,
                #"curve_smoothing_level" : 0.4,
                }

# TODO: default to aux for labels if available or pcoord dim if None
plot_options = {#"ylabel" : r"M2Oe-M1He1 Distance ($\AA$)", 
                #"ylabel" : "RMSD ($\AA$)", 
                #"ylabel" : "WE Iteration", 
                #"ylabel" : "RMSD to XTAL ($\AA$)", 
                #"xlabel" : "Helical Angle (°)",
                #"title" : "2KOD 20-100° WE",
                #"title" : "2KOD 10µs RMSD WE",
                #"xlim" : (1,7),
                #"ylim" : (2,8),
                #"xlim" : (20, 100),
                #"xlim" : (17, 22),
                #"ylim" : (30, 100),
                #"xlim" : (-180,180),
                #"ylim" : (-180,180),
                #"xlim" : (20,100),
                "grid" : True,
                #"minima" : True, 
                # TODO: diagonal line option
                }


# time the run
import timeit
start = timeit.default_timer()

# TODO: eventually use this format to write unit tests of each pdist method

#X, Y, Z = H5_Plot(**data_options)
#H5_Plot(X, Y, Z).plot_hist_2d()

# TODO: I should be able to use the classes sepertely or together
#H5_Plot(plot_options=plot_options, **data_options).plot_contour()
#wedap = H5_Plot(plot_options=plot_options, **data_options).plot()

#wedap = H5_Pdist(**data_options)
#X, Y, Z = wedap.pdist()
#plt.pcolormesh(X, Y, Z)

# TODO: put this in a seperate file
# data for tests
# mode = "instant"
# for pcoord in ["pcoord", "dihedral_2"]:
#     for pcoord2 in ["dihedral_3", "dihedral_4"]:
#         pdist = H5_Pdist("data/p53.h5", mode, Xname=pcoord, Yname=pcoord2)
#         X, Y, Z = pdist.pdist()
#         np.savetxt(f"tests/{mode}_{pcoord}_{pcoord2}_X.txt", X)
#         np.savetxt(f"tests/{mode}_{pcoord}_{pcoord2}_Y.txt", Y)
#         np.savetxt(f"tests/{mode}_{pcoord}_{pcoord2}_Z.txt", Z)

#wedap.plot()
#plt.savefig("west_c2.png")
#print(wedap.auxnames)

# TODO: test using different p_max values and bar

# 1D example
# pdist = H5_Pdist("data/west_i200.h5", X="1_75_39_c2", **data_options)
# X, Y = pdist.run()
# plt.plot(X, Y)

stop = timeit.default_timer()
execution_time = stop - start
print(f"Executed in {execution_time:04f} seconds")

plt.show()

# TODO: build an tracer function that finds the iter,seg,frame(s) for an input hist bin