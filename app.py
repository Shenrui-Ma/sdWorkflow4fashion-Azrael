import os
import subprocess
from flask import Flask, request, send_file
from flask_cors import CORS
import glob
import io
from scripts.api_youdao import createRequest
from scripts.sd_comfy_ui_api_generate_cloth_dreamshaper import (
    generate_cloth_dreamshaper,
)

app = Flask(__name__)
CORS(app)

# TRANSLATE_SCRIPT_PATH = "C:/Users/女明星/Desktop/综英小组作业/youdao.py"
# TRANSLATE_SCRIPT_PATH = "E:/Projects/Repos/sdWorkflow4fashion-Azrael/youdao.py"
TRANSLATE_SCRIPT_PATH = (
    "E:/Projects/Repos/sdWorkflow4fashion-Azrael/scripts/api_youdao.py"
)
# 需要修改api_youdao.py的路径
# IMAGE_FOLDER = "C:/Users/女明星/Desktop/综英小组作业/generate_images"
IMAGE_FOLDER = "E:\ComfyUI-aki\ComfyUI-aki-v1.3\output"
# 需要修改存储最新生成的图片的文件夹路径
prompt = None


# 测试用的
@app.route("/")
def index():
    return "OK!"


@app.route("/generate_cloth", methods=["GET", "POST"])
def get_prompt():
    global prompt
    if request.method == "POST":
        # 对于 POST 请求，假设数据是以 JSON 格式发送的
        user_input = request.json.get("user_input")
    else:
        # 对于 GET 请求，从 URL 参数获取
        user_input = request.args.get("user_input")
    if user_input is None:
        return "No user input provided", 400

    # 调用翻译脚本createRequest函数
    result = createRequest(q=user_input)
    prompt = str(result)  # 提取标准输出
    print("******************************************生成文本")
    print(prompt)

    if not prompt:
        print("Failed to generate prompt")
        return "Failed to generate prompt", 500
    else:
        print("******************************************调用生成文本")
        print("******************************************调用画图")
        # 调用生成图片的函数，并直接返回其结果
        return generate_cloth()


def generate_cloth():
    # 调用生成图片脚本 generate_cloth_dreamshaper
    image_data = generate_cloth_dreamshaper(prompt, "generate_cloth_dreamshaper", "15")

    newest_image = get_newest_image(IMAGE_FOLDER)
    if newest_image:
        return send_file(newest_image, mimetype="image/png")  # 确保使用正确的MIME类型
    else:
        return "No image found", 404


import os
import glob


def get_newest_image(folder):
    """
    获取指定文件夹中最新的.png格式图片的路径。

    参数:
    folder (str): 要搜索的文件夹路径。

    返回:
    str: 最新的.png图片的完整路径。如果没有找到任何.png图片，返回None。
    """
    # 构建搜索模式，匹配所有.png文件
    search_pattern = os.path.join(folder, "*.png")
    # 使用glob.glob找到所有匹配的文件
    list_of_files = glob.glob(search_pattern)

    # 检查是否有找到文件
    if not list_of_files:
        return None

    # 使用max函数和os.path.getctime找到最新的文件
    newest_file = max(list_of_files, key=os.path.getctime)
    print("最新图片路径：", newest_file)

    return newest_file


if __name__ == "__main__":
    app.run(debug=True)
