import getopt
import sys
import subprocess
import os
import glob
from pathlib import Path

dictionary = {
    "architecture" : ""
}

for file in glob.glob("./cuda_files/*.cu"):
    finfo = Path(file)
    explod_file = finfo.name.split('.')
    title_file = '.'.join(explod_file[:-1])
    title = f"echo Name: {title_file} >>  ./log_application_files/{title_file}.csv 2>&1"

    architecture = ['30', '35', '52']

    if title_file == 'subSeqMax':
        tile_width = ['128']

    else:
        #tile_width = ['8', '16', '32']
        tile_width = ['16']
        
    for row in architecture:

        if row == '30':
            dictionary['architecture'] = row.replace('30','3.0')
        elif row == '35':
            dictionary['architecture'] = row.replace('35','3.5')
        elif row == '52':
            dictionary['architecture'] = row.replace('52','5.2')
        
        for line in tile_width:
            tw = f"echo Tile_Width: {line} >> ./log_application_files/{title_file}.csv 2>&1"
            arch = f"echo Architecture: {dictionary['architecture']} >> ./log_application_files/{title_file}.csv 2>&1"
            run_script = f"nvcc -D Tile_Width={line} -arch=sm_{row} -Xptxas=-v {file} -w >> ./log_application_files/{title_file}.csv 2>&1"
            subprocess.call(title, shell=True)
            subprocess.call(tw, shell=True)
            subprocess.call(arch, shell=True)
            subprocess.call(run_script, shell=True)
print("Complete!")
