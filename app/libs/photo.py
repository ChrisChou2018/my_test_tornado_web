# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import os
# import uuid
# import subprocess


# photo_specs = [
#     {"type": "thumb", "width": 180, "height": 180, "quality": 86},
#     {"type": "thumbicon", "is_square": True, "width": 100, "quality": 86},
#     {"type": "title", "width": 300, "height": 200, "is_crop": True, "quality": 86},
#     {"type": "photo", "length": 650, "quality": 86},
# ]

# pic_specs = [
#     {"type": "mpic", "pixel": 14500, "quality": 88},
#     {"type": "spic", "pixel": 6500, "quality": 88}
# ]


# def convert_photo(photo_id, base_static_path, photo_type="photo",
#         is_from_source=False):
#     if is_from_source:
#         f_path_raw = os.path.join(base_static_path, "source", "photos", "raw",
#             photo_id[:2], photo_id+".jpg"
#         )
#     else:
#         f_path_raw = os.path.join(base_static_path, "photos", "raw",
#             photo_id[:2], photo_id + ".jpg"
#         )

#     target_specs = photo_specs
#     target_path_name = "photos"
#     if photo_type == "pic":
#         target_specs = pic_specs
#         target_path_name = "pics"

#     for spec in target_specs:
#         d_path_target = os.path.join(base_static_path, target_path_name,
#             spec["type"], photo_id[:2]
#         )
#         if not os.path.exists(d_path_target):
#             os.makedirs(d_path_target)

#         cmd_params = ""
#         if spec.has_key("is_square") and spec["is_square"]:
#             width_str = str(spec["width"])
#             cmd_params = "".join(["-geometry '", width_str, "x", width_str,
#                 "^>' -gravity center -crop ", width_str, "x", width_str, "+0+0"]
#             )
#         elif spec.has_key("width") and spec.has_key("height"):
#             if spec.has_key("is_crop") and spec["is_crop"]:
#                 cmd_params = "".join(["-geometry '", str(spec["width"]), "x",
#                     str(spec["height"]), "^>' -gravity center -crop ",
#                     str(spec["width"]), "x", str(spec["height"]), "+0+0"]
#                 )
#             else:
#                 cmd_params = "".join(["-geometry '", str(spec["width"]), "x",
#                     str(spec["height"]), ">'"]
#                 )
#         elif spec.has_key("width"):
#             cmd_params = "".join(["-geometry '", str(spec["width"]), "x>'"])
#         elif spec.has_key("length"):
#             # 定义最大长度
#             cmd_params = "".join(["-geometry '", str(spec["length"]), "x",
#                 str(spec["length"]), ">'"]
#             )
#         elif spec.has_key("pixel"):
#             cmd_params = "".join(["-geometry ", str(spec["pixel"]), "@"])

#         if not cmd_params:
#             continue

#         f_path_target = os.path.join(d_path_target, photo_id + ".jpg")
#         cmd = " ".join(["gm convert", f_path_raw, cmd_params,
#             "-quality", str(spec["quality"]), "+profile \"+\"", f_path_target]
#         )
#         ret_code = subprocess.call(cmd, shell=True)
#         if ret_code != 0:
#             return False

#     return True


# def remove_photo(photo_id, base_static_path, photo_type="photo"):
#     target_specs = photo_specs
#     target_path_name = "photos"
#     if photo_type == "pic":
#         target_specs = pic_specs
#         target_path_name = "pics"

#     for spec in target_specs:
#         f_path_target = os.path.join(base_static_path, target_path_name, spec["type"],
#             photo_id[:2], photo_id + ".jpg"
#         )
#         try:
#             os.remove(f_path_target)
#         except OSError:
#             pass


# def get_photo_size(photo_id):
#     f_path_raw = os.path.join(base_static_path, "photos", "raw", photo_id[:2],
#                               photo_id + ".jpg"
#     )

#     cmd_identify = "gm identify -format \"%m|%w|%h\" " + f_path_raw
#     popen = subprocess.Popen(cmd_identify, shell=True, stdout=subprocess.PIPE)
#     cmd_code = popen.wait()
#     cmd_output = popen.stdout.read()
#     output_list = cmd_output.split("|")

#     if cmd_code == 0 and len(output_list) == 3:
#         return (output_list[1], output_list[2])
#     else:
#         return None


# def save_upload_photo(photo_file, base_static_path):
#     photo_id = uuid.uuid4().hex

#     d_path_raw = os.path.join(base_static_path, "photos", "raw", photo_id[:2])
#     f_path_raw = os.path.join(d_path_raw, photo_id+".jpg")
#     if not os.path.exists(d_path_raw):
#         os.makedirs(d_path_raw, 0755)
#     with open(f_path_raw, "wb") as f:
#         f.write(photo_file["body"])

#     # TODO: check if it's a valid photo file
#     if convert_photo(photo_id, base_static_path):
#         return photo_id

