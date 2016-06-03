# Download the french citites dataset
# !curl http://freakonometrics.free.fr/popfr19752010.csv > french_cities.csv
# !curl http://johmathe.nonutc.fr/presidentielles.tar.bz2 > presidentielles.tar.bz2
# !tar -jxvf presidentielles.tar.bz2


from mpl_toolkits.basemap import Basemap
from scipy.interpolate import Rbf
import csv
import editdistance
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pygrib
import unicodedata
from scipy import interpolate.Rbf

FR_LATMIN = 40
FR_LATMAX = 53
FR_LONMIN = -7
FR_LONMAX = 10

cities = []
with open('french_cities.csv') as f:
    csvreader = csv.reader(f)
    for r in csvreader:
        cities.append(r)

file_mappings = {2007: 'presidentielles_data/presidentielles_2007.csv.0',
                 2012: 'presidentielles_data/presidentielles_2012.csv.0',
                 2002:
                 'presidentielles_data/presidentielles_2002_1ertour.csv.0'}
# 1995: 'presidentielles_data/presidentielles_1995.csv.0'}
elections = {}

for y, f in file_mappings.items():
    print('Reading election file for year', y)
    with open(f) as fd:
        csvreader = csv.reader(fd)
        for r in csvreader:
            elections.setdefault(y, []).append(r)


def plot_france_locations(locations,
                          vmin=None,
                          vmax=None,
                          scale='LogNorm',
                          title=''):
    """
    :locations: [(lat, lon, data), ...]
    """
    # create new figure, axes instances.
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # setup mercator map projection.
    m = Basemap(llcrnrlon=FR_LONMIN,
                llcrnrlat=FR_LATMIN,
                urcrnrlon=FR_LONMAX,
                urcrnrlat=FR_LATMAX,
                rsphere=(6378137.00, 6356752.3142),
                resolution='h',
                projection='merc',
                lat_0=40.,
                lon_0=-20.,
                lat_ts=20.)

    m.drawcoastlines()
    m.fillcontinents()
    m.drawparallels(np.arange(10, 90, 2), labels=[1, 1, 0, 1])
    m.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 0, 1])

    ax.set_title(title)

    lats = [float(c[0]) for c in locations]
    lons = [float(c[1]) for c in locations]

    # We'll take the log, we better make this one >= 1.
    data = [float(c[2]) for c in locations]

    # Normalize with regards to log of the population.
    if vmin is None:
        vmin = 1
    if vmax is None:
        vmax = max(data)
    if scale is 'LogNorm':
        norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=vmax)
        data = [d + 1 for d in data]
    else:
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)

    # Do the actual plot.
    cmap = matplotlib.cm.get_cmap('hot')
    for i, (d, lat, lon) in enumerate(zip(data, lats, lons)):
        # pop = myrbf(lon, lat)
        x, y = m(lat, lon)
        m.plot(x, y, '.', color=cmap(norm(d)), markersize=5)

    # A colorbar. That was extremely painful. Thank you internet.
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    plt.colorbar(sm)


def plot_elections_participation(elections_data, title=''):
    PARTICIPATION_ID = 13
    CITY_ID = 3
    participations = [float(e[PARTICIPATION_ID]) for e in elections_data[1:]]

    latlon_val = []
    for e in elections_data[1:]:
        try:
            latlon_val.append(normalized_latlons[e[CITY_ID]] + (float(e[
                PARTICIPATION_ID]), ))
        except KeyError:
            pass

    sigma = np.std(participations)
    mu = np.mean(participations)
    vmin = mu-2*sigma
    vmax = mu+2*sigma
    plot_france_locations(latlon_val,
                          vmin,
                          vmax,
                          scale='Normalize',
                          title=title)


def plot_temperature_for_day(date, elections_data, title=''):
    PARTICIPATION_ID = 13
    CITY_ID = 3
    participations = [float(e[PARTICIPATION_ID]) for e in elections_data[1:]]

    latlon_val = []
    for e in elections_data[1:]:
        try:
            latlon_val.append(normalized_latlons[e[CITY_ID]] + (float(e[
                PARTICIPATION_ID]), ))
        except KeyError:
            pass

    sigma = np.std(participations)
    mu = np.mean(participations)
    vmin = mu-2*sigma
    vmax = mu+2*sigma
    plot_france_locations(latlon_val,
                          vmin,
                          vmax,
                          scale='Normalize',
                          title=title)


plot_france_locations(
    [(c[5], c[6], c[8]) for c in cities[1:]],
    title='City Temperatures, 2002/04/17',
    vmin=2,
    vmax=15,
    scale='bs')


# Clean up the city keys. This code is pretty slow, so keep the
# normalized_latlons in memory and don't call the normalization
# funciton often.


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u''.join([c for c in nfkd_form if not unicodedata.combining(c)])


def normalize_city_to_latlon(elections, cities):
    city_dic = {}
    for c in cities[1:]:
        city_name = remove_accents(c[3].lower() + c[4].lower())
        city_dic[city_name] = (c[5], c[6])
    misses = 0
    city_to_latlon = {}
    for e in elections[1:]:
        try:
            city_name = remove_accents(e[3].lower())
            city_to_latlon[e[3]] = city_dic[city_name]
        except KeyError:
            distances = []
            for city in city_dic:
                distances.append((editdistance.eval(city, city_name), city))
            best_city = min(distances)
            if best_city[0] > 1:
                misses += 1
            else:
                city_to_latlon[e[3]] = city_dic[best_city[1]]
    return city_to_latlon



normalized_latlons = normalize_city_to_latlon(elections, cities)


for y, data in elections.items():
    plt.figure()
    plot_elections_participation(data, title='Presidentielles %s' % y)



plt.figure(figsize=(10,10))
for i, (y, d) in enumerate(elections.items()):
    plt.subplot(3, 1, i + 1)
    part = [float(d[13]) for d in elections[y][1:]]
    plt.hist(part, 150)
    plt.title('Histogram of participation rate for year %s' % y)
    plt.xlim(40, 100)
    plt.grid()




grbs = pygrib.open('res2')
for grb in grbs:
    print(grb)

data=grb.values - 273.15

lat,lon = grb.latlons()


# From this point on the code is almost identical to the previous example.
# Plot the field using Basemap. Start with setting the map projection using the limits of the lat/lon data itself:

fig = plt.figure(figsize=(10, 10))
m = Basemap(lon_0=180,
            projection='mill',
            llcrnrlon=-180,
            llcrnrlat=-90,
            urcrnrlat=90,
            urcrnrlon=180,
            resolution='i')

# Convert the lat/lon values to x/y projections.
x, y = m(lon, lat)
cs = m.pcolormesh(x,y,data,shading='flat',cmap=plt.cm.hot)
# Add a coastline and axis values.
m.drawcoastlines()

# Add a colorbar and title, and then show the plot.
plt.title('Global Temperatures on 2002 Election day')
plt.show()


newlats = []
newlons = []
newdata = []
for i, la in enumerate(lat.flatten()):
    lo = lon.flatten()[i]
    if lo > 180:
        lo -= 360
    if la > FR_LATMIN and la < FR_LATMAX and lo > FR_LONMIN and lo < FR_LONMAX:
        newlats.append(la)
        newlons.append(lo)
        newdata.append(data.flatten()[i])
        print(data.flatten()[i])

myrbf = interpolate.Rbf(newlats, newlons, newdata)


print(myrbf(2.35,48))
