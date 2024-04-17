import os
import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TRANSLATE_SCRIPT_PATH = "C:/Users/女明星/Desktop/综英小组作业/youdao.py"
# 需要修改api_youdao.py的路径
GENERATE_SCRIPT_PATH = os.path.join('C:','Users','女明星','Desktop','综英小组作业','sd_comfy_ui_api_generate_cloth_dreamshaper.py')
# 同上
IMAGE_FOLDER = "C:/Users/女明星/Desktop/综英小组作业/generate_images"
# 需要修改存储最新生成的图片的文件夹路径


@app.route('/generate_cloth', methods=['POST'])
def generate_cloth():
    # 获取用户发送的自然语言输入
    user_input = request.json.get('user_input')

    # 调用翻译脚本 api_youdao.py，并传递翻译后的文本作为参数
    translation_command = ['python', TRANSLATE_SCRIPT_PATH, user_input]
    result = subprocess.run(translation_command, capture_output=True, text=True)

    # 获取标准输出并按行拆分
    output_lines = result.stdout.strip().split('\n')

    prompt = None

    for line in output_lines:
        if 'prompt:' in line:
            prompt = line.split('prompt:')[1].strip()
            break
    # 获取prompt中的信息

    # 调用生成服装脚本 sd_comfy_ui_api_generate_cloth_dreamshaper.py
    generate_command = ['python', GENERATE_SCRIPT_PATH, prompt]  # 将翻译后的文本作为 prompt 参数传递给生成服装脚本
    subprocess.run(generate_command)

    # 获取最新生成的图片路径
    latest_image_path = os.path.join(IMAGE_FOLDER, 'latest_image.jpg')

    # 返回给前端展示
    return send_file(latest_image_path, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)