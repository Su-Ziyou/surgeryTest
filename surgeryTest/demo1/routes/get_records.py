#routes/get_records.py
from flask import Blueprint, render_template, session, redirect, url_for

get_records_bp = Blueprint('get_records_bp', __name__)

@get_records_bp.route('/get-records')
def get_records():
    if 'doctor_id' not in session:
        return redirect(url_for('login.login'))
    return render_template('statistics.html')