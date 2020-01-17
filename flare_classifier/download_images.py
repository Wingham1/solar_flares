"""
A script to download EUV images of B and C class solar flares using a combination of HESSI and GOeS flare data
"""

from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = [10, 9]  # make plots larger

import sunpy.map
from sunpy.instr.aia import aiaprep
from sunpy.net import Fido, attrs as a

from astropy.coordinates import SkyCoord
from astropy import units as u

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import datetime as dt
import os

def get_box_coord(flare_x, flare_y, box_size):
    """
    A function that takes a flare location and returns co-ordinates for a box around the flare
    
    Param: flare_x,integer flare location x
           flare_y, integer flare location y
           box_size, length of the sides of the box
    
    return: list of tuple integers for the vertices of a box of a given size around a flare (top left, top right, bottom left, bottom right)
    """
    
    return [(flare_x - 0.5*box_size, flare_y + 0.5*box_size), (flare_x + 0.5*box_size, flare_y + 0.5*box_size), (flare_x - 0.5*box_size, flare_y - 0.5*box_size), (flare_x + 0.5*box_size, flare_y - 0.5*box_size)]

def get_image(t, x, y):
    """
    This function gets an AIA EUV image from the SDO (AIA = Atmospheric Imaging Assembly, EUV = Extreme UltraViolent, SDO = SOlar Dynamics Observatory)
    at a given time t, and crops the image to given location x, y.
    
    Param:
          t datetime, the datetime of the flare
          x integer, the longitude position of the flare in arcsec
          y integer, the latitude position of the flare in arcsec
    
    Return:
           aia_sub sunpy Map, the cropped image
    """

    # request the data for the given time
    result = Fido.search(a.Time(t - dt.timedelta(seconds=10), t), a.Instrument("aia"), a.Wavelength(94*u.angstrom), a.vso.Sample(12*u.second))
    print('found result')
    #print(result)

    # download the data
    file_download = Fido.fetch(result[0, -1], site='ROB')
    print('downloaded data')
    #print(file_download)

    # load the data to a sun map
    aia1 = sunpy.map.Map(file_download)
    print('loaded to sun map')
    #print(aia1)

    # calibrate it
    aia = aiaprep(aia1)
    print('calibrated')
    
    # plot it
    aia.plot()
    plt.colorbar()
    #plt.show()
    
    # get the co-ordinates of the top right and bottom left of the crop box
    co_ords = get_box_coord(x, y, 100)
    tr = co_ords[1]
    bl = co_ords[2]
    
    # sub-map
    top_right = SkyCoord(tr[0]*u.arcsec, tr[1]*u.arcsec, frame=aia.coordinate_frame)
    bottom_left = SkyCoord(bl[0]* u.arcsec, bl[1]* u.arcsec, frame=aia.coordinate_frame)
    aia_sub = aia.submap(top_right, bottom_left)
    aia_sub.plot_settings['cmap'] = plt.get_cmap('Greys_r')
    ax = plt.subplot(projection=aia_sub)
    aia_sub.plot()
    #plt.show()
    print('made sub map')

    return aia_sub

if __name__ == '__main__':
    
    # get the flare data
    data = pd.read_csv('hessi_goes_flare_data.csv')
    data['Peak_time'] = pd.to_datetime(data['Peak_time'], format='%Y-%m-%d %H:%M:%S')
    data = data[data['Peak_time'] >= dt.datetime.strptime('2010-06-06 02:52:58', '%Y-%m-%d %H:%M:%S')] # SDO started after HESSI and GOES!!!!
    print(data.head())
    print('number of valid flares = {}'.format(len(data.index)))
    
    # save the images to their respective directories
    for idx, row in data.head().iterrows():
        print('getting image {}/{}'.format(idx, len(data.index)))
        img = get_image(row['Peak_time'], row['X_pos'], row['Y_pos'])
        img.plot()
        img_name = str(row['Peak_time']).replace(' ', '_').replace(':', '_').replace('-', '_') + '.png'
        if row['Class'] == 'B':
            img_name = os.path.join('B_class', img_name)
        elif row['Class'] == 'C':
            img_name = os.path.join('C_class', img_name)
        plt.imsave(fname = os.path.join('data', img_name), arr=img.data, cmap = plt.cm.gray)
        print('image saved\n')
    print('Done')