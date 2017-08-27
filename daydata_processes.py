# -*- coding: utf-8 -*-
# CHAMP卫星一天的数据处理

import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

# 定义结构数组
data_type = np.dtype({
    "names": ['S_GPS', 'Year', 'Month', 'Day', 'Hour', 'minute', 'second', 'radius',
              'geo-latitude', 'geo-longitude', 'Ne'],
    "formats": ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'f', 'f', 'f', 'i']
})
datafile = "C:\\DATA\\CHAMP\\2003\\CH-ME-2-PLP+2003-03-01_1.dat"
thisdata = np.loadtxt(datafile, dtype=data_type)

len_data = len(thisdata)  # 记录数据数
print('len(data):', len_data)


def height(data):
    """
    plot the height variation of CHAMP in one day
    :return: bool
    """
    r = 6371.393
    h = data[:]['radius'] - r
    t = data[:]['Hour'] + data[:]['minute'] / 60

    plt.plot(t, h, '.')
    plt.xlabel('time(Hour)')
    plt.ylabel('H_satellite(Km)')
    time = str(data[0]['Year']) + '-' + str(data[0]['Month']) + '-' + str(data[0]['Day'])
    plt.title('The Height of CHAMP satellite at {0}'.format(time))

    print('time of picture:', time)
    plt.savefig('E:\\master\\pic\\CHAMP\\' + str(time), fmt='png', dpi=200)

    plt.show()


def orbit(data, output_path):
    """
    give the projection of the CHAMP's orbit in one day on the map
    :param output_path: tht picture output path
    :param data: datafile
    :return: None
    """
    from mpl_toolkits.basemap import Basemap
    figure = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='l')
    figure.drawcoastlines(linewidth=0.5)

    figure.drawmapboundary(fill_color='aqua')
    figure.fillcontinents(color='coral', lake_color='aqua')

    figure.drawparallels(np.arange(-80., 81., 20.))
    figure.drawmeridians(np.arange(-180., 181., 20))

    glon, glat = data[:]['geo-longitude'], data[:]['geo-latitude']
    mask_y = abs(glat) > 80                              # 设置掩码数组
    my = ma.array(glat, mask=mask_y)

    x, y = figure(glon, my)
    figure.plot(x, y, 'b')

    plt.title("CHAMP satellite's orbit projection")
    time = str(data[0]['Year']) + '-' + str(data[0]['Month']) + '-' + str(data[0]['Day'])
    plt.savefig(output_path + str(time + 'orbit'), fmt='png', dpi=200)

    plt.show()


def ne_latitude(data, output_path):
    rows = 6
    cols = 6
    abs_max_lat = 80  # 选取数据的最大纬度
    i = 0
    num = 0  # 子图数

    f = plt.figure(figsize=(25, 20))
    while i < len_data - 1:
        while abs(data[i]['geo-latitude']) > abs_max_lat:
            i += 1
            if i == len_data:
                break
        else:                                     # first指向第一个纬度小于 abs_max_lat的数据
            first = i
            while abs(data[i]['geo-latitude']) <= abs_max_lat:
                i += 1
                if i == len_data - 1:
                    last = i                       # last指向最后一个纬度小于 abs_max_lat的数据
                    print(last, i)
                    break
            else:
                last = i - 1
                i += 1
        if i == last or i == last + 2:            # 避免结尾数据纬度超过范围时画图
            num += 1
            f.add_subplot(rows, cols, num)
            x = data[first:last]['geo-latitude']
            y = data[first:last]['Ne'] / 10 ** 5
            label = '{}-{}'.format(data[last]['Hour'], data[last]['minute'])
            plt.plot(x, y, 'k', label=label)
            plt.xlabel('geo-latitude', horizontalalignment='center')
            plt.xticks(list(range(-90, 110, 20)))
            plt.ylabel('Ne(10^5)', horizontalalignment='center')
            plt.legend()
            plt.title('{}-{}'.format(data[last]['Hour'], data[last]['minute']))

            f.savefig(output_path + '{}-{}-{}'.format(data[-1]['Year'], data[-1]['Month'], data[-1]['Day']))


figure_path = "C:\\DATA\\CHAMP\\figure\\"
orbit(thisdata, figure_path)
print('done')
