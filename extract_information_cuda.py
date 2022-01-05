import getopt
import sys
import subprocess
import os
import glob
from pathlib import Path

#architecture = ['30', '35', '52']
#tile_width = ['8', '16', '32']

teste = {
    "arc" : ""
}

if not os.path.exists(f"/home/luan/cuda_project/cuda_files"):
    new_folder = os.mkdir(f"/home/luan/cuda_project/cuda_files")
else:
    pass

for file in glob.glob("/home/luan/cuda_project/files/*.cu"):
    finfo = Path(file)
    explod_file = finfo.name.split('.')
    title_file = '.'.join(explod_file[:-1])
    title = f"echo Name: {title_file} >>  ./cuda_files/{title_file}.csv 2>&1"

    architecture = ['30', '35', '52']

    if title_file == 'subSeqMax':
        tile_width = ['128']

    else:
        #tile_width = ['8', '16', '32']
        tile_width = ['16']
        
    for row in architecture:

        if row == '30':
            teste['arc'] = row.replace('30','3.0')
        elif row == '35':
            teste['arc'] = row.replace('35','3.5')
        elif row == '52':
            teste['arc'] = row.replace('52','5.2')
        
        for line in tile_width:
            tw = f"echo Tile_Width: {line} >> ./cuda_files/{title_file}.csv 2>&1"
            arch = f"echo Architecture: {teste['arc']} >> ./cuda_files/{title_file}.csv 2>&1"
            run_script = f"nvcc -D Tile_Width={line} -arch=sm_{row} -Xptxas=-v {file} -w >> ./cuda_files/{title_file}.csv 2>&1"
            subprocess.call(title, shell=True)
            subprocess.call(tw, shell=True)
            subprocess.call(arch, shell=True)
            subprocess.call(run_script, shell=True)
print("Complete!")
