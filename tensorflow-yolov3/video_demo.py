#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2018 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : video_demo.py
#   Author      : YunYang1994
#   Created date: 2018-11-30 15:56:37
#   Description :
#
#================================================================

import cv2
import time
import numpy as np
import tensorflow as tf
from PIL import Image
from core import utils, shared_globals
import requests
import json
import urllib

count = 0
webserver = 'http://10.0.2.117:8080/api'

def sendStats():
    print("Sending Data to Webserver: ")
    a = shared_globals.data
    print(shared_globals.data)
    requests.post(webserver + '?data=' + json.dumps(shared_globals.data))


def updateData():
    for key in shared_globals.data.keys():
        shared_globals.data[key]['Occupancy'] = (shared_globals.data[key]['Available']) / shared_globals.data[key]['Total']
        print("Key: {0}, Available: {1}".format(key, shared_globals.data[key]['Available']))
    print("======================")


IMAGE_H, IMAGE_W = 416, 416
# video_path = "./data/demo_data/road.mp4"
# video_path = 0 # use camera
video_path = "192.75.71.26/mjpg/video.mjpg"
classes = utils.read_coco_names('./data/coco.names')
num_classes = len(classes)
input_tensor, output_tensors = utils.read_pb_return_tensors(tf.get_default_graph(),
                                                            "./checkpoint/yolov3_cpu_nms.pb",
                                                            ["Placeholder:0", "concat_9:0", "mul_6:0"])
with tf.Session() as sess:


    # r = requests.get('http://192.75.71.26/mjpg/video.mjpg', stream=True)
    # r = requests.get('http://62.163.246.48:50001/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER', stream=True)
    # r = requests.get('http://194.44.38.196:8082/mjpg/video.mjpg', stream = True)
    r = requests.get('http://192.75.71.26/mjpg/video.mjpg', stream = True)

    if r.status_code == 200:
        bytes = bytes()
        for chunk in r.iter_content(chunk_size=1024):
            bytes += chunk
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                image = Image.fromarray(image)
                img_resized = np.array(image.resize(size=(IMAGE_H, IMAGE_W)), dtype=np.float32)
                img_resized = img_resized / 255.
                prev_time = time.time()

                boxes, scores = sess.run(output_tensors, feed_dict={input_tensor: np.expand_dims(img_resized, axis=0)})
                boxes, scores, labels = utils.cpu_nms(boxes, scores, num_classes, score_thresh=0.4, iou_thresh=0.5)
                image = utils.draw_boxes(image, boxes, scores, labels, classes, (IMAGE_H, IMAGE_W), show=False)

                updateData()

                curr_time = time.time()
                exec_time = curr_time - prev_time
                result = np.asarray(image)
                info = "time: %.2f ms" % (1000 * exec_time)
                cv2.putText(result, text=info, org=(50, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 0), thickness=2)
                info2 = "Vehicle: " + str(shared_globals.data['A']['Available'])
                cv2.putText(result, text=info2, org=(50, 110), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=1, color=(255, 0, 0), thickness=2)
                cv2.namedWindow("result", cv2.WINDOW_NORMAL)
                result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

                # where the image is stored
                cv2.imshow("result", result)
                # print(result)
                if count > 10:
                    sendStats()
                    count = 0

                count = count + 1
                if cv2.waitKey(1) & 0xFF == ord('q'): break

                # cv2.imshow('i', i)
                # if cv2.waitKey(1) == 27:
                #     exit(0)

    # ######
    # # vid = cv2.VideoCapture("http://192.75.71.26/mjpg/video.mjpg?camera=1")
    # vid = cv2.VideoCapture("./data/demo_data/road.mp4")
    # # vid.open("http://192.75.71.26/mjpg/video.mjpg?camera=1&dummy=param.mjpg")
    # # vid.open("http://129.21.219.231:8080/?action=stream&dummy=param.mjpg")
    # # print(vid.isOpened())
    # while True:
    #     return_value, frame = vid.read()
    #     # print(return_value, frame)
    #     if return_value:
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         image = Image.fromarray(frame)
    #     else:
    #         raise ValueError("No image!")
    #     img_resized = np.array(image.resize(size=(IMAGE_H, IMAGE_W)), dtype=np.float32)
    #     img_resized = img_resized / 255.
    #     print(img_resized.size)
    #     prev_time = time.time()
    #
    #     boxes, scores = sess.run(output_tensors, feed_dict={input_tensor: np.expand_dims(img_resized, axis=0)})
    #     boxes, scores, labels = utils.cpu_nms(boxes, scores, num_classes, score_thresh=0.4, iou_thresh=0.5)
    #     image = utils.draw_boxes(image, boxes, scores, labels, classes, (IMAGE_H, IMAGE_W), show=False)
    #
    #     updateData()
    #
    #     curr_time = time.time()
    #     exec_time = curr_time - prev_time
    #     result = np.asarray(image)
    #     info = "time: %.2f ms" %(1000*exec_time)
    #     cv2.putText(result, text=info, org=(50, 70), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #                 fontScale=1, color=(255, 0, 0), thickness=2)
    #     cv2.namedWindow("result", cv2.WINDOW_AUTOSIZE)
    #     result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
    #     cv2.imshow("result", result)
    #     if count > 160:
    #         sendStats()
    #         count = 0
    #
    #     count = count + 1
    #     if cv2.waitKey(1) & 0xFF == ord('q'): break

    #
