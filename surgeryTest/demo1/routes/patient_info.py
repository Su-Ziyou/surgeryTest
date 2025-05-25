# routes/patient_info.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import os

patient_info_bp = Blueprint('patient_info', __name__, template_folder='../../templates',url_prefix='/patient-info')

@patient_info_bp.route('/', methods=['GET', 'POST'])
def patient_info_page():
    # ✅ 判断是否已登录（没有 session 则跳转登录页）
    if 'doctor_id' not in session:
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        # 获取病人信息表单内容
        patient_data = {
            'name': request.form.get('name'),
            'sex': request.form.get('sex'),
            'age': request.form.get('age'),
            'hospital_id': request.form.get('hospital_id'),
            'tumor_location': request.form.get('tumor_location'),
            'surgery_type': request.form.get('surgery_type'),
            'surgeon': request.form.get('surgeon'),
            'surgery_time': request.form.get('surgery_time'),
            'phase': request.form.get('phase'),
            'stim_location': request.form.get('stim_location') if request.form.get('phase') == '术中' else None
        }
        session['patient_info'] = patient_data  # 存入 session

        return redirect(url_for('test_control.test_control_page'))  # 跳转测试控制界面

    return render_template('patient_info.html')