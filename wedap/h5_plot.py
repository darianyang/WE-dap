"""
Main plotting class of wedap.
Plot all of the datasets generated with H5_Pdist.

# TODO: all plotting options with test.h5, compare output
    # 1D Evo, 1D and 2D instant and average
    # optional: diff max_iter and bins args

TODO: maybe make methods for the following plots:
contourf--plot contour levels
histogram--plot histogram.
lines--plot contour lines only.
contourf_l--plot contour levels and lines.
histogram_l--plot histogram and contour lines.
option - with and without side histograms
- mpl mosaic options
- see mpl scatter hist: https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_hist.html
maybe a ridgeline plot?
- This would be maybe for 1D avg of every 100 iterations
- https://matplotlib.org/matplotblog/posts/create-ridgeplots-in-matplotlib/
Option to overlay different datasets, could be done easily with python but maybe a cli option?                

TODO: plot clustering centroids option?
      can then grab the search_aux at the centroid

TODO: bin visualizer? and maybe show the trajectories as just dots?
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage
from warnings import warn
from numpy import inf

from .h5_pdist import *

# TODO: maybe put the pdist object into the plot class and have this object be flexible
# so it could just be a pdist.h5 file from westpa or make your own
# or read in a pdist.h5 and create pdist object using that dataset

class H5_Plot(H5_Pdist):
    """
    These methods provide various plotting options for pdist data.
    """
    def __init__(self, X=None, Y=None, Z=None, plot_mode="hist2d", cmap="viridis", smoothing_level=None,
        color="tab:blue", ax=None, plot_options=None, p_min=None, p_max=None, contour_interval=1,
        cbar_label=None, *args, **kwargs):
        """
        Plotting of pdists generated from H5 datasets.

        Parameters
        ----------
        X, Y : arrays
            x and y axis values, and if using aux_y or evolution (with only aux_x), also must input Z.
        Z : 2darray
            Z is a 2-D matrix of the normalized histogram values.
        plot_mode : str
            TODO: update and expand. Can be 'hist2d' (default), 'contour', 'line', 'scatter3d'.
        cmap : str
            Can be string or cmap to be input into mpl. Default = viridis.
        smoothing_level : float
            Optionally add gaussian noise to smooth Z data. A good value is around 0.4 to 1.0.
        color : str
            Color for 1D plots.
        ax : mpl axes object
        plot_options : kwargs dictionary
            Include mpl based plot options (e.g. xlabel, ylabel, ylim, xlim, title).
        p_min : int
            The minimum probability limit value.
        p_max : int
            The maximum probability limit value.
        contour_interval : int
            Interval to put contour levels if using 'contour' plot_mode.
        cbar_label : str
            Label for the colorbar.
        ** args
        ** kwargs
        """
        # include the init args for H5_Pdist
        # TODO: how to make some of the args optional if I want to use classes seperately?
        #super().__init__(*args, **kwargs)

        if ax is None:
            self.fig, self.ax = plt.subplots()
        else:
            self.fig = plt.gcf()
            self.ax = ax

        self.smoothing_level = smoothing_level

        # TODO: option if you want to generate pdist
        # also need option of just using the input X Y Z args
        # or getting them from w_pdist h5 file, or from H5_Pdist output file
        # user inputs XYZ
        if X is None and Y is None and Z is None:
            super().__init__(*args, **kwargs)
            X, Y, Z = H5_Pdist(*args, **kwargs).pdist()

        self.X = X
        self.Y = Y
        self.Z = Z

        self.p_min = p_min
        self.p_max = p_max
        self.contour_interval = contour_interval

        self.plot_mode = plot_mode
        self.cmap = cmap
        self.color = color # 1D color
        self.plot_options = plot_options

        # TODO: not compatible if inputing data instead of running pdist
        # try checking for the variable first, could use a t/e block
        #if self.p_units in locals():
        # if self.p_units == "kT":
        #     self.cbar_label = "$-\ln\,P(x)$"
        # elif self.p_units == "kcal":
        #     self.cbar_label = "$-RT\ \ln\, P\ (kcal\ mol^{-1})$"

        # user override None cbar_label TODO
        if cbar_label:
            self.cbar_label = cbar_label
        else:
            self.cbar_label = "-ln P(x)"

    # TODO: load from w_pdist, also can add method to load from wedap pdist output
    # def _load_from_pdist_file(self):
    #     '''
    #     Load data from a w_pdist output file. This includes bin boundaries. 
    #     '''
    #     # Open the HDF5 file.
    #     self.pdist_HDF5 = h5py.File(self.args.pdist_file)

    #     # Load the histograms and sum along all axes except those specified by
    #     # the user.  Also, only include the iterations specified by the user.
    #     histogram      = numpy.array(self.pdist_HDF5['histograms'])

    #     # Figure out what iterations to use
    #     n_iter_array   = numpy.array(self.pdist_HDF5['n_iter'])
    #     if self.args.first_iter is not None:
    #         first_iter = self.args.first_iter
    #     else:
    #         first_iter = n_iter_array[0] 
    #     if self.args.last_iter is not None:
    #         last_iter = self.args.last_iter
    #     else:
    #         last_iter = n_iter_array[-1]
    #     first_iter_idx = numpy.where(n_iter_array == first_iter)[0][0]
    #     last_iter_idx  = numpy.where(n_iter_array == last_iter)[0][0]
    #     histogram      = histogram[first_iter_idx:last_iter_idx+1]

    #     # Sum along axes
    #     self.axis_list = self._get_bins_from_expr(self.args.pdist_axes)
    #     self.H         = self._sum_except_along(histogram, self.axis_list) 

    #     # Make sure that the axis ordering is correct.
    #     if self.axis_list[0] > self.axis_list[1]:
    #         self.H = self.H.transpose()

    def add_cbar(self, cax=None):
        """
        Add cbar.

        Parameters
        ----------
        cax : mpl cbar axis
            Optionally specify the cbar axis.
        """
        cbar = self.fig.colorbar(self.plot, cax=cax)
        # TODO: lines on colorbar?
        # TODO: related, make a discrete colorbar/mapping for hist2d?
        #if lines:
        #    cbar.add_lines(lines)
        # TODO: move labelpad here to style
        cbar.set_label(self.cbar_label, labelpad=14)

        # allow for cbar object manipulation (e.g. removal in movie)
        self.cbar = cbar
    
    def plot_hist2d(self):
        """
        2d hist plot.
        """
        # 2D heatmaps
        # TODO: westpa makes these the max to keep the pdist shape
        # if self.p_max:
        #     self.Z[self.Z > self.p_max] = inf
        self.plot = self.ax.pcolormesh(self.X, self.Y, self.Z, cmap=self.cmap, 
                                       shading="auto", vmin=self.p_min, vmax=self.p_max)

    def plot_contour(self):
        """
        2d contour plot.
        """
        # TODO: seperate functions for contourf and contourl?
            # then can use hist and contourl
        # TODO: could clean up this logic better
        if self.p_min is None:
            self.p_min = np.min(self.Z)
        # 2D contour plots
        if self.p_max is None:
            warn("With 'contour' plot_type, p_max should be set. Otherwise max Z is used.")
            levels = np.arange(self.p_min, np.max(self.Z[self.Z != np.inf ]), self.contour_interval)
        elif self.p_max <= 1:
            warn("You may want to change the `contour_interval` argument to be < 1")
            levels = np.arange(self.p_min, self.p_max + self.contour_interval, self.contour_interval)
        else:
            levels = np.arange(self.p_min, self.p_max + self.contour_interval, self.contour_interval)

        self.lines = self.ax.contour(self.X, self.Y, self.Z, levels=levels, colors="black", linewidths=1)
        self.plot = self.ax.contourf(self.X, self.Y, self.Z, levels=levels, cmap=self.cmap)

    def plot_bar(self):
        """
        Simple bar plot.
        """
        # 1D data
        self.ax.bar(self.X, self.Y, color=self.color)
        self.ax.set_ylabel("P(x)")

    # def plot_hist1d(self):
    #     # 1D data : TODO: not working currently
    #     # recover the pdf from the -ln P
    #     # TODO: does this account for p_max naturally?
    #     # TODO: I can get the raw data and then get the counts right from XYZ functions
    #     self.ax.hist(self.X, self.Y)
    #     self.ax.set_ylabel("P(x)")

    def plot_line(self):
        """
        1d line plot.
        """
        # 1D data
        if self.p_max:
            self.Y[self.Y > self.p_max] = inf
        self.ax.plot(self.X, self.Y, color=self.color)
        self.ax.set_ylabel(self.cbar_label)
    
    def plot_scatter3d(self, interval=10, s=1):
        """
        3d scatter plot.

        Parameters
        ----------
        interval : int
            Interval to consider the XYZ datasets, increase to use less data.
        s : float
            mpl scatter marker size.
        """
        self.plot = self.ax.scatter(self.X[::interval], 
                                    self.Y[::interval], 
                                    c=self.Z[::interval], 
                                    cmap=self.cmap, s=s,
                                    vmin=self.p_min, vmax=self.p_max)

    def plot_hexbin3d(self):
        """
        Hexbin plot?
        """
        # TODO
        self.plot = self.ax.hexbin(self.X, self.Y, C=self.Z, 
                                   reduce_C_function=np.mean,
                                   cmap=self.cmap)

    def _unpack_plot_options(self):
        """
        Unpack the plot_options kwarg dictionary.
        """
        # unpack plot options dictionary
        # TODO: put all in ax.set()?
        for key, item in self.plot_options.items():
            if key == "xlabel":
                self.ax.set_xlabel(item)
            if key == "ylabel":
                self.ax.set_ylabel(item)
            if key == "xlim":
                self.ax.set_xlim(item)
            if key == "ylim":
                self.ax.set_ylim(item)
            if key == "title":
                self.ax.set_title(item)
            if key == "grid" and item is True:
                self.ax.grid(item, alpha=0.5)
            if key == "minima": # TODO: this is essentially bstate, also put maxima?
                # reorient transposed hist matrix
                Z = np.rot90(np.flip(self.Z, axis=0), k=3)
                # get minima coordinates index (inverse maxima since min = 0)
                maxima = np.where(1 / Z ==  np.amax(1 / Z, axis=(0, 1)))
                # plot point at x and y bin midpoints that correspond to mimima
                self.ax.plot(self.X[maxima[0]], self.Y[maxima[1]], 'ko')
                print(f"Minima: ({self.X[maxima[0]][0]}, {self.Y[maxima[1]][0]})")

    # TODO: cbar issues with 1d plots
    def plot(self, cbar=True):
        """
        Main public method.
        Master plotting run function
        Parse plot type and add cbars/tightlayout/plot_options/smoothing

        TODO: some kind 1d vs 2d indicator, then if not 1d plot cbar

        Parameters
        ----------
        cbar : bool
            Whether or not to include a colorbar.
        """
        # smooth the data if specified
        if self.smoothing_level:
            self.Z = scipy.ndimage.gaussian_filter(self.Z, sigma=self.smoothing_level)

        if self.plot_mode == "contour":
            self.plot_contour()

        # TODO: auto label WE iterations on evolution? (done via __main__ right now)
        elif self.plot_mode == "hist2d":
            # I run into this error when I run something like instant with 
            # the h5 but didn't adjust the plot mode to something like line
            try:
                self.plot_hist2d()
            except (TypeError,ValueError):
                # TODO: put the text into logger?
                print("ERROR: Did you mean to use the default 'hist2d' plot mode?")
                print("Perhaps you need to define another dimension via '--Yname'?")
                sys.exit()
            #self.add_cbar()

        elif self.plot_mode == "bar":
            self.plot_bar()
            Warning("'bar' plot_mode is still under development")
            #self.ax.set_ylabel(self.cbar_label)

        elif self.plot_mode == "line":
            self.plot_line()
            self.ax.set_ylabel(self.cbar_label)

        elif self.plot_mode == "scatter3d":
            self.plot_scatter3d()

        elif self.plot_mode == "hexbin3d":
            self.plot_hexbin3d()

        # error if unknown plot_mode
        else:
            raise ValueError(f"plot_mode = '{self.plot_mode}' is not valid.")

        # TODO: can this work with non H5_Pdist input?
        # if self.Xname == "pcoord":
        #     self.ax.set_xlabel(f"Progress Coordinate {self.Xindex}")
        # if self.Yname == "pcoord":
        #     self.ax.set_ylabel(f"Progress Coordinate {self.Yindex}")

        # don't add cbar if not specified or if using a 1D plot
        if cbar and self.plot_mode not in ["line", "bar"]:
            self.add_cbar()

        if self.plot_options is not None:
            self._unpack_plot_options()
        self.fig.tight_layout()
