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
import hessidf as hdf
import os


def get_image(t, x, y):
    #get some data
    result = Fido.search(a.Time(t - dt.timedelta(seconds=10), t), a.Instrument("aia"), a.Wavelength(94*u.angstrom), a.vso.Sample(12*u.second))
    print('found result')
    #print(result)

    #download the data
    file_download = Fido.fetch(result[0, -1], site='ROB')
    print('downloaded data')
    #print(file_download)

    #load the data to a sun map
    aia1 = sunpy.map.Map(file_download)
    print('loaded to sun map')
    #print(aia1)

    #calibrate it
    aia = aiaprep(aia1)
    print('calibrated')
    
    #plot it
    aia.plot()
    plt.colorbar()
    #plt.show()
    
    co_ords = hdf.get_box_coord(x, y, 100)
    tr = co_ords[1]
    bl = co_ords[2]
    
    #sub-map
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

    data = pd.read_csv('cross_data.csv')
    data['Peak_time'] = pd.to_datetime(data['Peak_time'], format='%Y-%m-%d %H:%M:%S')
    data = data[data['Peak_time'] >= dt.datetime.strptime('2010-06-06 02:52:58', '%Y-%m-%d %H:%M:%S')]
    print(data.head())
    print('number of valid flares = {}'.format(len(data.index)))

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