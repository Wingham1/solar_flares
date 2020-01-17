"""
This script uses data from the hessi mission to find the location (x, y, in arcsec) of flares and their dates,
and the goes mission to find the class of flares and their dates, then it makes a new dataset with the date, class and location of each flare,
the dataset is exported to a csv file so it can be read into a pandas dataframe for future projects.

"""

import hessi_df as hdf
import goes_df as gdf
import datetime as dt
import pandas as pd

def intersect_hessi_goes(to_csv=False):
    """
    Groups the datetime, location and class of each solar flare in one dataframe (GOES mass missing location data and isn't as accurate)
    
    Param:
          to_csv boolean, if True -> export the datframe to csv
    
    Return:
           data pandas dataframe, this contains the matched flares with their date, location and class
    """
    
    # HESSI mission has good locations for flares with their dates
    print('Getting HESSI flare data')
    hessi = hdf.hessi_flare_dataframe(web=False)
    
    # filtering
    print('Filtering')
    bad_flags = ['NS','SD'] # NS non solar event, SD spacecraft in South Atlantic Anomaly where magnetic data is weird https://image.gsfc.nasa.gov/poetry/ask/q525.html
    hessi = hdf.filter(hessi, bad_flags)
    print(hessi.head())
    
    # GOES mission is used to classify flares with their dates
    print('Getting GOES flare data')
    goes = gdf.goes_dataframe()
    print(goes.head())
    
    # Combine, for each flare in GOES find the flare in HESSI for the accurate location
    print('Using dates to match flares in each dataset and create a new dataframe')
    data = {'Peak_time': [], 'X_pos': [], 'Y_pos': [], 'Class': []}
    for idx, row in goes.iterrows():        
        match = hessi[hessi['Peak_time'].between(row['Start_time'], row['End_time'])]
        # currently only find flares where there was one match (multiple flares happening together are ignored)
        if len(match.index) == 1:
            hessi_idx = match.index
            data['Peak_time'].append(match['Peak_time'].to_numpy()[0]) # use to_numpy!!
            data['X_pos'].append(match['X Pos (asec)'].to_numpy()[0])
            data['Y_pos'].append(match['Y Pos (asec)'].to_numpy()[0])
            data['Class'].append(row['Class'])
    data = pd.DataFrame.from_dict(data)
    print('total flares = {}, num B class = {}, num C class = {}'.format(len(data.index), len(data[data['Class'] == 'B'].index), len(data[data['Class'] == 'C'].index)))
    print(data.head())
    if to_csv:
        data.to_csv('hessi_goes_flare_data.csv', index=False)
    
    return data

if __name__ == '__main__':
    together = intersect_hessi_goes(to_csv=True)
    