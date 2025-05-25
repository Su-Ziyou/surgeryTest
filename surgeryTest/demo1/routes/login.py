# routes/login.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import os

login_bp = Blueprint('login', __name__,template_folder='../../templates')

# 假医生账号（可扩展为数据库验证）
DOCTOR_CREDENTIALS = {
    '123456': 'admin123',
    '100001': 'neuro2025'
}
@login_bp.route('/')
def index():
    return redirect(url_for('login.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        password = request.form.get('password')

        if doctor_id in DOCTOR_CREDENTIALS and DOCTOR_CREDENTIALS[doctor_id] == password:
            session['doctor_id'] = doctor_id
            return redirect(url_for('login.main_menu'))
        else:
            return render_template('login.html', error='工号或密码错误')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.pop('doctor_id', None)
    return redirect(url_for('login.login'))

@login_bp.route('/main')
def main_menu():
    if 'doctor_id' not in session:
        return redirect(url_for('login.login'))
    return render_template('main_menu.html')
