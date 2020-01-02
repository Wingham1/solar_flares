import hessidf

if __name__ == '__main__':
    HESSI = hessidf.hessi_flare_dataframe()
    hessidf.plot_flare_locations(HESSI)
    #loc = find_locations(HESSI, 'A')
    #print(loc)
