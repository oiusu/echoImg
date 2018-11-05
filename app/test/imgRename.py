#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/24 11:39 AM
@desc:
'''
import os
import shutil


def appendToExclude(i):
    # global f
    with open("exclude", 'a') as f:
        f.write(i + "\n")


# offset 记录 图片消费的index , exclude 记录已经处理的文件夹 ,
# 程序是把图片拷贝到 当前目录下imgs_final_result 文件夹， 并且 按 项目编号_类型_编号 重命名 ，记录 新文件名 和 原文件名的 映射文件
if __name__ == '__main__':
    # year = "2018"
    projectNumber = "1"  # 项目编号
    type = "detection"  # detection 检测 ； classification 分类 ； segmentation 分割

    cwd= os.getcwd()
    print("cwd = %s " % cwd)

    originImgDir = os.path.join(cwd,"imgs_result")
    print("originImgDir = %s " % originImgDir)

    offsetFile = os.path.join(cwd, "offset")
    print("offsetFile = %s " % offsetFile)

    excludeFile = os.path.join(cwd, "exclude")
    print("excludeFile = %s " % excludeFile)

    renameMapFile = os.path.join(cwd, "renameMap")
    print("renameMapFile = %s " % renameMapFile)

    finalImgDir = os.path.join(cwd, "imgs_final_result")
    print("finalImgDir = %s " % finalImgDir)
    if not os.path.exists(finalImgDir):
        os.mkdir(finalImgDir)

    if  not os.path.exists(offsetFile):
        file = open("offset", 'w')
        file.close()

    if not os.path.exists(excludeFile):
        file = open("exclude", 'w')
        file.close()

    if not os.path.exists(renameMapFile):
        file = open("renameMap", 'w')
        file.close()

    # 读取exclude 已处理文件夹列表
    excludeArr = []
    with open("exclude", 'r') as f:
        excludeArr = f.readlines()
        for i in range(0, len(excludeArr)):
            excludeArr[i] = excludeArr[i].rstrip('\n')
    print("excludeArr = %s" %excludeArr)

    # 读取offset 已处理图片的 下标
    offset = 0
    with open("offset", 'r') as f:
        val = f.readline().rstrip('\n')
        offset = 0 if val == '' else int(val)
        print("begin offset = %s" % offset)





    # 遍历dir下子文件夹目录
    with open("renameMap", 'a') as nmf1:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
        fs = os.listdir(originImgDir)
        for i in fs:
            tmp_path = os.path.join(originImgDir, i)
            if  os.path.isdir(tmp_path) and i not in excludeArr:
                print("excute tmp_path = %s" %tmp_path)
                files = os.listdir(tmp_path)
                for j in files:
                    if j in ['dense','sparse']:
                        tmp_child_path = os.path.join(tmp_path, j)
                        print("excute tmp_child_path = %s" % tmp_child_path)
                        subFiles = os.listdir(tmp_child_path)
                        for k in subFiles:
                            if os.path.splitext(k)[1] == '.jpeg':
                                # 移动文件  年份_批次__类型_编号  （Decetion,Segmentation, classification）  目前就是检测
                                src_img_path = os.path.join(tmp_child_path, k)
                                offset += 1
                                dest_name =  projectNumber + "_" + type + "_" + str(offset) + ".jpeg"
                                # dest_name = year + "_" + projectNumber + "_" + type + "_" + str(offset) + ".jpeg"
                                dest_img_path = os.path.join(finalImgDir,dest_name )
                                shutil.copyfile(src_img_path, dest_img_path)
                                nmf1.write(dest_name+"\t"+k+"\n")
                print("finish excute tmp_path = %s" %tmp_path)
                # f.write(i+"\n")
                appendToExclude(i)
    # 记录最终offset
    with open("offset", 'w') as f:
        f.write(str(offset))
        print("final offset = %s" % str(offset))

    print("finish ..")