# geoplotpy

geoplotpy is a library for plotting geography maps.

## Installation

### Using pip (recommended)
```bash
pip install geoplotpy
```

### Install from source
```bash
git clone https://github.com/hensier/geoplotpy.git
cd geoplotpy
pip install -e .
```

## Quick start

### Example 1: Plot 2*2 subplots with provinces in the first subplot.
```python
import geoplotpy as gpp
fig, axes = gpp.plot_maps(
    nrows = 2, ncols = 2,
    figsize = (8, 6),
    west = [100, -80, -125, -180],
    east = [137, -43, -70, 180],
    south = [16, -74, 25, -90],
    north = [54, -36, 49, 90],
    gridlines = [True, True, False, False],
    gridstep = [10, 10, -1, -1]
)
gpp.plot_provinces(axes[0], file = 'JSON/china_provinces.json')
gpp.save_fig('ex1.png')
```

### Example 2: Plot a map with a colorbar.
```python
import numpy as np
import cartopy.crs as ccrs
import geoplotpy as gpp

np.random.seed(998244353)
west, east = np.sort(np.random.uniform(-180, 180, 2))
south, north = np.sort(np.random.uniform(-90, 90, 2))
lons, lats = np.random.uniform(west, east, 100), np.random.uniform(south, north, 100)

fig, ax = gpp.plot_map(west = west, east = east, south = south, north = north)
cmap, norm = gpp.get_colorbar(bounds = [0.2, 0.4, 0.6, 0.8, 1], colors = 'Q4')
sc = ax.scatter(lons, lats, c = np.random.uniform(0, 1, 100), cmap = cmap, norm = norm, s = 50, edgecolor = 'black', linewidth = 0.5, alpha = 0.8, transform = ccrs.PlateCarree())
gpp.plot_colorbar(sc, ax)
gpp.save_fig('ex2.png')
```

### Version
0.1.4