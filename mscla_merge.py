import rasterio
from rasterio.merge import merge
import glob
import os

# Caminho para o diretório onde estão os arquivos .tif
dem_path = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\DEM"
dem_files = glob.glob(os.path.join(dem_path, "*.tif"))

# Abrir os arquivos .tif
src_files_to_mosaic = []
for fp in dem_files:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

# Mesclar os arquivos
mosaic, out_trans = merge(src_files_to_mosaic)

# Metadados do arquivo de saída
out_meta = src.meta.copy()
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
    "crs": src.crs
})

# Caminho para o arquivo de saída
output_file = r"C:\Users\arthu\OneDrive\Desktop\projeto_mapa\DEM\gmted2010_merged_dem.tif"

# Salvar o arquivo mesclado
with rasterio.open(output_file, "w", **out_meta) as dest:
    dest.write(mosaic)

# Fechar os arquivos fonte
for src in src_files_to_mosaic:
    src.close()
