import hessidf as hdf

if __name__ == '__main__':

    print(hdf.goes_dataframe())

    """
    HESSI = hessidf.hessi_flare_dataframe()
    
    # filtering
    bad_flags = ['NS','SD'] # NS non solar event, SD spacecraft in South Atlantic Anomaly where magnetic data is weird https://en.wikipedia.org/wiki/South_Atlantic_Anomaly
    HESSI = hessidf.filter(HESSI, bad_flags)
    
    hessidf.plot_flare_locations(HESSI)
    #loc = find_locations(HESSI, 'A')
    #print(loc)
    """
