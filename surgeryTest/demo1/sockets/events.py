# sockets/events.py
from flask import session
from datetime import datetime
from utils.recorder import append_record

def register_socket_events(socketio):
    @socketio.on('send_image')
    def handle_send_image(data):
        image_path = data.get('image_path')
        question = data.get('question', '')
        print(f"[Socket] 发送图片: {image_path}")
        socketio.emit('display_image', {
            'image_path': image_path,
            'question': question
        })

    @socketio.on('answer_complete')
    def handle_answer_complete(data):
        image = data.get("image")
        correct = data.get("correct")
        reaction_time = data.get("reaction_time")

        record = {
            "image": image,
            "correct": correct,
            "reaction_time": reaction_time,
            "phase": session.get("patient_info", {}).get("phase"),
            "stim_location": session.get("patient_info", {}).get("stim_location"),
            "doctor_id": session.get("doctor_id"),
            "patient_info": session.get("patient_info"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        append_record(record)
        print("[记录完成]", record)
