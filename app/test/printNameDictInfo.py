#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/11/2 2:25 PM
@desc:
'''


def dictCount(dict,key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1

if __name__ == '__main__':
    nameMapDict = {}
    # 读取 nameMapFile , 获取图片类别
    with open("renameMap", 'r') as f:
        nameMapLines = f.readlines()
        for i in range(0, len(nameMapLines)):
            kv = nameMapLines[i].rstrip('\n').split("\t")
            nameMapDict[kv[1]] = kv[0]

    keys = nameMapDict.keys()
    # dense_4_normal_daytime_urban_v1539936572761_011.jpeg

    # 天气：正常（normal）  多云（cloudy） 雨天（rainy）
    # 时段：白天（daytime）    傍晚（dusk）  夜晚（night）
    # 道路：城市道路（urban）高速道路（expressway）
    # normal_daytime_urban.mp4
    densityDict = {}  # 密度
    weatherDict = {}  # 天气
    timeSlotDict = {}  # 时间段
    scenesDict = {}  # 场景

    for i in keys:
        try:
            splits = i.split("_")
            density = splits[0]
            weather = splits[2]
            timeSlot = splits[3]
            scenes = splits[4]

            dictCount(densityDict, density)
            dictCount(weatherDict, weather)
            dictCount(timeSlotDict, timeSlot)
            dictCount(scenesDict, scenes)
        except Exception as e:
            print("error,i=%s , e=%s" % (i, e))

    print(densityDict)
    print(weatherDict)
    print(timeSlotDict)
    print(scenesDict)
    print("total count=%s" %len(keys))