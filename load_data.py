# Module with loading and preprocessing of the data to be visualised
#

import pandas as pd
import numpy as np
import os

# Get csv filenames from the present directory
def get_filenames():

    filenames = []
    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".csv"):
            filenames.append(filename)
    return filenames

