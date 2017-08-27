# -*- coding: utf-8 -*-
# CHAMP卫星一天的数据处理

# import os
import numpy as np
import matplotlib.pyplot as plt

# 定义结构数组
data_type = np.dtype({
    "names": ['S_GPS', 'Year', 'Month', 'Day', 'Hour', 'minute', 'second', 'radius',
              'geo-latitude', 'geo-longitude', 'Ne'],
    'formats': ['i', 'i', 'i', 'i', 'i', 'i', 'i', 'f', 'f', 'f', 'i']
})

datafile = "C:\\DATA\\CHAMP\\2003\\CH-ME-2-PLP+2003-03-01_3.dat"
this_data = np.loadtxt(datafile, dtype=data_type)

len_data = len(this_data)
print('len(data):', len_data)


# ==================================== # 电子密度纬度剖面,每日一幅图
def ne_latitude(data, output_path) -> bool:
    rows = 6
    cols = 6
    abs_max_lat = 80                   # 选取数据的最大纬度
    i = 0
    num = 0  # 子图数

    f = plt.figure(figsize=(25, 20))
    while i < len_data - 1:
        while abs(data[i]['geo-latitude']) > abs_max_lat:
            i += 1
            if i == len_data:
                break
        else:                          # first指向第一个纬度小于 abs_max_lat的数据
            first = i
            while abs(data[i]['geo-latitude']) <= abs_max_lat:
                i += 1
                if i == len_data - 1:
                    last = i            # last指向最后一个纬度小于 abs_max_lat的数据
                    print(last, i)
                    break
            else:
                last = i - 1
                i += 1
        if i == last or i == last + 2:  # 避免结尾数据纬度超过范围时画图
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
            plt.show()

            #f.savefig(output_path + '{}-{}-{}'.format(data[-1]['Year'], data[-1]['Month'], data[-1]['Day']))
    return True

figure_path = 'C:\\DATA\\CHAMP\\figure\\Ne\\2003\\'
ne_latitude(this_data, figure_path)
