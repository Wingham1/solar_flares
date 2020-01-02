"""
File for reading and processing HESSI flare data as a pandas dataframe

maybe use a class
"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os

def hessi_flare_dataframe():
    """
    returns flare data from HESSI webpage as a pandas dataframe
    
    header line in the file isn't on the first row and the variable units were in the line underneith so had to fix the header line for the dataframe
    """
    header = ['Flare', 'Start time', 'Peak', 'End', 'Dur (s)', 'Peak (c/s)', 'Total (Counts)', 'Energy (keV)', 'X Pos (asec)', 'Y Pos (asec)', 'Radial (asec)', 'AR', 'Flags']
    int_indexes = [0, 4, 5, 6, 8, 9, 10, 11]
    dt_indexes = [1, 2, 3]
    
    #df = pd.read_csv('https://hesperia.gsfc.nasa.gov/hessidata/dbase/hessi_flare_list.txt', sep='\t', header=None, skiprows=6, engine='python', skipfooter=39)
    df = pd.read_csv(os.path.join('hessidf','hessi_flare_list.txt'), sep='\t', header=None, skiprows=6, engine='python', skipfooter=39)
    
    """
    pandas read_csv reads all the data into a dataframe with one column and lots of rows
    each column is seperated by a space in the .txt file but some values contain spaces such as time and flag columns
    reformat to make start time, end time and peak time columns datetime objects and number columns ints
    """
    data = []
    for row_index in range(len(df)):
        row_data = df.iat[row_index, 0].split()
        not_flag_col = row_data[:13]
        flag_col = '-'.join(row_data[13:]) # want flags to be seperated by a dash -
        start_date = not_flag_col.pop(1) # add date to times, if a flare occures close to midnight this method may cause issues
        for i in dt_indexes:
            not_flag_col[i] = start_date + ' ' + not_flag_col[i]
        data.append(not_flag_col+[flag_col])
    
    """
    TODO: fix endtime, what if a flare starts around midnight, the day for the endtime might be a day after the start time day
          (currently the day of endtime is the same as the day for start time)
    
    """
    
    df = pd.DataFrame(np.array(data), columns=header)
    for i in int_indexes:
        df[header[i]] = pd.to_numeric(df[header[i]])
    for i in dt_indexes:
        df[header[i]] = pd.to_datetime(df[header[i]])
    
    print(df.dtypes)
    
    # filtering
    bad_flags = ['NS','SD'] # NS non solar event, SD spacecraft in South Atlantic Anomaly where magnetic data is weird https://en.wikipedia.org/wiki/South_Atlantic_Anomaly
    df = filter(df, bad_flags)
    
    return df

def filter(df, remove_flags):
    """
    remove bad radial values and bad flags
    """
    
    df = df[df['Radial (asec)'] <= np.percentile(df['Radial (asec)'].values, 99)] # remove outliers as done here https://www.kaggle.com/lesagesj/solar-flares-from-rhessi-mission/notebook
    bad_indexes = find_flags(df, remove_flags)
    df.drop(bad_indexes)
    return df


def find_flags(df, flags):
    """
    returns indexes of rows that contain given flags
    """
    
    indexes = []
    for idx, row in df.iterrows():
        split_flags = row['Flags'].split('-')
        for flag in split_flags:
            if flag in flags:
                indexes.append(idx)
    return indexes

def plot_flare_locations(hessi):
    """
    A function that uses the HESSI database to plot the locations of flares
    
    Param:
          hessi, the HESSI database as a pandas dataframe
    """
    
    plt.scatter(hessi['X Pos (asec)'].values, hessi['Y Pos (asec)'].values, color='r', s=0.5)
    plt.show()

def find_locations(df, flare_class):
    class_to_peak = {'A':'3-6', 'B':'6-12', 'C':'12-25', 'M':'25-50', 'x':5}
    flares = df[df['Energy (keV)'] == class_to_peak[flare_class]]
    return flares[['X Pos (asec)', 'Y Pos (asec)']]
