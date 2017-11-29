"""Generate temperature images from noaa data.
Don't forget to install the dependencies:
$ pip3 install geopy joblib pygrib click

Example run:

$ python3 plot_temperatures.py --llclat=35 --llclon=-10 \
        --urclat=50 --urclon=30
"""
import matplotlib
matplotlib.use('Agg')  # NOQA

from datetime import timedelta, datetime
from geopy.distance import great_circle
from mpl_toolkits.basemap import Basemap
import click
import joblib
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pygrib
import scipy.interpolate as interpolate
import urllib.request

__author__ = 'johan.mathe@gmail.com'

CAL_COORDS = {'north': 43, 'south': 32, 'west': -125, 'east': -114}
NOAA_SERVER = 'https://nomads.ncdc.noaa.gov/'
N_PROC = 8
# ALL THE LATITUDES ON EARTH!!! OMG!!!
ALL_LONS = np.arange(-180, 180, 0.5)
ALL_LATS = np.arange(90, -90.5, -0.5)


def daterange(start_date, end_date):
    """If you need a comment for this, a career change might be necessary."""
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def download_file(url, local):
    """Download url to a local file if it doens't exist."""
    print('downloading file: %s' % url)
    if os.path.exists(local):
        print('already exists!')
        return
    try:
        urllib.request.urlretrieve(url, local)
    except urllib.request.HTTPError as e:
        if e.code == 404:
            print('%s: %s' % (e, url))
        else:
            raise


def get_url_and_files_from_dates(start_date, end_date):
    """Build a list of url and local files with dates."""
    files_to_download = []
    for date in daterange(start_date, end_date):
        for hour in range(3, 24, 3):
            filename = date.strftime('gfs_4_%%Y%%m%%d_0000_%03d.grb2' % hour)
            uri = ('data/gfs4/%%Y%%m/%%Y%%m%%d/%s' % filename)
            str_fmt = '%s/%s' % (NOAA_SERVER, uri)
            url = date.strftime(str_fmt)
            files_to_download.append((url, filename))
    return files_to_download


def realign_noaa_data(data):
    """Shift NOAA data from 0->360 to -180->180."""
    return np.append(data[:, 360:720], data[:, 0:360], axis=1)


def width_height_from_bbox(llclat, llclon, urclat, urclon):
    """Compute width and height in meters from a given bbox."""
    small_lat = np.min([np.abs(urclat), np.abs(llclat)])
    width = great_circle((llclon, small_lat), (urclon, small_lat)).meters
    height = great_circle((0, llclat), (0, urclat)).meters
    return (width, height)


def render_map(grb_file, llclat, llclon, urclat, urclon, altitude_layer):
    """Given a grb file, renders a jpg map on disk."""
    print('processing file %s ' % grb_file)
    grbs = pygrib.open(grb_file)
    data = grbs.select(name='Temperature')[altitude_layer]['values']
    plt.figure(figsize=(12, 12))

    # We don't like the way noaa aligns things. We like monotonic variations.
    data = realign_noaa_data(data)
    lonlat2temp = interpolate.interp2d(ALL_LONS, ALL_LATS, data, kind='linear')
    lats_interp = np.arange(llclat, urclat, 0.01)
    lons_interp = np.arange(llclon, urclon, 0.01)
    data_interp = lonlat2temp(lons_interp, lats_interp)
    # Size of the img to render in meters.
    width, height = width_height_from_bbox(llclat, llclon, urclat, urclon)
    m = Basemap(
        projection='cass',
        lat_ts=10,
        lat_0=(urclat + llclat) / 2,
        lon_0=(llclon + urclon) / 2,
        resolution='i',
        width=width,
        height=height)
    x, y = m(*np.meshgrid(lons_interp, lats_interp))

    # Draw plenty of fancy stuff
    m.drawstates()
    m.drawcountries()
    m.drawlsmask()
    m.drawrivers()
    m.drawcoastlines()
    m.shadedrelief()
    m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
    m.drawmeridians(np.arange(-180., 180., 60.), labels=[0, 0, 0, 1])
    m.pcolormesh(
        x,
        y,
        data_interp,
        shading='flat',
        cmap=plt.cm.jet,
        alpha=0.05,
        vmin=260,
        vmax=305)
    m.colorbar(location='right')
    plt.title('Temperature')
    image = '%s.jpg' % grb_file
    plt.savefig(image)
    plt.close()


def get_files_to_process(files_to_check):
    """Look on local disk and finds which files to process."""
    files = []
    for local in files_to_check:
        img_name = '%s.jpg' % local

        if os.path.exists(img_name):
            print('skipping %s' % img_name)
            continue
        if not os.path.exists(local):
            continue
        files.append(local)
    return files


@click.command()
@click.option(
    '--llclat', help='Lower left corner lat.', default=CAL_COORDS['south'])
@click.option(
    '--llclon', help='Lower left corner lon.', default=CAL_COORDS['west'])
@click.option(
    '--urclat', help='Upper right corner lat.', default=CAL_COORDS['north'])
@click.option(
    '--urclon', help='Upper right corner lon.', default=CAL_COORDS['east'])
@click.option(
    '--start_date_str', help='Start date YYYY-MM-DD.', default='2017-10-01')
@click.option(
    '--end_date_str', help='End date YYYY-MM-DD.', default='2017-10-02')
@click.option(
    '--altitude_layer', help='Altitude Layer (see NOAA Spec).', default=37)
def main(llclat, llclon, urclat, urclon, start_date_str, end_date_str,
         altitude_layer):
    assert type(llclat) is int
    assert type(llclon) is int
    assert type(llclat) is int
    assert type(llclat) is int
    llclat = int(llclat)
    llclon = int(llclon)
    urclat = int(urclat)
    urclon = int(urclon)
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    url_and_files = get_url_and_files_from_dates(start_date, end_date)
    joblib.Parallel(n_jobs=N_PROC)(joblib.delayed(download_file)(url, local)
                                   for url, local in url_and_files)
    files_allegedly_downloaded = [f[1] for f in url_and_files]
    files_to_process = get_files_to_process(files_allegedly_downloaded)
    joblib.Parallel(n_jobs=N_PROC)(joblib.delayed(render_map)(
        f, llclat, llclon, urclat, urclon, altitude_layer)
                                   for f in files_to_process)


if __name__ == '__main__':
    main()
