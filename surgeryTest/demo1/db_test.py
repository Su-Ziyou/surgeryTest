from database import SurgeryDBManager
import os
import datetime
import json

# 初始化数据库路径
db_path = "surgery_test.db"

# 初始化管理器
db = SurgeryDBManager()
# 如果旧的测试库存在则删除
if os.path.exists(db_path):
    os.remove(db_path)
print("✅ 已删除旧数据库文件")

# 运行初始化
db.initialize_database()

# 测试患者管理功能
print("\n[添加患者]")
db.insert_patient("H123456", "张三", "男", 45)
print("患者信息：", db.get_patient("H123456"))

print("\n[通过 JSON 添加患者]")
json_patient = '{"hospital_id": "H789012", "name": "李四", "gender": "男", "age": 30}'
db.insert_patient_from_json(json_patient)
print("通过 JSON 添加的患者信息：", db.get_patient("H789012"))

print("\n[更新患者年龄]")
db.update_patient_age("H123456", 46)
print("更新后的患者信息：", db.get_patient("H123456"))

# 测试手术管理功能
print("\n[添加手术记录]")
surgery_time = "2024-01-01 09:00:00"
db.insert_surgery("H123456", surgery_time, "上叶", "根治术", "李医生")
print("手术记录：", db.get_surgeries("H123456"))

print("\n[通过 JSON 添加手术记录]")
json_surgery = '{"hospital_id": "H123456", "surgery_time": "2024-01-02 10:00:00", "tumor_position": "右肺下叶", "surgery_type": "肺叶切除术", "surgeon": "王医生"}'
db.insert_surgery_from_json(json_surgery)
print("通过 JSON 添加手术记录后：", db.get_surgeries("H123456"))

# 测试测试图片管理功能
print("\n[添加测试图片]")
db.insert_image("image1.png", "CT")
db.insert_image("image2.png", "MRI")
print("CT 图片：", db.get_images_by_type("CT"))
print("MRI 图片：", db.get_images_by_type("MRI"))

print("\n[通过 JSON 添加测试图片]")
json_image = '{"image_name": "image3.png", "category": "CT"}'
db.insert_image_from_json(json_image)
print("通过 JSON 添加测试图片后 CT 图片：", db.get_images_by_type("CT"))

# 测试测试记录管理功能
print("\n[添加测试记录]")
check_time = "2024-01-03 15:00:00"
db.insert_test_session("H123456", check_time, "术前", surgery_time)
print("测试记录：", db.get_test_sessions("H123456"))

print("\n[通过 JSON 添加测试记录]")
json_test_session = '{"hospital_id": "H123456", "check_time": "2024-01-04 16:00:00", "stage": "术前", "surgery_time": "2024-01-01 09:00:00"}'
db.insert_test_session_from_json(json_test_session)
print("通过 JSON 添加测试记录后：", db.get_test_sessions("H123456"))

# 测试图片测试结果管理功能
print("\n[添加测试结果]")
db.insert_image_test_result("H123456", check_time, "CT", "image1.png", 8.2, 1, "正确定位")
db.insert_image_test_result("H123456", check_time, "MRI", "image2.png", 9.5, 0, "误诊")

print("\n[通过 JSON 添加测试结果]")
json_test_result = '{"hospital_id": "H123456", "check_time": "2024-01-03 15:00:00", "category": "CT", "image_name": "image3.png", "used_time": 7.5, "is_correct": 1, "comment": "正确定位"}'
db.insert_image_test_result_from_json(json_test_result)

# 测试测试总结管理功能
print("\n[添加测试总结]")
db.insert_test_summary("H123456", check_time, 0.5, "左上叶: 0.5", 17.7)
print("测试总结：", db.get_test_summary("H123456", check_time))

print("\n[通过 JSON 添加测试总结]")
json_test_summary = '{"hospital_id": "H123456", "check_time": "2024-01-03 15:00:00", "accuracy_total": 0.6, "accuracy_by_position": "左上叶: 0.6", "total_time": 18.7}'
db.insert_test_summary_from_json(json_test_summary)
print("通过 JSON 添加测试总结后：", db.get_test_summary("H123456", check_time))




# 查询指定住院号的手术测试详情
hospital_id = "H123456"
details = db.get_patient_surgery_test_details(hospital_id)
print("\n[查询手术测试详情]")
print(details)

# 测试删除患者功能
print("\n[删除患者]")
db.delete_patient("H123456")
print("查询已删除患者：", db.get_patient("H123456"))

# 测试清空数据库功能
db.clear_database()
print("✅ 数据库已清空")