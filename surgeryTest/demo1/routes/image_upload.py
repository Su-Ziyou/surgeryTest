# routes/image_upload.py
from flask import Blueprint, render_template, session, redirect, url_for

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/image-upload')
def image_upload_page():
    if 'doctor_id' not in session:
        return redirect(url_for('login.login'))
    return render_template('image_upload.html')
