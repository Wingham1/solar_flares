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
    header = ['Flare', 'Start', 'Peak', 'End', 'Dur (s)', 'Peak (c/s)', 'Total (Counts)', 'Energy (keV)', 'X Pos (asec)', 'Y Pos (asec)', 'Radial (asec)', 'AR', 'Flags']
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
    
    for idx, row in df.iterrows():
        if row['End'] < row['Start']:
            row.loc['End'] = row['End'].replace(day = row['End'].day + 1)
        if row['Peak'] < row['Start']:
            row.loc['Peak'] = row['Peak'].replace(day = row['Peak'].day + 1)
        if row['End'] < row['Start']:
            print("end error")
        if row['Peak'] < row['Start']:
            print("peak error")
           
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

def get_box_coord(flare_x, flare_y, box_size):
    """
    A function that takes a flare location and returns co-ordinates for a box around the flare
    
    Param: flare_x,integer flare location x
           flare_y, integer flare location y
           box_size, length of the sides of the box
    
    return: list of tuple integers for the vertices of a box of a given size around a flare (top left, top right, bottom left, bottom right)
    """
    
    return [(flare_x - 0.5*box_size, flare_y + 0.5*box_size), (flare_x + 0.5*box_size, flare_y + 0.5*box_size), (flare_x - 0.5*box_size, flare_y - 0.5*box_size), (flare_x + 0.5*box_size, flare_y - 0.5*box_size)]

def flag_meanings():
    """
    print the meanings of the flags
    """
    
    print("Flare Flag Codes: \na0 - In attenuator state 0 (None) sometime during flare \na1 - In attenuator state 1 (Thin) sometime during flare \na2 - In attenuator state 2 (Thick) sometime during flare \na3 - In attenuator state 3 (Both) sometime during flare \nAn - Attenuator state (0=None, 1=Thin, 2=Thick, 3=Both) at peak of flare \nDF - Front segment counts were decimated sometime during flare\nDR - Rear segment counts were decimated sometime during flare \nED - Spacecraft eclipse (night) sometime during flare\nEE - Flare ended in spacecraft eclipse (night) \nES - Flare started in spacecraft eclipse (night) \nFE - Flare ongoing at end of file \nFR - In Fast Rate Mode \nFS - Flare ongoing at start of file \nGD - Data gap during flare \nGE - Flare ended in data gap\nGS - Flare started in data gap \nMR - Spacecraft in high-latitude zone during flare \nNS - Non-solar event\nPE - Particle event: Particles are present \nPS - Possible Solar Flare; in front detectors, but no position\nPn - Position Quality: P0 = Position is NOT valid, P1 = Position is valid \nQn - Data Quality: Q0 = Highest Quality, Q11 = Lowest Quality\nSD - Spacecraft was in SAA sometime during flare \nSE - Flare ended when spacecraft was in SAA\nSS - Flare started when spacecraft was in SAA")
    
    pass
    

def goes_dataframe():
    """
    return a dataframe for the goes flare data
    """
    
    df = pd.DataFrame()
    
    for y in range(2, 18, 1):
    
        """
        2006
        https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_2006.txt
        https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_2008.txt
        """
        
        year = 2000 + y
        
        if year == 2015:
            url = 'https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_' + str(year) + '_modifiedreplacedmissingrows.txt'
        elif year == 2017:
            url = 'https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_' + str(year) + '-ytd.txt'
        else:
            url = 'https://www.ngdc.noaa.gov/stp/space-weather/solar-data/solar-features/solar-flares/x-rays/goes/xrs/goes-xrs-report_' + str(year) + '.txt'
        
        #clean
        goes = pd.read_fwf(url, sep='\t', lineterminator='\n', header=None)
        header = ['Date', 'Start_time', 'End_time', 'Peak_time', 'Class']
        d = pd.Series([str(code)[5:11] for code in goes.iloc[:, 0].values])
        s = pd.Series(goes_times(goes, 1))
        e = pd.Series(goes_times(goes, 2))
        p = pd.Series(goes_times(goes, 3))
        c = goes.iloc[:, 5]
        #i = pd.Series(goes.iloc[:, 6].values / 10)
        goes = pd.concat([d, s, e, p, c], axis=1)
        goes.columns = header
        goes.dropna(inplace=True)
        goes = goes[goes['Peak_time'] != '////'] # revome this row in 2011, its strange and thros and error
        goes['Date'] = pd.to_datetime(goes['Date'], format='%y%m%d')
        for i in range(1, 4):
            goes[header[i]] = pd.to_datetime(goes[header[i]], format='%H%M').dt.time
        
        df = pd.concat([df, goes])
        
    return df

def goes_times(goes, idx):
    e = []
    for code in goes.iloc[:, idx].values:
        time_string = str(code).split('.')[0]
        if time_string != 'nan':
            while len(time_string) < 4:
                time_string = '0' + time_string
        e.append(time_string)
    return e
