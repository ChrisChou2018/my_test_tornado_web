from PIL import Image
import os
import subprocess
import uuid
from app.models import items_model
# photo_specs = [
#     {"type": "thumb", "width": 180, "height": 180, "quality": 86},
#     {"type": "thumbicon", "is_square": True, "width": 100, "quality": 86},
#     {"type": "title", "width": 300, "height": 200, "is_crop": True, "quality": 86},
#     {"type": "photo", "length": 650, "quality": 86},
# ]
photo_specs = {
    "item_title": { "width": 180, "height": 180, "quality": 86},
    "thumbicon": {"width": 100, "quality": 86, "is_square": True},
    "title": {"width": 300, "height": 200, "quality": 86, "is_crop": True},
    "item_info": {"width": 300, "height": 200},
    "item": {"width": 300, "height": 200},
}

# pic_specs = [
#     {"type": "mpic", "pixel": 14500, "quality": 88},
#     {"type": "spic", "pixel": 6500, "quality": 88}
# ]

def convert_photo(photo_id, base_static_path, photo_type):
    try:
        f_path_raw = os.path.join(base_static_path, "raw", photo_id + ".jpg"
        )
        image_obj = Image.open(f_path_raw)
        new_image_obj = None
        width = None
        height = None
        spec = photo_specs.get(photo_type)
        d_path_target = os.path.join(base_static_path, photo_type)
        if not os.path.exists(d_path_target):
            os.makedirs(d_path_target)

        if spec.get("is_square") and spec["is_square"]:
            width = spec["width"]
            height = width
            new_image_obj = image_obj.resize((width, height))
        elif spec.get("width") and spec.get("height"):
            if spec.get("is_crop") and spec["is_crop"]:
                width = spec["width"]
                height = spec["height"]
                new_image_obj = image_obj.crop((width,height,
                                                width,height))
            else:
                width = spec["width"]
                height = spec["height"]
                new_image_obj = image_obj.resize((width,
                                                 height,))
        convert_photo_path = os.path.join(d_path_target, photo_id+".jpg")
        new_image_obj.save(convert_photo_path)
        return {"file_size":os.path.getsize(convert_photo_path),
                "resolution":"{0}*{1}".format(width, height),
                'file_type':'jpg'}
    except Exception:
        return None

def save_upload_photo(photo_file, base_static_path, server_file_path, photo_type):
    photo_id = uuid.uuid4().hex
    d_path_raw = os.path.join(base_static_path, "raw")
    f_path_raw = os.path.join(d_path_raw, photo_id+".jpg")
    if not os.path.exists(d_path_raw):
        os.makedirs(d_path_raw)
    with open(f_path_raw, "wb") as f:
        f.write(photo_file["body"])

    data = convert_photo(photo_id, base_static_path, photo_type)
    if data:
        server_file_path = server_file_path.replace('assets', 'static')
        data.update({"image_path":os.path.join(server_file_path, photo_type, photo_id + '.jpg')})
        return data
    else:
        return None