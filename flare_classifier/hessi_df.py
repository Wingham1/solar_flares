"""
Script for reading and processing HESSI flare data as a pandas dataframe, can read from a web address or downloaded txt file provided ('hessi_flare_list.txt').

"""

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt

def hessi_flare_dataframe(web=True):
    """
    Uses flare data from HESSI webpage to make a pandas dataframe (can use downloaded txt file).
    
    Param:
          web boolean, True to use web address or False to use downloaded txt file
          
    Return:
           df pandas dataframe, Dataframe containing HESSI flare data
    """
    
    # header line in the file isn't on the first row and the variable units were in the line underneith so had to fix the header line for the dataframe
    header = ['Flare', 'Start_time', 'Peak_time', 'End_time', 'Dur (s)', 'Peak (c/s)', 'Total (Counts)', 'Energy (keV)', 'X Pos (asec)', 'Y Pos (asec)', 'Radial (asec)', 'AR', 'Flags']
    int_indexes = [0, 4, 5, 6, 8, 9, 10, 11]
    dt_indexes = [1, 2, 3]
    
    if web:
        df = pd.read_csv('https://hesperia.gsfc.nasa.gov/hessidata/dbase/hessi_flare_list.txt', sep='\t', header=None, skiprows=6, engine='python', skipfooter=39)
    else:
        df = pd.read_csv('hessi_flare_list.txt', sep='\t', header=None, skiprows=6, engine='python', skipfooter=39)
    
    """
    pandas read_csv reads all the data into a dataframe with one column (as a string) and lots of rows
    each column is seperated by a space in the .txt file but some columns contain spaces in the values such as the time and flag columns (also spaces in some column names!),
    reformat to make start time, end time and peak time columns datetime objects and number columns ints
    """
    
    # split the string into columns and make new dataframe
    data = []
    for row_index in range(len(df)):
        row_data = df.iat[row_index, 0].split()
        not_flag_col = row_data[:13]
        flag_col = '-'.join(row_data[13:]) # want flags to be seperated by a dash -
        start_date = not_flag_col.pop(1) # add date to times, if a flare occures close to midnight this method may cause issues
        for i in dt_indexes:
            not_flag_col[i] = start_date + ' ' + not_flag_col[i]
        data.append(not_flag_col+[flag_col])
    df = pd.DataFrame(np.array(data), columns=header)
    
    # sort types
    for i in int_indexes:
        df[header[i]] = pd.to_numeric(df[header[i]])
    for i in dt_indexes:
        df[header[i]] = pd.to_datetime(df[header[i]])
    
    # fix bug: End_time had the wrong date when the flare started around midnight because I used the start date to make the datetime object
    for idx, row in df.iterrows():
        if row['End_time'] < row['Start_time']:
            row.loc['End_time'] = row['End_time'] + dt.timedelta(days=1)
        if row['Peak_time'] < row['Start_time']:
            row.loc['Peak_time'] = row['Peak_time'] + dt.timedelta(days=1)
           
    return df

def find_flags(df, flags):
    """
    Finds indexes of rows that contain given flags
    
    Param:
          df pandas dataframe, the dataframe to find the flag in (expected to contain hessi data with flag column as returned by hessi_flare_dataframe function)
          flags list of strings, the flags to find in the dataframe
          
    Return:
           indexes list of integers, a list of integers of row indexes that contain the given flag
    """
    
    indexes = []
    for idx, row in df.iterrows():
        split_flags = row['Flags'].split('-')
        for f in split_flags:
            if f in flags:
                indexes.append(idx)
    
    return indexes

def filter(df, remove_flags):
    """
    Removes bad radial values, bad flags and strange active regions (shouldn't be 0 but a lot are 0)
    
    Param:
          df pandas dataframe, the dataframe to find the flag in (expected to contain hessi data with flag column as returned by hessi_flare_dataframe function)
          flags list of strings, the flags to find in the dataframe
          
    Return:
           df pandas dataframe, the same dataframe without rows that contain given flags or strange results such as location or active region
    """
    
    df = df[df['Radial (asec)'] <= np.percentile(df['Radial (asec)'].values, 99)] # remove outliers as done here https://www.kaggle.com/lesagesj/solar-flares-from-rhessi-mission/notebook
    bad_indexes = find_flags(df, remove_flags)
    df.drop(bad_indexes)
    df = df[df['AR'] > 0]
    
    return df

def plot_flare_locations(hessi):
    """
    A function that uses the HESSI database to plot the locations of flares
    
    Param:
          hessi, the HESSI database as a pandas dataframe
    """
    
    plt.scatter(hessi['X Pos (asec)'].values, hessi['Y Pos (asec)'].values, color='r', s=0.5)
    plt.show()
    
    pass

def flag_meaning(flag):
    """
    return the meaning of a flag, return all meanings if flag == all
    
    Param:
          flag, string
    
    Return:
           meaning, string
    """
    
    if flag == 'all':
        meaning = "Flare Flag Codes: \na0 - In attenuator state 0 (None) sometime during flare \na1 - In attenuator state 1 (Thin) sometime during flare \na2 - In attenuator state 2 (Thick) sometime during flare \na3 - In attenuator state 3 (Both) sometime during flare \nAn - Attenuator state (0=None, 1=Thin, 2=Thick, 3=Both) at peak of flare \nDF - Front segment counts were decimated sometime during flare\nDR - Rear segment counts were decimated sometime during flare \nED - Spacecraft eclipse (night) sometime during flare\nEE - Flare ended in spacecraft eclipse (night) \nES - Flare started in spacecraft eclipse (night) \nFE - Flare ongoing at end of file \nFR - In Fast Rate Mode \nFS - Flare ongoing at start of file \nGD - Data gap during flare \nGE - Flare ended in data gap\nGS - Flare started in data gap \nMR - Spacecraft in high-latitude zone during flare \nNS - Non-solar event\nPE - Particle event: Particles are present \nPS - Possible Solar Flare; in front detectors, but no position\nPn - Position Quality: P0 = Position is NOT valid, P1 = Position is valid \nQn - Data Quality: Q0 = Highest Quality, Q11 = Lowest Quality\nSD - Spacecraft was in SAA sometime during flare \nSE - Flare ended when spacecraft was in SAA\nSS - Flare started when spacecraft was in SAA"
    elif flag == 'a0':
        meaning = 'a0 - In attenuator state 0 (None) sometime during flare'
    elif flag == 'a1':
        meaning = 'a1 - In attenuator state 1 (Thin) sometime during flare'
    elif flag == 'a2':
        meaning = 'a2 - In attenuator state 2 (Thick) sometime during flare'
    elif flag == 'a3':
        meaning = 'a3 - In attenuator state 3 (Both) sometime during flare'
    elif flag[0] == 'A':
        meaning = 'An - Attenuator state (0=None, 1=Thin, 2=Thick, 3=Both) at peak of flare'
    elif flag == 'DF':
        meaning = 'DF - Front segment counts were decimated sometime during flare'
    elif flag == 'DR':
        meaning = 'DR - Rear segment counts were decimated sometime during flare'
    elif flag == 'ED':
        meaning = 'ED - Spacecraft eclipse (night) sometime during flare'
    elif flag == 'EE':
        meaning = 'EE - Flare ended in spacecraft eclipse (night)'
    elif flag == 'ES':
        meaning = 'ES - Flare started in spacecraft eclipse (night)'
    elif flag == 'FE':
        meaning = 'FE - Flare ongoing at end of file'
    elif flag == 'FR':
        meaning = 'FR - In Fast Rate Mode'
    elif flag == 'FS':
        meaning = 'FS - Flare ongoing at start of file'
    elif flag == 'GD':
        meaning = 'GD - Data gap during flare'
    elif flag == 'GE':
        meaning = 'GE - Flare ended in data gap'
    elif flag == 'GS':
        meaning = 'GS - Flare started in data gap'
    elif flag == 'MR':
        meaning = 'MR - Spacecraft in high-latitude zone during flare'
    elif flag == 'NS':
        meaning = 'NS - Non-solar event'
    elif flag == 'PE':
        meaning = 'PE - Particle event: Particles are present'
    elif flag == 'PS':
        meaning = 'PS - Possible Solar Flare; in front detectors, but no position'
    elif flag[0] == 'P':
        meaning = 'Pn - Position Quality: P0 = Position is NOT valid, P1 = Position is valid'
    elif flag[0] == 'Q':
        meaning = 'Qn - Data Quality: Q0 = Highest Quality, Q11 = Lowest Quality'  
    elif flag == 'SD':
        meaning = 'SD - Spacecraft was in SAA sometime during flare'
    elif flag == 'SE':
        meaning = 'SE - Flare ended when spacecraft was in SAA'
    elif flag == 'SS':
        meaning = 'SS - Flare started when spacecraft was in SAA'
    else:
        meaning = 'Error: invalid flag'
    
    return meaning

if __name__ == '__main__':
    print('Reading HESSI data - this can take some time with current implementation')
    hessi = hessi_flare_dataframe()
    bad_flags = ['NS','SD']
    for flag in bad_flags:
        print(flag_meaning(flag))
    print('Filtering')
    filtered = filter(hessi, bad_flags)
    print('Plotting')
    plot_flare_locations(filtered)
    