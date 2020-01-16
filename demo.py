import hessidf as hdf
import datetime as dt
from collections import defaultdict
import pandas as pd

if __name__ == '__main__':
    """
    I want to find the datetime, location and class of each solar flare
    """
    
    # HESSI mission has good locations for flares with their dates
    HESSI = hdf.hessi_flare_dataframe()
    
    # filtering
    bad_flags = ['NS','SD'] # NS non solar event, SD spacecraft in South Atlantic Anomaly where magnetic data is weird https://image.gsfc.nasa.gov/poetry/ask/q525.html
    HESSI = hdf.filter(HESSI, bad_flags)
    print(HESSI.head())
    
    # GOES mission is used to classify flares with their dates
    GOES = hdf.goes_dataframe()
    print(GOES.head())
    
    """
    TODO: for each flare in goes, find its location in hessi
    """
    data = {'Peak_time': [], 'X_pos': [], 'Y_pos': [], 'Class': []}
    for idx, row in GOES.iterrows():        
        match = HESSI[HESSI['Peak_time'].between(row['Start_time'], row['End_time'])]
        """
        find index of the matched row in hessi
        """
        if len(match.index) == 1:
            hessi_idx = match.index
            data['Peak_time'].append(match['Peak_time'].to_numpy()[0]) # use to_numpy!!
            data['X_pos'].append(match['X Pos (asec)'].to_numpy()[0])
            data['Y_pos'].append(match['Y Pos (asec)'].to_numpy()[0])
            data['Class'].append(row['Class'])
    data = pd.DataFrame.from_dict(data)
    print('total flares = {}, num B class = {}, num C class = {}'.format(len(data.index), len(data[data['Class'] == 'B'].index), len(data[data['Class'] == 'C'].index)))
    data.to_csv('cross_data.csv', index=False)
    