import rasterio
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap

def plot_ndvi(input_filepath, output_filepath):
    with rasterio.open(input_filepath) as src:
        ndvi = src.read(1)
    
    # Normalize the NDVI values to the range [0, 1] for color mapping
    norm = Normalize(vmin=-1.0, vmax=1.0)
    
    colors = ["darkred", "red", "orange", "yellow", "greenyellow", "green", "darkgreen"]
    cmap = LinearSegmentedColormap.from_list("ndvi", colors, N=256)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(ndvi, cmap=cmap, norm=norm)
    plt.colorbar(label='NDVI')
    plt.title('NDVI Visualization')
    plt.xlabel('Pixel')
    plt.ylabel('Pixel')

    # Save the figure to the specified output filepath
    plt.savefig(output_filepath, dpi=300, bbox_inches='tight')
    plt.close()
