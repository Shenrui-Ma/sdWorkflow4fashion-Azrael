import json
import random
import time
import urllib.parse
import urllib.request
import uuid
import websocket
from PIL import Image
import io


class SDComfyUIApi:
    def __init__(self, server_ip, server_port=8188) -> None: # 接受服务器地址和端口号作为参数
        # 初始化时，设置服务器地址和客户端ID
        self.SERVER_ADDRESS = server_ip + ":" + str(server_port)
        self.CLIENT_ID = str(uuid.uuid4())

    def queue_prompt(self, prompt):
        # 向服务器发送提示（prompt），并返回服务器的响应
        p = {"prompt": prompt, "client_id": self.CLIENT_ID}
        data = json.dumps(p).encode("utf-8") # 将数据编码为JSON格式
        req = urllib.request.Request( # 发送请求
            "http://{}/prompt".format(self.SERVER_ADDRESS), data=data
        )
        return json.loads(urllib.request.urlopen(req).read()) # 返回服务器的响应

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
        # 根据给定的提示和模板生成图像 (自定义模板路径)
        PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        payload = json.loads(PROMPT_TEXT)

        # positive prompt node
        payload["12"]["inputs"]["text"] = prompt
        # KSampler node
        payload["10"]["inputs"]["seed"] = (
            seed if seed is not None else random.randint(0, 1000000)
        )

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
    # 初始化SDComfyUIApi客户端
    server_ip = "127.0.0.1"  # 或者其他服务器IP
    sd_client = SDComfyUIApi(server_ip)
    
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

    # 定义自定义参数
    prompt = "best quality,masterpiece,artistic,1girl,standing,blue eyes,blonde hair,blue dress,blue ribbon,ribbon,ribbon in hair,smile,smiling,standing,white background"
    template_name = "test"
    output_node_id = "15"
    
    # 创建配置实例
    config = SDComfyUIConfig(prompt, template_name, output_node_id)
    
    # 调用main函数
    main(config)