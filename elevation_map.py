import geopandas as gpd
import matplotlib.pyplot as plt
from rasterio.plot import show
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Carregar o shapefile do estado de Minas Gerais
mg_shapefile = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\shapefiles_MG\31UF2500G.shp"
mg = gpd.read_file(mg_shapefile)

# Verificar e definir o CRS, se necessário
if mg.crs is None:
    mg = mg.set_crs("EPSG:4326")  # Definindo CRS padrão (WGS84)

# Carregar o arquivo raster de elevação
dem_file = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\DEM\gmted2010_merged_dem.tif"
dem = rasterio.open(dem_file)

# Reprojetar o raster de elevação para o CRS do shapefile
dst_crs = mg.crs.to_string()
transform, width, height = calculate_default_transform(
    dem.crs, dst_crs, dem.width, dem.height, *dem.bounds)
kwargs = dem.meta.copy()
kwargs.update({
    'crs': dst_crs,
    'transform': transform,
    'width': width,
    'height': height
})

# Criar um novo arquivo raster reprojetado
dem_reprojected_file = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\DEM\gmted2010_reprojected_dem.tif"
with rasterio.open(dem_reprojected_file, 'w', **kwargs) as dst:
    for i in range(1, dem.count + 1):
        reproject(
            source=rasterio.band(dem, i),
            destination=rasterio.band(dst, i),
            src_transform=dem.transform,
            src_crs=dem.crs,
            dst_transform=transform,
            dst_crs=dst_crs,
            resampling=Resampling.nearest)

# Carregar o raster reprojetado
dem_reprojected = rasterio.open(dem_reprojected_file)

# Plotar o mapa de elevação
fig, ax = plt.subplots(figsize=(12, 10))

# Mostrar o raster de elevação
img = show(dem_reprojected, ax=ax, title="Mapa de Elevação - Minas Gerais", cmap='terrain')

# Adicionar a borda do shapefile de Minas Gerais
mg.boundary.plot(ax=ax, linewidth=1, edgecolor='black')

# Adicionar a legenda (barra de cores)
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(img.get_images()[0], cax=cax)
cbar.set_label('Elevação (metros)')

# Ajustar a visualização
ax.set_title("Mapa de Elevação - Minas Gerais")
ax.set_axis_off()

# Salvar a imagem
output_image = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\mapa_elevacao_minas_gerais.png"  # Substitua pelo caminho onde deseja salvar a imagem
plt.savefig(output_image, dpi=300, bbox_inches='tight')
plt.show()
