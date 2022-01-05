import getopt
import sys
import subprocess
import os
import csv
import glob 
import pandas as pd
from pathlib import Path
import datetime

encoding = 'utf-8'

def Convert(string):
    li = list(string.split("\n"))
    return li

if not os.path.exists(f"/home/luan/cuda_project/cuda_to_csv"):
    new_folder = os.mkdir(f"/home/luan/cuda_project/cuda_to_csv")
else:
    pass

data_teste = datetime.datetime.now().strftime("%Y-%m-%d")

for file in glob.glob("./log_application_files/*.csv"):
    finfo = Path(file)
    explod_file = finfo.name.split('.')
    title_file = '.'.join(explod_file[:-1])
    title_file = Convert(title_file)[0]

    architecture = "grep Architecture -Fw " + file + " | awk '{ print $2 }'"
    tt = subprocess.Popen(architecture, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    tt = tt.decode(encoding)
    out_architecture = tt.rstrip('\n')
    out_architecture = Convert(out_architecture)
    
    tw = "cat " + file + " | grep Tile_Width | awk -F'[^0-9]*' '{print $2}'"
    out_tw = subprocess.Popen(tw, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    out_tw = out_tw.decode(encoding)
    out_tile_width = out_tw.rstrip('\n')
    out_tile_width = Convert(out_tile_width)

    run1 = "cat ./log_application_files/"+title_file+".csv | grep registers | awk -F'[^0-9]*' '{print $2}'"
    out1 = subprocess.Popen(run1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    out1 = out1.decode(encoding)
    out_registers = out1.rstrip('\n')
    out_registers = Convert(out_registers)

    run2 = "cat ./log_application_files/"+title_file+".csv | grep smem | awk -F'[^0-9]*' '{print $3}'"
    out2 = subprocess.Popen(run2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    out2 = out2.decode(encoding)
    out_smem = out2.rstrip('\n')
    out_smem = Convert(out_smem)

    if out_smem == ['']:
        out_smem = '0'
        run_again = "cat ./log_application_files/"+title_file+".csv | grep cmem | awk -F'[^0-9]*' '{print $3}'"
        out4 = subprocess.Popen(run_again, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        out4 = out4.decode(encoding)
        out_cmem_1 = out4.rstrip('\n')
        out_cmem = out_cmem_1
        out_cmem = Convert(out_cmem)
        dict = {'Algorithm': title_file, 'Tile_Width':out_tile_width, 'Architecture': out_architecture, 'Registers': out_registers, 'smem': out_smem, 'cmem' : out_cmem } 
        df = pd.DataFrame(dict) 
        df.to_csv(f'./datasets/dataset-{data_teste}.csv', mode='a', header= False)
 
    else:
        run3 = "cat ./log_application_files/"+title_file+".csv | grep cmem | awk -F'[^0-9]*' '{print $4}'"
        out3 = subprocess.Popen(run3, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
        out3 = out3.decode(encoding)
        out_cmem = out3.rstrip('\n')
        out_cmem = Convert(out_cmem)
 
        dict = {'Algorithm': title_file, 'Tile_Width':out_tile_width, 'Architecture': out_architecture, 'Registers': out_registers, 'smem': out_smem, 'cmem' : out_cmem }
        df = pd.DataFrame(dict) 
        df.to_csv(f'./datasets/dataset-{data_teste}.csv', mode='a', header= False)