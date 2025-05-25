from flask import Flask
from flask_socketio import SocketIO
from routes.patient import patient_bp
from routes.api import api_bp
from sockets.events import register_socket_events
from routes.login import login_bp
from routes.patient_info import patient_info_bp
from routes.test_control import test_control_bp
from db_instance import db
from routes.image_api import image_api_bp
from routes.image_upload import upload_bp
from routes.statistics import statistics_bp
from routes.get_records import get_records_bp
import os


app = Flask(__name__,template_folder='templates')
app.config.from_object('config')
socketio = SocketIO(app)

# 处理打包后的路径问题



# 连接数据库
# 初始化数据库管理器 # 创建 SurgeryDBManager 实例

# 检查数据库是否存在，若不存在则初始化
if not os.path.exists(db.db_path):
    print("数据库文件不存在，开始初始化数据库...")
    db.initialize_database()
else:
    print("数据库文件已存在，直接连接数据库。")


# 注册蓝图
app.register_blueprint(patient_bp)
app.register_blueprint(api_bp)
app.register_blueprint(login_bp)
app.register_blueprint(patient_info_bp)

app.register_blueprint(test_control_bp)

app.register_blueprint(upload_bp)
app.register_blueprint(image_api_bp)

app.register_blueprint(statistics_bp)

app.register_blueprint(get_records_bp)


# 注册 socket 事件
register_socket_events(socketio)


if __name__ == '__main__':
    # 创建上传目录和记录目录（如果不存在）
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RECORD_FOLDER'], exist_ok=True)
    socketio.run(app, debug=True)

