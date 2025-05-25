# utils/image_helper.py
import os

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

def is_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_images_from_groups(groups, base_path='static/uploads'):
    image_paths = []
    for group in groups:
        group_path = os.path.join(base_path, group)
        if os.path.isdir(group_path):
            for fname in sorted(os.listdir(group_path)):
                if is_image_file(fname):
                    image_paths.append(f"/static/uploads/{group}/{fname}")
    return image_paths
