import json
import sqlite3
import os


class SurgeryDBManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # 获取当前脚本所在的目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建数据库文件的绝对路径
            self.db_path = os.path.join(script_dir, '../records/surgery.db')
        else:
            self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _execute(self, sql, params=None, fetch=False):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = ON;")  # 开启外键支持
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            if fetch:
                return cursor.fetchall()
        except Exception as e:
            print("❌ SQL 执行错误：", e)
        finally:
            cursor.close()
            conn.close()

    # 删库函数，慎用
    def delete_database(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"✅ 数据库文件 {self.db_path} 已删除")
        else:
            print(f"❌ 数据库文件 {self.db_path} 不存在，无法删除")

    # 清空数据，慎用
    def clear_database(self):
        tables = [
            "image_test_results",
            "test_summary",
            "test_sessions",
            "surgeries",
            "test_images",
            "patients"
        ]
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = OFF;")  # 临时关闭外键约束
            for table in tables:
                cursor.execute(f"DELETE FROM {table};")
            cursor.execute("PRAGMA foreign_keys = ON;")  # 重新开启外键约束
            conn.commit()
            print("✅ 数据库已清空")
        except Exception as e:
            conn.rollback()
            print(f"❌ 清空数据库时出错: {e}")
        finally:
            cursor.close()
            conn.close()

    def initialize_database(self):
        sql_file_path = "./database/resource/init.sql"
        if not os.path.exists(sql_file_path):
            print(f"❌ 未找到 SQL 文件：{sql_file_path}")
            return

        conn = self._connect()
        cursor = conn.cursor()

        try:
            conn = self._connect()
            cursor = conn.cursor()
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            cursor.executescript(sql_script)
            conn.commit()
            print("✅ 数据库初始化完成")
        except Exception as e:
            print("❌ 初始化失败：", e)
        finally:
            cursor.close()
            conn.close()

    # --- 患者管理 ---
    def insert_patient(self, hospital_id, name, gender, age):
        sql = "INSERT INTO patients (hospital_id, name, gender, age) VALUES (?, ?, ?, ?)"
        self._execute(sql, (hospital_id, name, gender, age))

    def insert_patient_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            hospital_id = data.get('hospital_id')
            name = data.get('name')
            gender = data.get('gender')
            age = data.get('age')
            if hospital_id and name and gender and age:
                self.insert_patient(hospital_id, name, gender, age)
                print("✅ 患者信息添加成功")
            else:
                print("❌ 患者信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_patient(self, hospital_id):
        sql = "SELECT * FROM patients WHERE hospital_id = ?"
        return self._execute(sql, (hospital_id,), fetch=True)

    def update_patient_age(self, hospital_id, new_age):
        sql = "UPDATE patients SET age = ? WHERE hospital_id = ?"
        self._execute(sql, (new_age, hospital_id))

    def delete_patient(self, hospital_id):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys = ON;")

            # 依赖关系表删除
            cursor.execute("DELETE FROM image_test_results WHERE hospital_id = ?", (hospital_id,))
            cursor.execute("DELETE FROM test_summary WHERE hospital_id = ?", (hospital_id,))
            cursor.execute("DELETE FROM test_sessions WHERE hospital_id = ?", (hospital_id,))
            cursor.execute("DELETE FROM surgeries WHERE hospital_id = ?", (hospital_id,))
            cursor.execute("DELETE FROM patients WHERE hospital_id = ?", (hospital_id,))

            conn.commit()
            print(f"[成功] 已删除患者 {hospital_id} 及其相关数据")
        except Exception as e:
            conn.rollback()
            print(f"[失败] 删除患者 {hospital_id} 时出错: {e}")
        finally:
            cursor.close()
            conn.close()

    # --- 手术管理 ---
    def insert_surgery(self, hospital_id, surgery_time, tumor_position, surgery_type, surgeon):
        sql = """INSERT INTO surgeries 
        (hospital_id, surgery_time, tumor_position, surgery_type, surgeon) 
        VALUES (?, ?, ?, ?, ?)"""
        self._execute(sql, (hospital_id, surgery_time, tumor_position, surgery_type, surgeon))

    def insert_surgery_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            hospital_id = data.get('hospital_id')
            surgery_time = data.get('surgery_time')
            tumor_position = data.get('tumor_position')
            surgery_type = data.get('surgery_type')
            surgeon = data.get('surgeon')
            if hospital_id and surgery_time:
                self.insert_surgery(hospital_id, surgery_time, tumor_position, surgery_type, surgeon)
                print("✅ 手术记录添加成功")
            else:
                print("❌ 手术记录信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_surgeries(self, hospital_id):
        sql = "SELECT * FROM surgeries WHERE hospital_id = ?"
        return self._execute(sql, (hospital_id,), fetch=True)

    # --- 测试图片管理 ---
    def insert_image(self, image_name, category):
        relative_path = os.path.join('images', category, image_name)
        sql = "INSERT INTO test_images (image_name, relative_path, category) VALUES (?, ?, ?)"
        self._execute(sql, (image_name, relative_path, category))

    def insert_image_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            image_name = data.get('image_name')
            category = data.get('category')
            if image_name and category:
                self.insert_image(image_name, category)
                print("✅ 测试图片信息添加成功")
            else:
                print("❌ 测试图片信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_images_by_type(self, category):
        sql = "SELECT * FROM test_images WHERE category = ?"
        results = self._execute(sql, (category,), fetch=True)
        base_dir = os.path.dirname(os.path.dirname(self.db_path))
        absolute_results = []
        for row in results:
            image_id, image_name, relative_path, category = row
            absolute_path = os.path.join(base_dir, relative_path)
            absolute_results.append((image_id, image_name, absolute_path, category))
        return absolute_results
    # 会自动删除图片
    def delete_image(self, image_name, category):
        sql = "DELETE FROM test_images WHERE image_name = ? AND category = ?"
        self._execute(sql, (image_name, category))
        relative_path = os.path.join('images', category, image_name)
        absolute_path = os.path.join(os.path.dirname(os.path.dirname(self.db_path)), relative_path)
        if os.path.exists(absolute_path):
            os.remove(absolute_path)
            print(f"✅ 图片 {absolute_path} 已删除")
        else:
            print(f"❌ 图片 {absolute_path} 不存在，无法删除")

    # --- 测试记录管理 ---
    def insert_test_session(self, hospital_id, check_time, stage, surgery_time, position_number=None):
        sql = """INSERT INTO test_sessions 
        (hospital_id, check_time, stage, surgery_time, position_number) 
        VALUES (?, ?, ?, ?, ?)"""
        self._execute(sql, (hospital_id, check_time, stage, surgery_time, position_number))

    def insert_test_session_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            hospital_id = data.get('hospital_id')
            check_time = data.get('check_time')
            stage = data.get('stage')
            surgery_time = data.get('surgery_time')
            position_number = data.get('position_number')
            if hospital_id and check_time and stage and surgery_time:
                self.insert_test_session(hospital_id, check_time, stage, surgery_time, position_number)
                print("✅ 测试记录添加成功")
            else:
                print("❌ 测试记录信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_test_sessions(self, hospital_id):
        sql = "SELECT * FROM test_sessions WHERE hospital_id = ?"
        return self._execute(sql, (hospital_id,), fetch=True)

    # --- 每张图片的测试结果 ---
    def insert_image_test_result(self, hospital_id, check_time, category, image_name, used_time, is_correct, comment):
        sql = """INSERT INTO image_test_results 
        (hospital_id, check_time, category, image_name, used_time, is_correct, comment) 
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
        self._execute(sql, (hospital_id, check_time, category, image_name, used_time, is_correct, comment))

    def insert_image_test_result_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            hospital_id = data.get('hospital_id')
            check_time = data.get('check_time')
            category = data.get('category')
            image_name = data.get('image_name')
            used_time = data.get('used_time')
            is_correct = data.get('is_correct')
            comment = data.get('comment')
            if hospital_id and check_time and category and image_name and used_time is not None and is_correct is not None:
                self.insert_image_test_result(hospital_id, check_time, category, image_name, used_time, is_correct, comment)
                print("✅ 图片测试结果添加成功")
            else:
                print("❌ 图片测试结果信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_image_test_results(self, hospital_id, check_time):
        sql = "SELECT * FROM image_test_results WHERE hospital_id = ? AND check_time = ?"
        results = self._execute(sql, (hospital_id, check_time), fetch=True)
        base_dir = os.path.dirname(os.path.dirname(self.db_path))
        absolute_results = []
        for row in results:
            result_id, hospital_id, check_time, category, used_time, is_correct, comment = row
            image_info = self._get_image_info(category)
            if image_info:
                relative_path = image_info[2]
                absolute_path = os.path.join(base_dir, relative_path)
                absolute_results.append((result_id, hospital_id, check_time, category, used_time, is_correct, comment, absolute_path))
            else:
                absolute_results.append((result_id, hospital_id, check_time, category, used_time, is_correct, comment, None))
        return absolute_results

    def _get_image_info(self, category):
        sql = "SELECT * FROM test_images WHERE category = ?"
        return self._execute(sql, (category,), fetch=True)

    # --- 总结表 ---
    def insert_test_summary(self, hospital_id, check_time, accuracy_total, accuracy_by_position, total_time):
        sql = """INSERT INTO test_summary 
        (hospital_id, check_time, accuracy_total, accuracy_by_position, total_time)
        VALUES (?, ?, ?, ?, ?)"""
        self._execute(sql, (hospital_id, check_time, accuracy_total, accuracy_by_position, total_time))

    def insert_test_summary_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            hospital_id = data.get('hospital_id')
            check_time = data.get('check_time')
            accuracy_total = data.get('accuracy_total')
            accuracy_by_position = data.get('accuracy_by_position')
            total_time = data.get('total_time')
            if hospital_id and check_time and accuracy_total is not None and total_time is not None:
                self.insert_test_summary(hospital_id, check_time, accuracy_total, accuracy_by_position, total_time)
                print("✅ 测试总结添加成功")
            else:
                print("❌ 测试总结信息不完整")
        except json.JSONDecodeError:
            print("❌ JSON 解析错误")

    def get_test_summary(self, hospital_id, check_time):
        sql = "SELECT * FROM test_summary WHERE hospital_id = ? AND check_time = ?"
        return self._execute(sql, (hospital_id, check_time), fetch=True)

    # --- 查询视图 ---
    def get_patient_surgery_test_details(self, hospital_id):
        sql = "SELECT * FROM patient_surgery_test_view WHERE hospital_id = ?"
        results = self._execute(sql, (hospital_id,), fetch=True)
        base_dir = os.path.dirname(os.path.dirname(self.db_path))
        # print("base",base_dir)
        # 将查询结果转换为 JSON 格式
        columns = ['hospital_id', 'surgery_time', 'check_time', 'stage', 'stim_location', 'relative_path', 'is_correct',
                   'used_time', 'accuracy', 'avg_reaction_time']
        json_results = []
        for row in results:
            result_dict = dict(zip(columns, row))
            relative_path = result_dict.get('relative_path')
            if relative_path:
                # 确保 base_dir 是绝对路径
                base_dir = os.path.abspath(base_dir)
                absolute_path = os.path.join(base_dir, relative_path)
                # 规范化路径，处理可能的路径分隔符问题
                absolute_path = os.path.normpath(absolute_path)
                result_dict['relative_path'] = absolute_path
            json_results.append(result_dict)

        return json.dumps(json_results, ensure_ascii=False)
