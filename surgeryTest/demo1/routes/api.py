# routes/api.py
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.image_helper import get_images_from_groups

api_bp = Blueprint('api', __name__, url_prefix='/api')

MAX_FILE_SIZE_KB = 4096  # 最大允许大小为 4MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@api_bp.route('/upload', methods=['POST'])
def upload_image():
    group = request.form.get('group')
    new_group = request.form.get('new_group')
    group = new_group.strip() if new_group else group
    if not group:
        return jsonify({'error': '请选择或输入一个图片组名'}), 400

    group_path = os.path.join('static', 'uploads', secure_filename(group))
    os.makedirs(group_path, exist_ok=True)

    files = request.files.getlist('images')
    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            file.seek(0, os.SEEK_END)
            size_kb = file.tell() / 1024
            file.seek(0)
            if size_kb > MAX_FILE_SIZE_KB:
                return jsonify({'error': f'文件 {file.filename} 超过 4096KB 限制'}), 400

            filename = secure_filename(file.filename)
            file.save(os.path.join(group_path, filename))
            saved_files.append(f'/static/uploads/{group}/{filename}')

    return jsonify({'message': '上传成功', 'files': saved_files})


@api_bp.route('/images', methods=['POST'])
def get_group_images():
    data = request.get_json()
    groups = data.get('groups', [])

    image_paths = get_images_from_groups(groups)
    return jsonify({'images': image_paths})

