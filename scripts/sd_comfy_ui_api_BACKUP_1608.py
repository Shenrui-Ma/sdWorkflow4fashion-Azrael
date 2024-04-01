import json
import random
import time
import urllib.parse
import urllib.request
import uuid
import websocket
from PIL import Image
import io
<<<<<<< HEAD
import base64


class SDComfyUIConfig:
    def __init__(self, server_ip, server_port=8188, prompt=None, template_name=None,person_image_path=None,clothes_image_path=None,loadimage_node_id = None, output_node_id=None):
        self.server_ip = server_ip
        self.server_port = server_port
        self.prompt = prompt
        self.template_name = template_name
        self.output_node_id = output_node_id

        # 额外添加两个参数person_image_path和clothes_image_path，但在初始化时不需要传入，默认为None
        self.person_image_path = person_image_path
        self.clothes_image_path = clothes_image_path

        # 额外添加参数loadimga_node_id，但在初始化时不需要传入，默认为None
        self.loadimage_node_id = loadimage_node_id
=======
>>>>>>> parent of c74e314 (完成了基于sd的生成写实风衣服（generate),基本的图生图，移除衣服背景(rembg),给抠好的模特穿衣服(dress))


class SDComfyUIApi:
    def __init__(self, server_ip, server_port=8188) -> None: # 接受服务器地址和端口号作为参数
        # 初始化时，设置服务器地址和客户端ID
        self.SERVER_ADDRESS = server_ip + ":" + str(server_port)
        self.CLIENT_ID = str(uuid.uuid4())

<<<<<<< HEAD
    def find_positive_prompt_node_id(self,template):
        for node_id, node_info in template.items():
            if node_info.get("class_type") == "CLIPTextEncode":
                return node_id
        return None

    def find_k_sampler_node_id(self,template):
        for node_id, node_info in template.items():
            if node_info.get("class_type") == "KSampler":
                return node_id
        return None

    def find_output_node_id(self,template):
        for node_id, node_info in template.items():
            if node_info.get("class_type") == "SaveImage":
                return node_id
        return None

    def queue_prompt(self, prompt=None):  # 默认prompt可以为空
        p = {"client_id": self.CLIENT_ID}
        if prompt is not None:
            p["prompt"] = prompt
        data = json.dumps(p).encode("utf-8")  # 将数据编码为JSON格式
        headers = {'Content-Type': 'application/json'}  # 指定内容类型为JSON
        req = urllib.request.Request(  # 发送请求
            "http://{}/prompt".format(self.SERVER_ADDRESS), data=data, headers=headers
=======
    def queue_prompt(self, prompt):
        # 向服务器发送提示（prompt），并返回服务器的响应
        p = {"prompt": prompt, "client_id": self.CLIENT_ID}
        data = json.dumps(p).encode("utf-8") # 将数据编码为JSON格式
        req = urllib.request.Request( # 发送请求
            "http://{}/prompt".format(self.SERVER_ADDRESS), data=data
>>>>>>> parent of c74e314 (完成了基于sd的生成写实风衣服（generate),基本的图生图，移除衣服背景(rembg),给抠好的模特穿衣服(dress))
        )
        try:
            response = urllib.request.urlopen(req)
            return json.loads(response.read())  # 返回服务器的响应
        except urllib.error.HTTPError as e:
            print(f"请求失败，HTTP错误代码: {e.code}, 原因: {e.reason}")
            return None

    def get_image(self, filename, subfolder, folder_type):
        # 从服务器获取指定的图像
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(
            "http://{}/view?{}".format(self.SERVER_ADDRESS, url_values)
        ) as response:
            return response.read()

    def get_history(self, prompt_id):
        # 获取指定提示ID的历史记录
        with urllib.request.urlopen(
            "http://{}/history/{}".format(self.SERVER_ADDRESS, prompt_id)
        ) as response:
            return json.loads(response.read())

    def get_images(self, ws, prompt):
        # 通过WebSocket连接获取图像
        prompt_id = self.queue_prompt(prompt)["prompt_id"]
        output_images = {}
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message["type"] == "executing" and message["data"]["node"] is None and message["data"]["prompt_id"] == prompt_id:
                    break  # 执行完成
            else:
                continue  # 忽略二进制数据

        history = self.get_history(prompt_id)[prompt_id]
        for o in history["outputs"]:
            for node_id in history["outputs"]:
                node_output = history["outputs"][node_id]
                if "images" in node_output:
                    images_output = []
                    for image in node_output["images"]:
                        image_data = self.get_image(
                            image["filename"], image["subfolder"], image["type"]
                        )
                        images_output.append(image_data)
                output_images[node_id] = images_output

        return output_images

    def generate_image(self, prompt, template_name, output_node_id, seed=None) -> bytes:
<<<<<<< HEAD
        PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        payload = json.loads(PROMPT_TEXT) 

        # 使用函数获取节点id
        positive_prompt_node_id = self.find_positive_prompt_node_id(payload)
        k_sampler_node_id = self.find_k_sampler_node_id(payload)
        output_node_id = self.find_output_node_id(payload)  # 重新获取output_node_id

        # 根据获取的节点id修改payload
        if positive_prompt_node_id:
            payload[positive_prompt_node_id]["inputs"]["text"] = prompt

            
        if k_sampler_node_id:
            payload[k_sampler_node_id]["inputs"]["seed"] = (
                seed if seed is not None else random.randint(0, 1000000)
            )

        t = time.time()
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.SERVER_ADDRESS, self.CLIENT_ID))
        images = self.get_images(ws, payload)
        print("Time taken:", time.time() - t)

        # 返回指定节点ID的第一张图像
        return images[output_node_id][0] if output_node_id in images else None


class SDComfyUI_i2i_Api(SDComfyUIApi):
    def __init__(self, config: SDComfyUIConfig) -> None:
        super().__init__(config)

    def image_to_base64(self, image_path):
        # 将图片转换为Base64编码
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def generate_image_from_image(self, image_path, template_name, output_node_id, seed=None) -> bytes:
        # 读取模板
        PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        payload = json.loads(PROMPT_TEXT)

        # 将图片转换为Base64编码
        image_base64 = self.image_to_base64(image_path)

        # 使用函数获取节点id
        positive_prompt_node_id = self.find_positive_prompt_node_id(payload)
        k_sampler_node_id = self.find_k_sampler_node_id(payload)
        loadimage_node_id = self.config.loadimage_node_id
        output_node_id = self.find_output_node_id(payload)  # 重新获取output_node_id

        # 把图片作为作为LoadImage节点的输入，loadimage节点的id是9
        if loadimage_node_id:
            payload[loadimage_node_id]["inputs"]["image"] = image_base64

        if positive_prompt_node_id:
            print("给了给了"+payload[positive_prompt_node_id]["inputs"]["text"])
            payload[positive_prompt_node_id]["inputs"]["text"] = "best_quality"

        if k_sampler_node_id:
            payload[k_sampler_node_id]["inputs"]["seed"] = (
                seed if seed is not None else random.randint(0, 1000000)
            )
=======
        # 根据给定的提示和模板生成图像 (自定义模板路径)
        PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        payload = json.loads(PROMPT_TEXT)

        # positive prompt node
        payload["12"]["inputs"]["text"] = prompt
        # KSampler node
        payload["10"]["inputs"]["seed"] = (
            seed if seed is not None else random.randint(0, 1000000)
        )
>>>>>>> parent of c74e314 (完成了基于sd的生成写实风衣服（generate),基本的图生图，移除衣服背景(rembg),给抠好的模特穿衣服(dress))

        t = time.time()
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.SERVER_ADDRESS, self.CLIENT_ID))
        images = self.get_images(ws, payload)
        print("Time taken:", time.time() - t)

        # 返回指定节点ID的第一张图像
        return images[output_node_id][0]


# if __name__ == "__main__":
#     # 示例用法
#     # server_ip = "192.168.1.12"
#     server_ip = "127.0.0.1"
#     sd_client = SDComfyUIApi(server_ip)
#     # 调用generate_image方法生成图像
#     prompt = "best quality,masterpiece,artistic,1girl,standing,blue eyes,blonde hair,blue dress,blue ribbon,ribbon,ribbon in hair,smile,smiling,standing,white background"
#     # 模板名称
#     with open('templates/test.json') as f:
#         template_name = "test"
#     # 输出节点ID
#     output_node_id = "15" # 输出节点是指生成图像的节点
#     # sd_client.generate_image("你的提示", "模板名称", "输出节点ID")
#     sd_client.generate_image(prompt, template_name, output_node_id)
    

class SDComfyUIConfig:
    def __init__(self, prompt, template_name, output_node_id):
        self.prompt = prompt
        self.template_name = template_name
        self.output_node_id = output_node_id

def main(config):
<<<<<<< HEAD
    # init SDComfyUIApi instance with server ip  
    sd_client = SDComfyUIApi(config)
=======
    # 初始化SDComfyUIApi客户端
    server_ip = "127.0.0.1"  # 或者其他服务器IP
    sd_client = SDComfyUIApi(server_ip)
>>>>>>> parent of c74e314 (完成了基于sd的生成写实风衣服（generate),基本的图生图，移除衣服背景(rembg),给抠好的模特穿衣服(dress))
    
    # 从配置中获取参数
    prompt = config.prompt
    template_name = config.template_name
    output_node_id = config.output_node_id
    
    # 生成图像
    image_data = sd_client.generate_image(prompt, template_name, output_node_id)
    # 这里可以添加代码来处理image_data，例如保存到文件或显示图像

    # 展示图像到窗口
    image = Image.open(io.BytesIO(image_data))
    image.show()


if __name__ == "__main__":
<<<<<<< HEAD
    # 设置自定义参数
    prompt = "best quality,masterpiece,artistic,1girl,standing,blue eyes,blonde hair,blue dress,blue ribbon,ribbon,ribbon in hair,smile,smiling,standing,white background"
    template_name = "generate_cloth_meinamix"
    server_ip = "127.0.0.1"  # 服务器IP
    server_port = 8188  # 服务器端口，默认为8188
    output_node_id = "15"
    
    # 创建配置实例
    config = SDComfyUIConfig(server_ip=server_ip, server_port=server_port, prompt=prompt, template_name=template_name, output_node_id=output_node_id)
=======

    # 定义自定义参数
    prompt = "best quality,masterpiece,artistic,1girl,standing,blue eyes,blonde hair,blue dress,blue ribbon,ribbon,ribbon in hair,smile,smiling,standing,white background"
    template_name = "test"
    output_node_id = "15"
    
    # 创建配置实例
    config = SDComfyUIConfig(prompt, template_name, output_node_id)
>>>>>>> parent of c74e314 (完成了基于sd的生成写实风衣服（generate),基本的图生图，移除衣服背景(rembg),给抠好的模特穿衣服(dress))
    
    # 调用main函数
    main(config)