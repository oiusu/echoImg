#!/usr/bin/env python
# encoding: utf-8
'''
抽取图片
@author: chenc
@time: 2018/10/26 9:57 AM
@desc:
'''
import os
import random
import shutil
import time
from optparse import OptionParser, OptionGroup



currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))

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

    parser.add_option("-b", "--batchNum",
                      action="store", dest="batchNum",
                      help='''抽取数据的批次''')

    group = OptionGroup(parser, 'Warning',
                        "Default and Necessary option:   '-m'   "
                        "                         ./extractImg -n 10000   ")
    group.add_option('-w', action='store_true', help='Warning option')
    parser.add_option_group(group)
    (options, args) = parser.parse_args()
    if options.extractNum:
        Args["extractNum"] = int(options.extractNum)
    if options.batchNum:
        Args["batchNum"] = int(options.batchNum)
    return Args


def moveAndRecord(randNum,keys,finalImgDir,extractImgDir,batchNum,renameMapDict):
    with open("extractMap", 'a') as nmf1:

        for i in randNum:
            stepName = keys[i]
            src_path = os.path.join(finalImgDir, stepName)

            try:
                split = stepName.split(".")
                oldName = split[0]  # 1_detection_1460 项目编号_类型_编号
                houzui = split[1]  # jpeg

                name_split = oldName.split("_")

                projectNumber = name_split[0]
                type = name_split[1]
                offset = name_split[2]

                dest_name = currentDate + "_" + projectNumber + "_" + type + "_" + str(batchNum) + "_" + offset + "." + houzui

                dest_path = os.path.join(extractImgDir, dest_name)
                # tmp_path 移动到 extractImgDir
                shutil.move(src_path, dest_path)

                nmf1.write(dest_name + "\t" + renameMapDict[stepName] + "\n")
                # recordExtractMap(keys[i],dest_name)
                print("from %s  move to %s" % (src_path, dest_path))

            except Exception as e:
                print("error,i=%s , e=%s" % (i, e))

# def recordExtractMap(stepName,batchNum):
#     with open("extractMap", 'a') as nmf1:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
#         #stepName  1_detection_77.jpeg
#         nmf1.write(dest_name + "\t" + renameMapDict[i] + "\n")



if __name__ == '__main__':

    projectNumber = "1"  # 项目编号
    type = "detection"  # detection 检测 ； classification 分类 ； segmentation 分割

    args = parseArgs()

    extractNum = args["extractNum"]
    print("extractNum=%s" % extractNum)
    batchNum = args["batchNum"]
    print("batchNum=%s" % batchNum)

    print("currentDate = %s " % currentDate)

    extractDirName = currentDate + "_" + projectNumber + "_" + type + "_" + str(batchNum) +"_"+str(extractNum)
    # extractDirName = "extractImg_"+currentDate+"_"+str(extractNum)

    cwd = os.getcwd()
    print("cwd = %s " % cwd)

    renameMapFile = os.path.join(cwd, "renameMap")
    print("renameMapFile = %s " % renameMapFile)

    finalImgDir = os.path.join(cwd, "imgs_final_result")
    print("finalImgDir = %s " % finalImgDir)

    extractResultDir = os.path.join(cwd, "extract_result")
    print("extractResultDir = %s " % extractResultDir)

    extractImgDir = os.path.join(extractResultDir, extractDirName)
    print("extractImgDir = %s " % extractImgDir)

    if not os.path.exists(extractResultDir):
        os.mkdir(extractResultDir)

    if not os.path.exists(extractImgDir):
        os.mkdir(extractImgDir)

    renameMapDict = {}
    renameMapReverseDict = {} # 反转的字典 ， 根据val 查询用
    # 读取 renameMapFile , 获取图片类别
    with open("renameMap", 'r') as f:
        renameMapLines = f.readlines()
        for i in range(0, len(renameMapLines)):
            kv = renameMapLines[i].rstrip('\n').split("\t")
            renameMapDict[kv[0]] = kv[1]             # 1_detection_1480.jpeg	                                    sparse_4_normal_daytime_urban_v1539933691465_002.jpeg
            renameMapReverseDict[kv[1]] = kv[0]      # sparse_4_normal_daytime_urban_v1539933691465_002.jpeg        1_detection_1480.jpeg

    fs = os.listdir(finalImgDir)
    # 获得剩下的结果图片  imgs_final_result 的 字典
    finalResultMapDict = {}
    for i in fs :
        finalResultMapDict[i] = renameMapDict[i]

    originNames = finalResultMapDict.values()

    # 分成2个字典  dense or sparse
    denseDict = {}
    sparseDict = {}

    for i in originNames:
        try:
            splits = i.split("_")
            density = splits[0]
            weather = splits[2]
            timeSlot = splits[3]
            scenes = splits[4]

            if density == 'dense':
                stepName = renameMapReverseDict[i]
                denseDict[stepName] = i
            if density == 'sparse':
                stepName = renameMapReverseDict[i]
                sparseDict[stepName] = i

        except Exception as e:
            print("error,i=%s , e=%s" % (i, e))

    print("待抽取数=%s ,denseDict size=%s , sparseDict size=%s " % (extractNum, len(denseDict), len(sparseDict)))

    # 抽取数目 一半 denseDict ， 一半 sparseDict
    denseSize = int(extractNum / 2)
    sparseSize = extractNum - denseSize
    sparseRandNum = []
    denseRandNum = []

    # if denseSize > len(denseDict) and sparseSize > len(sparseDict) :
    if sparseSize >= len(sparseDict):
        # sparseDict 全抽取
        sparseRandNum = range(0,len(sparseDict))
        denseSize = extractNum - len(sparseDict)


    if denseSize >= len(denseDict) :
        # denseDict 全抽取
        denseRandNum = range(0, len(denseDict))
        sparseSize = extractNum - len(denseDict)

    if len(sparseRandNum) == 0 :
        sparseRandNum = random.sample(range(0, len(sparseDict)),sparseSize if sparseSize < len(sparseDict) else len(sparseDict))
    if len(denseRandNum) == 0 :
        denseRandNum = random.sample(range(0, len(denseDict)), denseSize if denseSize < len(denseDict) else len(denseDict))

    print("待抽取数=%s ,denseRandNum size=%s , sparseRandNum size=%s " % (extractNum, len(denseRandNum), len(sparseRandNum)))

    # randNum = random.sample(range(0, len(fs)), extractNum if extractNum < len(fs) else len(fs) )  # random.sample()生成不相同的随机数
    # print(randNum)
    #
    sparseKeys = list(sparseDict.keys())
    denseKeys = list(denseDict.keys())

    moveAndRecord(sparseRandNum,sparseKeys,finalImgDir,extractImgDir,batchNum,renameMapDict)
    moveAndRecord(denseRandNum,denseKeys,finalImgDir,extractImgDir,batchNum,renameMapDict)






    print("finish...")


