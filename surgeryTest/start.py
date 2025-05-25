import subprocess
import webbrowser
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
DEMO1_PATH = os.path.join(BASE_DIR, "demo1")

# ✅ 判断是否为打包状态
IS_FROZEN = getattr(sys, 'frozen', False)

if IS_FROZEN:
    # 打包后直接执行Flask应用程序
    FLASK_EXEC = os.path.join(DEMO1_PATH, "app.exe")
else:
    # 普通脚本运行
    FLASK_EXEC = sys.executable

print("使用解释器：", FLASK_EXEC)
print("Flask 目录：", DEMO1_PATH)

# 启动 Flask
try:
    if IS_FROZEN:
        # 打包状态下直接执行应用程序
        flask_process = subprocess.Popen([FLASK_EXEC], cwd=DEMO1_PATH)
    else:
        # 开发状态下使用Python解释器运行app.py
        flask_process = subprocess.Popen([FLASK_EXEC, "app.py"], cwd=DEMO1_PATH)

    # 给Flask应用启动时间
    time.sleep(3)

    # 打开浏览器
    webbrowser.open("http://127.0.0.1:5000/login")
    webbrowser.open("http://127.0.0.1:5000/patient/")

    # 等待Flask进程结束
    flask_process.wait()

except KeyboardInterrupt:
    # 处理Ctrl+C中断
    flask_process.terminate()
except Exception as e:
    # 处理其他异常
    print(f"启动应用程序时出错: {e}")
    if 'flask_process' in locals():
        flask_process.terminate()