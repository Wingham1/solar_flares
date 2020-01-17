# solar_flares
A project for classifying images of solar flares (currently B and C)

Data collection files include:
    hessi_df.py - this uses the HESSI mission to get a pandas dataframe with the HESSI data (primarily accurate flare locations and dates)
    goes_df.py - this uses the GOES mission to get a pandas dataframe with the GOES data (dates and class)
    interesct_hessi_goes.py - this combines the HESSI and GOES dataframes to create a new dataframe with the date, location and class
    download_images.py - this uses the combined data to download images of the flare

Classification:
    cnn.py - uses a builds, trains, saves, loads and evalutes a CNN to classifiy images of solar flares

Libraries include:
    numpy==1.17.2
    matplotlib==3.11
    pandas==0.25.1
    sunpy==1.1.0
    scikit-learn==0.22.1
    opencv-python==4.1.126
    tensorflow==1.14.0
