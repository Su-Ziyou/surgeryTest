# routes/test_control.py
import os
from flask import Blueprint, render_template, session, redirect, url_for

test_control_bp = Blueprint('test_control', __name__, template_folder='../../templates',url_prefix='/test-control')

@test_control_bp.route('/')
def test_control_page():
    # 检查是否登录
    if 'doctor_id' not in session:
        return redirect(url_for('login.login'))
    # 检查是否填写病人信息
    if 'patient_info' not in session:
        return redirect(url_for('patient_info.patient_info_page'))

    return render_template('test_control.html')
