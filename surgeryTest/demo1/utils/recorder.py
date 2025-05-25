from datetime import datetime
import os
import re
from db_instance import db

def append_record(record_data):
    # 提取信息
    hospital_id = record_data.get("patient_info", {}).get("hospital_id")
    check_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    image_url = record_data.get("image")
    image_name = os.path.basename(image_url)
    category = parse_category_from_path(image_url)

    # 拼接绝对路径
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    abs_image_path = os.path.normpath(os.path.join(project_root, image_url.lstrip('/')))

    used_time = float(record_data.get("reaction_time", 0))
    is_correct = 1 if record_data.get("correct") else 0
    comment = ""

    # 写入数据库
    db.insert_image_test_result(
        hospital_id=hospital_id,
        check_time=check_time,
        category=category,
        image_name=abs_image_path,
        used_time=used_time,
        is_correct=is_correct,
        comment=comment
    )

def parse_category_from_path(path):
    if not path:
        return "unknown"
    match = re.search(r"/uploads/([^/]+)/", path)
    if match:
        return match.group(1)
    return "unknown"
