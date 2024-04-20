import os
import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

# TRANSLATE_SCRIPT_PATH = "C:/Users/女明星/Desktop/综英小组作业/youdao.py"
# TRANSLATE_SCRIPT_PATH = "E:/Projects/Repos/sdWorkflow4fashion-Azrael/youdao.py"
TRANSLATE_SCRIPT_PATH = "E:/Projects/Repos/sdWorkflow4fashion-Azrael/scripts/api_youdao.py"
# 需要修改api_youdao.py的路径
# IMAGE_FOLDER = "C:/Users/女明星/Desktop/综英小组作业/generate_images"
IMAGE_FOLDER = "E:\ComfyUI-aki\ComfyUI-aki-v1.3\output"
# 需要修改存储最新生成的图片的文件夹路径
prompt=None


@app.route('/generate_cloth', methods=['GET', 'POST'])
def get_prompt():
    global prompt
    if request.method == 'POST':
        # 对于 POST 请求，假设数据是以 JSON 格式发送的
        user_input = request.json.get('user_input')
    else:
        # 对于 GET 请求，从 URL 参数获取
        user_input = request.args.get('user_input')
    if user_input is None:
        return "No user input provided", 400

    translation_command = ['python', TRANSLATE_SCRIPT_PATH, user_input]
    result = subprocess.run(translation_command, capture_output=True, text=True)
    prompt = result

    if prompt is None:
        return "Failed to generate prompt", 500
    else:
        return prompt
def generate_cloth():
    newest_image = get_newest_image(IMAGE_FOLDER)

    if newest_image:
        return send_file(newest_image, mimetype='image/jpeg')
    else:
        return 'No image found'


def get_newest_image(folder):
    list_of_files = glob.glob(os.path.join(folder, '*.jpg'))
    # 修改成文件中的图片格式
    if not list_of_files:
        return None
    lastest_file = max(list_of_files, key=os.path.getctime)
    return lastest_file

if __name__ == '__main__':
    app.run(debug=True)

