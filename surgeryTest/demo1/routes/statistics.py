# routes/statistics.py
import os
import json
from flask import Blueprint, request, jsonify
from db_instance import db

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/times')
def get_record_times():
    hid = request.args.get('hospital_id')
    if not hid:
        return jsonify([])
    #获取所有测试记录的时间
    sessions=db.get_sessions(hid)
    times=sorted(set(s[2][:10] for s in sessions))
    return jsonify(times)

@statistics_bp.route('/')
def get_record_by_time():
    hid = request.args.get('hospital_id')
    time_filter = request.args.get('time')
    all_results = db.get_patient_surgery_test_details(hid)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    results = []
    for item in all_results:
        if item['check_time'].startswith(time_filter):
            results.append({
                'image': item['relative_path'],
                'correct':item['is_correct']==1,
                'reaction_time':item['used_time'],
                'phase':item['stage']
            })
    return jsonify(results)
