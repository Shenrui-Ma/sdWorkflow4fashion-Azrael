# import json
# import base64
# import websocket
# from PIL import Image
# import io
# import uuid
# import urllib.request
# import urllib.parse
# import time
# from sd_comfy_ui_api import SDComfyUIConfig

# class SDComfyUIRemoveBg():
#     def __init__(self, config: SDComfyUIConfig) -> None:
#         self.SERVER_ADDRESS = config.server_ip + ":" + str(config.server_port)
#         self.CLIENT_ID = str(uuid.uuid4())
#         self.config = config

#     def image_to_base64(self, image_path):
#         # 将图片转换为Base64编码
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode('utf-8')
        
#     def get_image(self, filename, subfolder, folder_type):
#         # 从服务器获取指定的图像
#         data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
#         url_values = urllib.parse.urlencode(data)
#         with urllib.request.urlopen(
#             "http://{}/view?{}".format(self.SERVER_ADDRESS, url_values)
#         ) as response:
#             return response.read()

#     def generate_rembg_image(self, image_path, template_name, output_node_id):
#         # 读取模板文件
#         PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
#         payload = json.loads(PROMPT_TEXT)
        
#         # 将图片转换为Base64编码并插入到payload中
#         image_base64 = self.image_to_base64(image_path)
#         payload["9"]["inputs"]["image"] = image_base64
#         payload["client_id"] = self.CLIENT_ID


#         # 通过WebSocket发送payload
#         ws = websocket.WebSocket()
#         ws.connect("ws://{}/ws?clientId={}".format(self.SERVER_ADDRESS, self.CLIENT_ID))
#         print("Sending the image to the server...")
#         ws.send(json.dumps(payload))
#         print("Image sent to the server.")

#         # 设置超时时间，例如30秒
#         timeout = 30
#         start_time = time.time()
#         print("Waiting for the server to process the image...")

#         # 等待服务器返回处理后的图片
#         while True:
#             if time.time() - start_time > timeout:
#                 ws.close()  # 关闭WebSocket连接
#                 raise TimeoutError("服务器响应超时。")

#             response = ws.recv()
#             response_data = json.loads(response)
#             if "result" in response_data and response_data["result"] == "success":
#                 # 服务器处理成功，获取返回的文件名
#                 filename = response_data["filename"]
#                 break
#             elif "result" in response_data and response_data["result"] == "error":
#                 # 服务器处理出错
#                 error_message = response_data.get("message", "Unknown error.")
#                 ws.close()  # 关闭WebSocket连接
#                 raise Exception(f"Server returned an error: {error_message}")

#         # 关闭WebSocket连接
#         ws.close()

#         # 从服务器获取处理后的图片
#         return self.get_image(filename, "output", "processed")




# # 使用示例
# def main(config):
#     sd_client = SDComfyUIRemoveBg(config)

#     # 获取配置参数
#     template_name = config.template_name
#     output_node_id = config.output_node_id
    
#     # 生成图片
#     image_data = sd_client.generate_rembg_image(config.clothes_image_path, template_name, output_node_id)
    
#     # 显示图片
#     image = Image.open(io.BytesIO(image_data))
#     image.show()

# if __name__ == "__main__":
#     server_ip = "127.0.0.1"
#     output_node_id = "10"

#     template_name = "rembg"
#     clothes_image_path = r"E:\\ComfyUI-aki\\ComfyUI-aki-v1.3\\output\\ComfyUI_00277_.png"

#     config = SDComfyUIConfig(server_ip=server_ip, template_name=template_name, output_node_id=output_node_id, clothes_image_path=clothes_image_path)
#     main(config)


import json
import base64
import websocket
from PIL import Image
import io
import uuid
import urllib.request
import urllib.parse
import time

class SDComfyUIConfig:
    def __init__(self, server_ip, server_port=8188, image_path=None):
        self.server_ip = server_ip
        self.server_port = server_port
        self.image_path = image_path

class SDComfyUIRemoveBg:
    def __init__(self, config: SDComfyUIConfig) -> None:
        self.SERVER_ADDRESS = f"{config.server_ip}:{config.server_port}"
        self.CLIENT_ID = str(uuid.uuid4())
        self.config = config

    def image_to_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.SERVER_ADDRESS}/view?{url_values}") as response:
            return response.read()

    def generate_rembg_image(self):
        template_name = "rembg"
        # 读取模板文件
        PROMPT_TEXT = open(f"./templates/{template_name}.json", encoding='utf-8').read()
        payload = json.loads(PROMPT_TEXT)

        # 将图片转换为Base64编码并插入到payload中
        image_base64 = self.image_to_base64(self.config.image_path)
        payload["9"]["inputs"]["image"] = image_base64
        payload["client_id"] = self.CLIENT_ID

        # 通过WebSocket发送payload
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.SERVER_ADDRESS}/ws?clientId={self.CLIENT_ID}")
        print("Sending the image to the server...")
        ws.send(json.dumps(payload))
        print("Image sent to the server.")

        # 设置超时时间，例如30秒
        timeout = 30
        start_time = time.time()
        print("Waiting for the server to process the image...")

        # 等待服务器返回处理后的图片
        while True:
            if time.time() - start_time > timeout:
                ws.close()  # 关闭WebSocket连接
                raise TimeoutError("服务器响应超时。")

            response = ws.recv()
            response_data = json.loads(response)
            if "result" in response_data and response_data["result"] == "success":
                # 服务器处理成功，获取返回的文件名
                filename = response_data["filename"]
                break
            elif "result" in response_data and response_data["result"] == "error":
                # 服务器处理出错
                error_message = response_data.get("message", "Unknown error.")
                ws.close()  # 关闭WebSocket连接
                raise Exception(f"Server returned an error: {error_message}")

        # 关闭WebSocket连接
        ws.close()

        # 从服务器获取处理后的图片
        return self.get_image(filename, "output", "processed")

# 使用示例
def main():
    server_ip = "127.0.0.1"
    server_port = 8188
    image_path = r"C:\Users\KingR\Desktop\ComfyUI_00277_.png"

    config = SDComfyUIConfig(server_ip=server_ip, server_port=server_port, image_path=image_path)
    sd_client = SDComfyUIRemoveBg(config)

    # 生成图片
    image_data = sd_client.generate_rembg_image()
    
    # 显示图片
    image = Image.open(io.BytesIO(image_data))
    image.show()

if __name__ == "__main__":
    main()