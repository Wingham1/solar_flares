import pandas as pd
import datetime as dt

def goes_dataframe():
    """
    Uses the web to make a dataframe for the GOES flare data (2002 - 2017)
    
    Return:
           df pandas dataframe
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
        goes = goes[goes['Peak_time'] != '////'] # revome this row in 2011, its strange and throws and error
        goes['Date'] = pd.to_datetime(goes['Date'], format='%y%m%d')
        for i in range(1, 4):
            goes[header[i]] = pd.to_datetime(goes[header[i]], format='%H%M')
            for idx, row in goes.iterrows():
                date = row['Date']
                goes.iat[idx-1, i] = row[header[i]].replace(day = date.day, month=date.month, year=date.year)
        for idx, row in goes.iterrows():
            if row['End_time'] < row['Start_time']:
                row.loc['End_time'] = row['End_time'] + dt.timedelta(days=1)
            if row['Peak_time'] < row['Start_time']:
                row.loc['Peak_time'] = row['Peak_time'] + dt.timedelta(days=1)
        goes.drop(columns='Date', inplace=True)
        
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