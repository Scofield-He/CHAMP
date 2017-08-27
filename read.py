# -*- coding: utf-8 -*-
# CHAMP卫星日数据处理

import os
import numpy as np
import matplotlib.pyplot as plt

# 定义结构数组
data_type = np.dtype({
    "names": ['S_GPS', 'Year', 'Month', 'Day', 'Hour', 'minute', 'second',
              'radius', 'geo-latitude', 'geo-longitude', 'Ne'],
    'formats': ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'f', 'f', 'f', 'i']
})


def ne_latitude(data, out_path):
    rows = 6
    cols = 6
    abs_max_lat = 80  # 选取数据的最大纬度
    i = 0
    num_subplot = 0  # 子图数
    len_data = len(data)
    f = plt.figure(figsize=(25, 20))
    while i < len_data - 1:
        while abs(data[i]['geo-latitude']) > abs_max_lat:
            i += 1
            if i == len_data:
                break
        else:  # first指向第一个纬度小于 abs_max_lat的数据
            first = i
            try:
                while abs(data[i]['geo-latitude']) <= abs_max_lat:
                    i += 1
                    if i == len_data - 1:
                        last = i  # last指向最后一个纬度小于 abs_max_lat的数据
                        print(len_data, last, i, end=' ')
                        break
                else:
                    last = i - 1
                    i += 1
            except IndexError:
                print('IndexError occur')

            try:
                while abs(data[i]['geo-latitude']) <= abs_max_lat:
                    i += 1
                    if i == len_data - 1:
                        last = i  # last指向最后一个纬度小于 abs_max_lat的数据
                        print(len_data, last, i, end=' ')
                        break
                else:
                    last = i - 1
                    i += 1
            except IndexError:
                print('IndexError occur')

        if i == last or i == last + 2:  # 避免结尾数据纬度超过范围时画图
            num_subplot += 1
            f.add_subplot(rows, cols, num_subplot)
            x = data[first:last]['geo-latitude']
            y = data[first:last]['Ne'] / 10 ** 5
            label = '{}-{}'.format(data[last]['Hour'], data[last]['minute'])
            plt.plot(x, y, 'k', label=label)
            plt.xlabel('geo-latitude', horizontalalignment='center')
            plt.xticks(list(range(-90, 110, 20)))
            plt.ylabel('Ne(10^5)', horizontalalignment='center')
            plt.legend()

    f.savefig(out_path + '{}-{}-{}'.format(data[-1]['Year'], data[-1]['Month'], data[-1]['Day']))
    print('{}-{}'.format(data[-1]['Month'], data[-1]['Day']))
    plt.close()


count_3 = 0
num = 0
datapath = "C:\\DATA\\CHAMP\\2002\\"
outpath = 'C:\\DATA\\CHAMP\\figure\\Ne\\2002\\'
for datafile in os.listdir(datapath):
    if '_3' in datafile and 'dat' in datafile:  # 处理名称中包含'_3'，后缀为'.dat'的文件
        count_3 += 1  # 记录文件数
        dat = np.loadtxt(datapath + datafile, dtype=data_type)
        if len(dat[0]) == 11:
            num += 1
        if dat['Month'][-1] > 11:
            ne_latitude(dat, outpath)


print('the number of _3.data file: --> {}'.format(count_3))
print('the number of length == 11 datafile: --> {}'.format(num))
print('finished')
