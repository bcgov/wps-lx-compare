import numpy as np
import matplotlib.pyplot as plt

class LinkZoom:
    def __init__(self, fig, axs):
        self.fig = fig
        self.axs = axs
        self.syncing = False
        self._connect_zoom()

    def _connect_zoom(self):
        # Connect the zoom events to both axes
        self.axs[0].callbacks.connect('xlim_changed', self.link_zoom)
        self.axs[0].callbacks.connect('ylim_changed', self.link_zoom)
        self.axs[1].callbacks.connect('xlim_changed', self.link_zoom2)
        self.axs[1].callbacks.connect('ylim_changed', self.link_zoom2)

    def link_zoom(self, event):
        if self.syncing:
            return
        self.syncing = True
        xlim = self.axs[0].get_xlim()
        ylim = self.axs[0].get_ylim()
        # Sync second axis limits
        self.axs[1].set_xlim(xlim)
        self.axs[1].set_ylim(ylim)
        self.fig.canvas.draw_idle()
        self.syncing = False

    def link_zoom2(self, event):
        if self.syncing:
            return
        self.syncing = True
        xlim = self.axs[1].get_xlim()
        ylim = self.axs[1].get_ylim()
        # Sync first axis limits
        self.axs[0].set_xlim(xlim)
        self.axs[0].set_ylim(ylim)
        self.fig.canvas.draw_idle()
        self.syncing = False