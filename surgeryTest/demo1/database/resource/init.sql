-- 修改后的 init.sql
PRAGMA foreign_keys = ON;

--- 基础表 ---

CREATE TABLE IF NOT EXISTS patients (
    hospital_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT CHECK(gender IN ('男', '女')) NOT NULL,
    age INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS surgeries (
    surgery_id INTEGER PRIMARY KEY AUTOINCREMENT, -- 自增手术id
    hospital_id TEXT NOT NULL,
    surgery_time TEXT NOT NULL,
    tumor_position TEXT,
    surgery_type TEXT,
    surgeon TEXT,
    FOREIGN KEY(hospital_id) REFERENCES patients(hospital_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS test_images (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    category TEXT NOT NULL,
    UNIQUE (category, image_name)  -- 确保组合唯一
);

CREATE TABLE IF NOT EXISTS test_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id TEXT NOT NULL,
    check_time TEXT NOT NULL,
    stage TEXT NOT NULL,
    surgery_time TEXT NOT NULL,
    position_number INTEGER,
    FOREIGN KEY(hospital_id) REFERENCES patients(hospital_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS image_test_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id TEXT NOT NULL,
    check_time TEXT NOT NULL,
    category TEXT NOT NULL,
    image_name TEXT NOT NULL,
    used_time REAL,
    is_correct INTEGER NOT NULL CHECK(is_correct IN (0, 1)),
    comment TEXT,
    FOREIGN KEY(hospital_id) REFERENCES patients(hospital_id) ON DELETE CASCADE,
    FOREIGN KEY(category, image_name) REFERENCES test_images(category, image_name)
);

CREATE TABLE IF NOT EXISTS test_summary (
    summary_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hospital_id TEXT NOT NULL,
    check_time TEXT NOT NULL,
    accuracy_total REAL,
    accuracy_by_position TEXT,
    total_time REAL,
    FOREIGN KEY(hospital_id) REFERENCES patients(hospital_id) ON DELETE CASCADE
);

--- 查询视图 ---

--- get the hospital_id , patients,name,gender,age,surgeries information
CREATE VIEW patient_surgery_view AS
SELECT
    p.hospital_id,
    p.name AS patient_name,
    p.gender,
    p.age,
    s.surgery_id,
    s.surgery_time,
    s.tumor_position,
    s.surgery_type,
    s.surgeon
FROM
    patients p
LEFT JOIN
    surgeries s ON p.hospital_id = s.hospital_id;

--- get  all picture test records of a surgery ---
CREATE VIEW surgery_image_test_view AS
SELECT
    s.hospital_id,
    s.surgery_time,
    ts.check_time,
    itr.category,
    ti.image_name,
    ti.relative_path,
    itr.used_time,
    itr.is_correct,
    itr.comment
FROM surgeries s
JOIN test_sessions ts
    ON s.hospital_id = ts.hospital_id AND s.surgery_time = ts.surgery_time
JOIN image_test_results itr
    ON ts.hospital_id = itr.hospital_id AND ts.check_time = itr.check_time
JOIN test_images ti
    ON itr.category = ti.category AND itr.image_name = ti.image_name;

--- get the surgery details, test results, accuracy and average reaction time for a patient by hospital_id
CREATE VIEW patient_surgery_test_view AS
SELECT
    s.hospital_id,
    s.surgery_time,
    ts.check_time,
    ts.stage,
    ts.position_number AS stim_location,
    ti.relative_path,
    itr.is_correct,
    itr.used_time,
    -- Calculate the accuracy for each surgery
    (SELECT AVG(is_correct) FROM image_test_results WHERE hospital_id = s.hospital_id AND check_time = ts.check_time) AS accuracy,
    -- Calculate the average reaction time for each surgery
    (SELECT AVG(used_time) FROM image_test_results WHERE hospital_id = s.hospital_id AND check_time = ts.check_time) AS avg_reaction_time
FROM
    surgeries s
JOIN
    test_sessions ts ON s.hospital_id = ts.hospital_id AND s.surgery_time = ts.surgery_time
JOIN
    image_test_results itr ON ts.hospital_id = itr.hospital_id AND ts.check_time = itr.check_time
JOIN
    test_images ti ON itr.category = ti.category AND itr.image_name = ti.image_name;