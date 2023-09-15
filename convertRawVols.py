# Import os module to read directory
import os
#import sys
import numpy as np
from shutil import copyfile

intensity_range_origin = np.array([0, 1])
intensity_range_export = np.array([0, 65535])
# VALUES TO SET:
#     dirpath_origin -- absolute path to the folder with all the acquisitions
#     dirpath_export -- absolute path to the folder with the resampled recons
#     intensity_range_origin -- bounds of the 32-bit floating point intensity in raw images
#     intensity_range_export -- bounds of the 16-bit unsigned integer intensity in raw images
#     dirs_to_skip -- acquisition folders to skip from export
dirpath_origin = './'
dirpath_export = 'raw_uint16_to_go' # -- see below --
dirpath_export = os.path.join(dirpath_origin,dirpath_export) # the folder to export to will be relative to the main folder
intensity_range_origin[0] = 0.1
intensity_range_origin[1] = 0.6
#intensity_range_export[0] = <new_value> # keep commented for default values
#intensity_range_export[1] = <new_value> # keep commented for default values
dirs_to_skip = [ 'raw_uint16_to_go',
'rsync_raw_data_to_ruche.sh'
]

main_dir_list = os.listdir(dirpath_origin)
for acquisition_dir in main_dir_list:
    if acquisition_dir in dirs_to_skip or "tomod" not in acquisition_dir:
        print("skipped folder:", acquisition_dir)
        continue
    acquisition_dir_list = os.listdir(os.path.join(dirpath_origin,acquisition_dir))
    if not os.path.exists(os.path.join(dirpath_export,acquisition_dir)):
        os.mkdir(os.path.join(dirpath_export,acquisition_dir))
    for entry in acquisition_dir_list:
        if entry.endswith(".par"): # recon parameter file
            print("par file found:", entry)
            copyfile(os.path.join(dirpath_origin,acquisition_dir,entry),os.path.join(dirpath_export,acquisition_dir,entry))
        if entry.endswith(".vol"): # recon volume
            print("vol file found:", entry)
            data = np.fromfile(os.path.join(dirpath_origin,acquisition_dir,entry),dtype=float)
            data = (data-intensity_range_origin[0]) / (intensity_range_origin[1]-intensity_range_origin[0]) * ((intensity_range_export[1]-intensity_range_export[0])) + intensity_range_export[0]
            data.astype(np.uint16).tofile(os.path.join(dirpath_export,acquisition_dir,entry))
