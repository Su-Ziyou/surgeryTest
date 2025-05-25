from flask import Blueprint, render_template
import os

patient_bp = Blueprint('patient', __name__, template_folder='../../templates',url_prefix='/patient')

@patient_bp.route('/')
def patient_page():
    return render_template('patient.html')
