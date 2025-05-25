#已弃置

import sqlite3
import os

class InitDB:
    def init_db(db_path='surgery.db'):
        if os.path.exists(db_path):
            print(f"数据库文件 {db_path} 已存在，初始化将跳过创建。")
            return

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 启用外键约束
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 创建表
        cursor.executescript('''
        -- 患者表
        CREATE TABLE IF NOT EXISTS patients (
            hospital_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT CHECK (gender IN ('男', '女')) NOT NULL,
            age INTEGER CHECK (age >= 0)
        );
    
        -- 手术信息表
        CREATE TABLE IF NOT EXISTS surgeries (
            hospital_id TEXT,
            surgery_time TEXT,
            tumor_position TEXT,
            surgery_type TEXT,
            surgeon INTEGER,
            PRIMARY KEY (hospital_id, surgery_time),
            FOREIGN KEY (hospital_id) REFERENCES patients(hospital_id)
        );
    
        -- 测试图片表
        CREATE TABLE IF NOT EXISTS test_images (
            category TEXT,
            inner_number INTEGER,
            image_name TEXT,
            relative_path TEXT,
            PRIMARY KEY (category, inner_number)
        );
    
        -- 测试记录表（每次测试）
        CREATE TABLE IF NOT EXISTS test_sessions (
            hospital_id TEXT,
            check_time TEXT,
            stage TEXT CHECK (stage IN ('术前', '术中', '术后')),
            surgery_time TEXT,
            position_number INTEGER,
            PRIMARY KEY (hospital_id, check_time),
            FOREIGN KEY (hospital_id) REFERENCES patients(hospital_id),
            FOREIGN KEY (hospital_id, surgery_time) REFERENCES surgeries(hospital_id, surgery_time)
        );
    
        -- 图片测试详情表（每张图片结果）
        CREATE TABLE IF NOT EXISTS image_test_results (
            hospital_id TEXT,
            check_time TEXT,
            category TEXT,
            inner_number INTEGER,
            used_time REAL,
            is_correct INTEGER CHECK (is_correct IN (0, 1)),
            comment TEXT,
            PRIMARY KEY (hospital_id, check_time, category, inner_number),
            FOREIGN KEY (hospital_id, check_time) REFERENCES test_sessions(hospital_id, check_time),
            FOREIGN KEY (category, inner_number) REFERENCES test_images(category, inner_number)
        );
    
        -- 测试总结表
        CREATE TABLE IF NOT EXISTS test_summary (
            hospital_id TEXT,
            check_time TEXT,
            accuracy_total REAL,
            accuracy_by_position TEXT,
            total_time REAL,
            PRIMARY KEY (hospital_id, check_time),
            FOREIGN KEY (hospital_id, check_time) REFERENCES test_sessions(hospital_id, check_time)
        );
        ''')

        conn.commit()
        conn.close()
        print(f"数据库初始化完成：{os.path.abspath(db_path)}")
