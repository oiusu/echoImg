#!/usr/bin/env python
# encoding: utf-8
'''
临时的脚本 修改原来renameMap 的文件名  解决遗留问题用的
@author: chenc
@time: 2018/11/5 11:29 AM
@desc:
'''
import os
import time


def alterRenameMap(file,old_str,new_str):
    """
    替换文件中的字符串
    :param file:文件名
    :param old_str:就字符串
    :param new_str:新字符串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)


def alterFinalImgDir(finalImgDir):

    fs = os.listdir(finalImgDir)
    for i in fs:
        replace = i.replace("2018_", "")
        os.rename(finalImgDir + "/" + i, finalImgDir + "/" + replace)


if __name__ == '__main__':

    # projectNumber = "1"  # 项目编号
    # type = "detection"  # detection 检测 ； classification 分类 ； segmentation 分割

    batchNumber = "1"

    currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))
    currentDate = "20181026"
    print("currentDate = %s " % currentDate)

    cwd = os.getcwd()
    print("cwd = %s " % cwd)

    renameMapFile = os.path.join(cwd, "renameMap")
    print("renameMapFile = %s " % renameMapFile)

    extractMapFile = os.path.join(cwd, "extractMap")
    print("extractMapFile = %s " % extractMapFile)

    finalImgDir = os.path.join(cwd, "imgs_final_result")
    print("finalImgDir = %s " % finalImgDir)

    if not os.path.exists(extractMapFile):
        file = open("extractMap", 'w')
        file.close()

    # 先把 renameMap 的 key 去掉 年份。
    alterRenameMap("renameMap","2018_","")
    # imgs_final_result 文件重命名 去掉年份
    alterFinalImgDir(finalImgDir)

    # 查看 imgs_final_result 和  renameMap 的 key 的差集 是 以前处理批次的文件 （转换成20181106_1_detection_1_37127.jpeg  时间_项目编号_类型_批次_编号.jpeg）， 获得他们的保存在extractImgMap 里面。

    renameMapDict = {}

    with open("renameMap", 'r') as f:
        renameMapLines = f.readlines()
        for i in range(0, len(renameMapLines)):
            kv = renameMapLines[i].rstrip('\n').split("\t")
            renameMapDict[kv[0]] = kv[1]

    keys = renameMapDict.keys()
    # 1_detection_1460.jpeg

    fs = os.listdir(finalImgDir)

    oldFile = [item for item in keys if item not in fs]

    with open("extractMap", 'a') as nmf1:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
        for i in oldFile:

            try:
                split = i.split(".")
                oldName = split[0] # 1_detection_1460 项目编号_类型_编号
                houzui = split[1] # jpeg

                name_split = oldName.split("_")

                projectNumber = name_split[0]
                type = name_split[1]
                offset = name_split[2]

                dest_name = currentDate + "_" + projectNumber + "_"+ type + "_" + batchNumber+ "_" + offset + "."+houzui
                nmf1.write(dest_name + "\t" + renameMapDict[i] + "\n")

            except Exception as e:
                print("error,i=%s , e=%s" % (i, e))






