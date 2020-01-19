# solar_flares
A project for classifying images of solar flares (currently B and C flares during the peak flare time)

## Description
This project can load data from the NASA HESSI satellite and the NOAA GOES satellite into pandas DataFrame objects and combine matching flares.
It can use the flare information from these missions to download greyscale images taken by NASA's SDO in the 94A EUV part of the spectrum using the AIA instrument.
Finally it uses these images to train a CNN and classify images of the solar flares.

NASA - National Aeronautics and Space Administration
HESSI - High Energy Solar Spectroscopic Imager
NOAA - National Oceanic and Atmospheric Administration
GOES - Geostationary Operational Environment Satellite
SDO - Solar Dynamics Orbiter
94A - 94 angstrom wavelength
EUV - Extreame Ultra Violet
CNN - Convolutional Neural Network

## Data collection files include:
    hessi_df.py - this uses the HESSI mission to get a pandas dataframe with the HESSI data (primarily accurate flare locations and dates)\n
    goes_df.py - this uses the GOES mission to get a pandas dataframe with the GOES data (dates and class)\n
    interesct_hessi_goes.py - this combines the HESSI and GOES dataframes to create a new dataframe with the date, location and class\n
    download_images.py - this uses the combined data to download images of the flare\n

## Classification:
    cnn.py - uses a builds, trains, saves, loads and evalutes a CNN to classifiy images of solar flares

## Libraries include:
    numpy==1.17.2\n
    matplotlib==3.11\n
    pandas==0.25.1\n
    sunpy==1.1.0\n
    scikit-learn==0.22.1\n
    opencv-python==4.1.126\n
    tensorflow==1.14.0\n

## Instal dependancies with pip
```bash
pip install -r requirements.txt
```

## Roadmap
I want to include some options to use images of the solar active regioins some time before a flare to aid flare prediction capabilities.
I would also like to try using different wavlengths available from the AIA instrument and try a combination of wavelengths to improve accuracy.

## License

Copyright (c) [2020] [Matthew Wingham]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.