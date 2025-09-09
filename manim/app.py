# app.py
import os
import shutil
import uuid
import subprocess
import tempfile
from flask import Flask, request, jsonify, render_template, send_from_directory
from pathlib import Path
import time

app = Flask(__name__)

# manim官方生成的视频
VIDEO = Path("media/videos/1111/1080p60")
# VIDEO = Path("media/videos/1111/480p15")

STATUS='pending'   #'failed'  'completed'

# 存放生成的视频
VIDEO_DIR = Path("static/videos")
VIDEO_DIR.mkdir(exist_ok=True)

# 临时保存用户代码的目录
CODE_DIR = Path("temp_user_code")
CODE_DIR.mkdir(exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/media/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory('media/videos/', filename)

@app.route('/run', methods=['POST'])
def run_manim_code():
    folder_path = "media"
    # 判断文件夹是否存在并删除
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)  # 删除文件夹及其中的所有内容
        print(f"Folder {folder_path} and its contents have been deleted.")
    else:
        print("The folder does not exist.")
   
    try:
        user_code = request.json.get('code', '')

        if not user_code.strip():
            return jsonify({'error': '代码为空'}), 400

        # 为本次运行生成唯一 ID
        run_id = "1111"#str(uuid.uuid4())[:8]
        video_path = VIDEO_DIR / f"{run_id}.mp4"
        py_code_path = CODE_DIR / f"{run_id}.py"

        # 构造完整的 manim 代码，包含一个示例 Scene 类
        full_code = f"""
{user_code}
    """

        # 保存用户代码到临时 .py 文件
        try:
            with open(py_code_path, 'w', encoding='utf-8') as f:
                f.write(full_code)
        except Exception as e:
            return jsonify({'error': f'保存代码失败: {e}'}), 500

        # return jsonify({'success': True, 'video_url': str(VIDEO)+"/UserScene.mp4"})
        # return jsonify({'success': True, 'video_url': str(VIDEO_DIR)+"/1111"+".mp4"})
        # 调用 manim 命令行渲染动画（使用 -pqh 表示低质量快速预览）
        try:
            result = subprocess.Popen(
                ['manim', '-qk','-qh', str(py_code_path), 'UserScene']
                # ,
                # capture_output=True,
                # text=True,
                # timeout=10  # 限制执行时间，避免卡死
            )
            # stdout, stderr = result.communicate()  # 等待命令执行完成
            # result.wait()
            # time.sleep(10)
        except subprocess.TimeoutExpired:
            return jsonify({'error': '渲染超时（超过5秒）'}), 500
        except Exception as e:
            return jsonify({'error': f'执行 manim 失败: {e}'}), 500


        return jsonify({'success': True, 'video_url': str(VIDEO)+"/UserScene.mp4"})

    except Exception as e:
        # 捕获所有其他未知异常，防止服务崩溃
        print("服务器内部错误：")#, traceback.format_exc())
        return jsonify({'error': f'服务器内部错误：{e}'}), 500

@app.route('/run2', methods=['POST'])
def run_manim_code2():
    return jsonify({'success': True, 'video_url': str(VIDEO)+"/UserScene.mp4"})    

@app.route('/requestt', methods=['POST'])
def requestt():
    video_path=str(VIDEO)+"/UserScene.mp4"
    
    if os.path.exists(video_path):
        print('yes')
        return jsonify({'status':'completed'})
    else:
        print('no')
        return jsonify({'status':'pending'})

def indent_code(code: str) -> str:
    """给多行代码加上缩进（4个空格），因为要在类方法内"""
    lines = code.split('\n')
    return '\n'.join(f"        {line}" if line.strip() else '' for line in lines)

if __name__ == '__main__':
    app.run(debug=True)