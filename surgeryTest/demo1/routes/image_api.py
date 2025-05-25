# routes/image_api.py
import os
import shutil
from flask import Blueprint, request, jsonify, session, current_app
from werkzeug.utils import secure_filename

image_api_bp = Blueprint('image_api', __name__, url_prefix='/api')

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_api_bp.route('/image-upload', methods=['POST'])
def upload_image():
    if 'doctor_id' not in session:
        return jsonify({'error': '未登录'}), 403

    group = request.form.get('group') or request.form.get('new_group')
    if not group:
        return jsonify({'error': '请指定图片分组'}), 400

    group_path = os.path.join(UPLOAD_FOLDER, secure_filename(group))
    os.makedirs(group_path, exist_ok=True)

    files = request.files.getlist('images')
    saved = 0
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(group_path, filename)
            file.save(save_path)
            saved += 1

    return jsonify({'message': f'成功上传 {saved} 张图片'})


@image_api_bp.route('/image-delete', methods=['POST'])
def delete_image():
    if 'doctor_id' not in session:
        return jsonify({'error': '未登录'}), 403

    data = request.get_json()
    path = data.get('path')
    if not path or not path.startswith('/static/uploads/'):
        return jsonify({'error': '路径非法'}), 400

    abs_path = os.path.join(current_app.root_path, path.lstrip('/'))
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return jsonify({'message': '删除成功'})
    return jsonify({'error': '文件不存在'}), 404


@image_api_bp.route('/images/group')
def list_images_by_group():
    group = request.args.get('name')
    if not group:
        return jsonify([])

    group_path = os.path.join(UPLOAD_FOLDER, secure_filename(group))
    if not os.path.isdir(group_path):
        return jsonify([])

    files = [f for f in os.listdir(group_path) if allowed_file(f)]
    urls = [f'/static/uploads/{secure_filename(group)}/{f}' for f in files]
    return jsonify(urls)
