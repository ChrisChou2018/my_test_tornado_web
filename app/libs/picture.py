#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import uuid
from PIL import Image


picture_specs = [
    {"type": "thumb", "width": 120, "height": 120, "quality": 86},
    {"type": "smdl", "is_square": True, "width": 300, "height": 300, "quality": 86},
    {"type": "title", "width": 600, "height": 600, "is_crop": True, "quality": 86},
    {"type": "photo", "width": 800, "height": 800, "quality": 86},
    {"type": "hd", "width": 1080, "height": 1080, "quality": 86},
]

avatar_specs = [
    {"type": "icon", "is_square": True, "width": 80, "height": 80, "quality": 86},
    {"type": "thumb", "is_square": True, "width": 160, "height": 160, "quality": 86},
    {"type": "title", "is_square": True, "width": 320, "height": 320, "quality": 86},
    {"type": "hd", "width": 800, "height": 800, "quality": 86},
]

article_specs = [
    {"type": "thumb", "width": 70, "height": 40, "quality": 86},
    {"type": "title", "width": 350, "height": 197, "quality": 86},
    {"type": "hd", "width": 710, "height": 300, "quality": 86},
]


def convert_picture(picture_id, base_static_path, picture_path, picture_type="photos",
        is_from_source=False):
    picture_dict = dict()
    if is_from_source:
        f_path_raw = os.path.join(base_static_path, "source", "photos", "raw",
            picture_id[:2], picture_id+".jpg"
        )

    target_path_name = "photos"
    picture = Image.open(picture_path)
    picture_width, picture_height = picture.size
    picture_dict["picture_id"] = str(picture_id)
    picture_dict["picture_width"] = picture_width
    picture_dict["picture_height"] = picture_height
    picture_dict["picture_size"] = str(float(os.path.getsize(picture_path)/1024))+"KB"

    root_path = os.path.join(base_static_path, target_path_name, "root", picture_id[:2])
    if not os.path.exists(root_path):
        os.makedirs(root_path, 0755)

    picture.resize((picture_width, picture_height), Image.ANTIALIAS).save(
        root_path+"/"+picture_id+".jpg", "JPEG", quality=86
    )

    target_specs = picture_specs
    if picture_type == "avatar":
        target_specs = avatar_specs
    elif picture_type == "article":
        target_specs = article_specs

    for spec in target_specs:
        d_path_target = os.path.join(base_static_path, target_path_name,
            spec["type"], picture_id[:2]
        )
        if not os.path.exists(d_path_target):
            os.makedirs(d_path_target, 0755)

        width_scale = float(picture_width/float(spec["width"]))
        height_scale = float(picture_height/float(spec["height"]))
        box = ()
        if "is_square" in spec and spec["is_square"]:
            if width_scale > 1 and height_scale > 1:
                if width_scale > height_scale:
                    # (left, upper, right, lower)
                    box = (int((picture_width-picture_height)/2), 0,
                        int((picture_width-picture_height)/2)+picture_height, picture_height
                    )
                else:
                    box = (0, int((picture_height-picture_width)/2),
                        picture_width, picture_width+int((picture_height-picture_width)/2)
                    )
                new_width = spec["width"]
                new_height = spec["height"]
            else:
                if width_scale > height_scale:
                    box = (int((picture_width-picture_height)/2), 0,
                        int((picture_width-picture_height)/2)+picture_height, picture_height
                    )
                    new_width = int(picture_height)
                    new_height = int(picture_height)
                else:
                    box = (0, int((picture_height-picture_width)/2),
                        picture_width, picture_width+int((picture_height-picture_width)/2)
                    )
                    new_width = int(picture_width)
                    new_height = int(picture_width)
        else:
            if picture_type == "article" and spec["type"] == "hd":
                new_width = int(picture_width)
                new_height = int(picture_height)
            elif width_scale > 1 or height_scale > 1:
                if width_scale > height_scale:
                    if picture_type == "article":
                        resize_prop = float(spec["width"])/float(spec["height"])
                        cut_width = int((picture_width - picture_height*resize_prop)/2)
                        box = (cut_width, 0, int(picture_height*resize_prop), picture_height)
                        new_height = spec["height"]
                        new_width = spec["width"]
                    else:
                        if height_scale > 1:
                            new_height = spec["height"]
                        else:
                            new_height = picture_height
                        new_width = int(picture_width*new_height/picture_height)
                else:
                    if picture_type == "article":
                        resize_prop = float(spec["height"])/float(spec["width"])
                        cut_width = int((picture_height - picture_width*resize_prop)/2)
                        box = (0, cut_width, picture_width, int(picture_width*resize_prop))
                        new_height = spec["height"]
                        new_width = spec["width"]
                    else:
                        if width_scale > 1:
                            new_width = spec["width"]
                        else:
                            new_width = picture_width
                        new_height = int(picture_height*new_width/picture_width)
            else:
                if picture_type == "article":
                    if width_scale > height_scale:
                        resize_prop = float(spec["width"])/float(spec["height"])
                        cut_width = int((picture_width - picture_height*resize_prop)/2)
                        box = (cut_width, 0, int(picture_height*resize_prop), picture_height)
                    else:
                        resize_prop = float(spec["height"])/float(spec["width"])
                        cut_width = int((picture_height - picture_width*resize_prop)/2)
                        box = (0, cut_width, picture_width, int(picture_width*resize_prop))
                    new_height = spec["height"]
                    new_width = spec["width"]
                else:
                    new_width = int(picture_width)
                    new_height = int(picture_height)

        if box:
            region = picture.crop(box)
            region.resize((new_width, new_height), Image.ANTIALIAS).save(
                d_path_target+"/"+picture_id+".jpg", "JPEG", quality=spec["quality"]
            )
        else:
            picture.resize((new_width, new_height), Image.ANTIALIAS).save(
                d_path_target+"/"+picture_id+".jpg", "JPEG", quality=spec["quality"]
            )
    return picture_dict

def remove_picture(picture_id, base_static_path, picture_type="photos"):
    target_specs = picture_specs
    if picture_type == 'avatar':
        target_specs = avatar_specs

    for spec in target_specs:
        f_path_target = os.path.join(base_static_path, "photos", spec["type"],
            picture_id[:2], picture_id + ".jpg"
        )
        try:
            os.remove(f_path_target)
        except OSError:
            pass

def save_upload_picture(picture_file, base_static_path,
        picture_type="photos", is_api=False):
    picture_id = uuid.uuid4().hex
    d_path_raw = os.path.join(base_static_path, "photos", "raw", picture_id[:2])
    f_path_raw = os.path.join(d_path_raw, picture_id+".jpg")
    if not os.path.exists(d_path_raw):
        os.makedirs(d_path_raw, 0755)

    with open(f_path_raw, "wb") as f:
        if is_api:
            f.write(picture_file)
        else:
            f.write(picture_file["body"])

    return convert_picture(picture_id, base_static_path, f_path_raw, picture_type)
