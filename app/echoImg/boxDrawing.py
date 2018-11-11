#!/usr/bin/env python
# encoding: utf-8
'''
@author: chenc
@time: 2018/10/15 7:16 PM
@desc:
'''


import os
import cv2
import tensorflow as tf
import json
import xml.etree.ElementTree as ET

flags = tf.app.flags
flags.DEFINE_string('save_path', '/Users/chenc/Documents/test_ffmpeg/boxes_drawing/results/', 'Where to save imgs after boxes drawing')
flags.DEFINE_string('anno_dir', '/Users/chenc/Documents/test_ffmpeg/boxes_drawing/outputs/', 'Where to save imgs after boxes drawing')
flags.DEFINE_string('image_path', '/Users/chenc/Documents/test_ffmpeg/boxes_drawing/test/', 'pascal img dir')
FLAGS = flags.FLAGS

def parse_json(annotations_file):
    """parse a json file, especailly for BDD"""
    with tf.gfile.GFile(annotations_file, 'r') as fid:
        groundtruth_data = json.load(fid)
        filename = groundtruth_data['name']
        frames = groundtruth_data['frames']

    objects = []
    for info in frames:
        for object in info['objects']:
            obj_struct = {}
            category = object['category']
            obj_struct['name'] = category
            try:
                obj_struct['difficult'] = object['attributes']['occluded']
            except:
                break
            bbox = object['box2d']
            obj_struct['bbox'] = [float(bbox['y1'])/720,
                                  float(bbox['x1'])/1280,
                                  float(bbox['y2']) / 720,
                                  float(bbox['x2']) / 1280]
            objects.append(obj_struct)
    return objects


def parse_rec(filename):
    """Parse a PASCAL VOC xml file."""
    tree = ET.parse(filename)
    size = tree.find('size')
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text

        obj_struct['difficult'] = int(obj.find('difficult').text)
        bbox = obj.find('bndbox')
        obj_struct['bbox'] = [float(bbox.find('ymin').text) / int(size.find('height').text),
                              float(bbox.find('xmin').text) / int(size.find('width').text),
                              float(bbox.find('ymax').text) / int(size.find('height').text),
                              float(bbox.find('xmax').text) / int(size.find('width').text)]

        objects.append(obj_struct)

    return objects

def img_bboxdraw(upload_dir,imgFullName,bboxes,score,classes):

    black = (0,0,0)
    green = (0,255,0)
    blue = (255,0,0)
    yellow = (255,255,0)
    red = (0,0,255)
    pin = (255,0,255)
    white = (255,255,255)
    qin = (0,255,255)
    grey = (192,192,192)
    purple = (146,61,146)

    color_map = {'bike': green, '1':red}#, 'bus':pin, 'bicycle':yellow, 'motocycle':blue, 'traffic light': qin,
                # 'traffic sign':grey, 'truck':purple, 'cell phone': black, 'bottle': white}

    img = os.path.join(upload_dir,'jpg',imgFullName)
    #print(img)
    image = cv2.imread(img)
    h,w,_ = image.shape

    font = cv2.FONT_HERSHEY_SIMPLEX

    for i,bbox in enumerate(bboxes):
        #print(bbox)
        ymin,xmin,ymax,xmax = bbox
        if score[i] < 0.4:
            continue
        if classes[i] in color_map:
            line = color_map[classes[i]]
        else:
            line = black
            #continue
        line = green
        #s = str(round(score[i],2))
        cv2.rectangle(image,(int(xmin*w),int(ymin*h)),(int(xmax*w),int(ymax*h)),line,2)#green,2)
        #image = cv2.putText(image, s, (int(xmin*w),int(ymin*h)), font, 1.2, line, 1)


    # PATH = os.path.join(FLAGS.save_path,imgs +'.jpg')
    PATH = os.path.join(upload_dir,'result',imgFullName)
    cv2.imwrite(PATH,image)


def imgDrawBoxes(upload_dir,imgFullName):
    img_name = imgFullName.split('.')[0]

    boxes = []
    classes = []
    score = []

    try:
        xml_path = os.path.join(upload_dir,"xml", img_name + '.xml')
        objects = parse_rec(xml_path)

        for object in objects:
            boxes.append(object['bbox'])
            classes.append(object['name'])
            score.append(1)
    except:
        # undetect += 1
        print('except skip    ------------>',img_name)
        return
        # continue
    if not boxes:
        print('not boxes skip ------------>', img_name)
        return
        # continue
    img_bboxdraw(upload_dir,imgFullName, boxes, score, classes)

# def main(anno_dir,img_dir,img_names):
#     """
#     :param anno_dir: a folder contains bboxes, which are on txt files named by each picture name
#     :param img_dir: where the picture store
#     :param img_namefile: txt file, to get the picture name
#     """
#
#     #with open(img_namefile,'r') as f:
#     #    img_names = f.readlines()
#
#     # undetect = 0
#     for img_name in img_names:
#         if img_name == '.DS_store':
#             continue
#         if img_name.split('.')[-1] != 'jpg':
#             continue
#         img_name = img_name.split('.')[0]
#
#         imgDrawBoxes(anno_dir,img_dir,img_name)



# if __name__ == '__main__':
#
#     assert FLAGS.save_path, 'set save_path first'
#     assert FLAGS.anno_dir, 'anno_dir is not exits'
#
#     if not os.path.exists(FLAGS.save_path):
#         os.makedirs(FLAGS.save_path)
#     if os.path.isfile(FLAGS.save_path):
#         raise NameError
#
#     img_dir = FLAGS.image_path
#     img_names = os.listdir(img_dir)
#     main(FLAGS.anno_dir,img_dir,img_names)





