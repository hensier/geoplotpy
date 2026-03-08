import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import matplotlib.figure as mfigure
import matplotlib.axes as maxes
import matplotlib.collections as mcollections
import matplotlib.transforms as mtransforms
import matplotlib.contour as mcontour
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import geopandas as gpd
from geoplotpy import colorbar as clb
from typeguard import typechecked

@typechecked
def plot_maps(
    nrows: int = 1,
    ncols: int = 1,
    figsize: tuple[int | float, int | float] = (8, 8),
    west: int | float | list[int | float] = 100,
    east: int | float | list[int | float] = 137,
    south: int | float | list[int | float] = 16,
    north: int | float | list[int | float] = 54,
    gridlines: bool | list[bool] = True,
    gridstep: int | float | list[int | float] = 10
) -> tuple[mfigure.Figure, np.ndarray]:
    """
    Plot subplots.
    Args:
        nrows: The number of rows of the subplots.
        ncols: The number of columns of the subplots.
        figsize: The size of the maps.
        west: The west bound of the maps.
        east: The east bound of the maps.
        south: The south bound of the maps.
        north: The north bound of the maps.
        gridlines: Whether to plot gridlines.
        gridstep: The step of the gridlines.
    Returns:
        A tuple of the figure and the axes.
    """
    if isinstance(west, (int, float)):
        west = [west] * nrows * ncols
    if isinstance(east, (int, float)):
        east = [east] * nrows * ncols
    if isinstance(south, (int, float)):
        south = [south] * nrows * ncols
    if isinstance(north, (int, float)):
        north = [north] * nrows * ncols
    if isinstance(gridlines, bool):
        gridlines = [gridlines] * nrows * ncols
    if isinstance(gridstep, (int, float)):
        gridstep = [gridstep] * nrows * ncols
    
    fig, axes = plt.subplots(
        nrows = nrows,
        ncols = ncols,
        figsize = (figsize[0] * ncols, figsize[1] * nrows),
        squeeze = False,
        subplot_kw = {'projection': ccrs.PlateCarree()}
    )

    for i in range(nrows * ncols):
        ax = axes[i // ncols, i % ncols]
        ax.set_extent([west[i], east[i], south[i], north[i]], crs = ccrs.PlateCarree())
        ax.add_feature(cfeature.COASTLINE, linewidth = 0.8)
        ax.add_feature(cfeature.BORDERS, linestyle = ':', linewidth = 0.8)
        if gridlines[i]:
            gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color = 'gray', alpha = 0.5, linestyle = '--')
            gl.top_labels = False
            gl.right_labels = False
            gl.xlocator = mticker.FixedLocator(np.arange(np.ceil(west[i] / gridstep[i]) * gridstep[i], np.floor(east[i] / gridstep[i]) * gridstep[i] + gridstep[i], gridstep[i]))
            gl.ylocator = mticker.FixedLocator(np.arange(np.ceil(south[i] / gridstep[i]) * gridstep[i], np.floor(north[i] / gridstep[i]) * gridstep[i] + gridstep[i], gridstep[i]))
            gl.xlabel_style = {'size': 10}
            gl.ylabel_style = {'size': 10}

    return fig, axes.flatten()

@typechecked
def plot_map(
    figsize: tuple[int | float, int | float] = (8, 8),
    west: int | float = 100,
    east: int | float = 137,
    south: int | float = 16,
    north: int | float = 54,
    gridlines: bool = True,
    gridstep: int | float = 10
) -> tuple[mfigure.Figure, maxes.Axes]:
    """
    Plot a map.
    Args:
        figsize: The size of the figure.
        west: The west bound of the map.
        east: The east bound of the map.
        south: The south bound of the map.
        north: The north bound of the map.
        gridlines: Whether to plot gridlines.
    Returns:
        A tuple of the figure and the axes.
    """
    fig, axes = plot_maps(1, 1, figsize, west, east, south, north, gridlines, gridstep)
    return fig, axes[0]

@typechecked
def plot_provinces(axes: maxes.Axes | np.ndarray, file: str = 'JSON/china_provinces.json') -> None:
    """
    Plot the provinces of China on the map.
    Args:
        axes: The axes to plot on.
        file: The file to read the provinces from.
    Returns:
        None.
    """
    provinces = gpd.read_file(file)
    if isinstance(axes, maxes.Axes):
        axes = np.array([axes])
    for ax in axes:
        provinces.boundary.plot(ax = ax, edgecolor = 'gray', linewidth = 0.5, transform = ccrs.PlateCarree())

@typechecked
def get_colorbar(
    bounds: list[int | float] | str = 'O3',
    colors: list[str] | str = 'AQI'
) -> tuple[mcolors.ListedColormap, mcolors.BoundaryNorm]:
    """
    Get the color map and the norm for the colorbar.
    Args:
        bounds: The bounds of the colorbar.
        colors: The colors of the colorbar.
    Returns:
        A tuple of the color map and the norm.
    """
    if isinstance(bounds, str):
        if bounds in clb.bounds:
            bounds = clb.bounds[bounds]
        else:
            raise ValueError(f'Invalid bounds: {bounds}')
    if isinstance(colors, str):
        if colors in clb.colors:
            colors = clb.colors[colors]
        else:
            raise ValueError(f'Invalid colors: {colors}')

    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    return cmap, norm

@typechecked
def plot_colorbar(
    sc: mcollections.PathCollection | mcontour.QuadContourSet,
    ax: maxes.Axes | None = None,
    cax: maxes.Axes | None = None,
    orientation: str = 'vertical',
    extend: str = 'neither',
    pad: int | float = 0.02,
    aspect: int | float = 30,
    fraction: int | float = 0.02,
    label: str = 'MDA8 (μg $\\cdot$ m$^{-3}$)',
    fontsize: int | float = 12,
    labelsize: int | float = 10
) -> None:
    """
    Plot a colorbar.
    Args:
        sc: The scatter plot.
        ax: The axes to plot on.
        cax: The axes to plot the colorbar on.
        orientation: The orientation of the colorbar.
        pad: The padding of the colorbar.
        aspect: The aspect ratio of the colorbar.
        fraction: The fraction of the colorbar.
        label: The label of the colorbar.
        fontsize: The fontsize of the label.
        labelsize: The fontsize of the tick labels.
    Returns:
        None.
    """
    cbar = plt.colorbar(sc, ax = ax, cax = cax, orientation = orientation, extend = extend, pad = pad, aspect = aspect, fraction = fraction)
    cbar.set_label(label, fontsize = fontsize)
    cbar.ax.tick_params(labelsize = labelsize)

@typechecked
def save_fig(filename: str, dpi: int | float = 300, bbox_inches: None | mtransforms.Bbox | str = 'tight') -> None:
    """
    Save the figure.
    Args:
        filename: The filename of the figure.
        dpi: The DPI of the figure.
        bbox_inches: The bounding box inches of the figure.
    Returns:
        None.
    """
    plt.savefig(filename, dpi = dpi, bbox_inches = bbox_inches)
    plt.close()