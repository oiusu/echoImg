#!/usr/bin/env python
# encoding: utf-8
'''
抽取图片
@author: chenc
@time: 2018/10/26 9:57 AM
@desc:
'''
import random
import shutil
import time
from optparse import OptionParser, OptionGroup
from gevent import os

def dictCount(dict,key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def parseArgs():
    Args = {"extractNum": 0}
    parser = OptionParser(usage="\n%prog [options] ", version="%prog 1.1")
    parser.add_option("-n", "--extractNum",
                      action="store", dest="extractNum",
                      help='''抽取数量''')
    group = OptionGroup(parser, 'Warning',
                        "Default and Necessary option:   '-m'   "
                        "                         ./extractImg -n 10000   ")
    group.add_option('-w', action='store_true', help='Warning option')
    parser.add_option_group(group)
    (options, args) = parser.parse_args()
    if options.extractNum:
        Args["extractNum"] = int(options.extractNum)
    return Args

if __name__ == '__main__':

    args = parseArgs()

    extractNum = args["extractNum"]
    print("extractNum=%s" % extractNum)
    currentDate = time.strftime('%Y%m%d_%H%M', time.localtime(time.time()))
    print("currentDate = %s " % currentDate)

    extractDirName = "extractImg_"+currentDate+"_"+str(extractNum)

    cwd = os.getcwd()
    print("cwd = %s " % cwd)

    nameMapFile = os.path.join(cwd, "nameMap")
    print("nameMapFile = %s " % nameMapFile)

    finalImgDir = os.path.join(cwd, "imgs_final_result")
    print("finalImgDir = %s " % finalImgDir)

    extractImgDir = os.path.join(cwd, extractDirName)
    print("extractImgDir = %s " % extractImgDir)

    if not os.path.exists(extractImgDir):
        os.mkdir(extractImgDir)

    nameMapDict = {}
    # 读取 nameMapFile , 获取图片类别
    with open("nameMap", 'r') as f:
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
    densityDict = {} #密度
    weatherDict = {} #天气
    timeSlotDict = {} #时间段
    scenesDict = {} #场景


    for i in keys:
        try:
            splits = i.split("_")
            density = splits[0]
            weather = splits[2]
            timeSlot = splits[3]
            scenes = splits[4]

            dictCount(densityDict,density)
            dictCount(weatherDict,weather)
            dictCount(timeSlotDict,timeSlot)
            dictCount(scenesDict,scenes)
        except Exception as e:
            print("error,i=%s , e=%s" %(i , e))


    print(densityDict)
    print(weatherDict)
    print(timeSlotDict)
    print(scenesDict)


    # 读取finalImgDir 下文件数量 随机抽取 extractNum

    fs = os.listdir(finalImgDir)

    randNum = random.sample(range(0, len(fs)), extractNum if extractNum < len(fs) else len(fs) )  # random.sample()生成不相同的随机数
    print(randNum)

    for i in randNum:
        src_path = os.path.join(finalImgDir, fs[i])
        dest_path = os.path.join(extractImgDir, fs[i])
        # tmp_path 移动到 extractImgDir
        shutil.move(src_path, dest_path)
        print("from %s  move to %s" %(src_path,dest_path))

    print("finish...")


