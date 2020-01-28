#! /usr/bin/env python
# -*-coding=utf-8 -*-
import argparse
import cv2
import json
import os
import xml.dom.minidom


from xml_utils import create_child_node, create_object_node, write_xml_file


COCO_Year = '2017'
AUTHOR = 'fqy'
SEGMENTED = '0'

parser = argparse.ArgumentParser(description='COCO2VOC')
parser.add_argument('-input_json', default=None, type=str, help='the path to json')
parser.add_argument('-input_img_dir', default=None, type=str, help='the path to img folder')
parser.add_argument('-output_dir', default=None, type=str, help='save dir')
args = parser.parse_args()

with open(args.input_json, "r+") as f:
    label_dicts = json.load(f)
    annotations = label_dicts["annotations"]
    categories = label_dicts['categories']

id2class = {}
for item in categories:
    id2class[item['id']] = item['name']

processed_labels = []
for i in annotations:
    if (i['category_id'] in id2class.keys()):
        processed_labels.append({
            "filename": str(i["image_id"]),
            "name": id2class[i["category_id"]],
            "bndbox": i["bbox"]
        })

img_list = os.listdir(args.input_img_dir)
if img_list == 0:
    print("Do not find images in your img_path")
    os._exit(-1)

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

for img_name in img_list:
    save_name = img_name[:-4]
    print(save_name)

    xml_file_name = os.path.join(args.output_dir, (save_name + '.xml'))

    try:
        img = cv2.imread(os.path.join(args.input_img_dir, img_name))
        height, width, channel = img.shape

        my_dom = xml.dom.getDOMImplementation()
        doc = my_dom.createDocument(None, 'annotation', None)
        root_node = doc.documentElement

        create_child_node(doc, 'folder', args.input_img_dir, root_node)
        create_child_node(doc, 'filename', img_name, root_node)
        source_node = doc.createElement('source')
        create_child_node(doc, 'database', 'LOGODection', source_node)
        create_child_node(doc, 'annotation', 'COCO' + COCO_Year, source_node)

        create_child_node(doc, 'image', 'flickr', source_node)
        create_child_node(doc, 'flickrid', 'NULL', source_node)
        root_node.appendChild(source_node)
        owner_node = doc.createElement('owner')
        create_child_node(doc, 'flickrid', 'NULL', owner_node)
        create_child_node(doc, 'name', AUTHOR, owner_node)
        root_node.appendChild(owner_node)

        size_node = doc.createElement('size')
        create_child_node(doc, 'width', str(width), size_node)
        create_child_node(doc, 'height', str(height), size_node)
        create_child_node(doc, 'depth', str(channel), size_node)
        root_node.appendChild(size_node)
        create_child_node(doc, 'segmented', SEGMENTED, root_node)

        for label in processed_labels:
            if save_name == label["filename"]:
                object_node = create_object_node(doc, label)
                root_node.appendChild(object_node)
                write_xml_file(doc, xml_file_name)
    except AttributeError:
        print('error in {}'.format(os.path.join(args.input_img_dir, img_name)))
