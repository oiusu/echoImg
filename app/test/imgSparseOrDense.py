# encoding utf-8
# wangpengye
import os
import shutil
import time

import cv2
import numpy as np
import tensorflow as tf



def IsNeededDetectionObj(iter_class):
    # 1:person;2:bicycle;3:car;4:motorcycle;6:bus;8:truck
    needArr = [1,2,3,4,6,8]
    return iter_class in needArr




if __name__ == '__main__':



    start=time.time()


    flags = tf.app.flags
    # dev
    # flags.DEFINE_string('save_path', '/Users/chenc/Documents/test_ffmpeg/imgs_result/',
    #                     'Where to save imgs after boxes drawing')
    # flags.DEFINE_string('pb_path', '/Users/chenc/Documents/test_ffmpeg/frozen_inference_graph.pb',
    #                     'Where to save imgs after boxes drawing')
    # flags.DEFINE_string('image_path', '/Users/chenc/Documents/test_ffmpeg/imgs_test/', 'pascal img dir')

    # test
    flags.DEFINE_string('save_path', '/home/chenc/test_ffmpeg/imgs_result/',
                        'Where to save imgs after boxes drawing')
    flags.DEFINE_string('pb_path', '/home/chenc/test_ffmpeg/frozen_inference_graph.pb',
                        'Where to save imgs after boxes drawing')
    flags.DEFINE_string('image_path', '/home/chenc/test_ffmpeg/imgs/', 'pascal img dir')

    FLAGS = flags.FLAGS

    # PATH_TO_CKPT = '/Users/wangpengye/code/models-master/research/object_detection/pb/25/newtask1/frozen_inference_graph.pb'
    PATH_TO_CKPT = FLAGS.pb_path
    images_path = FLAGS.image_path
    images = os.listdir(images_path)
    images = [images_path + x for x in images]

    if not os.path.exists(FLAGS.save_path):
        os.makedirs(FLAGS.save_path)
    if not os.path.exists(FLAGS.save_path+"dense/"):
        os.makedirs(FLAGS.save_path+"dense/")
    if not os.path.exists(FLAGS.save_path+ "sparse/"):
        os.makedirs(FLAGS.save_path+ "sparse/")
    if not os.path.exists(FLAGS.save_path + "none/"):
        os.makedirs(FLAGS.save_path + "none/")


    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    with detection_graph.as_default():
        with tf.Session() as sess:
            # Get handles to input and output tensors

            ops = tf.get_default_graph().get_operations()
            all_tensor_names = {output.name for op in ops for output in op.outputs}
            tensor_dict = {}

            for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']:

                tensor_name = key + ':0'
                if tensor_name in all_tensor_names:
                    tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)

            image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

            for img in images:
                t1 = time.time()
                if img.split('.')[-1] != 'jpeg':
                    continue
                image_np = cv2.imread(img)
                b, g, r = np.split(image_np, 3, axis=2)
                image_np = np.concatenate((r, g, b), axis=2)
                # image_np = cv2.resize(image,shape)
                output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image_np, axis=0)})

                output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]

                countObj = 0
                for item in range(30):
                    if output_dict['detection_scores'][item] < 0.35:
                        break

                    iter_class = output_dict['detection_classes'][item]
                    iter_score = output_dict['detection_scores'][item]
                    result = []

                    result.append(str(iter_class))
                    result.append(str(iter_score))
                    # result += [str(x) for x in output_dict['detection_boxes'][item]]
                    if IsNeededDetectionObj(iter_class):
                        countObj = countObj + 1
                    # print(result)

                print("countObj=", countObj)
                tmp = img.split('/')[-1].split('_')

                if countObj >= 10:
                    shutil.move(img, FLAGS.save_path + "dense/" + '_'.join(['dense'] + tmp))
                elif countObj == 0:
                    shutil.move(img, FLAGS.save_path + "none/" + '_'.join(['none'] + tmp))
                else:
                    shutil.move(img, FLAGS.save_path + "sparse/" + '_'.join(['sparse'] + tmp))
                t2 = time.time()
                print("per img cost time: %s Seconds" %(t2-t1))
                    # f.writelines(' '.join(result)+'\n')


    #中间写上代码块
    end=time.time()
    print('finish total Running time: %s Seconds'%(end-start))